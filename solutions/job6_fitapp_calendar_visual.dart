// Solution for Issue #40 (nick-transition/fitapp):
// UI: Calendar visual upgrade
// Bounty: $300 USD (Size M)

import 'package:flutter/material.dart';

Widget buildCalendarDayTile({
  required BuildContext context,
  required DateTime date,
  required bool isSelected,
  required bool isToday,
  required int sessionCount,
  required VoidCallback onTap,
}) {
  final theme = Theme.of(context);
  final isDark = theme.brightness == Brightness.dark;

  Color backgroundColor = Colors.transparent;
  Color textColor = isDark ? Colors.white70 : Colors.black87;

  if (isSelected) {
    backgroundColor = theme.colorScheme.primary;
    textColor = theme.colorScheme.onPrimary;
  } else if (isToday) {
    backgroundColor = theme.colorScheme.primaryContainer.withOpacity(0.4);
    textColor = theme.colorScheme.primary;
  }

  return InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(12),
    child: AnimatedContainer(
      duration: const Duration(milliseconds: 150),
      margin: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(12),
        border: isToday && !isSelected
            ? Border.all(color: theme.colorScheme.primary, width: 1.5)
            : null,
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            '${date.day}',
            style: TextStyle(
              fontWeight: isSelected || isToday ? FontWeight.bold : FontWeight.normal,
              color: textColor,
            ),
          ),
          if (sessionCount > 0) ...[
            const SizedBox(height: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(
                sessionCount > 3 ? 3 : sessionCount,
                (_) => Container(
                  width: 5,
                  height: 5,
                  margin: const EdgeInsets.symmetric(horizontal: 1),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isSelected
                        ? theme.colorScheme.onPrimary
                        : theme.colorScheme.tertiary,
                  ),
                ),
              ),
            ),
          ],
        ],
      ),
    ),
  );
}
