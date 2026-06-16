# 🧠 PaperMind AI

## GenAI-Powered Research Paper Assistant Using RAG

PaperMind AI is a Generative AI-based research paper assistant that helps users understand, analyze, and interact with research papers. The system allows users to upload research paper PDFs and generate summaries, ask source-grounded questions, create quizzes, compare papers, generate PowerPoint content, and search research papers using arXiv Paper Finder.

This project was developed as a capstone/internship project under the IBM-AICTE / Edunet Foundation program.

---

## 📌 Project Title

**GenAI-Powered Research Paper Simplifier and Knowledge Assistant Using RAG**

---

## ❗ Problem Statement

Students and researchers often face difficulty understanding complex research papers due to technical language, lengthy content, mathematical explanations, and domain-specific terminology. Manually reading, summarizing, comparing, and preparing presentations from research papers takes significant time and effort.

There is a need for an AI-powered system that can simplify research papers, answer user questions based on paper content, generate learning material, and support research discovery.

---

## 💡 Proposed Solution

PaperMind AI provides an interactive web application where users can upload research paper PDFs and use AI-powered tools to understand the content. The system uses Retrieval-Augmented Generation, or RAG, to retrieve relevant chunks from the uploaded paper and generate grounded answers.

The system also includes an arXiv Paper Finder feature that helps users search research papers by topic and access abstracts and PDF links.

---

## ✨ Key Features

* 📄 PDF upload and text extraction
* 🧹 Text cleaning and chunking
* 🧠 Embedding generation using Sentence Transformers
* 🔎 FAISS-based vector search
* 💬 RAG-based question answering
* 📝 Research paper summarization
* 🎯 Key contribution extraction
* ⚙️ Methodology and result extraction
* 🚀 Future scope generation
* 🧩 Interactive quiz generation
* 📊 Research paper comparison
* 📑 PowerPoint presentation generation
* 🔍 arXiv Paper Finder for discovering research papers
* 🔁 Hybrid AI response generation using Gemini, Groq, and Ollama fallback

---

## 🛠️ Technology Used

### 🌐 Frontend

* Streamlit
* HTML/CSS inside Streamlit for custom UI

### 🐍 Backend

* Python

### 🤖 AI/ML Components

* Sentence Transformers
* FAISS Vector Database
* Gemini API
* Groq API
* Ollama Local LLM fallback

### 📄 PDF and Document Processing

* PyPDF
* Python-PPTX

### 🔍 Research Paper Search

* arXiv API
* Feedparser

---

## 🧱 System Development Approach

The system follows a modular pipeline:

1. User uploads a research paper PDF.
2. Text is extracted from the PDF.
3. Extracted text is cleaned and preprocessed.
4. Cleaned text is divided into chunks.
5. Embeddings are generated for each chunk.
6. FAISS vector index is created.
7. User selects a feature such as summary, Q&A, quiz, PPT, or comparison.
8. Relevant chunks are retrieved using semantic search.
9. AI model generates output using retrieved context.
10. Output is displayed in the Streamlit interface.

---

## 🔁 RAG Workflow

The project uses Retrieval-Augmented Generation to improve answer accuracy.

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Chunking
    ↓
Embedding Generation
    ↓
FAISS Vector Store
    ↓
User Question
    ↓
Relevant Chunk Retrieval
    ↓
LLM Response Generation
    ↓
Source-Grounded Answer
```

---

## 📁 Project Modules

```text
ResearchPaperAssistant PROJECT/
│
├── app.py
├── requirements.txt
├── .env
│
├── utils/
│   ├── __init__.py
│   ├── pdf_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── gemini_helper.py
│   ├── groq_helper.py
│   ├── ollama_helper.py
│   ├── hybrid_helper.py
│   ├── quiz_generator.py
│   ├── pptx_generator.py
│   └── paper_finder.py
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2️⃣ Create Virtual Environment

For Windows:

