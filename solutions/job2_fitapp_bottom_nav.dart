// Solution for Issue #36 (nick-transition/fitapp):
// UI: Replace top TabBar with bottom NavigationBar
// Reward: $300 - $600 USD (Size M)

import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'screens/connected_apps_screen.dart';
import 'screens/calendar_screen.dart';
import 'screens/coach_screen.dart';
import 'screens/faq_screen.dart';
import 'screens/subscription_screen.dart';
// Note: _ProgramsTab, _SessionsTab and other tab contents imported or embedded

class HomeScreenWithBottomNav extends StatefulWidget {
  const HomeScreenWithBottomNav({super.key});

  @override
  State<HomeScreenWithBottomNav> createState() => _HomeScreenWithBottomNavState();
}

class _HomeScreenWithBottomNavState extends State<HomeScreenWithBottomNav> {
  int _selectedIndex = 0;

  final List<Widget> _destinations = const [
    _ProgramsTab(),
    _WorkoutsTabPlaceholder(), // or Workouts tab
    CalendarScreen(),
    _SessionsTab(),
  ];

  final List<String> _titles = const [
    'Programs',
    'Workouts',
    'Calendar',
    'Sessions',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_titles[_selectedIndex]),
        actions: [
          IconButton(
            icon: const Icon(Icons.card_membership),
            tooltip: 'Subscription',
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SubscriptionScreen()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.people),
            tooltip: 'Coach Sharing',
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const CoachScreen()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.smart_toy_outlined),
            tooltip: 'Connected Apps',
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ConnectedAppsScreen()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.help_outline),
            tooltip: 'Help & Setup',
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const FaqScreen()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Sign Out',
            onPressed: () => FirebaseAuth.instance.signOut(),
          ),
        ],
      ),
      // M3 Animated destination transition
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 250),
        switchInCurve: Curves.easeInOut,
        switchOutCurve: Curves.easeInOut,
        transitionBuilder: (Widget child, Animation<double> animation) {
          return FadeTransition(opacity: animation, child: child);
        },
        child: KeyedSubtree(
          key: ValueKey<int>(_selectedIndex),
          child: _destinations[_selectedIndex],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (int index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        indicatorColor: Theme.of(context).colorScheme.primaryContainer,
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.folder_outlined),
            selectedIcon: Icon(Icons.folder),
            label: 'Programs',
          ),
          NavigationDestination(
            icon: Icon(Icons.fitness_center_outlined),
            selectedIcon: Icon(Icons.fitness_center),
            label: 'Workouts',
          ),
          NavigationDestination(
            icon: Icon(Icons.calendar_month_outlined),
            selectedIcon: Icon(Icons.calendar_month),
            label: 'Calendar',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_outlined),
            selectedIcon: Icon(Icons.history),
            label: 'Sessions',
          ),
        ],
      ),
    );
  }
}
