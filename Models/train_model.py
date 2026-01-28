import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

DATASET_PATH = '../datasets/Complete_Large_Dataset.csv'
MODEL_FILE = 'vishing_model.pkl'
VECTORIZER_FILE = 'tfidf_vectorizer.pkl'

def train_brain():
    print("Starting Model Training...")
    
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Could not find {DATASET_PATH}")
        return

    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset Loaded: {len(df)} rows")

    df['TARGET'] = df['LABEL'].apply(lambda x: 1 if str(x).lower().strip() == 'scam' else 0)

    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['TEXT'])
    y = df['TARGET']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"\nModel Accuracy: {acc*100:.2f}%")
    print("-" * 50)
    print(classification_report(y_test, predictions))
    print("-" * 50)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(vectorizer, VECTORIZER_FILE)
    print(f"Success! Model saved as '{MODEL_FILE}'")
    print(f"Success! Vectorizer saved as '{VECTORIZER_FILE}'")

if __name__ == "__main__":
    train_brain()