import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer


# =========================================================
# NLP ENGINE
# =========================================================

def analyze_meeting(meeting_text):

    # Clean text
    meeting_text = meeting_text.strip()

    # Split into sentences
    sentences = re.split(
        r'(?<=[.!?])\s+',
        meeting_text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    # -----------------------------------------------------
    # PARTICIPANT DETECTION
    # -----------------------------------------------------

    participants = []

    for sentence in sentences:

        match = re.match(
            r'([A-Z][a-zA-Z]+)\s*:',
            sentence
        )

        if match:
            name = match.group(1)

            if name not in participants:
                participants.append(name)

    # -----------------------------------------------------
    # ACTION ITEM DETECTION
    # -----------------------------------------------------

    action_keywords = [
        "will",
        "need to",
        "should",
        "must",
        "prepare",
        "complete",
        "check",
        "clean",
        "submit",
        "finish",
        "create",
        "develop",
        "review",
        "send",
        "update",
        "fix",
        "design",
        "test",
        "implement"
    ]

    action_items = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in action_keywords
        ):

            # Person
            name_match = re.match(
                r'([A-Z][a-zA-Z]+)\s*:',
                sentence
            )

            person = (
                name_match.group(1)
                if name_match
                else "Unassigned"
            )

            # Deadline
            deadline_match = re.search(
                r'\b('
                r'Monday|Tuesday|Wednesday|Thursday|'
                r'Friday|Saturday|Sunday|'
                r'today|tomorrow|'
                r'next week|next month|'
                r'this week'
                r')\b',
                sentence,
                re.IGNORECASE
            )

            deadline = (
                deadline_match.group(1)
                if deadline_match
                else "Not specified"
            )

            # Task
            task = re.sub(
                r'^[A-Z][a-zA-Z]+\s*:\s*',
                '',
                sentence
            )

            action_items.append({
                "Person": person,
                "Task": task,
                "Deadline": deadline
            })

    # -----------------------------------------------------
    # KEY DECISION DETECTION
    # -----------------------------------------------------

    decision_keywords = [
        "decided",
        "agreed",
        "will use",
        "finalized",
        "selected",
        "approved",
        "choose",
        "chosen",
        "confirmed"
    ]

    key_decisions = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in decision_keywords
        ):

            decision = re.sub(
                r'^[A-Z][a-zA-Z]+\s*:\s*',
                '',
                sentence
            )

            key_decisions.append(decision)

    # -----------------------------------------------------
    # SUMMARY USING TF-IDF
    # -----------------------------------------------------

    if len(sentences) <= 3:

        summary = " ".join(sentences)

    else:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(sentences)

        scores = matrix.sum(axis=1).A1

        number_of_sentences = min(4, len(sentences))

        top_indices = scores.argsort()[
            -number_of_sentences:
        ][::-1]

        top_indices = sorted(top_indices)

        summary = " ".join(
            sentences[i]
            for i in top_indices
        )

    # -----------------------------------------------------
    # PRIORITY DETECTION
    # -----------------------------------------------------

    urgent_words = [
        "urgent",
        "asap",
        "immediately",
        "critical",
        "emergency",
        "high priority"
    ]

    priority = "Normal"

    if any(
        word in meeting_text.lower()
        for word in urgent_words
    ):
        priority = "High"

    # -----------------------------------------------------
    # MEETING TONE
    # -----------------------------------------------------

    positive_words = [
        "good",
        "great",
        "successful",
        "approved",
        "progress",
        "excellent"
    ]

    negative_words = [
        "problem",
        "issue",
        "delay",
        "failed",
        "concern",
        "risk"
    ]

    positive_count = sum(
        word in meeting_text.lower()
        for word in positive_words
    )

    negative_count = sum(
        word in meeting_text.lower()
        for word in negative_words
    )

    if positive_count > negative_count:
        tone = "Positive"

    elif negative_count > positive_count:
        tone = "Concerned"

    else:
        tone = "Neutral"

    # -----------------------------------------------------
    # RETURN RESULTS
    # -----------------------------------------------------

    return {
        "summary": summary,
        "participants": participants,
        "action_items": action_items,
        "key_decisions": key_decisions,
        "priority": priority,
        "tone": tone,
        "sentence_count": len(sentences),
        "word_count": len(meeting_text.split())
    }


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        text-align: center;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI Meeting Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform meeting conversations into structured insights using NLP.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DEMO TEXT
# =========================================================

