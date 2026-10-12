import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, classification_report)
import joblib

import warnings
warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", 100)
RANDOM_STATE = 42

#EXPLORATORY DATA ANALYSIS 
df = pd.read_csv(r"C:\Users\hp\OneDrive\Documents\machine-learning-crash-course\ml-crash-course-main\ml-crash-course-main\13_capstone_project_product_return_prediction\dataset\returns_dataset.csv")

print(df.head(5))

print(df['returned'].value_counts())

return_counts = df['returned'].value_counts()

plt.bar(return_counts.index, return_counts.values)
plt.xlabel('Returned')
plt.ylabel('Count')
plt.title('Returned Values Distribution')
plt.show()

print(df.isna().sum())
print(df.info())
print(df.describe().T)

categorical_columns = ['product_category', 'sub_category', 'brand', 'fulfillment_type', 'payment_method']

for i in categorical_columns:
    print(df[i].value_counts())



fig, axes = plt.subplots(1, 3, figsize=(18, 5))

overall = df["returned"].mean()

for ax, col in zip(axes, ["payment_method", "product_category", "fulfillment_type"]):
    rate = df.groupby(col)["returned"].mean().sort_values(ascending=False)
    rate.plot(kind="bar", ax=ax, color="#4c72b0")

    ax.axhline(overall, color="red", ls="--", lw=1, label=f"Overall ({overall:.2f})")
    ax.set_title(f"Return rate by {col}")
    ax.set_ylabel("Return rate")
    ax.tick_params(axis="x", rotation=30)
    ax.legend()

plt.tight_layout()
plt.show()

num_show = ["product_price", "discount_percent", "product_rating", "review_count",
            "shipping_distance_km", "product_page_views", "defect_rate", "quantity"]
df[num_show].hist(figsize=(15, 9), bins=40); plt.tight_layout(); 
plt.show()

#finding the correlation between the end target and the numeric columns inverse or linear

plt.figure(figsize=(12, 10))
corr = df.select_dtypes(include=[np.number]).corr()
sns.heatmap(corr, cmap="coolwarm", center=0, square=True)
plt.title("Numeric feature correlations"); plt.show()
corr["returned"].drop("returned").reindex(
    corr["returned"].drop("returned").abs().sort_values(ascending=False).index).round(3)

#NOW WE WILL CLEAN THE DATA 

df_clean = df.copy()

print(df_clean['fulfillment_type'].value_counts())

df_clean["fulfillment_type"]=(df_clean['fulfillment_type']
                              .astype('str')
                              .str.strip()
                              .str.title())
print(df_clean["fulfillment_type"].value_counts())

df_clean =df_clean.drop(columns=['order_id'])
print(df_clean.head(5))

before =len(df)

df_clean =df_clean.drop_duplicates()
print(f'{before-len(df_clean)}')

#FEATURE ENGINEERING

def add_features(d):
    d['total_support_contacts'] = d['customer_support_calls']+d['chat_interactions']
    d['log_price'] = np.log1p(d['product_price'])
    d= d.drop(columns=['product_price','customer_support_calls','chat_interactions'])
    return d
df_feat = add_features(df_clean)
print(df_feat.head(5))

df_feat.to_csv('cleaned_dataset/cleaned_returns.csv',index=False)

new_cols = ['total_support_contacts','log_price']
print(df_feat[new_cols].describe().T)

#MACHINE LEARNING MODLE 

from sklearn.model_selection import train_test_split
X =df_feat.drop(columns=['returned'])
y =df_feat['returned'].astype(int)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20,stratify=y,random_state=RANDOM_STATE)
print("Train:", X_train.shape, "Test:", X_test.shape)

#OUTLIERS DETECTION

box_cols = ["log_price", "review_count", "product_page_views",
            "shipping_distance_km", "discount_percent"]
fig, axes = plt.subplots(1, len(box_cols), figsize=(20, 4))
for ax, c in zip(axes, box_cols):
    sns.boxplot(y=X_train[c], ax=ax, color="#4c72b0"); ax.set_title(c)
plt.tight_layout(); plt.show()

outlier_cols = ["log_price"]
mask = pd.Series(True, index=X_train.index)
for c in outlier_cols:
    q1, q3 = X_train[c].quantile(0.25), X_train[c].quantile(0.75)
    upper = q3 + 3 * (q3 - q1)
    mask &= X_train[c] <= upper
removed = (~mask).sum()
X_train, y_train = X_train[mask], y_train[mask]
print(f"Removed {removed} extreme-outlier rows from training set. New train shape: {X_train.shape}")


#binary and encoding bcoz model doesnt recognize the string 

binary_flags = ["fragile_item", "warranty_available", "delayed_delivery", "wishlist_before_purchase"]
categorical_features = ["product_category", "sub_category", "brand", "fulfillment_type", "payment_method"]
numeric_features = [c for c in X_train.columns if c not in binary_flags + categorical_features]

all_features = numeric_features + binary_flags  # continuous + binary
print(f"Numeric features ({len(numeric_features)}):", numeric_features)
print(f"Binary flags ({len(binary_flags)}):", binary_flags)
print(f"Categorical features ({len(categorical_features)}):", categorical_features)


# 1. Impute missing values (median from training set)
train_medians = X_train[all_features].median().to_dict()
X_train[all_features] = X_train[all_features].fillna(train_medians)
X_test[all_features] = X_test[all_features].fillna(train_medians)

#NOW SCLAING OF DATA 
scaler = StandardScaler()
X_train[numeric_features] = scaler.fit_transform(X_train[numeric_features])
X_test[numeric_features] = scaler.transform(X_test[numeric_features])

