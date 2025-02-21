'''import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data from the CSV
data = pd.read_csv(r"C:\Users\Gowtham Reddy\Desktop\ePharma\model\symptoms_medicine.csv")

# Vectorize the symptoms column
vectorizer = TfidfVectorizer()
X_train = data["symptom"]  # Column containing symptoms
y_train = data["medication"]  # Column containing medications
X_train_tfidf = vectorizer.fit_transform(X_train)

# Train the model
model = RandomForestClassifier()
model.fit(X_train_tfidf, y_train)

# Save the vectorizer and model to a pickle file
with open('model/model.pkl', 'wb') as f:
    pickle.dump((vectorizer, model), f)'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
data = pd.read_csv('model/data.csv')

# Clean and preprocess data
data = data.dropna(subset=['medicine'])

# Combine symptoms into a single feature
def combine_symptoms(row):
    symptoms = [str(row['symptom1']), str(row['symptom2']), str(row['symptom3'])]
    return ' '.join([sym for sym in symptoms if sym.lower() != 'nan'])

data['combined_symptoms'] = data.apply(combine_symptoms, axis=1)

# Prepare features and target
X = data['combined_symptoms']
y = data['medicine']

# Split data with no stratification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create pipeline with TF-IDF and Logistic Regression
model = make_pipeline(
    TfidfVectorizer(stop_words='english', ngram_range=(1,2)),
    LogisticRegression(multi_class='ovr', max_iter=1000)
)

# Train the model
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy * 100:.2f}%')

# Detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'model.pkl')
print("Model training complete and saved.")
