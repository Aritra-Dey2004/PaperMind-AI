import streamlit as st
import re

from utils.pdf_loader import extract_text_from_pdf
from utils.text_cleaner import clean_text_func
from utils.chunker import chunk_text
from utils.embeddings import create_embeddings, model
from utils.vector_store import create_faiss_index
from utils.retriever import retrieve_chunks
from utils.gemini_helper import setup_gemini
from utils.hybrid_helper import generate_hybrid_response
from utils.pptx_generator import create_pptx
from utils.quiz_generator import quiz_prompt
from utils.paper_finder import search_arxiv_papers

st.set_page_config(
    page_title="PaperMind AI: GenAI Research Assistant",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
   html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 15%, rgba(124, 58, 237, 0.32), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(6, 182, 212, 0.30), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(34, 197, 94, 0.22), transparent 32%),
        linear-gradient(135deg, #e9ddff 0%, #cdf6ff 45%, #f1f5f9 100%) !important;
}
}

.block-container {
    padding-top: 2.5rem;
    max-width: 1200px;
}

/* Top brand bar */
.pm-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 4px 30px 4px;
}

.pm-logo {
    font-size: 28px;
    font-weight: 900;
    color: #5b21b6;
}

.pm-badge {
    background: #ede9fe;
    color: #5b21b6;
    padding: 9px 18px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 14px;
}

/* Hero section */
.pm-hero {
    text-align: center;
    padding: 30px 20px 55px 20px;
}

.pm-title {
    font-size: 66px;
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: -2.5px;
    color: #0f172a;
}

.pm-gradient {
    background: linear-gradient(90deg, #7c3aed, #06b6d4, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.pm-subtitle {
    margin-top: 22px;
    font-size: 20px;
    color: #64748b;
    line-height: 1.55;
}

.pm-cta {
    display: inline-block;
    margin-top: 32px;
    padding: 15px 36px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white;
    border-radius: 999px;
    font-size: 16px;
    font-weight: 900;
    box-shadow: 0 16px 35px rgba(124, 58, 237, 0.22);
}

/* Cards */
.pm-feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin: 10px 0 35px 0;
}

.pm-card {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(124, 58, 237, 0.18);
    border-radius: 24px;
    padding: 24px;
    min-height: 155px;
    box-shadow: 0 14px 35px rgba(79, 70, 229, 0.08);
    transition: 0.25s ease;
}

.pm-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 42px rgba(6, 182, 212, 0.16);
}

.pm-icon {
    font-size: 34px;
    margin-bottom: 14px;
}

.pm-card-title {
    font-size: 19px;
    font-weight: 900;
    color: #1e1b4b;
    margin-bottom: 8px;
}

.pm-card-desc {
    font-size: 14px;
    color: #64748b;
    line-height: 1.45;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.92);
    border: 2px dashed #8b5cf6;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 14px 35px rgba(124, 58, 237, 0.10);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white;
    border-radius: 999px;
    padding: 0.7rem 1.45rem;
    border: none;
    font-weight: 900;
}

.stButton > button:hover {
    color: white;
    transform: scale(1.02);
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #16a34a, #06b6d4);
    color: white;
    border-radius: 999px;
    border: none;
    font-weight: 900;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.85);
    border-radius: 999px;
    padding: 12px 20px;
    color: #4c1d95;
    font-weight: 900;
    border: 1px solid #ddd6fe;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #06b6d4) !important;
    color: white !important;
}

.stAlert {
    border-radius: 16px;
}

[data-testid="stExpander"] {
    border-radius: 16px;
    border: 1px solid #e9d5ff;
    background: rgba(255,255,255,0.75);
}

input, textarea {
    border-radius: 14px !important;
}

hr {
    border-color: #ddd6fe;
}

@media (max-width: 900px) {
    .pm-title {
        font-size: 46px;
    }

    .pm-feature-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .pm-navbar {
        flex-direction: column;
        gap: 12px;
    }
}

@media (max-width: 600px) {
    .pm-feature-grid {
        grid-template-columns: 1fr;
    }

    .pm-title {
        font-size: 38px;
    }
}
</style>

