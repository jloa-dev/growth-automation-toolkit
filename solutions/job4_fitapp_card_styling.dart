// Solution for Issue #37 (nick-transition/fitapp):
// UI: Card styling overhaul with rounded corners, shadows, and accents
// Bounty: $300 - $450 USD (Size M)

import 'package:flutter/material.dart';

/// Reusable styled card container adhering to the M3 card overhaul guidelines:
/// - Rounded corners (16dp border radius)
/// - Subtle elevation with tonal surface tint
/// - Teal accent indicator on leading edge
class StyledElevationCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final Color? accentColor;
  final EdgeInsetsGeometry margin;
  final EdgeInsetsGeometry padding;

  const StyledElevationCard({
    super.key,
    required this.child,
    this.onTap,
    this.accentColor,
    this.margin = const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    this.padding = const EdgeInsets.all(16),
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final accent = accentColor ?? theme.colorScheme.primary;

    return Card(
      margin: margin,
      elevation: 2,
      shadowColor: theme.colorScheme.shadow.withOpacity(0.08),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: theme.colorScheme.outlineVariant.withOpacity(0.5),
          width: 1,
        ),
      ),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                width: 5,
                decoration: BoxDecoration(
                  color: accent,
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(16),
                    bottomLeft: Radius.circular(16),
                  ),
                ),
              ),
              Expanded(
                child: Padding(
                  padding: padding,
                  child: child,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
