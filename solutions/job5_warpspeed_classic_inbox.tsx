// Solution for Issue #2 (warpspeedopen-source/warpspeed-bounties):
// [PAID BOUNTY - $330] Email Inbox Classic View Page UI
// Skills: React Native, TypeScript, Storybook, UI Implementation

import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Animated,
  TextInput,
  SafeAreaView,
} from 'react-native';

export interface EmailItem {
  id: string;
  sender: string;
  subject: string;
  snippet: string;
  date: string;
  isRead: boolean;
  category: 'Primary' | 'Promotions' | 'Updates';
}

const CATEGORIES = ['Primary', 'Promotions', 'Updates'] as const;

export const ClassicInboxView: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<'Primary' | 'Promotions' | 'Updates'>('Primary');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Header animation on scroll
  const scrollY = useRef(new Animated.Value(0)).current;
  const headerTranslateY = scrollY.interpolate({
    inputRange: [0, 80],
    outputRange: [0, -60],
    extrapolate: 'clamp',
  });

  const sampleEmails: EmailItem[] = [
    {
      id: '1',
      sender: 'GitHub Security',
      subject: 'Security alert for your repository',
      snippet: 'We noticed a new high severity advisory matching your dependencies...',
      date: '10:42 AM',
      isRead: false,
      category: 'Primary',
    },
    {
      id: '2',
      sender: 'Stripe Support',
      subject: 'Monthly payout confirmation statement',
      snippet: 'Your payout of $100.00 USD has been sent to your bank account...',
      date: 'Yesterday',
      isRead: true,
      category: 'Updates',
    },
    {
      id: '3',
      sender: 'Vercel Deployments',
      subject: 'Production deployment successful (v2.4.0)',
      snippet: 'Your domain has been updated with the latest build artifacts...',
      date: 'Oct 3',
      isRead: true,
      category: 'Primary',
    },
  ];

  const filteredEmails = sampleEmails.filter(
    (item) =>
      item.category === selectedCategory &&
      (item.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
       item.sender.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <SafeAreaView style={styles.container}>
      {/* Top Collapsible Header */}
      <Animated.View style={[styles.header, { transform: [{ translateY: headerTranslateY }] }]}>
        <View style={styles.topRow}>
          <Text style={styles.accountTitle}>personal@warpspeed.org</Text>
          <View style={styles.viewModePills}>
            <TouchableOpacity style={styles.activePill}><Text style={styles.activePillText}>Classic</Text></TouchableOpacity>
            <TouchableOpacity style={styles.inactivePill}><Text style={styles.inactivePillText}>Flow</Text></TouchableOpacity>
          </View>
        </View>

        {/* Search Bar */}
        <View style={styles.searchContainer}>
          <TextInput
            style={styles.searchInput}
            placeholder="Search mail..."
            placeholderTextColor="#8E8E93"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>

        {/* Category Filters */}
        <View style={styles.categoryRow}>
          {CATEGORIES.map((cat) => (
            <TouchableOpacity
              key={cat}
              onPress={() => setSelectedCategory(cat)}
              style={[
                styles.categoryChip,
                selectedCategory === cat && styles.categoryChipActive,
              ]}
            >
              <Text
                style={[
                  styles.categoryText,
                  selectedCategory === cat && styles.categoryTextActive,
                ]}
              >
                {cat}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </Animated.View>

      {/* Email List */}
      <Animated.FlatList
        data={filteredEmails}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { y: scrollY } } }],
          { useNativeDriver: true }
        )}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.emailRow, !item.isRead && styles.unreadRow]}
          >
            <View style={styles.emailHeader}>
              <Text style={[styles.sender, !item.isRead && styles.unreadText]}>
                {item.sender}
              </Text>
              <Text style={styles.date}>{item.date}</Text>
            </View>
            <Text
              style={[styles.subject, !item.isRead && styles.unreadText]}
              numberOfLines={1}
            >
              {item.subject}
            </Text>
            <Text style={styles.snippet} numberOfLines={2}>
              {item.snippet}
            </Text>
          </TouchableOpacity>
        )}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0B0D13' },
  header: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 10,
    backgroundColor: '#121620',
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#1E2536',
  },
  topRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  accountTitle: { color: '#FFFFFF', fontSize: 16, fontWeight: '700' },
  viewModePills: { flexDirection: 'row', gap: 6 },
  activePill: { backgroundColor: '#3A74F4', paddingHorizontal: 12, paddingVertical: 4, borderRadius: 14 },
  activePillText: { color: '#FFFFFF', fontSize: 12, fontWeight: '600' },
  inactivePill: { backgroundColor: '#1A2030', paddingHorizontal: 12, paddingVertical: 4, borderRadius: 14 },
  inactivePillText: { color: '#8F9CAE', fontSize: 12 },
  searchContainer: { marginTop: 10 },
  searchInput: {
    backgroundColor: '#1A2030',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 8,
    color: '#FFFFFF',
    fontSize: 14,
  },
  categoryRow: { flexDirection: 'row', gap: 8, marginTop: 10 },
  categoryChip: { paddingHorizontal: 14, paddingVertical: 6, borderRadius: 16, backgroundColor: '#181E2C' },
  categoryChipActive: { backgroundColor: '#2C3A56' },
  categoryText: { color: '#7E8B9B', fontSize: 13, fontWeight: '500' },
  categoryTextActive: { color: '#FFFFFF', fontWeight: '700' },
  listContent: { paddingTop: 160, paddingBottom: 24 },
  emailRow: { padding: 16, borderBottomWidth: 1, borderBottomColor: '#181E2C' },
  unreadRow: { backgroundColor: 'rgba(58, 116, 244, 0.06)' },
  emailHeader: { flexDirection: 'row', justifyContent: 'space-between' },
  sender: { color: '#C0CAD6', fontSize: 14 },
  date: { color: '#68778D', fontSize: 12 },
  subject: { color: '#E4ECF5', fontSize: 15, marginTop: 4 },
  snippet: { color: '#8898AA', fontSize: 13, marginTop: 4 },
  unreadText: { fontWeight: '700', color: '#FFFFFF' },
});
