import streamlit as st
from pathlib import Path
from datetime import datetime
from html import escape

from pages.upload import show_upload
from pages.authenticated_sidebar import show_authenticated_sidebar

from database.database import (
    get_dashboard_stats,
    get_dashboard_similarity_trend,
    get_pending_analysis_documents,
    get_analyzed_documents
)


# =========================================================
# BASE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"


# =========================================================
# HELPERS
# =========================================================

def format_percentage(value):

    if value is None:
        return "—"

    return f"{float(value):.0f}%"


def format_analysis_date(date_value):

    if not date_value:
        return "Unknown date"

    try:

        date_obj = datetime.strptime(
            str(date_value),
            "%Y-%m-%d %H:%M:%S"
        )

        today = datetime.now().date()

        if date_obj.date() == today:
            return "Today"

        if (today - date_obj.date()).days == 1:
            return "Yesterday"

        return date_obj.strftime("%d %b %Y")

    except (ValueError, TypeError):

        return str(date_value)


def get_similarity_level(score):

    if score is None:
        return "No score"

    score = float(score)

    if score >= 70:
        return "High"

    if score >= 40:
        return "Moderate"

    return "Low"


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    if not st.session_state.get("logged_in", False):

        st.warning("Please log in to access the dashboard.")
        return


    # =====================================================
    # USER INFORMATION
    # =====================================================

    user_name = st.session_state.get(
        "user_name",
        "User"
    )

    user_email = st.session_state.get(
        "user_email",
        ""
    )

    user_id = st.session_state.get(
        "user_id"
    )


    if not user_id:

        st.error("User session could not be loaded.")
        return


    # =====================================================
    # LOAD DYNAMIC DATA
    # =====================================================

    dashboard_stats = get_dashboard_stats(
        user_id
    )

    trend_data = get_dashboard_similarity_trend(
        user_id,
        limit=7
    )

    pending_documents = get_pending_analysis_documents(
        user_id,
        limit=5
    )

    recent_analyses = get_analyzed_documents(
        user_id
    )[:5]


    # =====================================================
    # SIDEBAR
    # =====================================================

    show_authenticated_sidebar()


    # =====================================================
    # PAGE STYLING
    # =====================================================

    st.html("""
    <style>

        /* ====================================================
           GLOBAL
           ==================================================== */

        [data-testid="stAppViewContainer"] {

            background:
                radial-gradient(
                    circle at 90% 0%,
                    rgba(71, 112, 194, 0.11),
                    transparent 23%
                ),

                radial-gradient(
                    circle at 0% 48%,
                    rgba(89, 112, 184, 0.065),
                    transparent 25%
                ),

                linear-gradient(
                    180deg,
                    #f7f9fc 0%,
                    #f4f7fb 100%
                ) !important;
        }


        [data-testid="stHeader"] {
            background: transparent !important;
        }


        .block-container {

            padding:
                30px 52px 65px 52px !important;

            max-width: 1540px !important;
        }


        div[data-testid="stVerticalBlock"] {
            gap: 0;
        }

        /* ====================================================
           TOP HEADER
           ==================================================== */

        .dashboard-header {

            display: flex;

            justify-content:
                space-between;

            align-items:
                flex-start;

            gap: 30px;

            position: relative;
        }


        .header-content {

            position: relative;

            padding-left: 2px;
        }


        .dashboard-label {

            color:
                #5579cf;

            font-size:
                11px;

            font-weight:
                800;

            letter-spacing:
                2px;

            text-transform:
                uppercase;

            margin-bottom:
                8px;
        }


        .dashboard-title {

            color:
                #12264b;

            font-size:
                40px;

            font-weight:
                850;

            letter-spacing:
                -1.2px;

            line-height:
                1.08;

            margin:
                0;
        }


        .dashboard-title span {

            color:
                #4f73c8;
        }


        .dashboard-description {

            color:
                #65748c;

            font-size:
                15px;

            line-height:
                1.7;

            margin-top:
                11px;

            max-width:
                720px;
        }


        .header-status {

            display: flex;

            align-items:
                center;

            gap: 8px;

            padding:
                9px 13px;

            border-radius:
                10px;

            background:
                rgba(255,255,255,0.78);

            border:
                1px solid #dce4f0;

            box-shadow:
                0 5px 18px
                rgba(34, 65, 112, 0.045);

            color:
                #52647f;

            font-size:
                11px;

            font-weight:
                700;

            white-space:
                nowrap;
        }


        .status-dot {

            width: 7px;
            height: 7px;

            border-radius:
                50%;

            background:
                #4f9c79;

            box-shadow:
                0 0 0 4px
                rgba(79,156,121,0.10);
        }


        /* ====================================================
           HEADER DECORATION
           ==================================================== */

        .header-decoration {

            position:
                absolute;

            right:
                4%;

            top:
                -35px;

            width:
                155px;

            height:
                155px;

            border-radius:
                50%;

            border:
                1px solid
                rgba(77,113,188,0.10);

            pointer-events:
                none;
        }


        .header-decoration::before {

            content: "";

            position:
                absolute;

            inset:
                22px;

            border-radius:
                50%;

            border:
                1px solid
                rgba(77,113,188,0.08);
        }


        .header-decoration::after {

            content: "";

            position:
                absolute;

            width:
                6px;

            height:
                6px;

            border-radius:
                50%;

            background:
                #7697df;

            top:
                40px;

            right:
                22px;

            box-shadow:
                0 0 14px
                rgba(118,151,223,0.65);
        }


        /* ====================================================
           WELCOME HERO
           ==================================================== */

        .welcome-card {

            margin-top:
                30px;

            min-height:
                205px;

            padding:
                31px 34px;

            border-radius:
                21px;

            background:
                linear-gradient(
                    120deg,
                    #102952 0%,
                    #183968 43%,
                    #2b4f8e 72%,
                    #4464a2 100%
                );

            box-shadow:
                0 20px 45px
                rgba(27,57,105,0.17);

            position:
                relative;

            overflow:
                hidden;
        }


        .welcome-card::after {

            content: "";

            position:
                absolute;

            width:
                330px;

            height:
                330px;

            right:
                -125px;

            top:
                -185px;

            border-radius:
                50%;

            border:
                1px solid
                rgba(255,255,255,0.10);
        }


        .welcome-grid {

            position:
                relative;

            z-index:
                3;

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                center;

            gap:
                35px;
        }


        .welcome-eyebrow {

            color:
                #a8c1f1;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1.7px;

            text-transform:
                uppercase;

            margin-bottom:
                9px;
        }


        .welcome-title {

            color:
                #ffffff;

            font-size:
                26px;

            font-weight:
                800;

            line-height:
                1.2;

            margin-bottom:
                9px;

            letter-spacing:
                -0.4px;
        }


        .welcome-text {

            color:
                #d9e5f7;

            font-size:
                13.5px;

            line-height:
                1.75;

            max-width:
                710px;
        }


        .welcome-right {

            min-width:
                195px;

            display:
                flex;

            flex-direction:
                column;

            align-items:
                flex-end;

            gap:
                11px;
        }


        .welcome-badge {

            display:
                flex;

            align-items:
                center;

            gap:
                8px;

            padding:
                10px 13px;

            border-radius:
                10px;

            background:
                rgba(255,255,255,0.10);

            border:
                1px solid
                rgba(255,255,255,0.14);

            color:
                #e8f0ff;

            font-size:
                11px;

            font-weight:
                650;

            backdrop-filter:
                blur(8px);
        }


        .welcome-mini-stat {

            color:
                #c9d9f3;

            font-size:
                10.5px;

            text-align:
                right;

            line-height:
                1.6;
        }


        .welcome-mini-stat strong {

            color:
                #ffffff;

            font-size:
                17px;
        }


        .welcome-decoration-one {

            position:
                absolute;

            width:
                280px;

            height:
                280px;

            border:
                1px solid
                rgba(255,255,255,0.07);

            border-radius:
                50%;

            right:
                -95px;

            bottom:
                -190px;
        }


        .welcome-decoration-two {

            position:
                absolute;

            width:
                160px;

            height:
                160px;

            border:
                1px solid
                rgba(255,255,255,0.055);

            border-radius:
                50%;

            right:
                175px;

            top:
                -115px;
        }


        .welcome-dot {

            position:
                absolute;

            width:
                7px;

            height:
                7px;

            border-radius:
                50%;

            background:
                #b5ccff;

            right:
                120px;

            top:
                48px;

            box-shadow:
                0 0 18px
                rgba(169,196,255,0.75);
        }


        /* ====================================================
           SECTION HEADINGS
           ==================================================== */

        .section-block {

            margin-top:
                37px;

            margin-bottom:
                16px;
        }


        .section-heading-row {

            display:
                flex;

            align-items:
                flex-end;

            justify-content:
                space-between;

            gap:
                20px;
        }


        .section-heading {

            color:
                #17294d;

            font-size:
                20px;

            font-weight:
                800;

            letter-spacing:
                -0.3px;
        }


        .section-subheading {

            color:
                #78869b;

            font-size:
                12.5px;

            margin-top:
                4px;
        }


        .section-accent {

            width:
                42px;

            height:
                3px;

            border-radius:
                10px;

            background:
                linear-gradient(
                    90deg,
                    #426dc1,
                    #8ca8e6
                );

            margin-top:
                8px;
        }


        /* ====================================================
           KPI AREA
           ==================================================== */

        .kpi-wrapper {

            position:
                relative;
        }


        .kpi-card {

            position:
                relative;

            min-height:
                155px;

            padding:
                21px;

            border-radius:
                17px;

            background:
                rgba(255,255,255,0.96);

            border:
                1px solid #dee6f1;

            box-shadow:
                0 9px 27px
                rgba(34,65,112,0.055);

            overflow:
                hidden;

            transition:
                all 0.22s ease;
        }


        .kpi-card:hover {

            transform:
                translateY(-4px);

            border-color:
                #cbd8eb;

            box-shadow:
                0 16px 35px
                rgba(34,65,112,0.10);
        }


        .kpi-card::before {

            content: "";

            position:
                absolute;

            width:
                95px;

            height:
                95px;

            right:
                -50px;

            top:
                -50px;

            border-radius:
                50%;

            background:
                #eef4ff;
        }


        .kpi-top {

            display:
                flex;

            align-items:
                center;

            justify-content:
                space-between;

            position:
                relative;

            z-index:
                2;
        }


        .kpi-icon {

            width:
                42px;

            height:
                42px;

            border-radius:
                12px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-size:
                18px;

            background:
                linear-gradient(
                    145deg,
                    #edf3ff,
                    #e4ecfc
                );

            color:
                #496fc5;

            box-shadow:
                inset 0 0 0 1px
                rgba(72,108,184,0.06);
        }


        .kpi-status {

            color:
                #71819a;

            font-size:
                10px;

            font-weight:
                700;

            padding:
                5px 8px;

            border-radius:
                6px;

            background:
                #f4f6fa;
        }


        .kpi-label {

            color:
                #6d7c94;

            font-size:
                11px;

            font-weight:
                750;

            text-transform:
                uppercase;

            letter-spacing:
                0.8px;

            margin-top:
                16px;
        }


        .kpi-value {

            color:
                #14264a;

            font-size:
                31px;

            font-weight:
                850;

            letter-spacing:
                -0.9px;

            margin-top:
                3px;
        }


        .kpi-subtitle {

            color:
                #8a96a8;

            font-size:
                10.5px;

            margin-top:
                2px;
        }


        .kpi-line {

            position:
                absolute;

            height:
                3px;

            width:
                52px;

            bottom:
                0;

            left:
                21px;

            border-radius:
                5px 5px 0 0;

            background:
                linear-gradient(
                    90deg,
                    #4c72ca,
                    #7e9be0
                );
        }


        /* ====================================================
           ANALYTICS AREA
           ==================================================== */

        .analytics-card {

            padding:
                24px 26px;

            background:
                rgba(255,255,255,0.97);

            border:
                1px solid #dee6f1;

            border-radius:
                17px;

            box-shadow:
                0 9px 27px
                rgba(34,65,112,0.045);
        }


        .analytics-header {

            display:
                flex;

            justify-content:
                space-between;

            align-items:
                flex-start;

            margin-bottom:
                10px;
        }


        .analytics-title {

            color:
                #1a2d50;

            font-size:
                15px;

            font-weight:
                750;
        }


        .analytics-caption {

            color:
                #8490a3;

            font-size:
                11px;

            margin-top:
                4px;
        }


        .analytics-pill {

            padding:
                7px 10px;

            border-radius:
                8px;

            background:
                #edf3ff;

            color:
                #4b6fc2;

            font-size:
                10px;

            font-weight:
                750;

            border:
                1px solid #e0e9fb;
        }


        /* ====================================================
           SUMMARY CARD
           ==================================================== */

        .summary-card {

            min-height:
                100%;

            padding:
                25px;

            border-radius:
                17px;

            background:
                linear-gradient(
                    145deg,
                    #ffffff,
                    #f5f8fd
                );

            border:
                1px solid #dee6f1;

            box-shadow:
                0 9px 27px
                rgba(34,65,112,0.045);

            position:
                relative;

            overflow:
                hidden;
        }


        .summary-card::before {

            content: "";

            position:
                absolute;

            width:
                130px;

            height:
                130px;

            border-radius:
                50%;

            background:
                #edf3ff;

            right:
                -75px;

            top:
                -75px;
        }


        .summary-label {

            color:
                #77869e;

            font-size:
                10px;

            font-weight:
                750;

            letter-spacing:
                0.9px;

            text-transform:
                uppercase;
        }


        .summary-value {

            color:
                #17294d;

            font-size:
                38px;

            font-weight:
                850;

            letter-spacing:
                -1px;

            margin-top:
                7px;
        }


        .summary-description {

            color:
                #7a879b;

            font-size:
                11.5px;

            line-height:
                1.65;

            margin-top:
                4px;

            max-width:
                250px;
        }


        .summary-divider {

            height:
                1px;

            background:
                #e4e8ef;

            margin:
                19px 0;
        }


        .summary-row {

            display:
                flex;

            justify-content:
                space-between;

            margin-bottom:
                12px;
        }


        .summary-row-label {

            color:
                #718099;

            font-size:
                11px;
        }


        .summary-row-value {

            color:
                #253a60;

            font-size:
                11px;

            font-weight:
                750;
        }


        /* ====================================================
           LOWER CARDS
           ==================================================== */

        .analysis-card {

            padding:
                17px 19px;

            margin-bottom:
                9px;

            background:
                rgba(255,255,255,0.98);

            border:
                1px solid #e0e6ef;

            border-radius:
                13px;

            box-shadow:
                0 5px 17px
                rgba(34,65,112,0.035);

            transition:
                all 0.2s ease;
        }


        .analysis-card:hover {

            transform:
                translateY(-2px);

            border-color:
                #cbd7ea;

            box-shadow:
                0 10px 23px
                rgba(34,65,112,0.075);
        }


        .analysis-main {

            display:
                flex;

            align-items:
                center;

            gap:
                13px;
        }


        .document-icon {

            width:
                41px;

            height:
                41px;

            border-radius:
                11px;

            background:
                linear-gradient(
                    145deg,
                    #eef4ff,
                    #e7eefc
                );

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            color:
                #4d6fb9;

            font-size:
                16px;

            flex-shrink:
                0;
        }


        .analysis-document {

            color:
                #1b3157;

            font-size:
                13px;

            font-weight:
                700;
        }


        .analysis-meta {

            color:
                #8793a6;

            font-size:
                10.5px;

            margin-top:
                4px;
        }


        .score-badge {

            padding:
                7px 10px;

            border-radius:
                8px;

            background:
                #edf3ff;

            color:
                #4a6dc0;

            font-size:
                12px;

            font-weight:
                800;

            white-space:
                nowrap;
        }


        /* ====================================================
           PENDING ANALYSES
           ==================================================== */

        .pending-container {

            background:
                rgba(255,255,255,0.98);

            border:
                1px solid #e0e6ef;

            border-radius:
                14px;

            padding:
                7px 19px;

            box-shadow:
                0 5px 17px
                rgba(34,65,112,0.035);
        }


        .pending-item {

            display:
                flex;

            align-items:
                center;

            gap:
                12px;

            padding:
                14px 0;

            transition:
                all 0.18s ease;
        }


        .pending-item:not(:last-child) {

            border-bottom:
                1px solid #eef1f5;
        }


        .pending-item:hover {

            padding-left:
                4px;
        }


        .pending-icon {

            width:
                37px;

            height:
                37px;

            border-radius:
                10px;

            background:
                #eef4ff;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            color:
                #426dc1;

            font-size:
                15px;

            flex-shrink:
                0;
        }


        .pending-name {

            color:
                #1b3157;

            font-size:
                12.5px;

            font-weight:
                700;

            white-space:
                nowrap;

            overflow:
                hidden;

            text-overflow:
                ellipsis;
        }


        .pending-meta {

            color:
                #8290a5;

            font-size:
                10.5px;

            margin-top:
                4px;
        }


        /* ====================================================
           DIVIDERS
           ==================================================== */

        .dashboard-divider {

            height:
                1px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    #dce3ed 12%,
                    #dce3ed 88%,
                    transparent
                );

            margin:
                38px 0;
        }


        /* ====================================================
           STREAMLIT CHART POLISH
           ==================================================== */

        div[data-testid="stLineChart"] {

            background:
                transparent !important;

            border:
                none !important;

            padding:
                0 !important;
        }


        /* ====================================================
           BUTTONS
           ==================================================== */

        div.stButton > button {

            border-radius:
                9px !important;

            border:
                1px solid #d6dfed !important;

            background:
                #ffffff !important;

            color:
                #294064 !important;

            font-weight:
                650 !important;

            min-height:
                40px !important;

            transition:
                all 0.18s ease !important;
        }


        div.stButton > button:hover {

            border-color:
                #7697dc !important;

            background:
                #f5f8ff !important;

            color:
                #416cc9 !important;

            transform:
                translateY(-1px);
        }

    </style>
    """)


    # =====================================================
    # HEADER
    # =====================================================

    st.html("""
    <div class="dashboard-header">

        <div class="header-content">

            <div class="dashboard-label">
                SCHOLARSHIELD · AI-POWERED ACADEMIC ANALYSIS
            </div>

            <div class="dashboard-title">
                Academic Similarity
                <span>Dashboard</span>
            </div>

            <div class="dashboard-description">
                Monitor your academic documents, explore similarity
                patterns and understand your research workspace
                from one intelligent dashboard.
            </div>

        </div>

        <div>

            <div class="header-status">

                <div class="status-dot"></div>

                Analysis system ready

            </div>

        </div>

        <div class="header-decoration"></div>

    </div>
    """)


    # =====================================================
    # DYNAMIC VALUES
    # =====================================================

    total_documents = dashboard_stats.get(
        "total_documents",
        0
    )

    total_analyses = dashboard_stats.get(
        "total_analyses",
        0
    )

    average_similarity = format_percentage(
        dashboard_stats.get(
            "average_similarity"
        )
    )

    highest_similarity = format_percentage(
        dashboard_stats.get(
            "highest_similarity"
        )
    )

    lowest_similarity = format_percentage(
        dashboard_stats.get(
            "lowest_similarity"
        )
    )


    # =====================================================
    # WELCOME HERO
    # =====================================================

    safe_user_name = escape(
        str(user_name)
    )

    st.html(f"""
    <div class="welcome-card">

        <div class="welcome-decoration-one"></div>
        <div class="welcome-decoration-two"></div>
        <div class="welcome-dot"></div>

        <div class="welcome-grid">

            <div>

                <div class="welcome-eyebrow">
                    YOUR ACADEMIC WORKSPACE
                </div>

                <div class="welcome-title">
                    Welcome back, {safe_user_name} 👋
                </div>

                <div class="welcome-text">
                    ScholarShield goes beyond simple word matching.
                    Explore lexical, syntactic, semantic and contextual
                    relationships to understand why academic documents
                    are similar.
                </div>

            </div>

            <div class="welcome-right">

                <div class="welcome-badge">
                    <span class="status-dot"></span>
                    Workspace active
                </div>

                <div class="welcome-mini-stat">
                    <strong>{total_analyses}</strong><br>
                    analyses completed
                </div>

            </div>

        </div>

    </div>
    """)


    # =====================================================
    # ACTIVITY SECTION
    # =====================================================

    st.html("""
    <div class="section-block">

        <div class="section-heading">
            Your Activity
        </div>

        <div class="section-subheading">
            A quick overview of your academic document workspace.
        </div>

        <div class="section-accent"></div>

    </div>
    """)


    # =====================================================
    # KPI CARDS
    # =====================================================

    kpis = [

        (
            "▤",
            "Documents",
            str(total_documents),
            "Uploaded documents",
            "Active"
        ),

        (
            "◈",
            "Analyses",
            str(total_analyses),
            "Completed analyses",
            "Processed"
        ),

        (
            "◌",
            "Avg. Similarity",
            average_similarity,
            "Across all analyses",
            "Overall"
        ),

        (
            "↗",
            "Highest Similarity",
            highest_similarity,
            "Highest recorded score",
            "Maximum"
        ),

    ]


    columns = st.columns(
        4,
        gap="medium"
    )


    for column, (
        icon,
        label,
        value,
        subtitle,
        status
    ) in zip(
        columns,
        kpis
    ):

        with column:

            st.html(f"""
            <div class="kpi-wrapper">

                <div class="kpi-card">

                    <div class="kpi-top">

                        <div class="kpi-icon">
                            {icon}
                        </div>

                        <div class="kpi-status">
                            {status}
                        </div>

                    </div>

                    <div class="kpi-label">
                        {label}
                    </div>

                    <div class="kpi-value">
                        {value}
                    </div>

                    <div class="kpi-subtitle">
                        {subtitle}
                    </div>

                    <div class="kpi-line"></div>

                </div>

            </div>
            """)


    # =====================================================
    # ANALYTICS SECTION
    # =====================================================

    st.html("""
    <div class="dashboard-divider"></div>

    <div class="section-block" style="margin-top:0;">

        <div class="section-heading">
            Similarity Analytics
        </div>

        <div class="section-subheading">
            Track how similarity scores change across your recent
            document analyses.
        </div>

        <div class="section-accent"></div>

    </div>
    """)


    analytics_left, analytics_right = st.columns(
        [2.25, 1],
        gap="large"
    )


    # =====================================================
    # CHART CARD
    # =====================================================

    with analytics_left:

        st.html("""
        <div class="analytics-card">

            <div class="analytics-header">

                <div>

                    <div class="analytics-title">
                        Similarity Trend
                    </div>

                    <div class="analytics-caption">
                        Overall similarity score by recent analysis
                    </div>

                </div>

                <div class="analytics-pill">
                    Last 7 analyses
                </div>

            </div>

        </div>
        """)


        chart_values = {}

        for index, item in enumerate(
            trend_data,
            start=1
        ):

            if isinstance(item, dict):

                score = (
                    item.get("overall_score")
                    or item.get("similarity_score")
                    or item.get("score")
                )

            else:

                try:
                    score = item["overall_score"]
                except (TypeError, KeyError, IndexError):
                    score = item

            if score is not None:

                try:

                    chart_values[
                        f"Analysis {index}"
                    ] = float(score)

                except (
                    ValueError,
                    TypeError
                ):

                    continue


        if chart_values:

            st.line_chart(
                chart_values,
                height=250
            )

        else:

            st.html("""
            <div style="
                height:250px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#8793a6;
                font-size:12px;
            ">
                Similarity trend data will appear here
                after completed analyses.
            </div>
            """)


    # =====================================================
    # SUMMARY CARD
    # =====================================================

    with analytics_right:

        st.html(f"""
        <div class="summary-card">

            <div class="summary-label">
                Similarity Overview
            </div>

            <div class="summary-value">
                {average_similarity}
            </div>

            <div class="summary-description">
                Average similarity across your recorded
                document analyses.
            </div>

            <div class="summary-divider"></div>

            <div class="summary-row">

                <div class="summary-row-label">
                    Total analyses
                </div>

                <div class="summary-row-value">
                    {total_analyses}
                </div>

            </div>

            <div class="summary-row">

                <div class="summary-row-label">
                    Highest score
                </div>

                <div class="summary-row-value">
                    {highest_similarity}
                </div>

            </div>

            <div class="summary-row">

                <div class="summary-row-label">
                    Lowest score
                </div>

                <div class="summary-row-value">
                    {lowest_similarity}
                </div>

            </div>

        </div>
        """)


    # =====================================================
    # LOWER SECTION
    # =====================================================

    st.html("""
    <div class="dashboard-divider"></div>
    """)


    analysis_col, pending_col = st.columns(
        [2.15, 1],
        gap="large"
    )


    # =====================================================
    # RECENT ANALYSES
    # =====================================================

    with analysis_col:

        st.html("""
        <div class="section-block" style="margin-top:0;">

            <div class="section-heading">
                Recent Analyses
            </div>

            <div class="section-subheading">
                Your latest completed similarity analyses.
            </div>

            <div class="section-accent"></div>

        </div>
        """)


        if recent_analyses:

            for analysis in recent_analyses:

                filename = escape(
                    str(
                        analysis["filename"]
                    )
                )

                raw_filename = str(
                    analysis["filename"]
                )

                file_type = escape(
                    raw_filename.rsplit(
                        ".",
                        1
                    )[-1].upper()
                    if "." in raw_filename
                    else "DOCUMENT"
                )

                date = format_analysis_date(
                    analysis["analysis_date"]
                )

                score = analysis["overall_score"]

                score_text = format_percentage(
                    score
                )

                similarity_level = get_similarity_level(
                    score
                )


                st.html(f"""
                <div class="analysis-card">

                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        gap:15px;
                    ">

                        <div class="analysis-main">

                            <div class="document-icon">
                                ▤
                            </div>

                            <div style="
                                min-width:0;
                            ">

                                <div class="analysis-document">
                                    {filename}
                                </div>

                                <div class="analysis-meta">
                                    {file_type}
                                    &nbsp;·&nbsp;
                                    Analyzed {date}
                                    &nbsp;·&nbsp;
                                    {similarity_level} similarity
                                </div>

                            </div>

                        </div>

                        <div class="score-badge">
                            {score_text}
                        </div>

                    </div>

                </div>
                """)

        else:

            st.html("""
            <div class="analysis-card">

                <div style="
                    text-align:center;
                    padding:22px 10px;
                ">

                    <div style="
                        color:#557bcf;
                        font-size:26px;
                        margin-bottom:8px;
                    ">
                        ◌
                    </div>

                    <div style="
                        color:#31476b;
                        font-size:13px;
                        font-weight:700;
                    ">
                        No analyses yet
                    </div>

                    <div style="
                        color:#7d8a9e;
                        font-size:12px;
                        margin-top:4px;
                    ">
                        Your completed analyses will appear here.
                    </div>

                </div>

            </div>
            """)


    # =====================================================
    # PENDING ANALYSES
    # =====================================================

    with pending_col:

        st.html("""
        <div class="section-block" style="margin-top:0;">

            <div class="section-heading">
                Pending Analyses
            </div>

            <div class="section-subheading">
                Documents waiting for analysis.
            </div>

            <div class="section-accent"></div>

        </div>
        """)


        if pending_documents:

            st.html("""
            <div class="pending-container">
            """)


            for document in pending_documents:

                filename = escape(
                    str(
                        document["filename"]
                    )
                )

                file_type = escape(
                    str(
                        document["file_type"]
                        or "DOCUMENT"
                    ).upper()
                )

                word_count = document["word_count"]


                if word_count is not None:

                    word_text = (
                        f"{int(word_count):,} words"
                    )

                else:

                    word_text = (
                        "Word count unavailable"
                    )


                st.html(f"""
                <div class="pending-item">

                    <div class="pending-icon">
                        ▤
                    </div>

                    <div style="
                        min-width:0;
                        flex:1;
                    ">

                        <div class="pending-name">
                            {filename}
                        </div>

                        <div class="pending-meta">
                            {file_type}
                            &nbsp;·&nbsp;
                            {word_text}
                        </div>

                    </div>

                </div>
                """)


            st.html("""
            </div>
            """)

        else:

            st.html("""
            <div class="pending-container">

                <div style="
                    text-align:center;
                    padding:28px 12px;
                ">

                    <div style="
                        width:42px;
                        height:42px;
                        margin:0 auto 10px;
                        border-radius:50%;
                        background:#eef4ff;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#426dc1;
                        font-size:18px;
                    ">
                        ✓
                    </div>

                    <div style="
                        color:#263c60;
                        font-size:13px;
                        font-weight:700;
                    ">
                        All documents are analyzed
                    </div>

                    <div style="
                        color:#7d8a9e;
                        font-size:11.5px;
                        line-height:1.5;
                        margin-top:5px;
                    ">
                        Your workspace is up to date.
                    </div>

                </div>

            </div>
            """)


    # =====================================================
    # FINAL FOOTER
    # =====================================================

    st.html("""
    <div style="
        margin-top:42px;
        padding:18px 0 4px;
        border-top:1px solid #e1e6ee;
        display:flex;
        justify-content:space-between;
        align-items:center;
    ">

        <div style="
            color:#8793a6;
            font-size:10.5px;
        ">
            ScholarShield · Context-Aware Academic Similarity Analyzer
        </div>

        <div style="
            color:#6f83a5;
            font-size:10.5px;
            font-weight:650;
        ">
            Understand similarity. Don't just detect it.
        </div>

    </div>
    """)