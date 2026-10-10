import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from database.database import (
    get_user_documents,
    save_analysis
)
from nlp.analysis_engine import analyze_document_pair
from pages.authenticated_sidebar import show_authenticated_sidebar
from reports.report_generator import generate_analysis_report
from document_processing.pdf_extractor import extract_pdf_text
from document_processing.docx_extractor import extract_docx_text
from document_processing.text_extractor import extract_txt_text

# ============================================================
# PAGE STYLING
# ============================================================

def apply_analysis_styles():

    show_authenticated_sidebar()

    st.html(
        """
        <style>

        /* ========================================================
           GLOBAL
           ======================================================== */

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at 85% 5%,
                    rgba(83, 126, 218, 0.07),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 5% 55%,
                    rgba(92, 103, 190, 0.045),
                    transparent 25%
                ),
                #f5f7fb !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            padding: 38px 52px 60px 52px !important;
            max-width: 1540px !important;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0;
        }


        /* ========================================================
           PAGE HEADER
           ======================================================== */

        .analysis-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 30px;
        }

        .analysis-label {
            color: #5278d2;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .analysis-title {
            color: #14264a;
            font-size: 36px;
            font-weight: 800;
            letter-spacing: -0.8px;
            line-height: 1.12;
            margin: 0;
        }

        .analysis-description {
            color: #61718b;
            font-size: 15px;
            line-height: 1.7;
            margin-top: 10px;
            max-width: 760px;
        }


        /* ========================================================
           HERO
           ======================================================== */

        .analysis-hero {
            margin-top: 30px;
            min-height: 178px;

            padding: 29px 32px;

            border-radius: 18px;

            background:
                linear-gradient(
                    125deg,
                    #122b55 0%,
                    #1d4279 54%,
                    #385a9b 100%
                );

            box-shadow:
                0 16px 38px rgba(27, 57, 105, 0.16);

            position: relative;
            overflow: hidden;
        }

        .analysis-hero-content {
            position: relative;
            z-index: 3;
        }

        .analysis-hero-eyebrow {
            color: #9db9ef;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .analysis-hero-title {
            color: #ffffff;
            font-size: 24px;
            font-weight: 750;
            line-height: 1.2;
            margin-bottom: 8px;
        }

        .analysis-hero-text {
            color: #dce7f8;
            font-size: 13.5px;
            line-height: 1.7;
            max-width: 700px;
        }

        .analysis-hero-badge {
            position: absolute;
            right: 30px;
            top: 30px;

            padding: 10px 14px;
            border-radius: 10px;

            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.13);

            color: #e8f0ff;
            font-size: 11px;
            font-weight: 650;

            backdrop-filter: blur(8px);
        }

        .analysis-decoration-one {
            position: absolute;

            width: 280px;
            height: 280px;

            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 50%;

            right: -100px;
            top: -135px;
        }

        .analysis-decoration-two {
            position: absolute;

            width: 180px;
            height: 180px;

            border: 1px solid rgba(255,255,255,0.055);
            border-radius: 50%;

            right: 65px;
            bottom: -120px;
        }

        .analysis-dot {
            position: absolute;

            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #a9c4ff;

            right: 110px;
            top: 55px;

            box-shadow:
                0 0 18px rgba(169,196,255,0.7);
        }


        /* ========================================================
           SECTION HEADERS
           ======================================================== */

        .section-block {
            margin-top: 34px;
            margin-bottom: 15px;
        }

        .section-heading {
            color: #17294d;
            font-size: 20px;
            font-weight: 750;
            letter-spacing: -0.2px;
        }

        .section-subheading {
            color: #78869b;
            font-size: 12.5px;
            margin-top: 4px;
        }

        .section-label {
            color: #5278d2;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }


        /* ========================================================
           WORKSPACE
           ======================================================== */

        .workspace-card {
            padding: 22px 24px 21px;

            border-radius: 15px;

            background:
                linear-gradient(
                    145deg,
                    #ffffff,
                    #f8faff
                );

            border: 1px solid #e0e6ef;

            box-shadow:
                0 7px 24px rgba(34, 65, 112, 0.045);
        }

        .workspace-heading {
            color: #1a2d50;
            font-size: 15px;
            font-weight: 720;
        }

        .workspace-caption {
            color: #8490a3;
            font-size: 11px;
            line-height: 1.5;
            margin-top: 4px;
            margin-bottom: 14px;
        }

        .field-label {
            color: #6d7c94;
            font-size: 10px;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
        }


        /* ========================================================
           STREAMLIT SELECTBOX / MULTISELECT
           ======================================================== */

        div[data-baseweb="select"] > div {
            min-height: 40px !important;
            border-radius: 9px !important;

            border: 1px solid #d6dfed !important;

            background: #ffffff !important;

            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: #a9bddd !important;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: #7697dc !important;

            box-shadow:
                0 0 0 1px #7697dc !important;
        }

        div[data-baseweb="select"] span {
            font-size: 12px !important;
            color: #294064;
        }

        .stMultiSelect [data-baseweb="tag"] {
            background: #edf3ff !important;
            border: 1px solid #d8e5fb !important;
            color: #416cc9 !important;
            border-radius: 7px !important;
        }


        /* ========================================================
           DOCUMENT INFO STRIP
           ======================================================== */

        .document-info-strip {
            display: grid;

            grid-template-columns: 1fr 1.8fr;

            gap: 1px;

            margin-top: 13px;

            background: #dfe5ec;

            border: 1px solid #dfe5ec;
            border-radius: 11px;

            overflow: hidden;
        }

        .document-info-item {
            background: #ffffff;
            padding: 12px 15px;
            min-height: 65px;
        }

        .document-info-label {
            color: #8490a3;

            font-size: 9px;
            font-weight: 800;

            letter-spacing: 0.9px;
            text-transform: uppercase;

            margin-bottom: 4px;
        }

        .document-info-value {
            color: #253a60;

            font-size: 11.5px;
            font-weight: 650;

            line-height: 1.45;

            word-break: break-word;
        }

        .reference-chip {
            display: inline-block;

            padding: 4px 8px;

            margin: 1px 3px 2px 0;

            border-radius: 7px;

            background: #edf3ff;
            border: 1px solid #d8e5fb;

            color: #416cc9;

            font-size: 10px;
            font-weight: 650;
        }


        /* ========================================================
           BUTTONS
           ======================================================== */

        div.stButton > button {
            border-radius: 9px !important;

            border: 1px solid #d6dfed !important;

            background: #ffffff !important;

            color: #294064 !important;

            font-weight: 650 !important;

            min-height: 40px !important;

            transition:
                all 0.18s ease !important;
        }

        div.stButton > button:hover {
            border-color: #7697dc !important;

            background: #f5f8ff !important;

            color: #416cc9 !important;

            transform: translateY(-1px);
        }

        div.stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #203f79,
                    #526ec4
                ) !important;

            border: none !important;

            color: #ffffff !important;

            min-height: 43px !important;

            font-size: 12px !important;
            font-weight: 700 !important;

            box-shadow:
                0 8px 20px rgba(39, 68, 130, 0.18);
        }

        div.stButton > button[kind="primary"]:hover {
            background:
                linear-gradient(
                    135deg,
                    #294d8f,
                    #607bd0
                ) !important;

            color: #ffffff !important;

            box-shadow:
                0 11px 25px rgba(39, 68, 130, 0.23);
        }


        /* ========================================================
           DIVIDER
           ======================================================== */

        .analysis-divider {
            height: 1px;

            background: #e1e6ee;

            margin: 34px 0 28px;
        }


        /* ========================================================
           RESULTS HEADER
           ======================================================== */

        .results-top {
            display: flex;

            align-items: flex-end;

            justify-content: space-between;

            gap: 20px;

            margin-bottom: 14px;
        }

        .results-count {
            padding: 7px 11px;

            border-radius: 9px;

            background: #edf3ff;

            border: 1px solid #d8e5fb;

            color: #4b6fc2;

            font-size: 10px;

            font-weight: 750;

            white-space: nowrap;
        }


        /* ========================================================
           RESULT CARD
           ======================================================== */

        .result-wrapper {
            margin-bottom: 30px;
        }

        .comparison-card {
            position: relative;

            min-height: 174px;

            padding: 25px 28px;

            border-radius: 16px;

            background:
                linear-gradient(
                    125deg,
                    #122b55 0%,
                    #1d4279 54%,
                    #385a9b 100%
                );

            box-shadow:
                0 12px 30px rgba(27, 57, 105, 0.13);

            overflow: hidden;
        }

        .comparison-decoration-one {
            position: absolute;

            width: 260px;
            height: 260px;

            right: -105px;
            top: -135px;

            border-radius: 50%;

            border: 1px solid rgba(255,255,255,0.075);
        }

        .comparison-decoration-two {
            position: absolute;

            width: 145px;
            height: 145px;

            right: 80px;
            bottom: -100px;

            border-radius: 50%;

            border: 1px solid rgba(255,255,255,0.055);
        }

        .comparison-content {
            position: relative;
            z-index: 3;
        }

        .comparison-grid {
            display: grid;

            grid-template-columns:
                minmax(0, 1fr)
                70px
                minmax(0, 1fr);

            align-items: center;

            gap: 20px;
        }

        .comparison-side-label {
            color: #9db9ef;

            font-size: 9px;

            font-weight: 800;

            letter-spacing: 1.2px;

            text-transform: uppercase;

            margin-bottom: 7px;
        }

        .comparison-document-name {
            color: #ffffff;

            font-size: 14px;

            font-weight: 700;

            line-height: 1.45;

            word-break: break-word;
        }

        .comparison-meta {
            color: #b9cbea;

            font-size: 10.5px;

            margin-top: 5px;
        }

        .comparison-vs {
            width: 42px;
            height: 42px;

            margin: auto;

            border-radius: 13px;

            display: flex;

            align-items: center;
            justify-content: center;

            background:
                rgba(255,255,255,0.11);

            border:
                1px solid rgba(255,255,255,0.16);

            color: #dce7fb;

            font-size: 10px;

            font-weight: 800;
        }

        .comparison-score-side {
            text-align: right;
        }

        .comparison-score-label {
            color: #9db9ef;

            font-size: 9px;

            font-weight: 800;

            letter-spacing: 1.1px;

            text-transform: uppercase;

            margin-bottom: 4px;
        }

        .comparison-score {
            color: #ffffff;

            font-size: 34px;

            font-weight: 800;

            letter-spacing: -0.8px;

            line-height: 1;
        }

        .comparison-level {
            display: inline-block;

            margin-top: 8px;

            padding: 5px 9px;

            border-radius: 8px;

            background:
                rgba(255,255,255,0.10);

            border:
                1px solid rgba(255,255,255,0.13);

            color: #e4edff;

            font-size: 9px;

            font-weight: 750;
        }


        /* ========================================================
           SCORE CARDS
           ======================================================== */

        .score-grid {
            display: grid;

            grid-template-columns:
                repeat(6, 1fr);

            gap: 10px;

            margin-top: 12px;
        }

        .score-card {
            position: relative;

            min-height: 112px;

            padding: 15px 15px 14px;

            border-radius: 13px;

            background: #ffffff;

            border: 1px solid #e0e6ef;

            box-shadow:
                0 6px 20px rgba(34,65,112,0.045);

            overflow: hidden;

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }

        .score-card:hover {
            transform: translateY(-2px);

            box-shadow:
                0 10px 25px rgba(34,65,112,0.07);
        }

        .score-icon {
            width: 30px;
            height: 30px;

            display: flex;

            align-items: center;
            justify-content: center;

            border-radius: 8px;

            background: #edf3ff;

            color: #4b6fc2;

            font-size: 12px;

            margin-bottom: 10px;
        }

        .score-label {
            color: #718099;

            font-size: 10px;

            font-weight: 750;

            letter-spacing: 0.65px;

            text-transform: uppercase;
        }

        .score-value {
            color: #17294d;

            font-size: 24px;

            font-weight: 800;

            letter-spacing: -0.5px;

            line-height: 1;

            margin-top: 4px;
        }

        .score-line {
            position: absolute;

            height: 3px;

            width: 38px;

            bottom: 0;

            left: 15px;

            border-radius:
                5px 5px 0 0;

            background: #587bd0;
        }


        /* ========================================================
           INSIGHT SECTION
           ======================================================== */

        .insight-card {
            margin-top: 18px;

            padding: 19px 21px;

            border-radius: 14px;

            background:
                linear-gradient(
                    145deg,
                    #ffffff,
                    #f8faff
                );

            border: 1px solid #e0e6ef;

            box-shadow:
                0 6px 20px rgba(34,65,112,0.04);
        }

        .insight-header {
            display: flex;

            align-items: center;

            gap: 10px;

            margin-bottom: 9px;
        }

        .insight-icon {
            width: 32px;
            height: 32px;

            border-radius: 9px;

            background: #edf3ff;

            color: #4b6fc2;

            display: flex;

            align-items: center;
            justify-content: center;

            font-size: 14px;

            flex-shrink: 0;
        }

        .insight-title {
            color: #1a2d50;

            font-size: 14px;

            font-weight: 720;
        }

        .insight-caption {
            color: #8490a3;

            font-size: 10.5px;

            margin-top: 2px;
        }

        .insight-text {
            color: #536176;

            font-size: 12.5px;

            line-height: 1.7;

            max-width: 1100px;
        }


        /* ========================================================
           TECHNICAL BREAKDOWN
           ======================================================== */

        .breakdown-header {
            display: flex;

            align-items: flex-end;

            justify-content: space-between;

            gap: 20px;

            margin-top: 25px;

            margin-bottom: 11px;
        }

        .breakdown-title {
            color: #17294d;

            font-size: 15px;

            font-weight: 720;
        }

        .breakdown-caption {
            color: #8490a3;

            font-size: 10.5px;

            margin-top: 3px;
        }

        .technical-grid {
            display: grid;

            grid-template-columns:
                repeat(5, 1fr);

            gap: 9px;
        }

        .technical-card {
            padding: 15px;

            min-height: 125px;

            border-radius: 12px;

            background: #ffffff;

            border: 1px solid #e0e6ef;

            box-shadow:
                0 5px 17px rgba(34,65,112,0.035);
        }

        .technical-top {
            display: flex;

            justify-content: space-between;

            align-items: center;

            gap: 7px;

            margin-bottom: 10px;
        }

        .technical-name {
            color: #52627a;

            font-size: 10px;

            font-weight: 800;

            letter-spacing: 0.65px;

            text-transform: uppercase;
        }

        .technical-score {
            color: #4b6fc2;

            font-size: 11px;

            font-weight: 800;
        }

        .technical-text {
            color: #7a8798;

            font-size: 11px;

            line-height: 1.55;
        }


        /* ========================================================
           INTERPRETATION
           ======================================================== */

        .interpretation-card {
            margin-top: 12px;

            padding: 12px 15px;

            border-radius: 10px;

            background: #edf3ff;

            border: 1px solid #dce8fb;

            border-left:
                3px solid #587bd0;

            color: #536176;

            font-size: 11.5px;

            line-height: 1.6;
        }

        .interpretation-label {
            color: #315b9f;

            font-weight: 750;
        }


        /* ========================================================
           SIMILAR PASSAGES
           ======================================================== */

        .passages-header {
            display: flex;

            justify-content: space-between;

            align-items: flex-end;

            gap: 20px;

            margin-top: 27px;

            margin-bottom: 11px;
        }

        .passages-title {
            color: #17294d;

            font-size: 20px;

            font-weight: 750;

            letter-spacing: -0.2px;
        }

        .passages-caption {
            color: #78869b;

            font-size: 12px;

            margin-top: 4px;
        }

        .passage-card {
            padding: 16px 17px;

            margin-bottom: 9px;

            border-radius: 13px;

            background: #ffffff;

            border: 1px solid #e0e6ef;

            box-shadow:
                0 5px 17px rgba(34,65,112,0.035);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }

        .passage-card:hover {
            transform: translateY(-1px);

            box-shadow:
                0 8px 21px rgba(34,65,112,0.06);
        }

        .passage-top {
            display: flex;

            justify-content: space-between;

            align-items: center;

            gap: 15px;

            margin-bottom: 11px;
        }

        .passage-number {
            color: #6d7c94;

            font-size: 9px;

            font-weight: 800;

            letter-spacing: 0.8px;

            text-transform: uppercase;
        }

        .passage-score {
            padding: 6px 9px;

            border-radius: 8px;

            background: #edf3ff;

            border: 1px solid #d8e5fb;

            color: #4b6fc2;

            font-size: 10px;

            font-weight: 800;
        }

        .passage-grid {
            display: grid;

            grid-template-columns:
                1fr 1fr;

            gap: 10px;
        }

        .passage-label {
            color: #8490a3;

            font-size: 9.5px;

            font-weight: 800;

            letter-spacing: 0.75px;

            text-transform: uppercase;

            margin-bottom: 5px;
        }

        .passage-text {
            padding: 11px 12px;

            border-radius: 9px;

            background: #f7f9fc;

            border: 1px solid #e9edf3;

            color: #536176;

            font-size: 11px;

            line-height: 1.6;
        }


        /* ========================================================
           EMPTY STATE
           ======================================================== */

        .empty-state {
            padding: 23px;

            border-radius: 14px;

            background:
                linear-gradient(
                    145deg,
                    #ffffff,
                    #f8faff
                );

            border: 1px solid #e0e6ef;

            box-shadow:
                0 6px 20px rgba(34,65,112,0.035);

            text-align: center;

            color: #6d7c94;

            font-size: 12px;
        }

        .empty-icon {
            width: 42px;
            height: 42px;

            margin: 0 auto 9px;

            border-radius: 12px;

            background: #edf3ff;

            color: #4b6fc2;

            display: flex;

            align-items: center;
            justify-content: center;

            font-size: 17px;
        }


        /* ========================================================
           STREAMLIT ALERTS / PROGRESS
           ======================================================== */

        div[data-testid="stAlert"] {
            border-radius: 9px;
            font-size: 12px;
        }

        div[data-testid="stProgress"] {
            margin-top: 8px;
            margin-bottom: 8px;
        }

        div[data-testid="stProgress"] > div > div {
            background-color: #5278d2;
        }


        /* ========================================================
           RESPONSIVE
           ======================================================== */

        @media (max-width: 1100px) {

            .score-grid {
                grid-template-columns:
                    repeat(3, 1fr);
            }

            .technical-grid {
                grid-template-columns:
                    repeat(3, 1fr);
            }

        }


        @media (max-width: 800px) {

            .block-container {
                padding: 28px 25px 45px 25px !important;
            }

            .analysis-title {
                font-size: 30px;
            }

            .analysis-hero-badge {
                display: none;
            }

            .comparison-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }

            .comparison-vs {
                margin: 0;
            }

            .comparison-score-side {
                text-align: left;
            }

            .score-grid {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .technical-grid {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .document-info-strip {
                grid-template-columns: 1fr;
            }

        }


        @media (max-width: 600px) {

            .analysis-title {
                font-size: 27px;
            }

            .analysis-description {
                font-size: 13px;
            }

            .analysis-hero {
                padding: 23px;
            }

            .analysis-hero-title {
                font-size: 21px;
            }

            .score-grid {
                grid-template-columns: 1fr;
            }

            .technical-grid {
                grid-template-columns: 1fr;
            }

            .passage-grid {
                grid-template-columns: 1fr;
            }

        }

        </style>
        """
    )