<div class="pm-navbar">
    <div class="pm-logo">🧠 PaperMind AI</div>
  
</div>

<div class="pm-hero">
    <div class="pm-title">
        Decode complex papers<br>
        with <span class="pm-gradient">AI clarity</span>
    </div>
    <div class="pm-subtitle">
        Upload research papers and instantly generate insights, quizzes,<br>
        source-grounded answers, comparisons, and presentation drafts.
    </div>
    <div class="pm-cta">Start by uploading your research paper</div>
</div>

<div class="pm-feature-grid">
    <div class="pm-card">
        <div class="pm-icon">✨</div>
        <div class="pm-card-title">Smart Insights</div>
        <div class="pm-card-desc">Generate summaries, methodology, results, contributions, and future scope.</div>
    </div>
    <div class="pm-card">
        <div class="pm-icon">🔎</div>
        <div class="pm-card-title">Grounded Q&A</div>
        <div class="pm-card-desc">Ask questions with answers backed by retrieved source chunks.</div>
    </div>
    <div class="pm-card">
        <div class="pm-icon">🧩</div>
        <div class="pm-card-title">Interactive Quiz</div>
        <div class="pm-card-desc">Generate MCQs, select answers, and get instant feedback.</div>
    </div>
    <div class="pm-card">
        <div class="pm-icon">📊</div>
        <div class="pm-card-title">PPT & Compare</div>
        <div class="pm-card-desc">Create presentation drafts and compare two research papers.</div>
    </div>
</div>
""", unsafe_allow_html=True)


def parse_quiz_text(quiz_text):
    pattern = (
        r"Q\d+\.\s*(.*?)\n+[\s\S]*?"
        r"A\)\s*(.*?)\n+"
        r"B\)\s*(.*?)\n+"
        r"C\)\s*(.*?)\n+"
        r"D\)\s*(.*?)\n+"
        r"Answer:\s*([A-D])\n+"
        r"Explanation:\s*([\s\S]*?)(?=\n+Q\d+\.|\Z)"
    )

    matches = re.findall(pattern, quiz_text, re.DOTALL)

    quiz_data = []

    for match in matches:
        quiz_data.append({
            "question": match[0].strip(),
            "options": {
                "A": match[1].strip(),
                "B": match[2].strip(),
                "C": match[3].strip(),
                "D": match[4].strip()
            },
            "correct_answer": match[5].strip(),
            "explanation": match[6].strip()
        })

    return {"quiz": quiz_data}


uploaded_files = st.file_uploader(
    "Upload Research Paper PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    uploaded_file = uploaded_files[0]

    st.success(f"{len(uploaded_files)} PDF file(s) uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)
    text = clean_text_func(text)
    chunks = chunk_text(text)

    try:
        gemini_model = setup_gemini()
    except Exception as e:
        gemini_model = None
        st.warning(
            "Gemini is not available. The app will continue with fallback generation. "
            f"({e})"
        )

    with st.expander("📦 Processing Details"):
        st.write(f"Total Chunks: {len(chunks)}")

    embeddings = create_embeddings(chunks)
    index = create_faiss_index(embeddings)

    st.success("Embeddings and FAISS Index Created Successfully!")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Insights",
        "🧠 Quiz",
        "📑 PPT",
        "🔍 Compare",
        "💬 Q&A",
        "🔎 Paper Finder"
    ])

    def run_insight(section_name):
        prompt = f"""
You are a research paper assistant.

From the following research paper, generate this section:

{section_name}

Research Paper:
{text[:12000]}