```bash
py -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File

Create a `.env` file in the root folder and add your API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Note: If Gemini or Groq is unavailable, the system can use Ollama local fallback if Ollama is installed and running.

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 📦 Requirements

```text
streamlit
pypdf
sentence-transformers
faiss-cpu
google-generativeai
python-dotenv
groq
requests
python-pptx
torch
torchvision
numpy
feedparser
```

---

## 🚀 How to Use

### 📄 1. Upload Research Paper

Upload one or more PDF research papers.

### 📌 2. Generate Insights

Use the Insights tab to generate:

* Summary
* Key Contributions
* Methodology
* Results
* Future Work

### 💬 3. Ask Questions

Use the Q&A tab to ask questions about the uploaded paper. The system retrieves relevant chunks and generates answers using RAG.

### 🧩 4. Generate Quiz

Use the Quiz tab to generate multiple-choice questions from the paper.

### 📑 5. Generate PPT

Use the PPT tab to generate a presentation draft from the uploaded research paper.

### 📊 6. Compare Papers

Upload at least two research papers and use the Compare tab to compare them based on objective, methodology, results, advantages, and limitations.

### 🔎 7. Find Research Papers

Use the arXiv Paper Finder tab to search research papers by topic. The system returns titles, authors, abstracts, publication dates, and PDF links.

---

## 🔍 arXiv Paper Finder Usage

The arXiv Paper Finder helps users discover research papers before uploading them into the system.

Example search topic:

```text
Transformer based text summarization
```

The system returns:

* Paper title
* Authors
* Published date
* Abstract
* arXiv paper link
* PDF download link

Ultimate workflow:

```text
Find paper → Upload paper → Analyze paper → Ask questions → Generate quiz/PPT
```

---

## ✅ Result

The system successfully performs AI-powered research paper analysis. It can extract text from PDFs, create embeddings, retrieve relevant chunks, and generate meaningful responses using LLMs.

Expected outputs include:

* Structured summaries
* Research insights
* Source-grounded answers
* Interactive quizzes
* PPT drafts
* Paper comparisons
* Research paper search results

---

## 🌱 Future Scope

* Add login and user history
* Add support for more file formats like DOCX and TXT
* Improve PPT design using advanced templates
* Add citation generation in IEEE/APA format
* Add voice-based paper explanation
* Add multilingual paper summarization
* Add full Semantic Scholar integration
* Deploy the app publicly using Streamlit Cloud

---

## ❓ Basic Q&A

### Q1. What is PaperMind AI?

PaperMind AI is a GenAI-powered research paper assistant that helps users understand research papers by generating summaries, answers, quizzes, PPT content, and comparisons.

### Q2. What problem does this project solve?

It reduces the time and effort required to understand complex research papers and helps students or researchers quickly extract useful information.

### Q3. What is RAG?

RAG stands for Retrieval-Augmented Generation. It retrieves relevant parts of the document first and then generates answers using those retrieved chunks.

### Q4. Why is FAISS used?

FAISS is used to store and search vector embeddings efficiently. It helps find the most relevant chunks from the research paper for a user query.

### Q5. What is the role of Sentence Transformers?

Sentence Transformers convert text chunks into numerical embeddings so that semantic search can be performed.

### Q6. Why are chunks created from the paper?

Research papers are usually long. Chunking divides the paper into smaller parts so that the system can retrieve only the most relevant sections.

### Q7. What is the use of the arXiv Paper Finder?

It helps users search research papers by topic and provides titles, abstracts, authors, publication dates, and PDF links.

### Q8. Can this system compare two research papers?

Yes. If the user uploads two PDFs, the system can compare them based on objective, methodology, results, advantages, limitations, and overall strength.

### Q9. Can the system work without Gemini?

Yes. The system uses a hybrid fallback approach. If Gemini is unavailable, it can use Groq or Ollama local fallback depending on configuration.

### Q10. Is this project useful for students?

Yes. It is useful for students preparing literature reviews, seminars, assignments, research projects, and presentations.

---

## 🧯 Troubleshooting Guide

### Problem 1: `ModuleNotFoundError: No module named 'pypdf'`

Solution:

```bash
pip install pypdf
```

---

### Problem 2: `ModuleNotFoundError: No module named 'sentence_transformers'`

Solution:

```bash
pip install sentence-transformers
```

---

### Problem 3: `ModuleNotFoundError: No module named 'faiss'`

Solution:

```bash
pip install faiss-cpu
```

---

### Problem 4: `ModuleNotFoundError: No module named 'dotenv'`

Solution:

```bash
pip install python-dotenv
```

---

### Problem 5: `ModuleNotFoundError: No module named 'feedparser'`

Solution:

```bash
pip install feedparser
```

---

### Problem 6: Gemini API Key Not Found

Error example:

```text
GOOGLE_API_KEY not found
```

Solution:

Create a `.env` file in the project root and add:

```env
GOOGLE_API_KEY=your_api_key_here
```

Also make sure `python-dotenv` is installed.

---

### Problem 7: Gemini Quota Exceeded

Error example:

```text
429 You exceeded your current quota
```

Solution:

* Wait for quota reset
* Use Groq fallback
* Use Ollama local fallback
* Use a different Gemini model if available

---

### Problem 8: Ollama Not Working

Solution:

Make sure Ollama is installed and running.

Run:

```bash
ollama serve
```

Then pull a model:

```bash
ollama pull llama3.2
```

---

### Problem 9: Streamlit App Not Opening

Solution:

```bash
streamlit run app.py
```

If the browser does not open automatically, copy the local URL from the terminal and paste it into your browser.

---

### Problem 10: PDF Text Not Extracting Properly

Possible reasons:

* The PDF is scanned/image-based
* The PDF has complex formatting
* The PDF has restricted text extraction

Solution:

Use a text-based research paper PDF instead of a scanned PDF.

---

### Problem 11: Quiz Parsing Failed

Reason:

The AI model may return quiz output in an unexpected format.

Solution:

Click the quiz generation button again or reduce the number of questions.

---

### Problem 12: PPT Generation Error

Possible reasons:

* AI did not return valid JSON
* Missing `python-pptx`
* Incorrect slide content format

Solution:

```bash
pip install python-pptx
```

Then try generating the PPT again.

---

### Problem 13: arXiv Paper Finder Shows No Result

Solution:

Try using simpler search keywords.

Example:

Instead of:

```text
Highly optimized transformer based multilingual abstractive summarization
```

Use:

```text
transformer summarization
```

---

## 🔐 Important Note

Do not upload your `.env` file publicly because it contains private API keys.

Create a `.gitignore` file and add:

```text
.env
venv/
__pycache__/
*.pyc
research_presentation.pptx
```

---

## 📚 References

* Python
* Streamlit
* FAISS
* Sentence Transformers
* Google Gemini API
* Groq API
* Ollama
* PyPDF
* Python-PPTX
* arXiv API
* Hugging Face

---

## 👨‍💻 Author

**Name:** Aritra Dey
**Department:** Computer Science and Engineering / Data Science
**Project:** GenAI-Powered Research Paper Simplifier and Knowledge Assistant Using RAG

---

## 🔗 Project Links

```text
Project Repository Link: Add your repository link here
Application Link: Add your application link here
```

---

