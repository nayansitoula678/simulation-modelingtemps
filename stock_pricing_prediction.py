import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    # Assumes df has columns: Date, Close (or Index)
    df = df.sort_values("Date").reset_index(drop=True)

    df["return_1d"] = df["Close"].pct_change()
    df["ma_5"] = df["Close"].rolling(5).mean()
    df["ma_10"] = df["Close"].rolling(10).mean()
    df["vol_5"] = df["return_1d"].rolling(5).std()

    # Target: 1 if tomorrow's close is higher than today's close, else 0
    df["target_up"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    df = df.dropna().reset_index(drop=True)
    return df


def main():
    # 1) Download NEPSE index history as CSV (from Merolagani/ShareSansar/NepseAlpha), then set the path here:
    csv_path = "nepse_index_history.csv"

    df = pd.read_csv(csv_path)

    # Normalize column names (adjust if your CSV uses different names)
    # You need at least Date and Close (index value)
    # Example mappings:
    if "Index Value" in df.columns and "Close" not in df.columns:
        df = df.rename(columns={"Index Value": "Close"})
    if "Date (AD)" in df.columns and "Date" not in df.columns:
        df = df.rename(columns={"Date (AD)": "Date"})

    df["Date"] = pd.to_datetime(df["Date"])
    df = df[["Date", "Close"]]

    df = add_features(df)

    features = ["return_1d", "ma_5", "ma_10", "vol_5"]
    X = df[features].values
    y = df["target_up"].values

    # Time-series cross-validation (no shuffling)
    tscv = TimeSeriesSplit(n_splits=5)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000))
    ])

    accs = []
    for train_idx, test_idx in tscv.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        accs.append(accuracy_score(y_test, preds))

    print(f"Average CV Accuracy: {np.mean(accs):.3f} (±{np.std(accs):.3f})")

    # Train on all data except last row, predict next day direction for last available day
    model.fit(X[:-1], y[:-1])
    last_features = X[-1].reshape(1, -1)
    prob_up = model.predict_proba(last_features)[0, 1]
    pred = model.predict(last_features)[0]

    last_date = df["Date"].iloc[-1].date()
    print(f"Last date in data: {last_date}")
    print(f"Predicted next-day direction: {'UP' if pred == 1 else 'DOWN'} (P(UP)={prob_up:.2f})")


if __name__ == "__main__":
    main()