# 3. One-hot encode categorical features
X_train = pd.get_dummies(X_train, columns=categorical_features, dtype=int)
X_test = pd.get_dummies(X_test, columns=categorical_features, dtype=int)

# Align columns (test may have missing/extra categories)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

model_columns = list(X_train.columns)
print(f"Final feature count: {len(model_columns)}")
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# Calculate scale_pos_weight for XGBoost
neg_count = (y_train == 0).sum()
pos_count = (y_train == 1).sum()
spw = neg_count / pos_count

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE),
    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced", random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(
        n_estimators=300, class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE),
    "XGBoost": XGBClassifier(
        n_estimators=400, learning_rate=0.05, max_depth=5,
        subsample=0.9, colsample_bytree=0.9, scale_pos_weight=spw,
        eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=-1),
}

fitted = {}
for name, est in models.items():
    est.fit(X_train, y_train)
    fitted[name] = est
    print("Trained:", name)

#now comparing models performances

def evaluate(model, X, y):
    pred = model.predict(X)
    return {
        "Accuracy": accuracy_score(y, pred),
        "Precision": precision_score(y, pred, zero_division=0),
        "Recall": recall_score(y, pred, zero_division=0),
        "F1": f1_score(y, pred, zero_division=0),
    }

comparison = pd.DataFrame({n: evaluate(m, X_test, y_test) for n, m in fitted.items()}).T
comparison = comparison.sort_values("F1", ascending=False)
comparison.round(4)

#with the help of boxplot we can know which model has best score

comparison.plot(kind="bar", figsize=(11, 6)); plt.title("Model comparison (test set)")
plt.ylabel("Score"); plt.ylim(0, 1); plt.legend(loc="lower right", ncol=4, fontsize=8)
plt.xticks(rotation=15, ha="right"); plt.tight_layout(); plt.show()


best_name = comparison.index[0]
print("Best model by F1:", best_name, "| imbalance: class_weight='balanced'") #basically its logistic regression

final_model = fitted[best_name]
tuned_metrics = evaluate(final_model, X_test, y_test)
print(f"Final {best_name} (class_weight='balanced') test metrics:")
for k, v in tuned_metrics.items():
    print(f"  {k:10s}: {v:.4f}")


cm = confusion_matrix(y_test, final_model.predict(X_test))
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["Not returned", "Returned"], yticklabels=["Not returned", "Returned"])
plt.title(f"Confusion Matrix - Tuned {best_name}"); plt.xlabel("Predicted"); plt.ylabel("Actual")
plt.tight_layout(); plt.show()
print(classification_report(y_test, final_model.predict(X_test),
                            target_names=["Not returned", "Returned"], digits=4))

print(final_model.coef_)
print(final_model.intercept_)

# Rank features by coefficient MAGNITUDE (so the strongest predictors are shown), but keep
# the SIGN via colour: red = pushes toward a return, blue = protective (pushes away).
# This is better than plotting raw signed values and taking head(20), which would silently
# drop the strongest features when their coefficient is negative.
imp = pd.Series(final_model.coef_[0], index=model_columns)
top = imp.reindex(imp.abs().sort_values(ascending=False).index).head(20)
colors = ["#c44e52" if v > 0 else "#4c72b0" for v in top]

plt.figure(figsize=(9, 8))
top[::-1].plot(kind="barh", color=colors[::-1])
plt.axvline(0, color="black", lw=0.8)
plt.title(f"Top 20 features - {best_name} (signed coefficient)\nred = increases return risk, blue = protective")
plt.xlabel("coefficient (log-odds)")
plt.tight_layout(); plt.show()
top.round(4)

#now we are saving the model using joblib library

# Feature importance dict for the API
fi_values = np.abs(final_model.coef_[0])
fi_series = pd.Series(fi_values, index=model_columns).sort_values(ascending=False)
feature_importance = [{"feature": k, "importance": round(float(v), 6)}
                      for k, v in fi_series.head(20).items()]

model_data = {
    "model": final_model,
    "model_name": best_name,
    "scaler": scaler,
    "model_columns": model_columns,
    "numeric_features": numeric_features,
    "binary_flags": binary_flags,
    "categorical_features": categorical_features,
    "train_medians": train_medians,
    "metrics": tuned_metrics,
    "feature_importance": feature_importance,
    "threshold": 0.5,
}
joblib.dump(model_data, "artifacts/model_data.joblib")
print("Saved -> artifacts/model_data.joblib")


loaded = joblib.load("artifacts/model_data.joblib")
sample = X_test.head(5)
proba = loaded["model"].predict_proba(sample)[:, 1]
pd.DataFrame({"return_probability": proba.round(3),
              "predicted_returned": (proba >= loaded["threshold"]).astype(int)})

print("=" * 60)
print("MODEL EVALUATION REPORT - Product Return Prediction")
print("=" * 60)
print(f"Orders: {df.shape[0]} | return rate: {y.mean():.1%}")
print(f"After outlier removal, train rows: {len(y_train)} | test rows: {len(y_test)}")
print(f"Total model features: {len(model_columns)}")
print(f"  Numeric: {len(numeric_features)} | Binary flags: {len(binary_flags)} | Categorical (encoded): {len(categorical_features)}")
print(f"\nModel comparison (all with class_weight='balanced'), sorted by F1:")
print(comparison.round(4).to_string())
print(f"\nFinal model: {best_name}")
print("\nFinal test metrics:")
for k, v in tuned_metrics.items():
    print(f"  {k:10s}: {v:.4f}")
print("\nArtifacts: dataset/cleaned_returns.csv, artifacts/model_data.joblib")
