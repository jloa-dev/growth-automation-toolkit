// Solution for Issue #43 (nick-transition/fitapp):
// UI: Marketing & login screen polish with gradients and animations
// Bounty: $300 USD (Size M)

import 'package:flutter/material.dart';

class MarketingHeroGradientHeader extends StatelessWidget {
  const MarketingHeroGradientHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 48),
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFF004D40), // Dark Teal
            Color(0xFF00796B), // Medium Teal
            Color(0xFF009688), // Teal accent
          ],
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.15),
              borderRadius: BorderRadius.circular(20),
            ),
            child: const Text(
              'FitApp 2.0 · Open Source AI Training',
              style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600),
            ),
          ),
          const SizedBox(height: 20),
          const Text(
            'Your AI-Powered\nWorkout Companion',
            style: TextStyle(
              color: Colors.white,
              fontSize: 36,
              fontWeight: FontWeight.bold,
              letterSpacing: -0.5,
              height: 1.15,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            'Create custom workout plans, track progression, and analyze your lifts with intelligent AI coaching.',
            style: TextStyle(
              color: Colors.white.withOpacity(0.85),
              fontSize: 16,
              height: 1.4,
            ),
          ),
        ],
      ),
    );
  }
}
