import pandas as pd
import numpy as np

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame `df` of all transactions, group by wallet and compute features:
      - total_deposit, total_borrow, total_repay, total_redeem, num_liquidations
      - action_counts: frequency of each action
      - distinct_assets
      - borrow_repay_delay_mean
      - amount_std
      - recency_days (from max timestamp)
    """
    # Ensure timestamp column is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # ------------------ Aggregate Action Counts and Amounts ------------------
    actions = ['deposit', 'borrow', 'repay', 'redeemunderlying', 'liquidationcall']

    # Count of each action
    action_counts = df.groupby(['wallet', 'action']).size().unstack(fill_value=0)
    action_counts.columns = [f"count_{col}" for col in action_counts.columns]

    # Sum of amount for each action
    action_sums = df.groupby(['wallet', 'action'])['amount'].sum().unstack(fill_value=0)
    action_sums.columns = [f"sum_{col}" for col in action_sums.columns]

    # ------------------ Distinct Assets ------------------
    distinct_assets = df.groupby('wallet')['asset'].nunique().rename("distinct_assets")

    # ------------------ Borrow → Repay Delay ------------------
    df_sorted = df.sort_values(['wallet', 'timestamp'])
    delays = []

    for wallet, group in df_sorted.groupby('wallet'):
        group = group.reset_index(drop=True)
        borrow_times = group[group['action'] == 'borrow']['timestamp']
        repay_times = group[group['action'] == 'repay']['timestamp']

        min_len = min(len(borrow_times), len(repay_times))
        if min_len > 0:
            aligned = pd.DataFrame({
                'borrow': borrow_times.iloc[:min_len].values,
                'repay': repay_times.iloc[:min_len].values
            })
            aligned['delay'] = (aligned['repay'] - aligned['borrow']).dt.total_seconds()
            avg_delay = aligned['delay'].mean()
        else:
            avg_delay = 0

        delays.append((wallet, avg_delay))

    delay_df = pd.Series(dict(delays)).rename("borrow_repay_delay")

    # ------------------ Amount Volatility ------------------
    amount_std = df.groupby('wallet')['amount'].std().rename("amount_std").fillna(0)

    # ------------------ Recency (days since last tx) ------------------
    now = pd.Timestamp.now()
    recency = df.groupby('wallet')['timestamp'].max().apply(lambda ts: (now - ts).days)
    recency.name = "recency_days"

    # ------------------ Combine All ------------------
    features = pd.concat([
        action_counts,
        action_sums,
        distinct_assets,
        delay_df,
        amount_std,
        recency
    ], axis=1).fillna(0)

    return features
