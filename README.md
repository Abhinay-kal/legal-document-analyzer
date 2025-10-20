# PlainSpeak Legal Analyzer

A Python-based tool designed to demystify complex legal documents. This application simplifies dense legal jargon into plain English and analyzes sentence structure to flag overly complex sentences, making legal text more accessible to everyone.

*(Note: Replace this line with a screenshot or GIF of your Gradio application!)*

---

## 🌟 Core Features

* **Lexical Simplification:** Automatically identifies and replaces hundreds of common legal jargon terms with their simpler, plain English equivalents.
* **Syntactic Analysis:** Processes the document to flag long and structurally complex sentences that could be difficult to understand, noting potential points for simplification.
* **Interactive Web Interface:** Built with Gradio, the simple UI allows users to paste text and instantly see the simplified version and a detailed explanation of the changes.
* **Detailed Explanations:** Provides a clear log of every change made, explaining why each term was replaced or which sentences were flagged for review.

---

## 🛠️ Tech Stack

* **Backend:** Python
* **NLP Libraries:**
    * **spaCy:** For robust and efficient sentence tokenization.
    * **NLTK:** For NLP prerequisites and utilities.
* **Web UI:** Gradio
* **Core Logic:** Regular Expressions (re) for pattern matching and replacement.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* Python 3.8 or newer
* pip (Python package installer)

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/Abhinay-kal/legal-document-analyzer.git](https://github.com/Abhinay-kal/legal-document-analyzer.git)
    cd legal-document-analyzer
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Download the necessary spaCy model:**
    ```sh
    python -m spacy download en_core_web_sm
    ```
    *(The NLTK data will be downloaded automatically on the first run)*

### Running the Application

1.  **Launch the Gradio web server:**
    ```sh
    python app.py
    ```
2.  Open your web browser and navigate to the local URL provided in the terminal (usually `http://127.0.0.1:7860`).

---

## 🛣️ Future Improvements

This project is a solid foundation, and here are some potential directions for future development:

* **Implement Automated Sentence Splitting:** Move from just analyzing complex sentences to automatically splitting them into shorter, more readable sentences.
* **Context-Aware Replacements:** Use more advanced NLP models (like transformers) to choose the best synonym based on the surrounding context, rather than a direct 1-to-1 replacement.
* **Document Upload Feature:** Allow users to upload files (`.pdf`, `.docx`) directly instead of pasting text.
