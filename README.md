# ScholarShield

### Context-Aware Academic Similarity Analyzer

ScholarShield is an NLP-based application that compares academic
documents at multiple levels and explains the similarities it
identifies. It is designed to help students, educators, and reviewers
examine overlapping text, sentence structure, and meaning.

> **Important:** ScholarShield is an academic review aid, not a
> definitive plagiarism detector. Similarity scores indicate overlap or
> related meaning and should be interpreted alongside the passages,
> context, citations, and human judgment.

## Problem Statement

Simple text-matching tools can miss paraphrased content or overemphasize
common phrases. ScholarShield combines several NLP analysis perspectives
to provide a broader view of how a target document relates to one or
more reference documents.

## Key Features

-   **Academic document upload** --- upload supported PDF, DOCX, and TXT
    documents.
-   **Document library** --- organize documents awaiting analysis,
    reference documents, and analyzed documents.
-   **Text preprocessing** --- prepare extracted text for analysis.
-   **Morphological analysis** --- examine word forms and linguistic
    properties.
-   **Syntax and dependency analysis** --- inspect sentence structure
    and grammatical relationships.
-   **Lexical similarity** --- compare word-level overlap.
-   **Syntactic similarity** --- compare aspects of sentence structure.
-   **Semantic similarity** --- estimate similarity in meaning using NLP
    representations.
-   **Word-sense and contextual analysis** --- consider how words are
    used in context.
-   **Meaning representation** --- analyze meaning-related linguistic
    structures.
-   **Similar passage detection** --- surface passages that may warrant
    closer review.
-   **Similarity explanations** --- provide evidence to help interpret
    the comparison.
-   **Multi-level similarity score** --- present several analysis
    dimensions together.
-   **Interactive dashboard** --- view documents and analysis results.
-   **Document comparison** --- compare a target document against one or
    more references.
-   **Explainable PDF report** --- generate a report containing scores
    and analysis details.

## Technology Stack

  -----------------------------------------------------------------------
  Area                                Technologies
  ----------------------------------- -----------------------------------
  Application interface               Python, Streamlit

  Natural Language Processing         NLTK, spaCy

  Text similarity and machine         scikit-learn, Sentence
  learning                            Transformers, PyTorch, Transformers

  Document extraction                 PyMuPDF, python-docx

  Database                            SQLite

  Visualizations                      Plotly

  PDF reports                         ReportLab

  Authentication                      PBKDF2-HMAC-SHA256 password hashing
  -----------------------------------------------------------------------

## How It Works

1.  **Upload:** The user uploads a target academic document and selects
    one or more reference documents.
2.  **Extract and preprocess:** Text is extracted from the supported
    file and prepared for NLP analysis.
3.  **Analyze:** ScholarShield evaluates different dimensions, such as
    lexical, syntactic, semantic, contextual, and meaning-related
    similarity.
4.  **Review evidence:** The user inspects scores, explanations, and
    similar passages rather than relying on a single number.
5.  **Generate a report:** The user can generate a PDF summarizing the
    analysis.

## Project Structure

``` text
ScholarShield/
├── app.py
├── assets/
│   └── logo.png
├── auth/
├── database/
│   ├── database.py
│   └── schema.sql
├── document_processing/
├── nlp/
├── pages/
├── reports/
├── storage/
├── requirements.txt
└── README.md
```

*Some directories contain additional modules not shown above.*

## Run Locally

### Prerequisites

-   Windows, macOS, or Linux
-   Python installed
-   Git (optional, if cloning the repository)
-   Internet access for installing dependencies and downloading NLP
    models when needed

### 1. Clone the repository

``` bash
git clone https://github.com/Nabeeha-Hassan07/ScholarShield.git
cd ScholarShield
```

If you already have the project folder, open a terminal in that folder
instead.

### 2. Create and activate a virtual environment

**Windows PowerShell**

``` powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you use another supported Python version, replace `-3.11` with the
version installed on your computer. Dependency compatibility can vary by
Python version.

**macOS/Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The current `requirements.txt` reflects the development environment and
may need adjustment for a different operating system or Python version.
If installation fails, check the error and package compatibility before
changing the working environment.

### 4. Initialize the database

From the project root, run:

``` bash
python -m database.database
```

### 5. Start ScholarShield

``` bash
streamlit run app.py
```

Streamlit normally opens the application in your browser. If it does
not, open the local URL printed in the terminal (commonly
`http://localhost:8501`).

## Typical Usage

1.  Register an account or log in.
2.  Upload a target document and the document(s) to use as references.
3.  Open the Analysis page.
4.  Choose the target document and reference document(s).
5.  Run the analysis.
6.  Review the similarity breakdown, explanations, and detected
    passages.
7.  Generate and download the PDF report.

Exact page labels and available options may depend on the current
application version.

## Understanding the Results

-   **Lexical similarity:** overlap in words or terms.
-   **Syntactic similarity:** similarity in sentence structure or
    grammatical patterns.
-   **Semantic similarity:** how closely the texts' meanings are
    represented as related.
-   **Contextual similarity:** similarity that considers words and their
    surrounding context.
-   **Meaning-related analysis:** linguistic representations of
    relationships and propositions in the text.
-   **Similar passages:** text segments identified as potentially
    related and worth reviewing.

Scores from different methods measure different things. A high semantic
score does not by itself prove copying, and a low lexical score does not
rule out paraphrasing. Review the underlying text and its citations
before drawing conclusions.

## Data, Privacy, and Limitations

-   The application uses a local SQLite database and local storage
    folders during local development.
-   Treat uploaded academic documents and generated reports as private.
    Do not commit real documents, database files, passwords, API keys,
    or other secrets to a public repository.
-   Local files on a hosted application may not persist reliably across
    restarts or redeployments. A production deployment that requires
    durable accounts, uploads, and reports should use persistent
    database and file-storage services.
-   NLP models may need to be downloaded the first time they are used,
    and model downloads can require internet access.
-   Results depend on text extraction quality, language, document
    length, and the NLP models and methods used.
-   ScholarShield supports review and explanation; it does not make
    final academic-integrity decisions.

## Academic Context

ScholarShield is an educational NLP project. Its analysis components
connect to concepts including text preprocessing, morphology, syntax and
dependency analysis, word-sense and semantic interpretation, meaning
representation, and similarity analysis.

## Repository

GitHub: https://github.com/Nabeeha-Hassan07/ScholarShield

## Copyright and Ownership

Copyright © 2026 Nabeeha-Hassan07 . All rights reserved.

ScholarShield – Context-Aware Academic Similarity Analyzer is an original academic project created by [Your Name].

The original source code, documentation, interface design, and other original materials in this repository are protected by applicable copyright laws.

No permission is granted to copy, redistribute, modify, republish, or reuse the project's original materials without the author's prior written permission, except where applicable law permits otherwise.

Third-party libraries and dependencies remain subject to their respective licenses.

## Publishing this repository on GitHub does not grant an open-source license for the project's original materials. ##

This notice does not claim exclusive copyright over an abstract idea, general method, or concept.

