import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

from data_generator import generate_returns_dataset

def build_and_train_pipeline(data_path="ecommerce_returns.csv"):
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Generating realistic dataset...")
        df = generate_returns_dataset(n_samples=4000, random_seed=42)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    features = [
        "customer_age",
        "product_category",
        "item_price",
        "discount_percent",
        "past_return_rate",
        "items_in_order",
        "bracket_buying",
        "payment_method",
        "delivery_days",
        "is_first_purchase",
        "size_variation"
    ]
    target = "returned"

    X = df[features]
    y = df[target]

    numeric_features = [
        "customer_age",
        "item_price",
        "discount_percent",
        "past_return_rate",
        "items_in_order",
        "delivery_days"
    ]
    categorical_features = [
        "product_category",
        "payment_method",
        "size_variation",
        "bracket_buying",
        "is_first_purchase"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ]
    )

    clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=6,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", clf)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Training Random Forest Return Classifier...")
    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, y_proba)
    print("\n--- MODEL PERFORMANCE ---")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)

    # Save artifact bundle
    model_bundle = {
        "pipeline": pipeline,
        "features": features,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "metrics": {
            "roc_auc": round(float(roc_auc), 4),
            "confusion_matrix": cm.tolist()
        }
    }

    joblib.dump(model_bundle, "return_model.joblib")
    print("\nModel pipeline saved to 'return_model.joblib'.")
    return model_bundle

if __name__ == "__main__":
    build_and_train_pipeline()

