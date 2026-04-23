from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text


# ---------------- EVALUATION ----------------
def evaluate_answer(user_answer, ideal_answer):
    user_answer = clean_text(user_answer)
    ideal_answer = clean_text(ideal_answer)

    # TF-IDF similarity
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([user_answer, ideal_answer])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    # Keyword matching (important words only)
    ideal_words = set(ideal_answer.split())
    user_words = set(user_answer.split())

    # Remove very common short words
    ideal_keywords = {w for w in ideal_words if len(w) > 3}
    user_keywords = {w for w in user_words if len(w) > 3}

    if len(ideal_keywords) == 0:
        keyword_score = 0
    else:
        common = ideal_keywords.intersection(user_keywords)
        keyword_score = len(common) / len(ideal_keywords)

    # Length factor (prevents harsh penalty for short answers)
    length_ratio = min(len(user_words) / len(ideal_words), 1)

    # Final weighted score
    final_score = (
        similarity * 0.5 +
        keyword_score * 0.3 +
        length_ratio * 0.2
    ) * 10

    # Clamp score between 1 and 10 (avoid extreme zero)
    final_score = max(1, min(final_score, 10))

    return round(final_score, 2)


# ---------------- FEEDBACK ----------------
def generate_feedback(score):
    if score >= 8:
        return "Excellent answer. Clear understanding and good explanation."
    elif score >= 6:
        return "Good answer. Covers main points but can be improved."
    elif score >= 4:
        return "Average answer. Partial understanding shown."
    else:
        return "Weak answer. Needs better clarity and key concepts."