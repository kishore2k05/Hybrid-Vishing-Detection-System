import joblib
import os

MODEL_PATH = 'vishing_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

def test_prediction():
    print("Loading the Brain...")
    
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("Error: Model files not found! Run 'train_model.py' first.")
        return

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model Loaded Successfully!\n")

    test_sentences = [
        "Sir, unga bank account block aagiruchu, udane KYC update pannunga.",
        "Hello, I am calling from Amazon to deliver your package.",
        "Unnoda lottery prize claim panna indha link-a click pannu.",
        "Vanakkam, nalaiku meeting 10 maniku iruku, marakaama vandhurunga.",
        "Urgent! Your credit card is compromised. Share OTP immediately."
    ]

    print("Testing Predictions:\n")
    
    features = vectorizer.transform(test_sentences)
    predictions = model.predict(features)
    probs = model.predict_proba(features)

    for text, label, prob in zip(test_sentences, predictions, probs):
        confidence = max(prob) * 100
        status = "SCAM" if label == 1 else "SAFE"
        print(f"Text: \"{text}\"")
        print(f"Prediction: {status} (Confidence: {confidence:.2f}%)")
        print("-" * 50)

if __name__ == "__main__":
    test_prediction()