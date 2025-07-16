import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the scores
df = pd.read_csv("scores.csv")

# Plot distribution
plt.figure(figsize=(10,6))
sns.histplot(df['score'], bins=20, kde=False, color='skyblue', edgecolor='black')
plt.title("Distribution of Wallet Credit Scores")
plt.xlabel("Score (0–1000)")
plt.ylabel("Number of Wallets")
plt.grid(True)
plt.tight_layout()
plt.savefig("score_distribution.png")
plt.show()
