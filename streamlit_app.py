import streamlit as st
import matplotlib.pyplot as plt
import random 

from utils.question_loader import get_all_questions
from utils.evaluator import evaluate_answer, generate_feedback

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Interview Evaluation System", layout="centered")

# ---------------- SESSION INIT ----------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.history = []
    st.session_state.scores = []
    st.session_state.answer_input = ""
    st.session_state.finished = False
    st.session_state.submitted = False

# ---------------- TITLE ----------------
st.title("💼 Interview Evaluation System")
st.markdown("Practice role-based questions and get instant feedback")
st.divider()

# ---------------- ROLE ----------------
roles = ["software_engineer", "data_analyst", "web_designer", "machine_learning_engineer"]

selected_role = st.selectbox("Select Role", roles)

# ---------------- START ----------------
if not st.session_state.started:
    if st.button("🚀 Start Interview"):
        questions = get_all_questions(selected_role)

        if questions:
            random.shuffle(questions)  # ✅ SHUFFLE QUESTIONS
            st.session_state.questions = questions[:3]  # pick random 3

            st.session_state.started = True
            st.session_state.current_q = 0
            st.session_state.history = []
            st.session_state.scores = []
            st.session_state.answer_input = ""
            st.session_state.finished = False
            st.session_state.submitted = False
            st.rerun()

# ---------------- INTERVIEW ----------------
if st.session_state.started and not st.session_state.finished:

    q_index = st.session_state.current_q
    question_data = st.session_state.questions[q_index]

    st.subheader(f"Question {q_index + 1}")
    st.write(question_data["question"])

    # -------- INPUT --------
    answer = st.text_area(
        "Your Answer",
        key=f"answer_{q_index}"
    )

    # -------- SUBMIT --------
    if st.button("Submit Answer"):

        score = evaluate_answer(answer, question_data["ideal_answer"])
        feedback = generate_feedback(score)

        st.session_state.history.append({
            "question": question_data["question"],
            "answer": answer,
            "correct": question_data["ideal_answer"],
            "score": score,
            "feedback": feedback
        })

        st.session_state.scores.append(score)
        st.session_state.submitted = True

    # -------- AFTER SUBMIT --------
    if st.session_state.submitted:

        last = st.session_state.history[-1]

        st.success(f"Score: {last['score']}/10")
        st.info(f"Feedback: {last['feedback']}")

        st.markdown("**Correct Answer:**")
        st.write(last["correct"])

        if st.button("Next Question"):

            st.session_state.current_q += 1
            st.session_state.submitted = False

            if st.session_state.current_q >= len(st.session_state.questions):
                st.session_state.finished = True

            st.rerun()

# ---------------- RESULTS ----------------
if st.session_state.finished:

    st.header("📊 Interview Result")

    avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
    st.success(f"Average Score: {round(avg_score, 2)}/10")

    # -------- GRAPH --------
    fig, ax = plt.subplots()
    ax.plot(st.session_state.scores, marker='o')
    ax.set_xlabel("Question")
    ax.set_ylabel("Score")
    ax.set_title("Performance Over Questions")
    st.pyplot(fig)

    # -------- REVIEW --------
    st.subheader("📝 Detailed Review")

    for i, item in enumerate(st.session_state.history):
        with st.expander(f"Q{i+1} - Score: {item['score']}/10"):
            st.write("**Question:**", item["question"])
            st.write("**Your Answer:**", item["answer"])
            st.write("**Correct Answer:**", item["correct"])
            st.write("**Feedback:**", item["feedback"])

    # -------- RESTART --------
    if st.button("🔄 Restart Interview"):
        st.session_state.clear()
        st.rerun()
