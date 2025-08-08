from .model import model

def analyze_comments(comments):
    predictions = model.predict(comments)
    probabilities = model.predict_proba(comments)
    results = []

    label_map = {
        0: "Negative",
        1: "Neutral",
        2: "Positive"
    }

    for comment, label, prob in zip(comments, predictions, probabilities):
        sentiment = label_map.get(label, "Unknown")
        rating = round(prob[label] * 10, 2)
        results.append({
            "comment": comment,
            "sentiment": sentiment,
            "rating": rating
        })
    return results

