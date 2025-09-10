# 💳 Aave V2 Wallet Credit Scoring

This project assigns a credit score (0–1000) to each wallet based on their historical transaction behavior with the Aave V2 DeFi protocol.

---

## 🧠 Method Chosen

We opted for a **manual feature engineering** approach combined with a **rule-based weighted scoring function** for the following reasons:

- **Transparency & Interpretability**: Stakeholders can easily understand how the score is computed. Each feature contributes in a known, controllable way — which is ideal for financial scoring tasks.
- **Limited Labeled Data**: Since this is an unsupervised setup with no ground-truth credit labels, training a supervised ML model wasn't feasible. A rule-based approach was better suited.
- **Lightweight & Fast**: The scoring system is computationally efficient, suitable for large-scale batch scoring without GPU requirements.
- **Behavior-Based Credit Modeling**: Our logic mimics traditional credit bureaus by rewarding responsible patterns (e.g., consistent repays, low volatility) and penalizing risk signals (e.g., liquidations, inactivity).

We engineered features such as:
- Total and frequency of repays, borrows, liquidations
- Recency of activity
- Transaction volatility
- Asset diversity

These features were normalized and combined using a weighted formula to generate a credit score between **0–1000**.

---

## 📁 Repository Structure

```
credit-scoring-aave/
├── data/
│ └── transactions.json # Input data file (raw user-level transactions)
├── src/
│ ├── features.py # Feature engineering logic
│ └── score_wallets.py # Scoring script (runs end-to-end)
├── requirements.txt
├── README.md
├── analysis.md
└── score_distribution.png # Score histogram plot
```
---

## ⚙️ Processing Flow

1. **Load JSON**  
   Parse `transactions.json`, flattening each entry and extracting:  
   - `wallet`, `timestamp`, `action`, `amount`, `assetSymbol`

2. **Feature Engineering** (`features.py`)  
   - Count of deposits, borrows, liquidations  
   - Sum of amounts per action  
   - Distinct assets used  
   - Delay between borrow and repay  
   - Standard deviation of transaction amounts  
   - Recency of last activity

3. **Scoring** (`score_wallets.py`)  
   - Normalize features  
   - Apply a weighted linear formula  
   - Rescale final score to range **0–1000**

4. **Output**  
   - `scores.csv` containing wallet and score  
   - Visual analysis saved to `score_distribution.png`

---

## Interactive Web Interface

This project also includes a Streamlit web application for an interactive experience.

### Running the App

1.  **Ensure all dependencies are installed**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Streamlit app from the project root directory**:
    ```bash
    streamlit run credit-scoring-aave/app.py
    ```
3.  **Upload your `transactions.json` file** using the file uploader in the web interface and click "Calculate Credit Scores".


---

## 🚀 Getting Started

### 1. Clone & Install

`git clone <repo_url> cd credit-scoring-aave pip install -r requirements.txt`

### 2. Prepare Data
- Download `transactions.json` (~87MB) into `data/` from:
[Google Drive Link](https://drive.google.com/file/d/1ISFbAXxadMrt7Zl96rmzzZmEKZnyW7FS/view?usp=sharing)


### 3. Run Scoring
`python src/score_wallets.py -i data/transactions.json -o scores.csv`

### 4. Explore Results
- `scores.csv` with columns `[wallet, score]`.
- `Open analysis.md` for interpretation and visualizations.

---

## ⚙️ Methodology
1. **Feature Engineering** in `src/features.py`:
   - Action counts & sums, liquidation counts, asset diversity, delays, volatility, recency.
2. **Scoring** in `score_wallets.py`:
   - Min–max normalize features.
   - Weighted linear combination.
   - Scale to 0–1000.

---

## 🔍 Analysis
See `[analysis.md]` for distribution plots and behavioral insights.
