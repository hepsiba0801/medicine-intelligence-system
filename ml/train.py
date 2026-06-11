import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

df = pd.read_csv("medicine_dataset.csv")
X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipeline = Pipeline([("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 4))), ("model", LogisticRegression(max_iter=1000))])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
print(classification_report(y_test, predictions))
joblib.dump(pipeline,"ml/model.joblib")
print("Model saved successfully.")