import streamlit as st
from database.database import (
    get_not_analyzed_documents,
    get_reference_documents,
    get_analyzed_documents,
    get_analysis_details
)
from pages.authenticated_sidebar import show_authenticated_sidebar


# =========================================================
# ANALYSIS DETAILS POPUP
# =========================================================

@st.dialog("Analysis Details", width="large")
def show_analysis_details_popup(analysis_details):

    if not analysis_details:
        st.error("Analysis details could not be loaded.")
        return

    target = analysis_details["target"]
    results = analysis_details["results"]

    st.html(f"""
    <div class="popup-header">

        <div class="popup-kicker">
            SCHOLARSHIELD · ANALYSIS RESULT
        </div>

        <div class="popup-title">
            {target["filename"]}
        </div>

        <div class="popup-subtitle">
            Analysis completed on {target["analysis_date"]}
        </div>

    </div>
    """)

    # -----------------------------------------------------
    # TARGET DOCUMENT
    # -----------------------------------------------------

    st.html(f"""
    <div class="popup-target-card">

        <div class="popup-card-label">
            ORIGINAL DOCUMENT
        </div>

        <div class="popup-target-name">
            📄 {target["filename"]}
        </div>

        <div class="popup-target-date">
            Analysis completed: {target["analysis_date"]}
        </div>

    </div>
    """)

    # -----------------------------------------------------
    # REFERENCE RESULTS
    # -----------------------------------------------------

    for result in results:

        reference_filename = result["filename"]

        lexical_score = result["lexical_score"] or 0
        semantic_score = result["semantic_score"] or 0
        syntactic_score = result["syntactic_score"] or 0
        contextual_score = result["contextual_score"] or 0
        meaning_score = result["meaning_score"] or 0
        overall_score = result["overall_score"] or 0

        similarity_level = (
            result["similarity_level"]
            or "Unknown"
        )

        st.html(f"""
        <div class="popup-result-card">

            <div class="popup-reference-heading">

                <span class="popup-reference-icon">
                    📄
                </span>

                <div>

                    <div class="popup-reference-label">
                        COMPARED WITH
                    </div>

                    <div class="popup-reference-name">
                        {reference_filename}
                    </div>

                </div>

            </div>

            <div class="popup-score-grid">

                <div class="popup-score-box">
                    <div class="popup-score-value">
                        {lexical_score:.2f}%
                    </div>
                    <div class="popup-score-label">
                        Lexical
                    </div>
                </div>

                <div class="popup-score-box">
                    <div class="popup-score-value">
                        {semantic_score:.2f}%
                    </div>
                    <div class="popup-score-label">
                        Semantic
                    </div>
                </div>

                <div class="popup-score-box">
                    <div class="popup-score-value">
                        {syntactic_score:.2f}%
                    </div>
                    <div class="popup-score-label">
                        Syntactic
                    </div>
                </div>

                <div class="popup-score-box">
                    <div class="popup-score-value">
                        {contextual_score:.2f}%
                    </div>
                    <div class="popup-score-label">
                        Context
                    </div>
                </div>

                <div class="popup-score-box">
                    <div class="popup-score-value">
                        {meaning_score:.2f}%
                    </div>
                    <div class="popup-score-label">
                        Meaning
                    </div>
                </div>

                <div class="popup-score-box popup-overall">
                    <div class="popup-score-value">
                        {overall_score:.2f}%
                    </div>
                    <div class="popup-score-label">
                        Overall
                    </div>
                </div>

                <div class="popup-level-box">
                    <div class="popup-level-value">
                        {similarity_level}
                    </div>
                    <div class="popup-score-label">
                        Similarity Level
                    </div>
                </div>

            </div>

        </div>
        """)

    st.button(
        "Close",
        key="close_analysis_popup",
        use_container_width=True
    )


# =========================================================
# PAGE
# =========================================================

