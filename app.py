import streamlit as st

from ai.generator import generate_course
from utils.pdf_generator import create_pdf

# -----------------------------
# SESSION STATE
# -----------------------------

if "roadmap" not in st.session_state:
    st.session_state.roadmap = None

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Roadmap Generator",
    page_icon="💡",
    layout="wide"
)

# -----------------------------
# LOAD CSS
# -----------------------------

with open("assets/styles.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.markdown(
    """
    <div style="
        font-size:2rem;
        font-weight:900;
        margin-top:0px;
        margin-bottom:20px;
        color:white;
        letter-spacing:-1px;
        line-height:1.2;
        word-break:break-word;
    ">
        PROMPT - COURSE
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <h3 style="
        margin-top:0;
        color:#60A5FA;
        margin-bottom:15px;
    ">
    🚀 AI Learning Platform
    </h3>

    <div style="
        line-height:2.1;
        font-size:1rem;
        margin-bottom:30px;
    ">
    • Personalized AI Roadmaps<br>
    • PDF Export<br>
    • Practice Platforms<br>
    • Smart Learning Paths
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <h3 style="color:white;">
    ⚡ Platform Status
    </h3>

    <div style="line-height:2;font-size:1rem;">
    🟢 AI Engine Online<br>
    📄 PDF Export Ready<br>
    💻 Local Deployment Active
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <h3 style="color:white;">
    🧠 Powered By
    </h3>

    <div style="line-height:2;font-size:1rem;">
    • Gemini AI<br>
    • Streamlit<br>
    • ReportLab
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HERO SECTION
# -----------------------------

st.markdown(
    """
    <div class="hero-title">
    AI Learning Roadmap Generator
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
    Generate AI-powered personalized learning roadmaps instantly.
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# EXAMPLE GOALS
# -----------------------------

st.markdown("### 💡 Example Goals")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("Learn Python in 6 months")

with c2:
    st.info("Become ML Engineer in 1 year")

with c3:
    st.info("Master DSA for placements")

# -----------------------------
# USER INPUT
# -----------------------------

prompt = st.text_area(
    "What do you want to learn?",
    placeholder="Example: Learn Python in 6 months",
    height=150
)

# -----------------------------
# OPTIONS
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    level = st.selectbox(
        "Select Your Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

with col2:

    goal_type = st.selectbox(
        "Goal Type",
        [
            "Job Ready",
            "Interview Preparation",
            "Competitive Programming",
            "Academic Learning",
            "Project Building"
        ]
    )

hours = st.slider(
    "Study Hours Per Day",
    1,
    10,
    2
)

# -----------------------------
# GENERATE BUTTON
# -----------------------------

generate = st.button(
    "Generate Roadmap"
)

# -----------------------------
# GENERATE ROADMAP
# -----------------------------

if generate:

    if prompt.strip() == "":

        st.warning(
            "Please enter a learning goal."
        )

    else:

        full_prompt = f"""
Goal: {prompt}

Level: {level}

Study Hours Per Day: {hours}

Goal Type: {goal_type}

Generate roadmap according to user's duration.

Rules:
- Keep concise
- Unique months
- No repetition
- Include:
  - Topics
  - Resources
  - Practice websites
- Use REAL resource links
- Beginner friendly
- Clean markdown
"""

        with st.spinner(
            "🧠 AI is building your personalized roadmap..."
        ):

            st.session_state.roadmap = generate_course(
                full_prompt
            )

# -----------------------------
# DISPLAY ROADMAP
# -----------------------------

if st.session_state.roadmap:



    # -----------------------------
    # ROADMAP CARDS
    # -----------------------------

    months = st.session_state.roadmap.split("## ")

    for month in months:

        if month.strip() != "":

            lines = month.split("\n")

            title = lines[0]

            content = "\n".join(lines[1:])

            st.markdown(
                f"""
                <div class="roadmap-card">

                <h2>
                📚 {title}
                </h2>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(content)

    # -----------------------------
    # SUCCESS
    # -----------------------------

    st.success(
        "✅ Roadmap generated successfully!"
    )

    # -----------------------------
    # PDF DOWNLOAD
    # -----------------------------

    try:

        pdf_file = create_pdf(
            st.session_state.roadmap
        )

        with open(
            pdf_file,
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Roadmap as PDF",
                data=file,
                file_name="AI_Roadmap.pdf",
                mime="application/pdf"
            )

    except Exception:

        st.warning(
            "PDF generation temporarily unavailable."
        )

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    """
    <div style='
        text-align:center;
        color:#94A3B8;
        padding-top:20px;
        padding-bottom:5px;
        margin-top:10px;
        font-size:0.95rem;
    '>

    Built with ❤️ using Streamlit + OpenRouter AI

    </div>
    """,
    unsafe_allow_html=True
)