Give the answer in clear bullet points.
"""
        answer, source_model = generate_hybrid_response(
            gemini_model,
            prompt,
            section_name
        )

        st.caption(f"Generated using: {source_model}")
        st.markdown(answer)

        return answer

    with tab1:
        st.subheader("Research Paper Insights")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate Summary"):
                with st.spinner("Generating summary..."):
                    summary = run_insight(
                        "Structured Summary with Overview, Main Contributions, "
                        "Methodology, Results, and Conclusion"
                    )

                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name="research_paper_summary.txt",
                        mime="text/plain"
                    )

            if st.button("Key Contributions"):
                with st.spinner("Finding key contributions..."):
                    run_insight("Key Contributions")

        with col2:
            if st.button("Methodology"):
                with st.spinner("Extracting methodology..."):
                    run_insight("Methodology")

            if st.button("Results"):
                with st.spinner("Extracting results..."):
                    run_insight("Results")

        if st.button("Future Work"):
            with st.spinner("Identifying future work..."):
                run_insight("Future Work")

    with tab2:
        st.subheader("AI Quiz Generator")

        if "quiz_data" not in st.session_state:
            st.session_state.quiz_data = None

        if "quiz_source" not in st.session_state:
            st.session_state.quiz_source = None

        if "quiz_submitted" not in st.session_state:
            st.session_state.quiz_submitted = False

        num_questions = st.slider(
            "Number of quiz questions",
            min_value=3,
            max_value=15,
            value=5
        )

        if st.button("Generate Interactive Quiz"):
            with st.spinner("Generating interactive quiz..."):
                prompt = quiz_prompt(text, num_questions)

                quiz_response, source_model = generate_hybrid_response(
                    gemini_model,
                    prompt,
                    "Generate quiz"
                )

                quiz_data = parse_quiz_text(quiz_response)

                if len(quiz_data["quiz"]) == 0:
                    st.error("Quiz parsing failed. Raw output shown below:")
                    st.code(quiz_response)
                else:
                    st.session_state.quiz_data = quiz_data
                    st.session_state.quiz_source = source_model
                    st.session_state.quiz_submitted = False
                    st.success("Quiz generated successfully!")

        if st.session_state.quiz_data:
            st.caption(f"Generated using: {st.session_state.quiz_source}")

            total = len(st.session_state.quiz_data["quiz"])

            for i, q in enumerate(st.session_state.quiz_data["quiz"]):
                st.markdown(f"### Q{i + 1}. {q['question']}")

                option_labels = [
                    f"{key}) {value}"
                    for key, value in q["options"].items()
                ]

                st.radio(
                    "Choose your answer:",
                    option_labels,
                    key=f"quiz_answer_{i}"
                )

                st.divider()

            if st.button("Check Answers"):
                st.session_state.quiz_submitted = True

            if st.session_state.quiz_submitted:
                score = 0

                st.subheader("Quiz Results")

                for i, q in enumerate(st.session_state.quiz_data["quiz"]):
                    selected = st.session_state.get(f"quiz_answer_{i}")

                    if selected is None:
                        selected_key = ""
                    else:
                        selected_key = selected.split(")")[0]

                    correct_key = q["correct_answer"]

                    st.markdown(f"### Q{i + 1}. {q['question']}")

                    if selected_key == correct_key:
                        st.success("✅ Correct")
                        score += 1
                    else:
                        st.error(f"❌ Wrong. Correct answer is {correct_key}")

                    with st.expander("Explanation"):
                        st.write(q["explanation"])

                st.subheader(f"🏆 Final Score: {score}/{total}")

    with tab3:
        st.subheader("AI PowerPoint Generator")

        if st.button("Generate PowerPoint Presentation"):
            with st.spinner("Generating PowerPoint..."):

                ppt_prompt = f"""
You are an AI presentation designer like Gamma AI.

Create a modern Canva-style presentation from this research paper.

Return ONLY valid JSON. No explanation.

Format:
{{
  "slides": [
    {{
      "title": "Slide title",
      "subtitle": "Short subtitle",
      "bullets": ["point 1", "point 2", "point 3"],
      "visual": "Short visual suggestion"
    }}
  ]
}}

Generate exactly 8 slides:
1. Title and Overview
2. Problem Statement
3. Research Objectives
4. Methodology
5. Model / System Architecture
6. Results and Findings
7. Applications and Advantages
8. Conclusion and Future Scope