def library_page():

    # -----------------------------------------------------
    # AUTHENTICATION
    # -----------------------------------------------------

    if not st.session_state.get("logged_in", False):

        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.query_params.clear()
        st.rerun()

    # -----------------------------------------------------
    # GLOBAL STYLING
    # -----------------------------------------------------

    st.html("""
    <style>

        /* =================================================
           GLOBAL PAGE
        ================================================= */

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at 92% 4%,
                    rgba(48, 103, 203, 0.075),
                    transparent 27%
                ),
                radial-gradient(
                    circle at 4% 82%,
                    rgba(77, 117, 203, 0.05),
                    transparent 25%
                ),
                #f5f7fb !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            padding: 0 48px 60px 48px !important;
            max-width: 1500px !important;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0;
        }


        /* =================================================
           LIBRARY HEADER / HERO
        ================================================= */

        .library-header {
            position: relative;

            min-height: 255px;

            margin-left: -48px;
            margin-right: -48px;

            padding: 54px 48px 47px 48px;

            overflow: hidden;

            background:
                linear-gradient(
                    118deg,
                    #122b55 0%,
                    #1d4279 48%,
                    #315b9f 100%
                );

            box-shadow:
                0 10px 30px rgba(31, 67, 123, .12);
        }


        /* -------------------------------------------------
           HEADER TOP ACCENT
        ------------------------------------------------- */

        .library-header-accent {
            position: absolute;

            left: 48px;
            top: 0;

            width: 78px;
            height: 4px;

            background: #82a9f5;

            border-radius:
                0 0 5px 5px;
        }


        /* -------------------------------------------------
           DECORATIVE CIRCLES
        ------------------------------------------------- */

        .library-header::before {
            content: "";

            position: absolute;

            width: 285px;
            height: 285px;

            right: 7%;
            top: -150px;

            border-radius: 50%;

            border: 1px solid rgba(255,255,255,.10);

            box-shadow:
                0 0 0 35px rgba(255,255,255,.025),
                0 0 0 70px rgba(255,255,255,.018);
        }

        .library-header::after {
            content: "";

            position: absolute;

            width: 165px;
            height: 165px;

            right: 22%;
            bottom: -105px;

            border-radius: 50%;

            background:
                rgba(255,255,255,.045);
        }


        /* -------------------------------------------------
           HEADER DOT
        ------------------------------------------------- */

        .library-header-dot {
            position: absolute;

            width: 7px;
            height: 7px;

            border-radius: 50%;

            right: 12%;
            top: 61px;

            background: #9abaff;

            box-shadow:
                0 0 18px rgba(154,186,255,.75);
        }


        /* -------------------------------------------------
           HEADER CONTENT
        ------------------------------------------------- */

        .library-header-content {
            position: relative;

            z-index: 3;

            max-width: 820px;
        }

        .library-eyebrow {
            color: #a9c7ff;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 1.8px;

            text-transform: uppercase;

            margin-bottom: 9px;
        }

        .library-title {
            color: #ffffff;

            font-size: 38px;
            font-weight: 800;

            letter-spacing: -0.9px;

            line-height: 1.12;

            margin: 0;
        }

        .library-description {
            color: rgba(235, 243, 255, .84);

            font-size: 15px;
            line-height: 1.7;

            margin-top: 11px;

            max-width: 710px;
        }


        /* -------------------------------------------------
           LIBRARY COUNT
        ------------------------------------------------- */

        .library-count {
            display: inline-flex;

            align-items: center;
            gap: 7px;

            margin-top: 17px;

            padding: 7px 12px;

            border-radius: 7px;

            background:
                rgba(255,255,255,.10);

            border:
                1px solid rgba(255,255,255,.16);

            color: #eaf2ff;

            font-size: 12px;
            font-weight: 700;

            letter-spacing: .15px;

            backdrop-filter: blur(4px);
        }

        .library-count-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #8fb5ff;

            box-shadow:
                0 0 0 3px rgba(143,181,255,.12);
        }

        /* =================================================
           SUMMARY
        ================================================= */

        .summary-area {
            display: flex;

            gap: 12px;

            margin-top: 18px;
        }

        .summary-box {
            background: #ffffff;

            border:
                1px solid #dfe6f0;

            border-radius: 11px;

            padding: 15px 20px;

            min-width: 165px;

            box-shadow:
                0 5px 16px rgba(35, 62, 104, 0.045);

            position: relative;

            overflow: hidden;
        }

        .summary-box::before {
            content: "";

            position: absolute;

            left: 0;
            top: 0;
            bottom: 0;

            width: 4px;

            background: #5278d2;
        }

        .summary-number {
            color: #20375e;

            font-size: 25px;
            font-weight: 800;

            line-height: 1;
        }

        .summary-label {
            color: #718097;

            font-size: 12px;
            font-weight: 800;

            letter-spacing: 0.6px;

            text-transform: uppercase;

            margin-top: 7px;
        }


        /* =================================================
           SECTION
        ================================================= */

        .section-header {
            margin-top: 35px;
            margin-bottom: 15px;
        }

        .section-title-line {
            display: flex;

            align-items: center;

            gap: 9px;
        }

        .section-title {
            color: #1a2e51;

            font-size: 20px;
            font-weight: 800;

            letter-spacing: -0.2px;
        }

        .section-count {
            background: #e9f0ff;

            color: #4b70bd;

            border-radius: 6px;

            padding: 4px 8px;

            font-size: 12px;
            font-weight: 800;
        }

        .section-description {
            color: #718097;

            font-size: 12px;
            line-height: 1.55;

            margin-top: 5px;
        }


        /* =================================================
           SEGMENTED CONTROL
        ================================================= */

        .document-view-switch {
            margin-top: 18px;
            margin-bottom: 20px;
        }

        div[data-testid="stSegmentedControl"] {
            background: #edf2fa !important;

            border:
                1px solid #dce4f0 !important;

            border-radius: 10px !important;

            padding: 4px !important;
        }

        div[data-testid="stSegmentedControl"] button {
            color: #64748b !important;

            font-size: 12px !important;
            font-weight: 750 !important;

            min-height: 36px !important;
        }

        div[data-testid="stSegmentedControl"]
        button[aria-checked="true"] {
            background: #ffffff !important;

            color: #4168b0 !important;

            border-radius: 7px !important;

            box-shadow:
                0 2px 7px rgba(35, 62, 104, 0.08) !important;
        }


        /* =================================================
           DOCUMENT CARDS
        ================================================= */

        .document-card {
            min-height: 250px;

            padding: 21px;

            background: #ffffff;

            border:
                1px solid #dfe5ef;

            border-radius: 13px;

            box-shadow:
                0 5px 18px rgba(35, 62, 104, 0.045);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;

            display: flex;

            flex-direction: column;

            position: relative;

            overflow: hidden;
        }

        .document-card::before {
            content: "";

            position: absolute;

            left: 0;
            top: 0;

            width: 100%;
            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    #315b9f,
                    #6e8fd5
                );
        }

        .document-card:hover {
            transform: translateY(-3px);

            border-color: #bdcde8;

            box-shadow:
                0 12px 28px rgba(35, 62, 104, 0.09);
        }


        /* =================================================
           FILE TOP
        ================================================= */

        .file-top {
            display: flex;

            justify-content: space-between;

            align-items: flex-start;
        }

        .file-icon {
            width: 48px;
            height: 48px;

            border-radius: 11px;

            background: #edf3ff;

            border:
                1px solid #dce7fb;

            display: flex;

            align-items: center;
            justify-content: center;

            font-size: 21px;
        }

        .file-type {
            padding: 5px 8px;

            border-radius: 6px;

            background: #f3f6fa;

            color: #718097;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.5px;
        }

        .file-name {
            color: #1b3157;

            font-size: 14px;
            font-weight: 800;

            line-height: 1.4;

            margin-top: 17px;

            min-height: 39px;

            word-break: break-word;
        }

        .file-meta {
            color: #8995a7;

            font-size: 12px;
            line-height: 1.55;

            margin-top: 7px;
        }

        .ready-badge {
            display: inline-flex;

            align-items: center;

            gap: 6px;

            width: fit-content;

            margin-top: 14px;

            padding: 6px 9px;

            border-radius: 6px;

            background: #eef5ff;

            color: #5578bf;

            font-size: 12px;

            font-weight: 800;
        }

        .ready-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #5f83c9;
        }


        /* =================================================
           REFERENCE DETAILS
        ================================================= */

        .reference-label {
            color: #7c8aa0;

            font-size: 12px;
            font-weight: 800;

            letter-spacing: 0.8px;

            margin-top: 14px;
            margin-bottom: 7px;
        }

        .reference-targets {
            max-height: 65px;

            overflow-y: auto;
        }

        .reference-target {
            color: #4168b0;

            background: #f3f6fc;

            border:
                1px solid #e1e8f4;

            border-radius: 6px;

            padding: 6px 8px;

            font-size: 12px;
            font-weight: 700;

            margin-bottom: 5px;

            word-break: break-word;
        }


        /* =================================================
           STREAMLIT BUTTONS
        ================================================= */

        div.stButton {
            margin-top: 10px;
        }

        div.stButton > button {
            min-height: 40px !important;

            border-radius: 8px !important;

            border:
                1px solid #d0dcef !important;

            background: #f8faff !important;

            color: #4168b0 !important;

            font-size: 12px !important;
            font-weight: 800 !important;

            transition:
                all 0.18s ease !important;
        }

        div.stButton > button:hover {
            background: #4775c9 !important;

            border-color: #4775c9 !important;

            color: #ffffff !important;

            transform: translateY(-1px);

            box-shadow:
                0 5px 14px rgba(65, 105, 181, 0.18);
        }


        /* =================================================
           DOWNLOAD BUTTON
        ================================================= */

        div[data-testid="stDownloadButton"] {
            margin-top: 8px;
        }

        div[data-testid="stDownloadButton"] > button {
            min-height: 40px !important;

            border-radius: 8px !important;

            border:
                1px solid #d0dcef !important;

            background: #203f79 !important;

            color: #ffffff !important;

            font-size: 12px !important;
            font-weight: 800 !important;

            transition:
                all 0.18s ease !important;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            background: #315b9f !important;

            border-color: #315b9f !important;

            box-shadow:
                0 5px 14px rgba(65, 105, 181, 0.18);
        }


        /* =================================================
           EMPTY STATE
        ================================================= */

        .empty-state {
            padding: 48px 20px;

            text-align: center;

            background: #ffffff;

            border:
                1px dashed #cbd6e6;

            border-radius: 13px;
        }

        .empty-icon {
            width: 52px;
            height: 52px;

            border-radius: 13px;

            background: #edf3fc;

            display: flex;

            align-items: center;
            justify-content: center;

            margin:
                0 auto 14px auto;

            font-size: 21px;
        }

        .empty-title {
            color: #273b5d;

            font-size: 15px;

            font-weight: 800;
        }

        .empty-text {
            color: #8793a6;

            font-size: 12px;

            line-height: 1.6;

            max-width: 430px;

            margin:
                7px auto 0 auto;
        }


        /* =================================================
           ANALYZED SECTION
        ================================================= */

        .future-section {
            margin-top: 44px;

            padding-top: 2px;
        }

        .future-line {
            height: 1px;

            background: #e1e6ee;

            margin-bottom: 31px;
        }


        /* =================================================
           ANALYZED CARD
        ================================================= */

        .analyzed-card {
            min-height: 270px;

            padding: 18px;

            background: #ffffff;

            border:
                1px solid #dfe5ef;

            border-radius: 11px;

            box-shadow:
                0 6px 20px rgba(34, 65, 112, 0.045);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;

            position: relative;

            overflow: hidden;
        }

        .analyzed-card::before {
            content: "";

            position: absolute;

            left: 0;
            top: 0;

            width: 100%;
            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    #315b9f,
                    #6e8fd5
                );
        }

        .analyzed-card:hover {
            transform: translateY(-3px);

            border-color: #bdcde8;

            box-shadow:
                0 12px 30px rgba(27, 57, 105, 0.13);
        }


        /* =================================================
           ANALYZED STATUS
        ================================================= */

        .analyzed-status {
            display: inline-flex;

            align-items: center;

            gap: 6px;

            padding: 6px 9px;

            border-radius: 6px;

            background: #eef5ff;

            color: #5578bf;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.6px;
        }

        .analyzed-status-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #5f83c9;
        }


        /* =================================================
           DATE
        ================================================= */

        .analysis-date {
            color: #8995a7;

            font-size: 12px;

            font-weight: 600;

            margin-top: 10px;
        }


        /* =================================================
           TARGET
        ================================================= */

        .analyzed-target-label {
            color: #7c8aa0;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.8px;

            margin-top: 14px;
        }

        .analyzed-target-name {
            color: #1b3157;

            font-size: 15px;

            font-weight: 800;

            line-height: 1.4;

            margin-top: 5px;

            word-break: break-word;
        }


        /* =================================================
           REFERENCES
        ================================================= */

        .analyzed-reference-label {
            color: #7c8aa0;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.8px;

            margin-top: 14px;

            margin-bottom: 7px;
        }

        .analyzed-reference-list {
            max-height: 65px;

            overflow-y: auto;
        }

        .analyzed-reference-item {
            color: #4168b0;

            background: #f3f6fc;

            border:
                1px solid #e1e8f4;

            border-radius: 6px;

            padding: 6px 8px;

            font-size: 12px;

            font-weight: 700;

            margin-bottom: 5px;

            word-break: break-word;
        }


        /* =================================================
           SCORE ROW
        ================================================= */

        .analysis-score-row {
            display: flex;

            gap: 9px;

            margin-top: 15px;
        }

        .analysis-score-box,
        .analysis-level {
            flex: 1;

            padding: 10px 11px;

            background: #f8faff;

            border:
                1px solid #e3e9f4;

            border-radius: 8px;
        }

        .analysis-score-box {
            background: #edf3ff;

            border-color: #d5e2f8;
        }

        .analysis-score-number {
            color: #294a82;

            font-size: 18px;

            font-weight: 850;

            line-height: 1;
        }

        .analysis-score-label,
        .analysis-level-label {
            color: #8995a7;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.4px;

            margin-top: 5px;
        }

        .analysis-level-value {
            color: #294a82;

            font-size: 13px;

            font-weight: 850;

            line-height: 1;
        }


        /* =================================================
           POPUP STYLING
        ================================================= */

        [data-testid="stDialog"] {
            border-radius: 18px !important;
        }

        [data-testid="stDialog"] > div {
            background: #f5f7fb !important;
        }

        .popup-header {
            padding: 2px 2px 17px 2px;

            border-bottom:
                1px solid #dfe6ef;
        }

        .popup-kicker {
            color: #5278d2;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 1.4px;

            text-transform: uppercase;
        }

        .popup-title {
            color: #172b50;

            font-size: 22px;

            font-weight: 800;

            line-height: 1.3;

            margin-top: 7px;

            word-break: break-word;
        }

        .popup-subtitle {
            color: #718097;

            font-size: 12px;

            margin-top: 5px;
        }

        .popup-target-card {
            margin-top: 16px;

            padding: 16px;

            background: #ffffff;

            border:
                1px solid #dfe5ef;

            border-radius: 11px;

            box-shadow:
                0 4px 14px rgba(35, 62, 104, 0.035);
        }

        .popup-card-label {
            color: #7c8aa0;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.7px;
        }

        .popup-target-name {
            color: #1b3157;

            font-size: 15px;

            font-weight: 800;

            margin-top: 7px;

            word-break: break-word;
        }

        .popup-target-date {
            color: #8995a7;

            font-size: 12px;

            margin-top: 5px;
        }

        .popup-result-card {
            margin-top: 14px;

            padding: 17px;

            background: #ffffff;

            border:
                1px solid #dfe5ef;

            border-radius: 11px;

            box-shadow:
                0 4px 14px rgba(35, 62, 104, 0.035);
        }

        .popup-reference-heading {
            display: flex;

            align-items: center;

            gap: 10px;
        }

        .popup-reference-icon {
            width: 36px;
            height: 36px;

            display: flex;

            align-items: center;
            justify-content: center;

            background: #edf3ff;

            border:
                1px solid #dce7fb;

            border-radius: 8px;

            font-size: 17px;
        }

        .popup-reference-label {
            color: #7c8aa0;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.7px;
        }

        .popup-reference-name {
            color: #1b3157;

            font-size: 14px;

            font-weight: 800;

            margin-top: 3px;

            word-break: break-word;
        }

        .popup-score-grid {
            display: grid;

            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 8px;

            margin-top: 15px;
        }

        .popup-score-box,
        .popup-level-box {
            padding: 12px;

            background: #f7f9fd;

            border:
                1px solid #e2e8f2;

            border-radius: 8px;
        }

        .popup-overall {
            background: #edf3ff;

            border-color: #d3e0f7;
        }

        .popup-level-box {
            background: #f1f5fc;

            border-color: #d7e1ef;
        }

        .popup-score-value {
            color: #294a82;

            font-size: 16px;

            font-weight: 850;

            line-height: 1.1;

            word-break: break-word;
        }

        .popup-level-value {
            color: #315b9f;

            font-size: 14px;

            font-weight: 850;

            line-height: 1.1;

            word-break: break-word;
        }

        .popup-score-label {
            color: #7d899c;

            font-size: 12px;

            font-weight: 750;

            margin-top: 5px;
        }


        /* =================================================
           SCROLLBARS
        ================================================= */

        .reference-targets::-webkit-scrollbar,
        .analyzed-reference-list::-webkit-scrollbar {
            width: 5px;
        }

        .reference-targets::-webkit-scrollbar-thumb,
        .analyzed-reference-list::-webkit-scrollbar-thumb {
            background: #c5d1e4;

            border-radius: 10px;
        }


        /* =================================================
           RESPONSIVE
        ================================================= */

        @media (max-width: 900px) {

            .block-container {
                padding:
                    0 25px 50px 25px !important;
            }

            .library-header {
                margin-left: -25px;
                margin-right: -25px;

                padding-left: 25px;
                padding-right: 25px;
            }

            .library-header-accent {
                left: 25px;
            }

            .library-title {
                font-size: 31px;
            }

            .workflow-panel {
                padding: 25px;
            }

            .popup-score-grid {
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }
        }


        @media (max-width: 600px) {

            .block-container {
                padding:
                    0 16px 40px 16px !important;
            }

            .library-header {
                margin-left: -16px;
                margin-right: -16px;

                padding:
                    38px 16px 38px 16px;
            }

            .library-header-accent {
                left: 16px;
            }

            .library-title {
                font-size: 28px;
            }

            .library-description {
                font-size: 13px;
            }

            .workflow-title {
                font-size: 20px;
            }

            .workflow-text {
                font-size: 13px;
            }

            .popup-score-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

    </style>
    """)

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    show_authenticated_sidebar()

    # -----------------------------------------------------
    # GET DOCUMENTS
    # -----------------------------------------------------

    documents = get_not_analyzed_documents(
        user_id
    )

    reference_documents = get_reference_documents(
        user_id
    )

    analyzed_documents = get_analyzed_documents(
        user_id
    )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    total_library_documents = (
        len(documents)
        + len(reference_documents)
        + len(analyzed_documents)
    )

    st.html(f"""
    <div class="library-header">

        <div class="library-header-accent"></div>

        <div class="library-header-dot"></div>

        <div class="library-header-content">

            <div class="library-eyebrow">
                SCHOLARSHIELD · DOCUMENT WORKSPACE
            </div>

            <div class="library-title">
                My Library
            </div>

            <div class="library-description">
                Manage your academic documents and move them
                through the ScholarShield similarity-analysis
                workflow.
            </div>

            <div class="library-count">

                <span class="library-count-dot"></span>

                {total_library_documents}
                &nbsp;
                {"documents" if total_library_documents != 1 else "document"}
                in your library

            </div>

        </div>

    </div>
    """)

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    st.html(f"""
    <div class="summary-area">

        <div class="summary-box">

            <div class="summary-number">
                {len(documents)}
            </div>

            <div class="summary-label">
                Yet to Analyze
            </div>

        </div>

    </div>
    """)

    # -----------------------------------------------------
    # YET TO ANALYZE
    # -----------------------------------------------------

    st.html("""
    <div class="section-header">

        <div class="section-title-line">

            <div class="section-title">
                Yet to Analyze
            </div>

        </div>

        <div class="section-description">
            Manage documents waiting to be analyzed or documents
            that have already been used as references.
        </div>

    </div>
    """)

    # -----------------------------------------------------
    # DOCUMENT VIEW SWITCH
    # -----------------------------------------------------

    document_view = st.segmented_control(
        "Document view",
        [
            "My Documents",
            "Reference Documents"
        ],
        default="My Documents",
        key="library_document_view",
        label_visibility="collapsed"
    )

    # -----------------------------------------------------
    # SELECT CURRENT DOCUMENT LIST
    # -----------------------------------------------------

    if document_view == "Reference Documents":

        display_documents = reference_documents

    else:

        display_documents = documents

    # -----------------------------------------------------
    # EMPTY STATE
    # -----------------------------------------------------

    if not display_documents:

        if document_view == "Reference Documents":

            st.html("""
            <div class="empty-state">

                <div class="empty-icon">
                    🔗
                </div>

                <div class="empty-title">
                    No reference documents yet
                </div>

                <div class="empty-text">
                    Documents used as references during similarity
                    analysis will appear here for easy tracking.
                </div>

            </div>
            """)

        else:

            st.html("""
            <div class="empty-state">

                <div class="empty-icon">
                    📄
                </div>

                <div class="empty-title">
                    No documents waiting for analysis
                </div>

                <div class="empty-text">
                    Upload a PDF, DOCX, or TXT academic document
                    and it will appear here when ready.
                </div>

            </div>
            """)

    else:

        # -------------------------------------------------
        # CARD GRID
        # -------------------------------------------------

        for start in range(
            0,
            len(display_documents),
            3
        ):

            row_documents = display_documents[
                start:start + 3
            ]

            columns = st.columns(
                3,
                gap="medium"
            )

            for index, document in enumerate(
                row_documents
            ):

                document_id = document["id"]
                filename = document["filename"]
                file_type = document["file_type"]
                word_count = document["word_count"]
                uploaded_at = document["uploaded_at"]

                with columns[index]:

                    # =====================================
                    # MY DOCUMENT CARD
                    # =====================================

                    if document_view == "My Documents":

                        st.html(f"""
                        <div class="document-card">

                            <div class="file-top">

                                <div class="file-icon">
                                    📄
                                </div>

                                <div class="file-type">
                                    {file_type}
                                </div>

                            </div>

                            <div class="file-name">
                                {filename}
                            </div>

                            <div class="file-meta">
                                {word_count:,} words
                                <br>
                                Uploaded {uploaded_at}
                            </div>

                            <div class="ready-badge">
                                <span class="ready-dot"></span>
                                READY FOR ANALYSIS
                            </div>

                        </div>
                        """)

                        if st.button(
                            "Analyze Document  →",
                            key=f"analyze_{document_id}",
                            use_container_width=True
                        ):

                            st.session_state.selected_document_id = (
                                document_id
                            )

                            st.session_state.open_analysis_request = True

                            st.session_state.analysis_from_library = True

                            st.session_state.pop(
                                "analysis_target_selector",
                                None
                            )

                            st.rerun()

                    # =====================================
                    # REFERENCE DOCUMENT CARD
                    # =====================================

                    else:

                        used_against = document["used_against"]

                        if used_against:

                            target_documents = [
                                name.strip()
                                for name in used_against.split(
                                    "|||"
                                )
                                if name.strip()
                            ]

                        else:

                            target_documents = []

                        target_count = len(
                            target_documents
                        )

                        if target_count == 1:

                            target_display = f"""
                            <div class="reference-target">
                                📄 {target_documents[0]}
                            </div>
                            """

                        elif target_count > 1:

                            target_items = "".join(
                                f"""
                                <div class="reference-target">
                                    📄 {name}
                                </div>
                                """
                                for name in target_documents
                            )

                            target_display = target_items

                        else:

                            target_display = """
                            <div class="reference-target">
                                No target document recorded
                            </div>
                            """

                        st.html(f"""
                        <div class="document-card">

                            <div class="file-top">

                                <div class="file-icon">
                                    🔗
                                </div>

                                <div class="file-type">
                                    {file_type}
                                </div>

                            </div>

                            <div class="file-name">
                                {filename}
                            </div>

                            <div class="file-meta">
                                {word_count:,} words
                                <br>
                                Uploaded {uploaded_at}
                            </div>

                            <div class="reference-label">
                                USED AS REFERENCE AGAINST
                            </div>

                            <div class="reference-targets">
                                {target_display}
                            </div>

                        </div>
                        """)

                        if st.button(
                            "Analyze as Target  →",
                            key=f"reference_analyze_{document_id}",
                            use_container_width=True
                        ):

                            st.session_state.selected_document_id = (
                                document_id
                            )

                            st.session_state.open_analysis_request = True

                            st.session_state.analysis_from_library = True

                            st.session_state.pop(
                                "analysis_target_selector",
                                None
                            )

                            st.rerun()

    # -----------------------------------------------------
    # ANALYZED DOCUMENTS
    # -----------------------------------------------------

    st.html("""
    <div class="future-section">

        <div class="future-line"></div>

        <div class="section-header">

            <div class="section-title-line">

                <div class="section-title">
                    Analyzed Documents
                </div>

                <div class="section-count">
                    COMPLETED
                </div>

            </div>

            <div class="section-description">
                Completed analysis sessions with their reference
                documents, similarity results, and generated reports.
            </div>

        </div>

    </div>
    """)

    # =====================================================
    # NO ANALYSES
    # =====================================================

    if not analyzed_documents:

        st.html("""
        <div class="empty-state">

            <div class="empty-icon">
                ✓
            </div>

            <div class="empty-title">
                No completed analyses yet
            </div>

            <div class="empty-text">
                Once you complete a similarity analysis,
                the target document, reference documents,
                results, and generated report will appear here.
            </div>

        </div>
        """)

    # =====================================================
    # ANALYZED DOCUMENT CARDS
    # =====================================================

    else:

        for start in range(
            0,
            len(analyzed_documents),
            3
        ):

            row_analyses = analyzed_documents[
                start:start + 3
            ]

            columns = st.columns(
                3,
                gap="medium"
            )

            for index, analysis in enumerate(
                row_analyses
            ):

                analysis_id = analysis[
                    "analysis_id"
                ]

                filename = analysis[
                    "filename"
                ]

                analysis_date = analysis[
                    "analysis_date"
                ]

                reference_documents_text = analysis[
                    "reference_documents"
                ]

                overall_score = (
                    analysis["overall_score"]
                    if analysis["overall_score"] is not None
                    else 0
                )

                # -----------------------------------------
                # SIMILARITY LEVEL
                # -----------------------------------------

                if overall_score >= 75:

                    similarity_level = "High"

                elif overall_score >= 50:

                    similarity_level = "Moderate"

                elif overall_score >= 25:

                    similarity_level = "Low"

                else:

                    similarity_level = "Very Low"

                # -----------------------------------------
                # REFERENCE DOCUMENTS
                # -----------------------------------------

                if reference_documents_text:

                    reference_documents = [
                        name.strip()
                        for name in
                        reference_documents_text.split(
                            "|||"
                        )
                        if name.strip()
                    ]

                else:

                    reference_documents = []

                with columns[index]:

                    if reference_documents:

                        reference_html = "".join(
                            f"""
                            <div class="analyzed-reference-item">
                                📄 {reference_name}
                            </div>
                            """
                            for reference_name
                            in reference_documents
                        )

                    else:

                        reference_html = """
                        <div class="analyzed-reference-item">
                            No reference documents
                        </div>
                        """

                    # -------------------------------------
                    # COMPLETE ANALYZED CARD
                    # -------------------------------------

                    st.html(f"""
                    <div class="analyzed-card">

                        <div class="analyzed-status">
                            <span class="analyzed-status-dot"></span>
                            ANALYSIS COMPLETED
                        </div>

                        <div class="analysis-date">
                            {analysis_date}
                        </div>

                        <div class="analyzed-target-label">
                            ANALYZED DOCUMENT
                        </div>

                        <div class="analyzed-target-name">
                            {filename}
                        </div>

                        <div class="analyzed-reference-label">
                            REFERENCE DOCUMENTS
                        </div>

                        <div class="analyzed-reference-list">
                            {reference_html}
                        </div>

                        <div class="analysis-score-row">

                            <div class="analysis-score-box">

                                <div class="analysis-score-number">
                                    {overall_score:.2f}%
                                </div>

                                <div class="analysis-score-label">
                                    OVERALL SIMILARITY
                                </div>

                            </div>

                            <div class="analysis-level">

                                <div class="analysis-level-value">
                                    {similarity_level}
                                </div>

                                <div class="analysis-level-label">
                                    SIMILARITY LEVEL
                                </div>

                            </div>

                        </div>

                    </div>
                    """)

                    # -------------------------------------
                    # VIEW ANALYSIS
                    # -------------------------------------

                    if st.button(
                        "View Analysis  →",
                        key=f"view_analysis_{analysis_id}",
                        use_container_width=True
                    ):

                        analysis_details = get_analysis_details(
                            analysis_id,
                            user_id
                        )

                        show_analysis_details_popup(
                            analysis_details
                        )

                    # -------------------------------------
                    # VIEW / DOWNLOAD REPORT
                    # -------------------------------------

                    analysis_details = get_analysis_details(
                        analysis_id,
                        user_id
                    )

                    report = (
                        analysis_details["report"]
                        if analysis_details
                        else None
                    )

                    if report:

                        report_path = report[
                            "report_path"
                        ]

                        try:

                            with open(
                                report_path,
                                "rb"
                            ) as report_file:

                                report_bytes = (
                                    report_file.read()
                                )

                            st.download_button(
                                "View / Download Report  ↓",
                                data=report_bytes,
                                file_name=report["report_name"],
                                mime="application/pdf",
                                key=f"report_{analysis_id}",
                                use_container_width=True
                            )

                        except FileNotFoundError:

                            st.button(
                                "Report unavailable",
                                key=f"missing_report_{analysis_id}",
                                disabled=True,
                                use_container_width=True
                            )