// Solution for Issue #38 (nick-transition/fitapp):
// UI: Add custom Google Font (Inter or Plus Jakarta Sans)
// Reward: $100 - $200 USD (Size S)

/*
Step 1: In pubspec.yaml under dependencies:
dependencies:
  google_fonts: ^6.2.1
*/

// Step 2: In lib/main.dart (or custom theme utility):
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

ThemeData buildFitAppTheme() {
  final baseTheme = ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.teal,
      brightness: Brightness.light,
    ),
    useMaterial3: true,
    appBarTheme: const AppBarTheme(
      centerTitle: true,
      elevation: 0,
      backgroundColor: Colors.transparent,
      foregroundColor: Colors.black87,
    ),
  );

  // Apply Inter with high-contrast typography hierarchy
  return baseTheme.copyWith(
    textTheme: GoogleFonts.interTextTheme(baseTheme.textTheme).copyWith(
      displayLarge: GoogleFonts.inter(
        fontWeight: FontWeight.w700,
        letterSpacing: -0.5,
      ),
      displayMedium: GoogleFonts.inter(
        fontWeight: FontWeight.w700,
        letterSpacing: -0.25,
      ),
      headlineLarge: GoogleFonts.inter(
        fontWeight: FontWeight.w700,
      ),
      headlineMedium: GoogleFonts.inter(
        fontWeight: FontWeight.w700,
      ),
      headlineSmall: GoogleFonts.inter(
        fontWeight: FontWeight.w600,
      ),
      titleLarge: GoogleFonts.inter(
        fontWeight: FontWeight.w700,
      ),
      titleMedium: GoogleFonts.inter(
        fontWeight: FontWeight.w600,
      ),
      titleSmall: GoogleFonts.inter(
        fontWeight: FontWeight.w600,
      ),
      bodyLarge: GoogleFonts.inter(
        fontWeight: FontWeight.w400,
      ),
      bodyMedium: GoogleFonts.inter(
        fontWeight: FontWeight.w400,
      ),
      bodySmall: GoogleFonts.inter(
        fontWeight: FontWeight.w400,
      ),
      labelLarge: GoogleFonts.inter(
        fontWeight: FontWeight.w600,
      ),
    ),
  );
}
