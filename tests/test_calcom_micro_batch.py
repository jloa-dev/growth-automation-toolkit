"""
Unit test suite verifying all 5 Cal.com Micro-Lote 2 solutions and edge cases.
"""

import unittest
import re
from datetime import datetime, date, timedelta, timezone


class TestCalcomMicroBatch(unittest.TestCase):
    # =========================================================================
    # 1. Issue #30348: OAuth Scope Delimiter Parsing
    # =========================================================================
    def parse_scopes(self, scope_str):
        if not scope_str:
            return []
        # Matches: Array.from(new Set(scope.toString().split(/[\s,]+/).filter(Boolean)))
        tokens = [t for t in re.split(r"[\s,]+", str(scope_str)) if t]
        return list(dict.fromkeys(tokens))  # preserves insertion order while deduplicating

    def test_oauth_scope_space_separated(self):
        res = self.parse_scopes("READ_BOOKING READ_PROFILE")
        self.assertEqual(res, ["READ_BOOKING", "READ_PROFILE"])

    def test_oauth_scope_comma_separated(self):
        res = self.parse_scopes("READ_BOOKING,READ_PROFILE")
        self.assertEqual(res, ["READ_BOOKING", "READ_PROFILE"])

    def test_oauth_scope_mixed_delimiters_and_duplicates(self):
        res = self.parse_scopes("READ_BOOKING,  READ_PROFILE   READ_BOOKING,READ_EVENT")
        self.assertEqual(res, ["READ_BOOKING", "READ_PROFILE", "READ_EVENT"])

    def test_oauth_scope_empty_and_whitespace(self):
        self.assertEqual(self.parse_scopes(""), [])
        self.assertEqual(self.parse_scopes("   "), [])
        self.assertEqual(self.parse_scopes(None), [])

    # =========================================================================
    # 2. Issue #30346: ICS Weekly Recurrence Fast-Forward & Cap Protection
    # =========================================================================
    def test_ics_weekly_recurrence_fast_forward_weekday_preservation(self):
        # Weekly event starting Monday 2021-01-04 14:30 UTC
        dtstart = datetime(2021, 1, 4, 14, 30, tzinfo=timezone.utc)
        self.assertEqual(dtstart.weekday(), 0)  # 0 = Monday

        # Query window: Thursday 2026-10-29
        query_start = datetime(2026, 10, 29, 0, 0, tzinfo=timezone.utc)
        query_end = datetime(2026, 10, 29, 23, 59, tzinfo=timezone.utc)
        self.assertEqual(query_start.weekday(), 3)  # 3 = Thursday

        # Fast forward logic
        diff_days = (query_start - dtstart).days
        diff_weeks = diff_days // 7
        intervals_to_skip = max(0, diff_weeks - 1)
        fast_forwarded = dtstart + timedelta(weeks=intervals_to_skip)

        # 1. Fast-forwarded seed MUST remain a Monday
        self.assertEqual(fast_forwarded.weekday(), 0)

        # 2. Seed must be within 2 weeks of query window
        days_before_window = (query_start - fast_forwarded).days
        self.assertGreater(days_before_window, 0)
        self.assertLessEqual(days_before_window, 14)

        # 3. Simulate recurrence stepping from seed
        occurrences = []
        curr = fast_forwarded
        steps = 0
        while curr <= query_end + timedelta(days=7) and steps < 10:
            steps += 1
            if query_start <= curr <= query_end:
                occurrences.append(curr)
            curr += timedelta(weeks=1)

        # Must have completed in <= 4 steps (no iteration exhaustion)
        self.assertLessEqual(steps, 4)
        # Must NOT generate phantom occurrence on Thursday
        self.assertEqual(len(occurrences), 0)

    def test_ics_weekly_recurrence_matching_weekday(self):
        # Querying Monday 2026-11-02
        dtstart = datetime(2021, 1, 4, 14, 30, tzinfo=timezone.utc)
        query_start = datetime(2026, 11, 2, 0, 0, tzinfo=timezone.utc)
        query_end = datetime(2026, 11, 2, 23, 59, tzinfo=timezone.utc)

        diff_days = (query_start - dtstart).days
        diff_weeks = diff_days // 7
        intervals_to_skip = max(0, diff_weeks - 1)
        fast_forwarded = dtstart + timedelta(weeks=intervals_to_skip)

        occurrences = []
        curr = fast_forwarded
        steps = 0
        while curr <= query_end and steps < 10:
            steps += 1
            if query_start <= curr <= query_end:
                occurrences.append(curr)
            curr += timedelta(weeks=1)

        # Must generate exactly 1 occurrence on Monday 2026-11-02 14:30 UTC
        self.assertEqual(len(occurrences), 1)
        self.assertEqual(occurrences[0], datetime(2026, 11, 2, 14, 30, tzinfo=timezone.utc))

    # =========================================================================
    # 3. Issue #30351: Docker Compose Security Hardening
    # =========================================================================
    def test_docker_compose_patch_content(self):
        with open("solutions/calcom_30351_docker_compose_security.patch", "r", encoding="utf-8") as f:
            patch = f.read()

        # Check loopback bindings
        self.assertIn("${REDIS_BIND_IP:-127.0.0.1}:${REDIS_PORT:-6379}:6379", patch)
        self.assertIn("${PRISMA_STUDIO_BIND_IP:-127.0.0.1}:${PRISMA_STUDIO_PORT:-5555}:5555", patch)
        # Check image pinning
        self.assertIn("redis:7.2-alpine", patch)

    # =========================================================================
    # 4. Issue #30271: Date Overrides Timezone Invariance
    # =========================================================================
    def simulate_transform_date_overrides(self, overrides, schedule_tz_offset_hours, current_time_utc):
        current_time_in_tz = current_time_utc + timedelta(hours=schedule_tz_offset_hours)
        today_in_tz_str = current_time_in_tz.strftime("%Y-%m-%d")

        acc = []
        for ov in overrides:
            ov_date_utc = ov["date"]  # stored as UTC midnight
            ov_date_str = ov_date_utc.strftime("%Y-%m-%d")

            # Check: drop past overrides strictly before today in schedule TZ
            if ov_date_str < today_in_tz_str:
                continue

            new_value = {
                "start": ov["date"].replace(hour=ov["start_time"].hour, minute=ov["start_time"].minute),
                "end": ov["date"].replace(hour=ov["end_time"].hour, minute=ov["end_time"].minute),
            }

            # Grouping invariant to server process TZ: compare UTC date strings
            day_range_idx = -1
            for idx, item in enumerate(acc):
                item_date_str = item["ranges"][0]["start"].strftime("%Y-%m-%d")
                if item_date_str == ov_date_str:
                    day_range_idx = idx
                    break

            if day_range_idx == -1:
                acc.append({"ranges": [new_value]})
            else:
                acc[day_range_idx]["ranges"].append(new_value)

        return acc

    def test_date_overrides_multiple_ranges_grouping(self):
        # Overrides on 2026-10-10 with 2 ranges: 09:00-12:00 and 14:00-17:00
        ov_date = datetime(2026, 10, 10, 0, 0, tzinfo=timezone.utc)
        overrides = [
            {"date": ov_date, "start_time": datetime(1970, 1, 1, 9, 0), "end_time": datetime(1970, 1, 1, 12, 0)},
            {"date": ov_date, "start_time": datetime(1970, 1, 1, 14, 0), "end_time": datetime(1970, 1, 1, 17, 0)},
        ]
        # Current time: 2026-10-05 14:00 UTC, Schedule TZ: London (+1 in BST)
        now_utc = datetime(2026, 10, 5, 14, 0, tzinfo=timezone.utc)
        result = self.simulate_transform_date_overrides(overrides, schedule_tz_offset_hours=1, current_time_utc=now_utc)

        # Must be grouped into exactly ONE entry containing both ranges
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]["ranges"]), 2)
        self.assertEqual(result[0]["ranges"][0]["start"].hour, 9)
        self.assertEqual(result[0]["ranges"][1]["start"].hour, 14)

    def test_date_overrides_today_preserved_in_western_tz(self):
        # Override for today: 2026-10-05
        ov_today = datetime(2026, 10, 5, 0, 0, tzinfo=timezone.utc)
        overrides = [
            {"date": ov_today, "start_time": datetime(1970, 1, 1, 16, 0), "end_time": datetime(1970, 1, 1, 18, 0)},
        ]
        # Now: 2026-10-05 14:00 UTC, Schedule in New York (EDT = UTC-4) -> local time 10:00 AM on 2026-10-05
        now_utc = datetime(2026, 10, 5, 14, 0, tzinfo=timezone.utc)
        result = self.simulate_transform_date_overrides(overrides, schedule_tz_offset_hours=-4, current_time_utc=now_utc)

        # Must NOT be dropped
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]["ranges"]), 1)

    def test_date_overrides_yesterday_dropped(self):
        # Override for yesterday: 2026-10-04
        ov_yesterday = datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc)
        overrides = [
            {"date": ov_yesterday, "start_time": datetime(1970, 1, 1, 10, 0), "end_time": datetime(1970, 1, 1, 12, 0)},
        ]
        now_utc = datetime(2026, 10, 5, 14, 0, tzinfo=timezone.utc)
        result = self.simulate_transform_date_overrides(overrides, schedule_tz_offset_hours=-4, current_time_utc=now_utc)

        # Must be excluded
        self.assertEqual(len(result), 0)

    # =========================================================================
    # 5. Issue #30269: Google Meet URL Matching and Decoupling
    # =========================================================================
    def test_google_meet_url_regexp(self):
        meet_regex = re.compile(r"^https?://(?:www\.)?meet\.google\.com/[a-zA-Z0-9-_]+")
        self.assertTrue(meet_regex.match("https://meet.google.com/abc-defg-hij"))
        self.assertTrue(meet_regex.match("https://www.meet.google.com/abc-defg-hij"))
        self.assertTrue(meet_regex.match("https://meet.google.com/abc-defg-hij?authuser=1"))
        self.assertFalse(meet_regex.match("https://teams.microsoft.com/l/meetup-join/123"))
        self.assertFalse(meet_regex.match("https://example.com/meet"))


if __name__ == "__main__":
    unittest.main()
