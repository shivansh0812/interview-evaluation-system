from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def evaluate_answer(user_answer, correct_answer):
    """
    Evaluate similarity between user answer and correct answer
    using TF-IDF + cosine similarity.
    Returns score out of 10 (less harsh, more realistic).
    """

    # ---------- CLEAN INPUT ----------
    if not user_answer or not user_answer.strip():
        return 0

    user_answer = user_answer.lower()
    correct_answer = correct_answer.lower()

    # ---------- TF-IDF ----------
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2)  # captures phrases too
    )

    tfidf = vectorizer.fit_transform([user_answer, correct_answer])

    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    # ---------- LENGTH FACTOR ----------
    user_len = len(user_answer.split())
    correct_len = len(correct_answer.split())

    length_ratio = min(user_len / (correct_len + 1), 1)

    # ---------- FINAL SCORE (BALANCED) ----------
    # weight similarity + length
    final_score = (0.75 * similarity) + (0.25 * length_ratio)

    # smoothing to avoid harsh scoring
    final_score = (final_score * 0.8) + 0.2

    score_out_of_10 = round(final_score * 10)

    return int(score_out_of_10)


def generate_feedback(score):
    """
    Generate human-like feedback based on score
    """

    if score >= 9:
        return "Excellent answer. Very clear, complete, and well-structured."

    elif score >= 7:
        return "Good answer. You covered most key points, just refine clarity."

    elif score >= 5:
        return "Decent answer. Some important concepts are missing."

    elif score >= 3:
        return "Basic understanding shown, but explanation is weak."

    else:
        return "Poor answer. Try to include key concepts and explain properly."
