import sys
import os
import hashlib

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from document_processing.pdf_extractor import extract_pdf_text
from document_processing.docx_extractor import extract_docx_text
from document_processing.text_extractor import extract_txt_text
from database.database import add_document
from pages.authenticated_sidebar import show_authenticated_sidebar

from document_processing.document_utils import (
    validate_file,
    count_sentences,
    save_uploaded_file
)


def show_upload():

    show_authenticated_sidebar()


    # ============================================================
    # GLOBAL STYLING
    # ============================================================

    st.html("""
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


        /* ========================================================
           PAGE HEADER
           ======================================================== */

        .upload-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 30px;
        }

        .upload-label {
            color: #5278d2;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .upload-title {
            color: #14264a;
            font-size: 36px;
            font-weight: 800;
            letter-spacing: -0.8px;
            line-height: 1.12;
            margin: 0;
        }

        .upload-description {
            color: #61718b;
            font-size: 15px;
            line-height: 1.7;
            margin-top: 10px;
            max-width: 720px;
        }


        /* ========================================================
           UPLOAD HERO
           ======================================================== */

        .upload-hero {
            margin-top: 30px;
            padding: 28px 32px;
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

        .upload-hero-content {
            position: relative;
            z-index: 3;
        }

        .upload-hero-eyebrow {
            color: #9db9ef;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .upload-hero-title {
            color: #ffffff;
            font-size: 22px;
            font-weight: 750;
            line-height: 1.25;
            margin-bottom: 8px;
        }

        .upload-hero-text {
            color: #dce7f8;
            font-size: 13px;
            line-height: 1.7;
            max-width: 720px;
        }

        .upload-hero-decoration-one {
            position: absolute;
            width: 280px;
            height: 280px;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 50%;
            right: -100px;
            top: -135px;
        }

        .upload-hero-decoration-two {
            position: absolute;
            width: 180px;
            height: 180px;
            border: 1px solid rgba(255,255,255,0.055);
            border-radius: 50%;
            right: 65px;
            bottom: -120px;
        }

        .upload-dot {
            position: absolute;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #a9c4ff;
            right: 110px;
            top: 55px;
            box-shadow: 0 0 18px rgba(169,196,255,0.7);
        }


        /* ========================================================
           SECTION
           ======================================================== */

        .upload-section {
            margin-top: 32px;
            margin-bottom: 14px;
        }

        .upload-section-title {
            color: #17294d;
            font-size: 20px;
            font-weight: 750;
            letter-spacing: -0.2px;
        }

        .upload-section-subtitle {
            color: #78869b;
            font-size: 12.5px;
            margin-top: 4px;
        }


        /* ========================================================
           UPLOAD CARD
           ======================================================== */

        .upload-card {
            background: #ffffff;
            border: 1px solid #e0e6ef;
            border-radius: 15px;
            padding: 24px;
            box-shadow:
                0 7px 24px rgba(34, 65, 112, 0.045);
        }

        .upload-card-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 18px;
        }

        .upload-icon {
            width: 43px;
            height: 43px;
            border-radius: 11px;
            background: #edf3ff;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #4b6fc2;
            font-size: 19px;
            flex-shrink: 0;
        }

        .upload-card-title {
            color: #1a2d50;
            font-size: 15px;
            font-weight: 720;
        }

        .upload-card-subtitle {
            color: #8490a3;
            font-size: 11px;
            margin-top: 3px;
        }


        /* ========================================================
           STREAMLIT FILE UPLOADER
           ======================================================== */

        [data-testid="stFileUploader"] {
            background: #f8faff;
            border: 1.5px dashed #b9c9e7;
            border-radius: 13px;
            padding: 10px;
        }

        [data-testid="stFileUploader"] section {
            border: none !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: transparent !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] {
            color: #61718b !important;
        }


        /* ========================================================
           DOCUMENT INFORMATION
           ======================================================== */

        .document-info-card {
            min-height: 112px;
            padding: 18px;
            border-radius: 13px;

            background: #ffffff;
            border: 1px solid #e0e6ef;

            box-shadow:
                0 5px 18px rgba(34, 65, 112, 0.04);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
        }

        .document-info-card:hover {
            transform: translateY(-2px);
            border-color: #ccd8eb;

            box-shadow:
                0 9px 22px rgba(34, 65, 112, 0.07);
        }

        .document-info-icon {
            font-size: 16px;
            margin-bottom: 9px;
            color: #4b6fc2;
        }

        .document-info-label {
            color: #718099;
            font-size: 10px;
            font-weight: 750;
            letter-spacing: 0.7px;
            text-transform: uppercase;
        }

        .document-info-value {
            color: #17294d;
            font-size: 17px;
            font-weight: 800;
            margin-top: 4px;
            word-break: break-word;
        }


        /* ========================================================
           STATUS
           ======================================================== */

        .success-card {
            padding: 17px 20px;
            border-radius: 13px;

            background: #f2f8f4;
            border: 1px solid #d2e7d8;

            box-shadow:
                0 5px 18px rgba(38, 105, 63, 0.035);

            margin-bottom: 20px;
        }

        .success-title {
            color: #28613b;
            font-size: 13px;
            font-weight: 750;
        }

        .success-text {
            color: #668270;
            font-size: 11px;
            margin-top: 4px;
        }


        /* ========================================================
           STORAGE CARD
           ======================================================== */

        .storage-card {
            padding: 17px 20px;
            border-radius: 13px;

            background: #ffffff;
            border: 1px solid #e0e6ef;

            box-shadow:
                0 5px 18px rgba(34, 65, 112, 0.04);
        }

        .storage-title {
            color: #1a2d50;
            font-size: 13px;
            font-weight: 720;
        }

        .storage-status {
            display: inline-block;
            margin-top: 8px;
            padding: 5px 9px;
            border-radius: 7px;

            background: #edf3ff;
            color: #4b6fc2;

            font-size: 10px;
            font-weight: 750;
            letter-spacing: 0.3px;
        }

        .storage-path {
            color: #8995a8;
            font-size: 10px;
            margin-top: 8px;
            word-break: break-all;
        }


        /* ========================================================
           PREVIEW
           ======================================================== */

        .preview-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
            margin-top: 30px;
            margin-bottom: 12px;
        }

        .preview-title {
            color: #17294d;
            font-size: 20px;
            font-weight: 750;
        }

        .preview-badge {
            padding: 6px 10px;
            border-radius: 7px;

            background: #edf3ff;
            color: #4b6fc2;

            font-size: 10px;
            font-weight: 750;
            letter-spacing: 0.4px;
        }


        /* ========================================================
           TEXT AREA
           ======================================================== */

        [data-testid="stTextArea"] textarea {
            background: #ffffff !important;
            color: #253a60 !important;

            border: 1px solid #dce3ed !important;
            border-radius: 13px !important;

            font-size: 13px !important;
            line-height: 1.7 !important;

            box-shadow:
                0 5px 18px rgba(34, 65, 112, 0.035);
        }


        /* ========================================================
           DIVIDER
           ======================================================== */

        .upload-divider {
            height: 1px;
            background: #e1e6ee;
            margin: 30px 0;
        }


        /* ========================================================
           ERROR
           ======================================================== */

        [data-testid="stAlert"] {
            border-radius: 11px !important;
        }


        /* ========================================================
           MOBILE
           ======================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding: 25px 18px 40px 18px !important;
            }

            .upload-title {
                font-size: 29px;
            }

            .upload-hero {
                padding: 23px;
            }

            .upload-hero-title {
                font-size: 19px;
            }

        }

    </style>
    """)


    # ============================================================
    # PAGE HEADER
    # ============================================================

    st.html("""
    <div class="upload-top">

        <div>

            <div class="upload-label">
                SCHOLARSHIELD · DOCUMENT WORKSPACE
            </div>

            <div class="upload-title">
                Upload Academic Document
            </div>

            <div class="upload-description">
                Add an academic document to prepare it for
                context-aware similarity analysis.
            </div>

        </div>

    </div>
    """)


    # ============================================================
    # HERO
    # ============================================================

    st.html("""
    <div class="upload-hero">

        <div class="upload-hero-decoration-one"></div>
        <div class="upload-hero-decoration-two"></div>
        <div class="upload-dot"></div>

        <div class="upload-hero-content">

            <div class="upload-hero-eyebrow">
                DOCUMENT ANALYSIS PIPELINE
            </div>

            <div class="upload-hero-title">
                Start with your academic document
            </div>

            <div class="upload-hero-text">
                ScholarShield extracts and prepares document content
                before applying lexical, syntactic and semantic
                similarity analysis.
            </div>

        </div>

    </div>
    """)


    # ============================================================
    # UPLOAD SECTION
    # ============================================================

    st.html("""
    <div class="upload-section">

        <div class="upload-section-title">
            Select Document
        </div>

        <div class="upload-section-subtitle">
            Supported formats: PDF, DOCX and TXT · Maximum file size: 10 MB
        </div>

    </div>
    """)


    st.html("""
    <div class="upload-card">

        <div class="upload-card-header">

            <div class="upload-icon">
                ↑
            </div>

            <div>

                <div class="upload-card-title">
                    Upload your academic document
                </div>

                <div class="upload-card-subtitle">
                    Drag and drop your file here or browse from your device.
                </div>

            </div>

        </div>

    </div>
    """)


    # ============================================================
    # FILE UPLOADER
    # ============================================================

    uploaded_file = st.file_uploader(
        "Choose a PDF, DOCX, or TXT file",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    # ============================================================
    # UPLOAD SESSION CONTROL
    # ============================================================

    if "processed_upload_signature" not in st.session_state:
        st.session_state.processed_upload_signature = None

    if "processed_upload_document_id" not in st.session_state:
        st.session_state.processed_upload_document_id = None

    if "processed_upload_path" not in st.session_state:
        st.session_state.processed_upload_path = None


    # ============================================================
    # DOCUMENT PROCESSING
    # ============================================================

    if uploaded_file is not None:

        is_valid, validation_message = validate_file(
            uploaded_file
        )

        if not is_valid:

            st.error(validation_message)

            st.stop()

        file_bytes = uploaded_file.getvalue()

        current_signature = hashlib.sha256(
            file_bytes
        ).hexdigest()

        # ------------------------------------------------------------
        # SAVE ONLY ONCE FOR THIS UPLOAD
        # ------------------------------------------------------------

        if (
            st.session_state.processed_upload_signature
            != current_signature
        ):

            file_path = save_uploaded_file(
                uploaded_file
            )

        else:

            file_path = st.session_state.processed_upload_path

    
        file_extension = (
            uploaded_file.name
            .split(".")[-1]
            .lower()
        )

        # --------------------------------------------------------
        # TEXT EXTRACTION
        # --------------------------------------------------------

        if file_extension == "pdf":

            extracted_text = extract_pdf_text(
                uploaded_file
            )

        elif file_extension == "docx":

            extracted_text = extract_docx_text(
               uploaded_file
           )
    
        elif file_extension == "txt":

            extracted_text = extract_txt_text(
                uploaded_file
            )

        else:

            extracted_text = ""


        # ========================================================
        # SUCCESSFUL EXTRACTION
        # ========================================================
    
        if extracted_text.strip():

            sentence_count = count_sentences(
                extracted_text
            )
            word_count = len(extracted_text.split())
            character_count = len(extracted_text)

        # ------------------------------------------------------------
        # ADD DOCUMENT TO DATABASE ONLY ONCE
        # ------------------------------------------------------------

            if (
                st.session_state.processed_upload_signature
                != current_signature
            ):

                document_id = add_document(
                    user_id=st.session_state.user_id,
                    filename=uploaded_file.name,
                    file_type=file_extension.upper(),
                    file_path=file_path,
                    file_size=uploaded_file.size,
                    word_count=word_count,
                    character_count=character_count,
                    sentence_count=sentence_count
                )

                st.session_state.processed_upload_signature = current_signature
                st.session_state.processed_upload_document_id = document_id
                st.session_state.processed_upload_path = file_path

            else:

                document_id = st.session_state.processed_upload_document_id

            # ----------------------------------------------------
            # SUCCESS STATUS
            # ----------------------------------------------------

            st.html("""
            <div class="success-card">

                <div class="success-title">
                    ✓ Document processed successfully
                </div>

                <div class="success-text">
                    The document has been validated, extracted
                    and stored successfully.
                </div>

            </div>
            """)


            # ----------------------------------------------------
            # DOCUMENT INFORMATION
            # ----------------------------------------------------

            st.html("""
            <div class="upload-section">

                <div class="upload-section-title">
                    Document Information
                </div>

                <div class="upload-section-subtitle">
                    Basic information extracted from the uploaded document.
                </div>

            </div>
            """)


            col1, col2, col3 = st.columns(3)


            with col1:

                st.html(f"""
                <div class="document-info-card">

                    <div class="document-info-icon">
                        ▤
                    </div>

                    <div class="document-info-label">
                        File Name
                    </div>

                    <div class="document-info-value">
                        {uploaded_file.name}
                    </div>

                </div>
                """)


            with col2:

                st.html(f"""
                <div class="document-info-card">

                    <div class="document-info-icon">
                        ◈
                    </div>

                    <div class="document-info-label">
                        File Type
                    </div>

                    <div class="document-info-value">
                        {file_extension.upper()}
                    </div>

                </div>
                """)


            with col3:
                
                st.html(f"""
                <div class="document-info-card">

                    <div class="document-info-icon">
                        ◌
                    </div>

                    <div class="document-info-label">
                        File Size
                    </div>

                    <div class="document-info-value">
                        {uploaded_file.size / 1024:.2f} KB
                    </div>

                </div>
                """)


            st.html("<div style='height:12px;'></div>")


            col4, col5, col6 = st.columns(3)


            with col4:

                st.html(f"""
                <div class="document-info-card">

                    <div class="document-info-icon">
                        Aa
                    </div>

                    <div class="document-info-label">
                        Word Count
                    </div>

                    <div class="document-info-value">
                        {len(extracted_text.split()):,}
                    </div>

                </div>
                """)


            with col5:

                st.html(f"""
                <div class="document-info-card">

                    <div class="document-info-icon">
                        #
                    </div>

                    <div class="document-info-label">
                        Characters
                    </div>

                    <div class="document-info-value">
                        {len(extracted_text):,}
                    </div>

                </div>
                """)


            with col6:

                st.html(f"""
                <div class="document-info-card">

                    <div class="document-info-icon">
                        ¶
                    </div>

                    <div class="document-info-label">
                        Sentences
                    </div>

                    <div class="document-info-value">
                        {sentence_count:,}
                    </div>

                </div>
                """)


            # ----------------------------------------------------
            # STORAGE
            # ----------------------------------------------------

            st.html("""
            <div class="upload-divider"></div>
            """)


            st.html("""
            <div class="upload-section" style="margin-top:0;">

                <div class="upload-section-title">
                    Storage Status
                </div>

                <div class="upload-section-subtitle">
                    The original document has been stored locally and is ready for processing.
                </div>

            </div>
            """)


            st.html(f"""
            <div class="storage-card">

                <div class="storage-title">
                    Document storage
                </div>

                <div class="storage-status">
                    ● STORED SUCCESSFULLY
                </div>

                <div class="storage-path">
                    {file_path}
                </div>

            </div>
            """)


            # ----------------------------------------------------
            # TEXT PREVIEW
            # ----------------------------------------------------

            st.html("""
            <div class="preview-header">

                <div class="preview-title">
                    Extracted Text Preview
                </div>

                <div class="preview-badge">
                    READY FOR ANALYSIS
                </div>

            </div>
            """)


            st.text_area(
                "Extracted document content",
                extracted_text,
                height=420,
                label_visibility="collapsed"
            )


        # ========================================================
        # NO EXTRACTABLE TEXT
        # ========================================================

        else:

            st.error(
                "No extractable text was found in this document."
            )
