import streamlit as st
import time
import random
import matplotlib.pyplot as plt

from utils.question_loader import get_random_question
from utils.evaluator import evaluate_answer, generate_feedback

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Interview Evaluation System", layout="centered")

# ---------------- TITLE ----------------
st.title("💼 Interview Evaluation System")
st.markdown("Practice role-based questions and get instant feedback")
st.divider()

# ---------------- ROLES ----------------
roles = [
    "software_engineer",
    "data_analyst",
    "web_designer",
    "machine_learning_engineer",
    "it_manager",
    "architect"
]

role = st.selectbox("Select Role", roles)

# ---------------- SESSION INIT ----------------
if "questions" not in st.session_state:
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.scores = []
    st.session_state.history = []
    st.session_state.start_time = None
    st.session_state.interview_started = False

# ---------------- START BUTTON ----------------
if st.button("🚀 Start Interview"):
    st.session_state.questions = [
        get_random_question(role) for _ in range(3)
    ]
    st.session_state.current_q = 0
    st.session_state.scores = []
    st.session_state.history = []
    st.session_state.interview_started = True
    st.session_state.start_time = time.time()

# ---------------- INTERVIEW FLOW ----------------
if st.session_state.interview_started:

    q_index = st.session_state.current_q

    if q_index < len(st.session_state.questions):

        q_data = st.session_state.questions[q_index]

        st.subheader(f"Question {q_index + 1}")
        st.write(q_data["question"])

        # ---------------- TIMER ----------------
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 120 - elapsed)

        st.info(f"⏳ Time left: {remaining} seconds")

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):

            score = evaluate_answer(answer, q_data["ideal_answer"])
            feedback = generate_feedback(score)

            st.success(f"Score: {round(score,2)}/10")
            st.write(f"Feedback: {feedback}")

            # Save per-session history
            st.session_state.scores.append(score)
            st.session_state.history.append({
                "question": q_data["question"],
                "answer": answer,
                "score": score
            })

            # Move next
            st.session_state.current_q += 1
            st.session_state.start_time = time.time()

            st.rerun()

    else:
        # ---------------- FINAL RESULT ----------------
        st.header("📊 Final Result")

        avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.success(f"Average Score: {round(avg_score,2)}/10")

        # ---------------- GRAPH ----------------
        st.subheader("📈 Performance Graph")

        fig, ax = plt.subplots()
        ax.plot(st.session_state.scores, marker='o')
        ax.set_xlabel("Question")
        ax.set_ylabel("Score")
        ax.set_title("Performance Over Questions")

        st.pyplot(fig)

        # ---------------- SESSION HISTORY ----------------
        st.subheader("🧾 Your Session History")

        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Q{i+1} - Score: {round(item['score'],2)}"):
                st.write("**Question:**", item["question"])
                st.write("**Your Answer:**", item["answer"])

        if st.button("🔄 Restart Interview"):
            st.session_state.clear()
            st.rerun()

# ---------------- NO GLOBAL HISTORY ----------------
st.divider()
st.info("Note: History is session-based and resets for each user.")
