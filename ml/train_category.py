import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


# Load Dataset
df = pd.read_csv("ml/medicine_category_dataset.csv")

print(f"Total Records: {len(df)}")
print(f"Total Categories: {df['category'].nunique()}")


# Features and Labels
X = df["medicine_name"]
y = df["category"]


# Improved TF-IDF
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    lowercase=True
)

X_vectorized = vectorizer.fit_transform(X)


# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Improved Logistic Regression
model = LogisticRegression(
    max_iter=5000,
    C=2.0,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Predict
predictions = model.predict(X_test)


# Metrics
accuracy = accuracy_score(y_test, predictions)

print("\nClassification Report\n")
print(classification_report(y_test, predictions))

print(f"\nAccuracy: {accuracy:.4f}")


# Save Vectorizer
joblib.dump(
    vectorizer,
    "ml/category_vectorizer.joblib"
)

# Save Model
joblib.dump(
    model,
    "ml/category_model.joblib"
)

print("\nCategory model saved successfully.")
print("Saved:")
print(" - ml/category_model.joblib")
print(" - ml/category_vectorizer.joblib")