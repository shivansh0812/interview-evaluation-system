import streamlit as st
import time
import matplotlib.pyplot as plt
from utils.question_loader import get_random_question

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Interview Evaluation System", layout="centered")

# ---------------- SESSION INIT ----------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.history = []
    st.session_state.scores = []
    st.session_state.start_time = None
    st.session_state.answer_input = ""

# ---------------- TITLE ----------------
st.title("💼 Interview Evaluation System")
st.markdown("Practice role-based questions and get instant feedback")
st.divider()

# ---------------- ROLE SELECTION ----------------
roles = [
    "software_engineer",
    "data_analyst",
    "web_designer",
    "machine_learning_engineer",
    "it_manager",
    "architect"
]

role = st.selectbox("Select Role", roles)

# ---------------- START INTERVIEW ----------------
if not st.session_state.started:
    if st.button("🚀 Start Interview"):
        st.session_state.started = True
        st.session_state.questions = [get_random_question(role) for _ in range(3)]
        st.session_state.current_q = 0
        st.session_state.history = []
        st.session_state.scores = []
        st.session_state.start_time = time.time()
        st.session_state.answer_input = ""
        st.rerun()

# ---------------- INTERVIEW FLOW ----------------
if st.session_state.started:

    q_index = st.session_state.current_q
    question_data = st.session_state.questions[q_index]

    st.subheader(f"Question {q_index + 1}")
    st.write(question_data["question"])

    # ---------------- TIMER ----------------
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 120 - elapsed)

    st.info(f"⏳ Time left: {remaining} seconds")

    # Auto refresh every 1 second
    time.sleep(1)
    st.rerun()

    # ---------------- ANSWER INPUT ----------------
    user_answer = st.text_area(
        "Your Answer",
        key="answer_input",
        height=150
    )

    # ---------------- SUBMIT ----------------
    if st.button("Submit Answer"):

        # simple scoring logic (you can improve later)
        score = min(len(user_answer.split()) // 5, 10)

        # save history
        st.session_state.history.append({
            "question": question_data["question"],
            "answer": user_answer,
            "ideal": question_data["answer"],
            "score": score
        })

        st.session_state.scores.append(score)

        st.success(f"Score: {score}/10")

        # show correct answer
        st.markdown("**✅ Ideal Answer:**")
        st.write(question_data["answer"])

        # reset answer
        st.session_state.answer_input = ""

        # reset timer
        st.session_state.start_time = time.time()

        # move next
        if st.session_state.current_q < 2:
            st.session_state.current_q += 1
        else:
            st.session_state.finished = True

        st.rerun()

    # ---------------- FINISH BUTTON ----------------
    if st.button("🏁 Finish Interview"):
        st.session_state.finished = True
        st.rerun()

# ---------------- RESULTS ----------------
if "finished" in st.session_state and st.session_state.finished:

    st.divider()
    st.header("📊 Interview Summary")

    if st.session_state.scores:
        avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.success(f"Average Score: {round(avg_score, 2)}/10")

        # graph
        fig, ax = plt.subplots()
        ax.plot(st.session_state.scores, marker='o')
        ax.set_xlabel("Question")
        ax.set_ylabel("Score")
        ax.set_title("Performance Over Questions")
        st.pyplot(fig)

    # ---------------- HISTORY ----------------
    st.subheader("📜 Detailed Review")

    for i, item in enumerate(st.session_state.history):
        with st.expander(f"Q{i+1} - Score: {item['score']}/10"):
            st.write("**Question:**", item["question"])
            st.write("**Your Answer:**", item["answer"])
            st.write("**Ideal Answer:**", item["ideal"])

    # ---------------- RESET ----------------
    if st.button("🔄 Restart Interview"):
        st.session_state.clear()
        st.rerun()
