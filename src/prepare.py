import json, pandas as pd
from sklearn.model_selection import train_test_split

SEED, TARGET = 42, "SeriousDlqin2yrs"

def clean(df):
    report, n = {}, len(df)
    def step(name, new):
        nonlocal n
        report[name] = n - len(new); n = len(new); return new

    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    df = step("duplicadas", df.drop_duplicates())
    df = step("idade fora de 18-100", df[df["age"].between(18, 100)])
    df = step("renda/dependentes nulos", df.dropna(subset=["MonthlyIncome", "NumberOfDependents"]))
    df = step("renda negativa", df[df["MonthlyIncome"] >= 0])
    late = [c for c in df.columns if "PastDue" in c or "90DaysLate" in c]
    df = step("codigos 96/98 (placeholder)", df[~df[late].isin([96, 98]).any(axis=1)])
    for col in ["DebtRatio", "RevolvingUtilizationOfUnsecuredLines"]:
        df = step(f"outlier {col} > p99", df[df[col] <= df[col].quantile(0.99)])
    return df.reset_index(drop=True), report

if __name__ == "__main__":
    df, report = clean(pd.read_csv("data/raw/cs-training.csv"))
    ref, holdout = train_test_split(df, test_size=0.3, stratify=df[TARGET], random_state=SEED)
    ref.to_parquet("data/reference/reference.parquet")
    holdout.to_parquet("data/production/holdout.parquet")
    json.dump(report, open("data/reference/cleaning_report.json", "w"), indent=2)
    print(report, len(ref), len(holdout))
    