demo_text = """Rahul: We need to complete the NLP project presentation by Friday.
Priya: I will clean the dataset and submit it tomorrow.
Aman: I will prepare the introduction and problem statement.
Rahul: We decided to use Python and Streamlit for the application.
Priya: The team should review the final model before Monday.
Aman: This is a high priority task because the presentation is next week."""


# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🧪 Load Demo Meeting",
        use_container_width=True
    ):

        st.session_state["meeting"] = demo_text


with col2:

    if st.button(
        "🗑️ Clear",
        use_container_width=True
    ):

        st.session_state["meeting"] = ""


# =========================================================
# INPUT
# =========================================================

if "meeting" not in st.session_state:

    st.session_state["meeting"] = ""


meeting_text = st.text_area(
    "🎙️ Meeting Conversation",
    value=st.session_state["meeting"],
    height=280,
    placeholder=(
        "Paste your meeting transcript here...\n\n"
        "Example:\n"
        "Rahul: I will complete the report by Friday."
    )
)


# =========================================================
# ANALYZE
# =========================================================

if st.button(
    "🚀 Analyze Meeting",
    type="primary",
    use_container_width=True
):

    if not meeting_text.strip():

        st.warning(
            "Please enter a meeting conversation first."
        )

    else:

        result = analyze_meeting(meeting_text)

        st.success(
            "Meeting analyzed successfully!"
        )

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">📊 Meeting Overview</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Participants",
                len(result["participants"])
            )

        with c2:
            st.metric(
                "Action Items",
                len(result["action_items"])
            )

        with c3:
            st.metric(
                "Decisions",
                len(result["key_decisions"])
            )

        with c4:
            st.metric(
                "Priority",
                result["priority"]
            )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">📝 Meeting Summary</div>',
            unsafe_allow_html=True
        )

        st.info(result["summary"])

        # -------------------------------------------------
        # PARTICIPANTS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">👥 Participants</div>',
            unsafe_allow_html=True
        )

        if result["participants"]:

            st.write(
                " • ".join(result["participants"])
            )

        else:

            st.info(
                "No named participants detected."
            )

        # -------------------------------------------------
        # ACTION ITEMS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">✅ Action Items</div>',
            unsafe_allow_html=True
        )

        if result["action_items"]:

            for index, item in enumerate(
                result["action_items"],
                start=1
            ):

                with st.expander(
                    f"Task {index} — {item['Person']}"
                ):

                    st.write(
                        f"**Task:** {item['Task']}"
                    )

                    st.write(
                        f"**Deadline:** {item['Deadline']}"
                    )

        else:

            st.info(
                "No action items detected."
            )

        # -------------------------------------------------
        # DECISIONS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">💡 Key Decisions</div>',
            unsafe_allow_html=True
        )

        if result["key_decisions"]:

            for decision in result["key_decisions"]:

                st.success(
                    f"✓ {decision}"
                )

        else:

            st.info(
                "No major decisions detected."
            )

        # -------------------------------------------------
        # INSIGHTS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">🧠 Meeting Insights</div>',
            unsafe_allow_html=True
        )

        st.write(
            f"**Meeting Tone:** {result['tone']}"
        )

        st.write(
            f"**Priority:** {result['priority']}"
        )

        st.write(
            f"**Sentences:** {result['sentence_count']}"
        )

        st.write(
            f"**Words:** {result['word_count']}"
        )

        # -------------------------------------------------
        # DOWNLOAD REPORT
        # -------------------------------------------------

        report = f"""
AI MEETING INTELLIGENCE REPORT
==============================

MEETING SUMMARY
{result['summary']}

PARTICIPANTS
{', '.join(result['participants'])}

ACTION ITEMS
"""

        for item in result["action_items"]:

            report += (
                f"\nPerson: {item['Person']}"
                f"\nTask: {item['Task']}"
                f"\nDeadline: {item['Deadline']}\n"
            )

        report += "\nKEY DECISIONS\n"

        for decision in result["key_decisions"]:

            report += f"- {decision}\n"

        report += (
            f"\nMEETING TONE: {result['tone']}"
            f"\nPRIORITY: {result['priority']}"
        )

        st.download_button(
            "📥 Download Meeting Report",
            report,
            file_name="meeting_report.txt",
            mime="text/plain",
            use_container_width=True
        )
