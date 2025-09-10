import argparse
import pandas as pd
# from src.features import compute_features
from features import compute_features



def load_data(path: str) -> pd.DataFrame:
    import json

    with open(path) as f:
        raw_data = json.load(f)

    records = []
    for item in raw_data:
        flat = {
            "wallet": item.get("userWallet"),
            "timestamp": item.get("timestamp"),
            "action": item.get("action"),
        }

        ad = item.get("actionData", {})
        flat["amount"] = float(ad.get("amount", 0)) / 1e6  # normalize USDC-style
        flat["asset"] = ad.get("assetSymbol", "UNKNOWN")
        records.append(flat)

    return pd.DataFrame(records)




def score(feat: pd.DataFrame) -> pd.Series:
    """Compute raw score between 0–1000 based on weighted features."""
    # Normalize each column to 0–1
    norm = (feat - feat.min()) / (feat.max() - feat.min() + 1e-9)

    # Define weights: positive behaviors positive weight; negative behaviors negative weight
    weights = {
        'sum_repay': +2,
        'count_deposit': +1,
        'sum_deposit': +1,
        'borrow_repay_delay': +1,
        'count_borrow': -1,
        'num_liquidations': -3,
        'recency_days': -0.5,
        'distinct_assets': +0.2,
        'amount_std': -0.1
    }

    # Some columns might be missing
    score = pd.Series(0, index=feat.index, dtype=float)
    for col, w in weights.items():
        if col in norm:
            score += w * norm[col]

    # Scale to 0–1000
    score = 1000 * (score - score.min()) / (score.max() - score.min() + 1e-9)
    return score.clip(0, 1000).round(0).astype(int)


def main(infile: str, outfile: str):
    df = load_data(infile)
    feat = compute_features(df)
    scores = score(feat)
    scores.rename('score').to_csv(outfile, header=True)
    print(f"Saved scores for {len(scores)} wallets to {outfile}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-i','--input', required=True, help='path to transactions.json')
    p.add_argument('-o','--output', default='scores.csv', help='output CSV')
    args = p.parse_args()
    main(args.input, args.output)