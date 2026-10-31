import json, joblib, pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, recall_score, roc_curve

SEED, TARGET = 42, "SeriousDlqin2yrs"
ref = pd.read_parquet("data/reference/reference.parquet")
X, y = ref.drop(columns=[TARGET]), ref[TARGET]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)

model = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05,
                      scale_pos_weight=(ytr == 0).sum() / (ytr == 1).sum(),
                      random_state=SEED, n_jobs=-1)
model.fit(Xtr, ytr)

p = model.predict_proba(Xte)[:, 1]
fpr, tpr, _ = roc_curve(yte, p)
metrics = {"auc": roc_auc_score(yte, p),
           "recall_at_0.5": recall_score(yte, p >= 0.5),
           "ks": float((tpr - fpr).max())}
joblib.dump(model, "models/model.joblib")
json.dump(metrics, open("models/metrics.json", "w"), indent=2)
print(metrics)
