import streamlit as st
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
    st.session_state.answer_input = ""
    st.session_state.submitted = False
    st.session_state.finished = False

# ---------------- TITLE ----------------
st.title("💼 Interview Evaluation System")
st.markdown("Practice role-based questions and get instant feedback")
st.divider()

# ---------------- ROLE ----------------
roles = [
    "software_engineer",
    "data_analyst",
    "web_designer",
    "machine_learning_engineer",
    "it_manager",
    "architect"
]

role = st.selectbox("Select Role", roles)

# ---------------- START ----------------
if not st.session_state.started:
    if st.button("🚀 Start Interview"):
        st.session_state.started = True
        st.session_state.questions = [get_random_question(role) for _ in range(3)]
        st.session_state.current_q = 0
        st.session_state.history = []
        st.session_state.scores = []
        st.session_state.answer_input = ""
        st.session_state.submitted = False
        st.session_state.finished = False
        st.rerun()

# ---------------- SCORING FUNCTION ----------------
def calculate_score(answer):
    words = len(answer.split())

    if words == 0:
        return 0
    elif words < 10:
        return 3
    elif words < 25:
        return 5
    elif words < 50:
        return 7
    elif words < 80:
        return 8
    else:
        score = 9 + (words // 50)

    return min(10, score)

# ---------------- FEEDBACK FUNCTION ----------------
def generate_feedback(user_answer, ideal_answer):
    user_words = set(user_answer.lower().split())
    ideal_words = set(ideal_answer.lower().split())

    common = user_words.intersection(ideal_words)
    overlap_ratio = len(common) / max(len(ideal_words), 1)

    length = len(user_answer.split())

    if length == 0:
        return "❌ You did not provide an answer."

    if overlap_ratio > 0.5:
        return "✅ Strong answer. You covered most key concepts clearly."
    elif overlap_ratio > 0.25:
        return "👍 Decent answer, but missing some important points."
    else:
        return "⚠️ Your answer lacks key concepts. Try to be more detailed and structured."

# ---------------- INTERVIEW ----------------
if st.session_state.started and not st.session_state.finished:

    q_index = st.session_state.current_q
    question_data = st.session_state.questions[q_index]

    st.subheader(f"Question {q_index + 1}")
    st.write(question_data["question"])

    # ---------------- ANSWER INPUT ----------------
    user_answer = st.text_area(
        "Your Answer",
        value=st.session_state.answer_input,
        key="answer_box",
        height=150,
        disabled=st.session_state.submitted
    )

    if not st.session_state.submitted:
        st.session_state.answer_input = user_answer

    # ---------------- SUBMIT ----------------
    if not st.session_state.submitted:
        if st.button("Submit Answer"):

            score = calculate_score(user_answer)
            feedback = generate_feedback(user_answer, question_data["answer"])

            st.session_state.history.append({
                "question": question_data["question"],
                "answer": user_answer,
                "ideal": question_data["answer"],
                "feedback": feedback,
                "score": score
            })

            st.session_state.scores.append(score)
            st.session_state.submitted = True

    # ---------------- AFTER SUBMIT ----------------
    if st.session_state.submitted:

        st.success(f"Score: {st.session_state.scores[-1]}/10")

        st.markdown("### 💬 Feedback")
        st.info(st.session_state.history[-1]["feedback"])

        st.markdown("### ✅ Ideal Answer")
        st.write(question_data["answer"])

        # ---------------- NEXT OR FINISH ----------------
        if st.session_state.current_q < 2:
            if st.button("➡️ Next Question"):
                st.session_state.current_q += 1
                st.session_state.answer_input = ""
                st.session_state.submitted = False
                st.rerun()
        else:
            if st.button("🏁 Finish Interview"):
                st.session_state.finished = True
                st.rerun()

# ---------------- RESULTS ----------------
if st.session_state.finished:

    st.divider()
    st.header("📊 Interview Summary")

    if st.session_state.scores:
        avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.success(f"Average Score: {round(avg_score, 2)}/10")

        # ---------------- GRAPH ----------------
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
            st.write("**Feedback:**", item["feedback"])
            st.write("**Ideal Answer:**", item["ideal"])

    # ---------------- RESET ----------------
    if st.button("🔄 Restart Interview"):
        st.session_state.clear()
        st.rerun()
