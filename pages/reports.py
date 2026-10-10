import streamlit as st

from database.database import (
    get_analyzed_documents,
    get_analysis_details
)
from pages.authenticated_sidebar import show_authenticated_sidebar

# =========================================================
# REPORTS PAGE
# =========================================================

def reports_page():

    # -----------------------------------------------------
    # AUTHENTICATED SIDEBAR
    # -----------------------------------------------------

    show_authenticated_sidebar()

    # -----------------------------------------------------
    # CHECK LOGIN
    # -----------------------------------------------------

    user_id = st.session_state.get("user_id")

    if not user_id:

        st.error(
            "Please log in to access your reports."
        )

        return

    # -----------------------------------------------------
    # PAGE STYLING
    # -----------------------------------------------------

    st.html("""
    <style>

        /* =================================================
           GLOBAL PAGE
        ================================================= */

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at 88% 8%,
                    rgba(83, 126, 218, 0.07),
                    transparent 24%
                ),
                radial-gradient(
                    circle at 4% 55%,
                    rgba(92, 103, 190, 0.045),
                    transparent 25%
                ),
                #f5f7fb !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            padding: 0 52px 60px 52px !important;
            max-width: 1540px !important;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0;
        }


        /* =================================================
           PAGE HEADER
        ================================================= */

        .reports-page {
            margin-top: 0;
            padding-top: 0;
        }

        .reports-header {
            position: relative;

            min-height: 255px;

            margin-left: -52px;
            margin-right: -52px;

            padding: 54px 52px 48px 52px;

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
           HEADER DECORATION
        ------------------------------------------------- */

        .reports-header::before {
            content: "";

            position: absolute;

            width: 270px;
            height: 270px;

            right: 7%;
            top: -145px;

            border-radius: 50%;

            border: 1px solid rgba(255,255,255,.10);

            box-shadow:
                0 0 0 35px rgba(255,255,255,.025),
                0 0 0 70px rgba(255,255,255,.018);
        }

        .reports-header::after {
            content: "";

            position: absolute;

            width: 150px;
            height: 150px;

            right: 20%;
            bottom: -95px;

            border-radius: 50%;

            background:
                rgba(255,255,255,.045);
        }


        /* -------------------------------------------------
           SMALL BLUE ACCENT
        ------------------------------------------------- */

        .reports-header-accent {
            position: absolute;

            left: 52px;
            top: 0;

            width: 72px;
            height: 4px;

            background: #82a9f5;

            border-radius:
                0 0 5px 5px;
        }


        /* -------------------------------------------------
           HEADER CONTENT
        ------------------------------------------------- */

        .reports-header-content {
            position: relative;

            z-index: 2;

            max-width: 850px;
        }

        .reports-kicker {
            color: #a9c7ff;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 1.8px;

            text-transform: uppercase;

            margin-bottom: 9px;
        }

        .reports-title {
            color: #ffffff;

            font-size: 38px;
            font-weight: 800;

            letter-spacing: -0.9px;

            line-height: 1.12;

            margin: 0;
        }

        .reports-description {
            color: rgba(235, 243, 255, .82);

            font-size: 15px;
            line-height: 1.7;

            margin-top: 11px;

            max-width: 700px;
        }


        /* -------------------------------------------------
           REPORT COUNT
        ------------------------------------------------- */

        .reports-count {
            display: inline-flex;

            align-items: center;
            gap: 7px;

            margin-top: 17px;

            padding: 7px 12px;

            border-radius: 7px;

            background: rgba(255,255,255,.10);

            border: 1px solid rgba(255,255,255,.16);

            color: #eaf2ff;

            font-size: 12px;
            font-weight: 700;

            letter-spacing: .15px;

            backdrop-filter: blur(4px);
        }

        .reports-count-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #8fb5ff;

            box-shadow:
                0 0 0 3px rgba(143,181,255,.12);
        }


        /* =================================================
           SECTION
        ================================================= */

        .reports-section {
            margin-top: 38px;
        }

        .reports-section-line {
            height: 1px;

            background: #dfe5ee;

            margin-bottom: 25px;
        }

        .reports-section-heading {
            color: #17294d;

            font-size: 18px;
            line-height: 1.3;

            font-weight: 750;

            margin-bottom: 5px;
        }

        .reports-section-description {
            color: #78869b;

            font-size: 12px;
            line-height: 1.5;

            margin-bottom: 19px;
        }


        /* =================================================
           REPORT CARD
        ================================================= */

        .report-card {
            position: relative;

            min-height: 315px;
            height: 100%;

            padding: 19px;

            background: #ffffff;

            border: 1px solid #dfe6ef;

            border-radius: 10px;

            box-shadow:
                0 6px 20px rgba(34, 65, 112, .045);

            overflow: hidden;

            transition:
                transform .18s ease,
                box-shadow .18s ease,
                border-color .18s ease;
        }

        .report-card::before {
            content: "";

            position: absolute;

            top: 0;
            left: 0;
            right: 0;

            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    #315b9f,
                    #587bd0
                );
        }

        .report-card:hover {
            transform: translateY(-3px);

            border-color: #bdcde8;

            box-shadow:
                0 12px 30px rgba(27, 57, 105, .13);
        }


        /* =================================================
           REPORT STATUS
        ================================================= */

        .report-status {
            display: inline-flex;

            align-items: center;
            gap: 6px;

            padding: 5px 8px;

            border-radius: 5px;

            background: #edf5ef;

            border: 1px solid #d8e8dc;

            color: #477155;

            font-size: 12px;
            font-weight: 700;
        }

        .report-status-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #5d8a69;
        }


        /* =================================================
           DATE
        ================================================= */

        .report-date {
            color: #78869b;

            font-size: 12px;
            line-height: 1.4;

            font-weight: 600;

            margin-top: 9px;
        }


        /* =================================================
           TARGET
        ================================================= */

        .report-target-label {
            color: #78869b;

            font-size: 12px;
            line-height: 1.3;

            font-weight: 700;

            text-transform: uppercase;

            letter-spacing: .35px;

            margin-top: 15px;
        }

        .report-target-name {
            color: #17294d;

            font-size: 15px;
            line-height: 1.4;

            font-weight: 750;

            margin-top: 4px;
            margin-bottom: 13px;

            word-break: break-word;
        }


        /* =================================================
           REFERENCES
        ================================================= */

        .report-reference-label {
            color: #78869b;

            font-size: 12px;
            line-height: 1.3;

            font-weight: 700;

            text-transform: uppercase;

            letter-spacing: .35px;

            margin-bottom: 6px;
        }

        .report-reference-list {
            max-height: 70px;

            overflow-y: auto;

            padding: 8px 9px;

            margin: 5px 0 14px 0;

            background: #f7f9fd;

            border: 1px solid #e2e7ef;

            border-radius: 7px;
        }

        .report-reference-item {
            color: #536176;

            font-size: 12px;
            line-height: 1.45;

            padding: 3px 0;

            word-break: break-word;
        }

        .report-reference-item::before {
            content: "•";

            color: #5278d2;

            font-weight: 800;

            margin-right: 7px;
        }


        /* =================================================
           SCORE ROW
        ================================================= */

        .report-score-row {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 8px;

            margin-top: 13px;
        }

        .report-score-box,
        .report-level-box {
            padding: 11px 12px;

            background: #f7f9fd;

            border: 1px solid #e1e6ee;

            border-radius: 7px;
        }

        .report-score-box {
            background: #edf3ff;

            border-color: #d5e2f8;
        }

        .report-score-number {
            color: #203f79;

            font-size: 18px;
            line-height: 1.1;

            font-weight: 760;
        }

        .report-score-label,
        .report-level-label {
            color: #78869b;

            font-size: 12px;
            line-height: 1.3;

            font-weight: 600;

            margin-top: 4px;
        }

        .report-level-value {
            color: #315b9f;

            font-size: 13px;
            line-height: 1.2;

            font-weight: 750;
        }


        /* =================================================
           EMPTY STATE
        ================================================= */

        .reports-empty {
            padding: 42px 24px;

            background: #f7f9fd;

            border: 1px solid #e1e6ee;

            border-radius: 10px;

            text-align: center;
        }

        .reports-empty-icon {
            font-size: 27px;

            margin-bottom: 8px;
        }

        .reports-empty-title {
            color: #17294d;

            font-size: 16px;

            font-weight: 750;

            margin-bottom: 5px;
        }

        .reports-empty-text {
            color: #78869b;

            font-size: 12px;

            line-height: 1.5;
        }


        /* =================================================
           BUTTON AREA
        ================================================= */

        .report-button-space {
            height: 8px;
        }

    </style>
    """)

    # -----------------------------------------------------
    # GET COMPLETED ANALYSES
    # -----------------------------------------------------

    analyzed_documents = get_analyzed_documents(
        user_id
    )

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    report_count = len(analyzed_documents)

    st.html(f"""
    <div class="reports-page">

        <div class="reports-header">

            <div class="reports-header-accent"></div>

            <div class="reports-header-content">

                <div class="reports-kicker">
                    SCHOLARSHIELD · ACADEMIC REPORTS
                </div>

                <div class="reports-title">
                    Analysis Reports
                </div>

                <div class="reports-description">
                    Review and download your completed academic
                    similarity analysis reports and findings.
                </div>

                <div class="reports-count">

                    <span class="reports-count-dot"></span>

                    {report_count}
                    &nbsp;
                    {"reports" if report_count != 1 else "report"}
                    generated

                </div>

            </div>

        </div>

    </div>
    """)

    # -----------------------------------------------------
    # EMPTY STATE
    # -----------------------------------------------------

    if not analyzed_documents:

        st.html("""
        <div class="reports-empty">

            <div class="reports-empty-icon">
                📄
            </div>

            <div class="reports-empty-title">
                No reports available
            </div>

            <div class="reports-empty-text">
                Complete a document similarity analysis to
                generate your first report.
            </div>

        </div>
        """)

        return

    # -----------------------------------------------------
    # SECTION HEADER
    # -----------------------------------------------------

    st.html("""
    <div class="reports-section">

        <div class="reports-section-line"></div>

        <div class="reports-section-heading">
            Generated Reports
        </div>

        <div class="reports-section-description">
            Completed similarity analyses and their
            generated PDF reports.
        </div>

    </div>
    """)

    # -----------------------------------------------------
    # REPORT CARDS
    # -----------------------------------------------------

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

            reference_documents_text = (
                analysis["reference_documents"]
            )

            overall_score = (
                analysis["overall_score"]
                if analysis["overall_score"] is not None
                else 0
            )

            # -------------------------------------------------
            # SIMILARITY LEVEL
            # -------------------------------------------------

            if overall_score >= 75:

                similarity_level = "High"

            elif overall_score >= 50:

                similarity_level = "Moderate"

            elif overall_score >= 25:

                similarity_level = "Low"

            else:

                similarity_level = "Very Low"

            # -------------------------------------------------
            # REFERENCES
            # -------------------------------------------------

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

            # -------------------------------------------------
            # REFERENCE HTML
            # -------------------------------------------------

            if reference_documents:

                reference_html = "".join(
                    f"""
                    <div class="report-reference-item">
                        {reference_name}
                    </div>
                    """
                    for reference_name
                    in reference_documents
                )

            else:

                reference_html = """
                <div class="report-reference-item">
                    No reference documents
                </div>
                """

            # -------------------------------------------------
            # REPORT CARD
            # -------------------------------------------------

            with columns[index]:

                st.html(f"""
                <div class="report-card">

                    <div class="report-status">

                        <span class="report-status-dot"></span>

                        REPORT GENERATED

                    </div>

                    <div class="report-date">
                        {analysis_date}
                    </div>

                    <div class="report-target-label">
                        ANALYZED DOCUMENT
                    </div>

                    <div class="report-target-name">
                        {filename}
                    </div>

                    <div class="report-reference-label">
                        REFERENCE DOCUMENTS
                    </div>

                    <div class="report-reference-list">
                        {reference_html}
                    </div>

                    <div class="report-score-row">

                        <div class="report-score-box">

                            <div class="report-score-number">
                                {overall_score:.2f}%
                            </div>

                            <div class="report-score-label">
                                OVERALL SIMILARITY
                            </div>

                        </div>

                        <div class="report-level-box">

                            <div class="report-level-value">
                                {similarity_level}
                            </div>

                            <div class="report-level-label">
                                SIMILARITY LEVEL
                            </div>

                        </div>

                    </div>

                </div>
                """)

                # -------------------------------------------------
                # BUTTONS
                # -------------------------------------------------

                details = get_analysis_details(
                    analysis_id,
                    user_id
                )

                if (
                    details
                    and details["report"]
                ):

                    report_path = details[
                        "report"
                    ]["report_path"]

                    try:

                        with open(
                            report_path,
                            "rb"
                        ) as report_file:

                            pdf_data = (
                                report_file.read()
                            )

                        st.download_button(
                            "Download Report",
                            data=pdf_data,
                            file_name=details[
                                "report"
                            ]["report_name"],
                            mime="application/pdf",
                            key=(
                                f"download_report_"
                                f"{analysis_id}"
                            ),
                            use_container_width=True
                        )

                    except FileNotFoundError:

                        st.error(
                            "Report file could "
                            "not be found."
                        )

                else:

                    st.button(
                        "Download Report",
                        disabled=True,
                        key=(
                            f"download_disabled_"
                            f"{analysis_id}"
                        ),
                        use_container_width=True
                    )