import streamlit as st
from utils.question_loader import get_random_question
from utils.evaluator import evaluate_answer, generate_feedback
from utils.db_helper import insert_record, get_all_records

import time
import random

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
defaults = {
    "questions": [],
    "current_q": 0,
    "scores": [],
    "answered": False,
    "user_answer": "",
    "start_time": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- LOAD QUESTIONS (RANDOM + UNIQUE) ----------------
def load_questions():
    st.session_state.questions = []
    used = set()

    # Try multiple times to ensure randomness
    while len(st.session_state.questions) < 3:
        q = get_random_question(role)
        if q and q["question"] not in used:
            st.session_state.questions.append(q)
            used.add(q["question"])

    st.session_state.current_q = 0
    st.session_state.scores = []
    st.session_state.answered = False
    st.session_state.user_answer = ""
    st.session_state.start_time = time.time()

# ---------------- START ----------------
if st.button("🚀 Start Interview"):
    load_questions()

# ---------------- MAIN FLOW ----------------
if st.session_state.questions:

    total = len(st.session_state.questions)
    idx = st.session_state.current_q

    if idx < total:
        q = st.session_state.questions[idx]

        # ---------------- TIMER (2 MIN) ----------------
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            remaining = max(0, 120 - elapsed)

            mins = remaining // 60
            secs = remaining % 60

            st.warning(f"⏱ Time Left: {mins:02d}:{secs:02d}")

            if remaining == 0:
                st.error("Time's up! Moving to next question.")
                st.session_state.current_q += 1
                st.session_state.start_time = time.time()
                st.session_state.answered = False
                st.rerun()

        # ---------------- PROGRESS ----------------
        st.progress((idx + 1) / total)
        st.markdown(f"### 📌 Question {idx+1} of {total}")
        st.info(q["question"])

        # ---------------- INPUT ----------------
        user_answer = st.text_area(
            "✍️ Your Answer",
            value=st.session_state.user_answer,
            key=f"answer_{idx}"
        )

        # ---------------- SUBMIT ----------------
        if st.button("Submit Answer"):
            if user_answer.strip() == "":
                st.warning("Please enter an answer.")
            else:
                score = evaluate_answer(user_answer, q["ideal_answer"])
                feedback = generate_feedback(score)

                st.session_state.scores.append(score)
                st.session_state.answered = True
                st.session_state.user_answer = user_answer

                insert_record(role, q["question"], user_answer, score, feedback)

                st.success(f"Score: {score}/10")
                st.info(f"Feedback: {feedback}")

                st.markdown("### ✅ Ideal Answer")
                st.success(q["ideal_answer"])

        # ---------------- NEXT ----------------
        if st.session_state.answered:
            if idx < total - 1:
                if st.button("➡️ Next Question"):
                    st.session_state.current_q += 1
                    st.session_state.answered = False
                    st.session_state.user_answer = ""
                    st.session_state.start_time = time.time()
                    st.rerun()
            else:
                if st.button("🏁 Finish Interview"):
                    st.session_state.current_q += 1
                    st.rerun()

    else:
        # ---------------- FINAL RESULT ----------------
        st.markdown("## 📊 Final Result")

        avg_score = round(sum(st.session_state.scores) / len(st.session_state.scores), 2)
        st.success(f"Average Score: {avg_score}/10")

        # ---------------- GRAPH ----------------
        st.markdown("### 📈 Performance Graph")
        st.line_chart(st.session_state.scores)

        # ---------------- RESTART ----------------
        if st.button("🔄 Restart Interview"):
            st.session_state.questions = []
            st.session_state.current_q = 0
            st.session_state.scores = []
            st.session_state.answered = False
            st.session_state.user_answer = ""
            st.session_state.start_time = None
            st.rerun()

# ---------------- HISTORY ----------------
st.divider()
st.markdown("## 📜 Interview History")

filter_role = st.selectbox("Filter by Role", ["All"] + roles)

if st.button("Show History"):
    records = get_all_records()

    if filter_role != "All":
        records = [r for r in records if r[0] == filter_role]

    if records:
        for i, r in enumerate(records, 1):
            with st.expander(f"{i}. {r[0]} | Score: {r[3]}/10"):
                st.write(f"**Question:** {r[1]}")
                st.write(f"**Answer:** {r[2]}")
                st.write(f"**Feedback:** {r[4]}")
    else:
        st.info("No records found.")