// Solution for Issue #62 (nick-transition/fitapp):
// Feature: Plan builder: choose exercises from the exercise library
// Bounty: $300 - $600 USD (Size M/L)

import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class ExerciseLibraryPickerDialog extends StatefulWidget {
  const ExerciseLibraryPickerDialog({super.key});

  @override
  State<ExerciseLibraryPickerDialog> createState() => _ExerciseLibraryPickerDialogState();
}

class _ExerciseLibraryPickerDialogState extends State<ExerciseLibraryPickerDialog> {
  final TextEditingController _searchController = TextEditingController();
  String _query = '';

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 500, maxHeight: 600),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Exercise Library', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 12),
              TextField(
                controller: _searchController,
                decoration: InputDecoration(
                  hintText: 'Search exercises...',
                  prefixIcon: const Icon(Icons.search),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 16),
                ),
                onChanged: (val) => setState(() => _query = val.trim().toLowerCase()),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: StreamBuilder<QuerySnapshot>(
                  stream: FirebaseFirestore.instance.collection('exercise_library').snapshots(),
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(child: CircularProgressIndicator());
                    }
                    final docs = snapshot.data?.docs ?? [];
                    final filtered = docs.where((doc) {
                      final data = doc.data() as Map<String, dynamic>;
                      final name = (data['name'] as String? ?? '').toLowerCase();
                      return name.contains(_query);
                    }).toList();

                    if (filtered.isEmpty) {
                      return const Center(child: Text('No exercises found'));
                    }

                    return ListView.builder(
                      itemCount: filtered.length,
                      itemBuilder: (context, index) {
                        final data = filtered[index].data() as Map<String, dynamic>;
                        return ListTile(
                          title: Text(data['name'] ?? 'Unnamed'),
                          subtitle: Text(data['muscleGroup'] ?? 'General'),
                          trailing: const Icon(Icons.add_circle_outline, color: Colors.teal),
                          onTap: () => Navigator.pop(context, {
                            'id': filtered[index].id,
                            'name': data['name'],
                            'videoUrl': data['videoUrl'],
                          }),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