# ============================================================
# DOCUMENT TEXT EXTRACTION
# ============================================================

def extract_document_text(document):

    file_path = document["file_path"]
    file_type = document["file_type"].lower()

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Document file not found: {file_path}"
        )

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if file_type == "pdf":

        with open(
            file_path,
            "rb"
        ) as file:

            return extract_pdf_text(file)

    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    elif file_type == "docx":

        with open(
            file_path,
            "rb"
        ) as file:

            return extract_docx_text(file)

    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    elif file_type == "txt":

        with open(
            file_path,
            "rb"
        ) as file:

            return extract_txt_text(file)

    # --------------------------------------------------------
    # UNSUPPORTED TYPE
    # --------------------------------------------------------

    else:

        raise ValueError(
            f"Unsupported document type: {file_type}"
        )

# ============================================================
# ANALYSIS PAGE
# ============================================================

def analysis_page():

    apply_analysis_styles()

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.html(
        """
        <div class="analysis-top">

            <div>

                <div class="analysis-label">
                    SCHOLARSHIELD - AI-POWERED ACADEMIC ANALYSIS
                </div>

                <div class="analysis-title">
                    Academic Similarity Analysis
                </div>

                <div class="analysis-description">
                    Compare academic documents and understand the
                    relationships behind their similarity across
                    language, structure, context and meaning.
                </div>

            </div>

        </div>
        """
    )

    # ========================================================
    # ANALYSIS HERO
    # ========================================================

    st.html(
        """
        <div class="analysis-hero">

            <div class="analysis-decoration-one"></div>
            <div class="analysis-decoration-two"></div>
            <div class="analysis-dot"></div>

            <div class="analysis-hero-content">

                <div class="analysis-hero-eyebrow">
                    CONTEXT-AWARE COMPARISON WORKSPACE
                </div>

                <div class="analysis-hero-title">
                    Explore how two academic documents relate
                </div>

                <div class="analysis-hero-text">
                    Select a target document and one or more
                    references. ScholarShield examines multiple
                    linguistic layers to show not only how similar
                    the documents are, but what contributes to that
                    relationship.
                </div>

            </div>

            <div class="analysis-hero-badge">
                ● NLP analysis engine ready
            </div>

        </div>
        """
    )

    # ========================================================
    # CURRENT USER
    # ========================================================

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.error(
            "User session not found. Please log in again."
        )

        return

    # ========================================================
    # LOAD DOCUMENTS
    # ========================================================

    documents = get_user_documents(user_id)

    if not documents:

        st.html(
            """
            <div class="section-block">

                <div class="section-heading">
                    Analysis Workspace
                </div>

            </div>

            <div class="empty-state">

                <div class="empty-icon">
                    ▤
                </div>

                <strong>
                    No documents available
                </strong>

                <div style="margin-top:4px;">
                    Upload documents before starting an analysis.
                </div>

            </div>
            """
        )

        return

    document_lookup = {
        document["id"]: document
        for document in documents
    }

    # ========================================================
    # DOCUMENT SELECTION SECTION
    # ========================================================

    st.html(
        """
        <div class="section-block">

            <div class="section-label">
                ANALYSIS WORKSPACE
            </div>

            <div class="section-heading">
                Build your comparison
            </div>

            <div class="section-subheading">
                Choose the document to analyze and the academic
                references you want to compare it against.
            </div>

        </div>
        """
    )

    # ========================================================
    # WORKSPACE CARD
    # ========================================================

    st.html(
        """
        <div class="workspace-card">

            <div class="workspace-heading">
                Document Selection
            </div>

            <div class="workspace-caption">
                Start with one target document, then select one
                or more reference documents for comparison.
            </div>

        </div>
        """
    )

    target_options = {
        document["filename"]: document["id"]
        for document in documents
    }

    # ========================================================
    # TARGET
    # ========================================================

    st.html(
        """
        <div style="
            margin-top:13px;
            margin-bottom:6px;
        ">
            <div class="field-label">
                Target Document
            </div>
        </div>
        """
    )

    selected_document_id = st.session_state.get(
        "selected_document_id"
    )

    opened_from_library = st.session_state.get(
        "analysis_from_library",
        False
    )

    target_filenames = list(
        target_options.keys()
    )

    if (
        opened_from_library
        and selected_document_id is not None
    ):

        selected_filename = None

        for filename, document_id in target_options.items():

            if document_id == selected_document_id:

                selected_filename = filename

                break

        if selected_filename is not None:

            st.session_state[
                "analysis_target_selector"
            ] = selected_filename

    target_filename = st.selectbox(
        "Select target document",
        options=target_filenames,
        index=None,
        placeholder="Choose a target document",
        label_visibility="collapsed",
        key="analysis_target_selector"
    )

    if opened_from_library:

        st.session_state.pop(
            "selected_document_id",
            None
        )

        st.session_state.pop(
            "analysis_from_library",
            None
        )

    # ========================================================
    # REFERENCES
    # ========================================================

    st.html(
        """
        <div style="
            margin-top:15px;
            margin-bottom:6px;
        ">
            <div class="field-label">
                Reference Documents
            </div>
        </div>
        """
    )

    if target_filename:

        target_id = target_options[
            target_filename
        ]

        reference_options = {
            document["filename"]: document["id"]
            for document in documents
            if document["id"] != target_id
        }

        if reference_options:

            selected_reference_names = st.multiselect(
                "Select reference documents",
                options=list(
                    reference_options.keys()
                ),
                placeholder="Choose one or more reference documents",
                label_visibility="collapsed"
            )

        else:

            selected_reference_names = []

            st.info(
                "You need at least two uploaded documents "
                "to perform a comparison."
            )

    else:

        selected_reference_names = []

        st.info(
            "Select a target document first."
        )

    # ========================================================
    # CONFIGURATION SUMMARY
    # ========================================================

    reference_html = ""

    if selected_reference_names:

        for reference_name in selected_reference_names:

            reference_html += (
                f'<span class="reference-chip">'
                f'{reference_name}'
                f'</span>'
            )

    else:

        reference_html = (
            '<span style="color:#94a3b8;">'
            'No reference selected'
            '</span>'
        )

    target_display = (
        target_filename
        if target_filename
        else "Not selected"
    )

    st.html(
        f"""
        <div class="document-info-strip">

            <div class="document-info-item">

                <div class="document-info-label">
                    Target Document
                </div>

                <div class="document-info-value">
                    {target_display}
                </div>

            </div>

            <div class="document-info-item">

                <div class="document-info-label">
                    Reference Documents
                </div>

                <div class="document-info-value">
                    {reference_html}
                </div>

            </div>

        </div>
        """
    )

    # ========================================================
    # START ANALYSIS
    # ========================================================

    target_selected = bool(
        target_filename
    )

    references_selected = (
        len(selected_reference_names) > 0
    )

    st.html(
        """
        <div style="margin-top:13px;">
        """
    )

    if st.button(
        "Start Analysis  →",
        type="primary",
        use_container_width=True
    ):

        if not target_selected:

            st.error(
                "Please select a target document."
            )

            return

        if not references_selected:

            st.error(
                "Please select at least one reference document."
            )

            return

        reference_ids = [
            reference_options[name]
            for name in selected_reference_names
        ]

        st.session_state[
            "analysis_target_id"
        ] = target_id

        st.session_state[
            "analysis_reference_ids"
        ] = reference_ids

        target_document = document_lookup[
            target_id
        ]

        # ----------------------------------------------------
        # TARGET TEXT
        # ----------------------------------------------------

        try:

            with st.spinner(
                "Reading target document..."
            ):

                target_text = extract_document_text(
                    target_document
                )

        except Exception as error:

            st.error(
                f"Unable to read the target document: {error}"
            )

            return

        if not target_text.strip():

            st.error(
                "The selected target document does not contain "
                "extractable text."
            )

            return

        # ----------------------------------------------------
        # ANALYSIS
        # ----------------------------------------------------

        analysis_results = []

        progress_bar = st.progress(0)

        total_references = len(
            reference_ids
        )

        for index, reference_id in enumerate(
            reference_ids
        ):

            reference_document = document_lookup[
                reference_id
            ]

            try:

                reference_text = extract_document_text(
                    reference_document
                )

                if not reference_text.strip():

                    st.warning(
                        f"Skipping "
                        f"{reference_document['filename']} "
                        "because no text could be extracted."
                    )

                    continue

                result = analyze_document_pair(
                    target_text,
                    reference_text
                )

                if result["success"]:

                    analysis_results.append(
                        {
                            "reference_document":
                                reference_document,

                            "result":
                                result
                        }
                    )

                else:

                    st.error(
                        f"Analysis failed for "
                        f"{reference_document['filename']}: "
                        f"{result.get('error', 'Unknown error')}"
                    )

            except Exception as error:

                st.error(
                    f"Unable to analyze "
                    f"{reference_document['filename']}: "
                    f"{error}"
                )

            progress_bar.progress(
                (index + 1) / total_references
            )

        progress_bar.empty()

        st.session_state[
            "analysis_results"
        ] = analysis_results

        if not analysis_results:

            st.error(
                "No analysis results were generated."
            )

            return

        st.success(
            "Analysis completed successfully."
        )

    st.html("</div>")

    # ========================================================
    # RESULTS
    # ========================================================

    analysis_results = st.session_state.get(
        "analysis_results",
        []
    )

    if not analysis_results:

        return

    # ========================================================
    # RESULTS HEADER
    # ========================================================

    st.html(
        f"""
        <div class="analysis-divider"></div>

        <div class="results-top">

            <div>

                <div class="section-label">
                    ANALYSIS RESULTS
                </div>

                <div class="section-heading">
                    Similarity Findings
                </div>

                <div class="section-subheading">
                    A multi-level view of the relationship between
                    your target document and its references.
                </div>

            </div>

            <div class="results-count">
                {len(analysis_results)}
                {"references" if len(analysis_results) != 1 else "reference"}
                analyzed
            </div>

        </div>
        """
    )

    # ========================================================
    # PDF REPORT GENERATION
    # ========================================================

    report_col1, report_col2 = st.columns(
        [3, 1]
    )

    with report_col1:

        st.html(
            """
            <div style="
                color:#6d7c94;
                font-size:11px;
                line-height:1.5;
                padding-top:7px;
            ">
                Generate a complete ScholarShield PDF report
                containing the similarity scores, explanations,
                NLP breakdown and similar passages.
            </div>
            """
        )

    with report_col2:

        if st.button(
            "Generate PDF Report",
            type="primary",
            use_container_width=True
        ):

            try:

                report_target_document = document_lookup.get(
                    st.session_state.get(
                        "analysis_target_id"
                    )
                )

                if not report_target_document:

                    st.error(
                        "Unable to identify the target document."
                    )

                else:

                    with st.spinner(
                        "Generating ScholarShield report..."
                    ):

                        report_path = generate_analysis_report(
                            target_document=report_target_document,
                            analysis_results=analysis_results
                        )

                    st.session_state[
                        "generated_report_path"
                    ] = report_path

                    st.success(
                        "PDF report generated successfully."
                    )

            except Exception as error:

                st.error(
                    f"Unable to generate the PDF report: {error}"
                )


    # ========================================================
    # PDF DOWNLOAD + SAVE ANALYSIS
    # ========================================================

    generated_report_path = st.session_state.get(
        "generated_report_path"
    )

    if generated_report_path and os.path.exists(
        generated_report_path
    ):

        st.html(
            """
            <div style="
                margin-top:14px;
                margin-bottom:8px;
                color:#1a2d50;
                font-size:13px;
                font-weight:700;
            ">
                Your analysis is ready
            </div>
            """
        )

        download_col, save_col = st.columns(
            [1, 1],
            gap="medium"
        )

        # ----------------------------------------------------
        # DOWNLOAD REPORT
        # ----------------------------------------------------

        with download_col:

            with open(
                generated_report_path,
                "rb"
            ) as report_file:

                st.download_button(
                    label="Download PDF Report",
                    data=report_file.read(),
                    file_name=os.path.basename(
                        generated_report_path
                    ),
                    mime="application/pdf",
                    use_container_width=True
                )

        # ----------------------------------------------------
        # SAVE ANALYSIS
        # ----------------------------------------------------

        with save_col:

            if st.button(
                "Save Analysis",
                type="primary",
                use_container_width=True
            ):

                try:

                    target_document_id = st.session_state.get(
                        "analysis_target_id"
                    )

                    if not target_document_id:

                        st.error(
                            "Unable to identify the target document."
                        )

                    else:

                        with st.spinner(
                            "Saving analysis to ScholarShield..."
                        ):

                            analysis_id = save_analysis(
                                target_document_id=target_document_id,
                                analysis_results=analysis_results,
                                report_path=generated_report_path
                            )

                        st.session_state[
                            "saved_analysis_id"
                        ] = analysis_id

                        st.success(
                            "Analysis saved successfully."
                        )

                except Exception as error:

                    st.error(
                        f"Unable to save the analysis: {error}"
                    )
    # ========================================================
    # EACH REFERENCE
    # ========================================================

    for analysis_item in analysis_results:

        reference_document = analysis_item[
            "reference_document"
        ]

        result = analysis_item[
            "result"
        ]

        multi_level = result[
            "multi_level"
        ]

        overall_score = multi_level[
            "overall_score"
        ]

        lexical_score = multi_level[
            "lexical_score"
        ]

        semantic_score = multi_level[
            "semantic_score"
        ]

        syntactic_score = multi_level[
            "syntactic_score"
        ]

        contextual_score = multi_level[
            "contextual_score"
        ]

        meaning_score = multi_level[
            "meaning_score"
        ]

        similarity_level = multi_level[
            "similarity_level"
        ]

        # ====================================================
        # RESULT WRAPPER
        # ====================================================

        st.html(
            """
            <div class="result-wrapper">
            """
        )

        # ====================================================
        # COMPARISON CARD
        # ====================================================

        st.html(
            f"""
            <div class="comparison-card">

                <div class="comparison-decoration-one"></div>
                <div class="comparison-decoration-two"></div>

                <div class="comparison-content">

                    <div class="comparison-grid">

                        <div>

                            <div class="comparison-side-label">
                                Target Document
                            </div>

                            <div class="comparison-document-name">
                                {target_filename}
                            </div>

                            <div class="comparison-meta">
                                Document selected for analysis
                            </div>

                        </div>

                        <div class="comparison-vs">
                            VS
                        </div>

                        <div class="comparison-score-side">

                            <div class="comparison-score-label">
                                Overall Similarity
                            </div>

                            <div class="comparison-score">
                                {overall_score:.1f}%
                            </div>

                            <div class="comparison-level">
                                {similarity_level}
                            </div>

                            <div class="comparison-meta">
                                {reference_document["filename"]}
                            </div>

                        </div>

                    </div>

                </div>

            </div>
            """
        )

        # ====================================================
        # SCORE CARDS
        # ====================================================

        score_items = [
            ("◈", "Overall", overall_score),
            ("▤", "Lexical", lexical_score),
            ("◆", "Semantic", semantic_score),
            ("⌘", "Syntactic", syntactic_score),
            ("◌", "Contextual", contextual_score),
            ("◎", "Meaning", meaning_score),
        ]

        score_html = """
        <div class="score-grid">
        """

        for icon, label, value in score_items:

            score_html += f"""
                <div class="score-card">

                    <div class="score-icon">
                        {icon}
                    </div>

                    <div class="score-label">
                        {label}
                    </div>

                    <div class="score-value">
                        {value:.1f}%
                    </div>

                    <div class="score-line"></div>

                </div>
            """

        score_html += """
        </div>
        """

        st.html(score_html)

        # ====================================================
        # EXPLANATION DATA
        # ====================================================

        explanation = result[
            "explanation"
        ]

        simple_explanation = explanation.get(
            "simple_explanation",
            explanation.get(
                "explanation",
                ""
            )
        )

        technical_explanation = explanation.get(
            "technical_explanation",
            ""
        )

        component_explanations = explanation.get(
            "component_explanations",
            {}
        )

        overall_interpretation = explanation.get(
            "overall_interpretation",
            ""
        )

        lexical_details = component_explanations.get(
            "lexical",
            {}
        )

        semantic_details = component_explanations.get(
            "semantic",
            {}
        )

        syntactic_details = component_explanations.get(
            "syntactic",
            {}
        )

        contextual_details = component_explanations.get(
            "contextual",
            {}
        )

        meaning_details = component_explanations.get(
            "meaning",
            {}
        )

        # ====================================================
        # MAIN INSIGHT
        # ====================================================

        st.html(
            f"""
            <div class="insight-card">

                <div class="insight-header">

                    <div class="insight-icon">
                        ◈
                    </div>

                    <div>

                        <div class="insight-title">
                            Why these documents are similar
                        </div>

                        <div class="insight-caption">
                            Plain-language interpretation of the analysis
                        </div>

                    </div>

                </div>

                <div class="insight-text">
                    {simple_explanation}
                </div>

            </div>
            """
        )

        # ====================================================
        # TECHNICAL BREAKDOWN
        # ====================================================

        st.html(
            """
            <div class="breakdown-header">

                <div>

                    <div class="breakdown-title">
                        NLP Component Breakdown
                    </div>

                    <div class="breakdown-caption">
                        How each linguistic layer contributed to the
                        overall similarity score.
                    </div>

                </div>

            </div>
            """
        )

        technical_items = [
            (
                "Lexical",
                lexical_score,
                lexical_details
            ),
            (
                "Semantic",
                semantic_score,
                semantic_details
            ),
            (
                "Syntactic",
                syntactic_score,
                syntactic_details
            ),
            (
                "Contextual",
                contextual_score,
                contextual_details
            ),
            (
                "Meaning",
                meaning_score,
                meaning_details
            ),
        ]

        technical_html = """
        <div class="technical-grid">
        """

        for name, score, details in technical_items:

            detail_text = " ".join(
                details.get(
                    "details",
                    []
                )
            )

            technical_html += f"""
                <div class="technical-card">

                    <div class="technical-top">

                        <div class="technical-name">
                            {name}
                        </div>

                        <div class="technical-score">
                            {score:.1f}%
                        </div>

                    </div>

                    <div class="technical-text">
                        {detail_text}
                    </div>

                </div>
            """

        technical_html += """
        </div>
        """

        st.html(technical_html)

        # ====================================================
        # OVERALL INTERPRETATION
        # ====================================================

        if overall_interpretation:

            st.html(
                f"""
                <div class="interpretation-card">

                    <span class="interpretation-label">
                        Overall interpretation:
                    </span>

                    &nbsp;

                    {overall_interpretation}

                </div>
                """
            )

        # ====================================================
        # SIMILAR PASSAGES
        # ====================================================

        similar_passages = result[
            "similar_passages"
        ]

        st.html(
            f"""
            <div class="passages-header">

                <div>

                    <div class="section-label">
                        MATCHED CONTENT
                    </div>

                    <div class="passages-title">
                        Similar Passages
                    </div>

                    <div class="passages-caption">
                        Sentences identified as meaningfully similar
                        between the two documents.
                    </div>

                </div>

                <div class="results-count">
                    {len(similar_passages)}
                    {"matches" if len(similar_passages) != 1 else "match"}
                </div>

            </div>
            """
        )

        if similar_passages:

            for passage_index, match in enumerate(
                similar_passages,
                start=1
            ):

                st.html(
                    f"""
                    <div class="passage-card">

                        <div class="passage-top">

                            <div class="passage-number">
                                MATCH {passage_index}
                            </div>

                            <div class="passage-score">
                                {match["similarity_score"]:.1f}%
                                similarity
                            </div>

                        </div>

                        <div class="passage-grid">

                            <div>

                                <div class="passage-label">
                                    Target Passage
                                </div>

                                <div class="passage-text">
                                    {match["target_sentence"]}
                                </div>

                            </div>

                            <div>

                                <div class="passage-label">
                                    Reference Passage
                                </div>

                                <div class="passage-text">
                                    {match["reference_sentence"]}
                                </div>

                            </div>

                        </div>

                    </div>
                    """
                )

        else:

            st.html(
                """
                <div class="empty-state">

                    <div class="empty-icon">
                        ◌
                    </div>

                    <strong>
                        No highly similar passages detected
                    </strong>

                    <div style="margin-top:4px;">
                        No passages exceeded the similarity threshold
                        used by the analysis engine.
                    </div>

                </div>
                """
            )

        # ====================================================
        # END RESULT
        # ====================================================

        st.html(
            """
            </div>
            """
        )


# ============================================================
# RUN PAGE
# ============================================================

if __name__ == "__main__":
    analysis_page()