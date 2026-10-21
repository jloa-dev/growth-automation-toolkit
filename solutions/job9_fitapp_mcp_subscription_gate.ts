// Solution for Issue #20 (nick-transition/fitapp):
// Security: Gate MCP tool access behind subscription tier
// Bounty: $300 - $500 USD (Size M)

import * as admin from 'firebase-admin';

export interface UserSubscription {
  status: 'active' | 'trialing' | 'canceled' | 'past_due' | 'none';
  tier: 'free' | 'pro' | 'coach';
}

export async function verifyUserSubscriptionTier(uid: string): Promise<UserSubscription> {
  const userDoc = await admin.firestore().collection('users').doc(uid).get();
  if (!userDoc.exists) {
    return { status: 'none', tier: 'free' };
  }

  const data = userDoc.data();
  const subscription = data?.subscription;
  if (!subscription || subscription.status !== 'active') {
    return { status: subscription?.status || 'none', tier: 'free' };
  }

  return {
    status: subscription.status,
    tier: subscription.tier || 'pro',
  };
}

export function assertMcpToolSubscription(
  subscription: UserSubscription,
  requiredTier: 'pro' | 'coach' = 'pro'
): void {
  if (subscription.status !== 'active') {
    throw new Error('Access denied: Active subscription required to access this MCP tool.');
  }

  if (requiredTier === 'coach' && subscription.tier !== 'coach') {
    throw new Error('Access denied: Coach tier subscription required.');
  }
}