Research Paper:
{text[:12000]}
"""

                slide_content, source_model = generate_hybrid_response(
                    gemini_model,
                    ppt_prompt,
                    "Generate PowerPoint content"
                )

                pptx_path = create_pptx(
                    slide_content,
                    "research_presentation.pptx"
                )

                st.caption(f"PPT content generated using: {source_model}")
                st.success("PowerPoint Presentation Created!")

                with open(pptx_path, "rb") as file:
                    st.download_button(
                        label="📥 Download PowerPoint",
                        data=file,
                        file_name="research_presentation.pptx",
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "presentationml.presentation"
                        )
                    )

    with tab4:
        st.subheader("Compare Two Research Papers")

        if len(uploaded_files) < 2:
            st.info("Upload at least 2 PDFs to use comparison.")
        else:
            if st.button("Compare Papers"):
                with st.spinner("Comparing papers..."):
                    paper1_text = clean_text_func(
                        extract_text_from_pdf(uploaded_files[0])
                    )

                    paper2_text = clean_text_func(
                        extract_text_from_pdf(uploaded_files[1])
                    )

                    compare_prompt = f"""
You are a research paper comparison assistant.

Compare the following two research papers.

Paper 1:
{paper1_text[:7000]}

Paper 2:
{paper2_text[:7000]}

Compare them under:
1. Research Objective
2. Methodology
3. Model/System Architecture
4. Results
5. Advantages
6. Limitations
7. Which paper is stronger and why

Give the answer in a clear table format.
"""

                    comparison, source_model = generate_hybrid_response(
                        gemini_model,
                        compare_prompt,
                        "Compare research papers"
                    )

                    st.caption(f"Generated using: {source_model}")
                    st.markdown(comparison)

    with tab5:
        st.subheader("Ask Questions About the Paper")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        query = st.text_input("Ask a question about the paper")

        if query:
            with st.spinner("Generating answer..."):
                results = retrieve_chunks(
                    query,
                    model,
                    index,
                    chunks,
                    top_k=3
                )

                context = "\n\n".join(results)

                prompt = f"""
You are a research paper assistant.

Use only the provided context to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

                answer, source_model = generate_hybrid_response(
                    gemini_model,
                    prompt,
                    query
                )

                st.session_state.chat_history.append({
                    "question": query,
                    "answer": answer,
                    "chunks": results,
                    "source_model": source_model
                })

        if st.session_state.chat_history:
            st.subheader("Chat History")

            for chat in reversed(st.session_state.chat_history):
                with st.expander(f"Q: {chat['question']}"):
                    st.caption(
                        f"Answer generated using: {chat['source_model']} | "
                        f"Sources: {len(chat['chunks'])} retrieved chunks"
                    )

                    st.markdown("**Answer:**")
                    st.write(chat["answer"])

                    st.markdown("### 📚 Sources Used")

                    for j, chunk in enumerate(chat["chunks"]):
                        st.write(f"📌 Source Chunk {j + 1}")

                        with st.expander(f"View Source Chunk {j + 1}"):
                            st.write(chunk)

        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    with tab6:
        st.subheader("🔎 Research Paper Finder")

        topic = st.text_input(
            "Enter a research topic",
            placeholder="Example: transformer based text summarization"
        )

        max_results = st.slider(
            "Number of papers to find",
            min_value=3,
            max_value=10,
            value=5
        )

        if st.button("Find Research Papers"):
            if topic.strip() == "":
                st.warning("Please enter a research topic.")
            else:
                with st.spinner("Searching arXiv papers..."):
                    papers = search_arxiv_papers(topic, max_results)

                    if not papers:
                        st.error("No papers found. Try another topic.")
                    else:
                        st.success(f"Found {len(papers)} papers.")

                        for i, paper in enumerate(papers):
                            with st.expander(f"{i + 1}. {paper['title']}"):
                                st.markdown(f"**Authors:** {paper['authors']}")
                                st.markdown(f"**Published:** {paper['published']}")
                                st.markdown("**Summary:**")
                                st.write(paper["summary"])

                                st.markdown(f"[Open Paper]({paper['paper_link']})")
                                st.markdown(f"[Download PDF]({paper['pdf_link']})")

else:
    st.info("Please upload one or more research paper PDFs to get started.")