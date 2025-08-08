import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

def train_and_save_model():
    df = pd.read_csv('data/sentiment.csv')

    df = df[['Sentiment', 'Comment']].dropna()
    df.columns = ['label', 'text']

    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    os.makedirs('model', exist_ok=True)

    joblib.dump(pipeline, 'model/sentiment_model.pkl')
    print("✅ Model trained and saved to 'model/sentiment_model.pkl'")

if __name__ == '__main__':
    train_and_save_model()

