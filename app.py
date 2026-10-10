import streamlit as st
from database.database import initialize_database
from auth.register import show_register_page
from auth.login import show_login_page
from pages.dashboard import show_dashboard
from pages.upload import show_upload
from pages.analysis import analysis_page
from pages.library import library_page
from pages.reports import reports_page
from pages.profile import profile_page

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ScholarShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)
initialize_database()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Home"


# =========================================================
# AUTHENTICATION ROUTING
# =========================================================

auth_page = st.query_params.get("auth")
session_marker = st.query_params.get("session")


# ---------------------------------------------------------
# RESTORE LOGIN AFTER PAGE REFRESH
# ---------------------------------------------------------

if session_marker == "authenticated":
    st.session_state.logged_in = True


# ---------------------------------------------------------
# LOGIN / REGISTER
# ---------------------------------------------------------

if not st.session_state.logged_in:

    if auth_page == "register":
        show_register_page()
        st.stop()

    if auth_page == "login":
        show_login_page()
        st.stop()


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if st.session_state.logged_in:

    # ---------------------------------------------------------
    # DIRECT NAVIGATION TO ANALYSIS
    # ---------------------------------------------------------

    if st.session_state.get("open_analysis_request", False):

        st.session_state.open_analysis_request = False
        st.session_state.dashboard_page = "Analysis"

        # Synchronize the existing sidebar radio
        st.session_state["workspace_navigation"] = "⌕  Analysis"

        analysis_page()
        st.stop()

    if "dashboard_page" not in st.session_state:
        st.session_state.dashboard_page = "Dashboard"

    if st.session_state.dashboard_page == "Upload Document":
        show_upload()

    elif st.session_state.dashboard_page == "My Library":
        library_page()

    elif st.session_state.dashboard_page == "Analysis":
        analysis_page()

    elif st.session_state.dashboard_page == "Reports":
        reports_page()

    elif st.session_state.dashboard_page == "Profile":
        profile_page()

    else:
        show_dashboard()

    st.stop()


# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
<style>

    /* ---------- GLOBAL ---------- */

    [data-testid="stAppViewContainer"] {
        background: #f5f8fc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }


  /* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background: #f1f3f6 !important;
    border-right: 1px solid #d7dce4 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

[data-testid="stSidebarContent"] {
    padding: 0 14px !important;
}

/* Hide Streamlit default navigation */
[data-testid="stSidebarNav"] {
    display: none !important;
}


/* ---------- ALL SIDEBAR TEXT ---------- */

[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a {
    color: #000000 !important;
}


/* ---------- SIDEBAR RADIO NAVIGATION ---------- */

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 7px !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 11px 12px !important;
    border-radius: 9px !important;
    color: #000000 !important;
    font-size: 15px !important;
    font-weight: 550 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #000000 !important;
    font-size: 15px !important;
}


/* ---------- HOVER ---------- */

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #e3e7ee !important;
    color: #000000 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover p {
    color: #000000 !important;
}


/* ---------- SELECTED ITEM ---------- */

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #dce4f2 !important;
    color: #000000 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: #000000 !important;
    font-weight: 650 !important;
}


/* ---------- SIDEBAR INPUT / ICONS ---------- */

[data-testid="stSidebar"] svg {
    color: #000000 !important;
    fill: #000000 !important;
}
    /* ---------- MAIN CONTENT ---------- */

    .main-page {
        width: 100%;
        overflow: hidden;
    }


    /* ---------- HERO ---------- */

    .hero {
        min-height: 430px;

        position: relative;

        display: flex;
        align-items: center;

        padding: 55px 7%;

        background:
            linear-gradient(
                90deg,
                rgba(6, 18, 39, 0.97) 0%,
                rgba(8, 22, 45, 0.91) 30%,
                rgba(8, 25, 48, 0.57) 58%,
                rgba(7, 20, 39, 0.35) 100%
            ),
            url("https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=2200&q=90");

        background-size: cover;
        background-position: center;
    }

    .hero-content {
        max-width: 690px;
        position: relative;
        z-index: 2;
    }

    .eyebrow {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.7px;
        color: #75a7ff;
        margin-bottom: 17px;
        text-transform: uppercase;
    }

    .hero-title {
        margin: 0;
        color: white;
        font-size: clamp(42px, 4vw, 64px);
        line-height: 1.06;
        font-weight: 750;
        letter-spacing: -2px;
    }

    .hero-title .gradient {
        background: linear-gradient(
            90deg,
            #58a6ff,
            #788cff,
            #c06cff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        margin-top: 23px;
        max-width: 620px;

        color: #d9e3f3;
        font-size: 17px;
        line-height: 1.7;
    }

    .hero-buttons {
        margin-top: 28px;
        display: flex;
        gap: 14px;
    }

    .hero-btn-primary,
    .hero-btn-secondary {
        display: inline-block;
        padding: 13px 27px;
        border-radius: 10px;

        text-decoration: none;
        font-size: 14px;
        font-weight: 650;
    }

    .hero-btn-primary {
        color: white;

        background:
            linear-gradient(
                135deg,
                #4c9cff,
                #8a5cff
            );

        box-shadow:
            0 8px 25px rgba(84, 113, 255, 0.30);
    }

    .hero-btn-secondary {
        color: white;
        border: 1px solid rgba(197, 215, 255, 0.65);
        background: rgba(255,255,255,0.05);
    }

    .hero-note {
        position: absolute;
        right: 8%;
        top: 90px;

        max-width: 190px;

        color: rgba(255,255,255,0.92);
        font-family: Georgia, serif;
        font-style: italic;

        font-size: 19px;
        line-height: 1.45;

        text-shadow: 0 2px 12px rgba(0,0,0,0.5);
    }


    /* ---------- SECTION ---------- */

    .section {
        padding: 43px 7%;
    }

    .section-label {
        color: #548cff;
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .section-title {
        color: #15274b;
        font-size: 27px;
        font-weight: 750;
        margin: 0;
    }

    .section-description {
        color: #52688d;
        font-size: 15px;
        line-height: 1.65;
        max-width: 680px;
        margin-top: 8px;
    }


    /* ---------- CAPABILITIES ---------- */

    .capabilities {
        background: #f7faff;
    }

    .cards {
        display: grid;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 15px;

        margin-top: 22px;
    }

    .capability-card {
        min-height: 155px;

        padding: 19px;

        border: 1px solid #dce7f8;
        border-radius: 10px;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f9fbff
            );

        box-shadow:
            0 5px 20px rgba(37, 72, 126, 0.06);
    }

    .capability-icon {
        width: 43px;
        height: 43px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        font-size: 21px;

        background: #e9f3ff;
        color: #438fff;

        margin-bottom: 13px;
    }

    .capability-card:nth-child(2) .capability-icon {
        background: #eeeaff;
        color: #725cff;
    }

    .capability-card:nth-child(3) .capability-icon {
        background: #e2f8f4;
        color: #16a58d;
    }

    .capability-card:nth-child(4) .capability-icon {
        background: #f0e7ff;
        color: #9a59e8;
    }

    .capability-title {
        color: #14284d;
        font-size: 14px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .capability-text {
        color: #52698e;
        font-size: 13.5px;
        line-height: 1.6;
    }


    /* ---------- PROCESS ---------- */

    .process {
        background: #f1f6fd;
    }

    .steps {
        display: grid;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 20px;

        margin-top: 26px;
    }

    .step {
        display: flex;
        align-items: flex-start;
        gap: 13px;
        position: relative;
    }

    .step-number {
        flex-shrink: 0;

        width: 38px;
        height: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        color: white;
        font-size: 14px;
        font-weight: 750;

        background:
            linear-gradient(
                135deg,
                #4199ff,
                #5d6cff
            );
    }

    .step:nth-child(2) .step-number {
        background:
            linear-gradient(
                135deg,
                #7655ff,
                #9b56e8
            );
    }

    .step:nth-child(3) .step-number {
        background:
            linear-gradient(
                135deg,
                #11aa91,
                #38b994
            );
    }

    .step:nth-child(4) .step-number {
        background:
            linear-gradient(
                135deg,
                #6557ed,
                #a05ee9
            );
    }

    .step-title {
        color: #14284d;
        font-size: 14px;
        font-weight: 750;
        margin-top: 2px;
    }

    .step-text {
        color: #5b7093;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 5px;
    }


    /* ---------- CTA ---------- */

    .cta {
        position: relative;
        overflow: hidden;

        padding: 34px 7% 42px;

        background:
            radial-gradient(
                circle at 15% 110%,
                rgba(101, 69, 205, 0.35),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 110%,
                rgba(31, 120, 224, 0.35),
                transparent 34%
            ),
            linear-gradient(
                135deg,
                #0b1429,
                #111d39
            );
    }

    .cta-content {
        position: relative;
        z-index: 2;
        text-align: center;
    }

    .cta-title {
        color: white;
        font-size: 24px;
        font-weight: 750;
        margin: 0;
    }

    .cta-description {
        color: #c3d0e6;
        font-size: 12px;
        margin-top: 7px;
    }

    .cta-cards {
        display: grid;
        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 20px;

        max-width: 850px;
        margin: 23px auto 0;
    }

    .cta-card {
        min-height: 75px;

        display: flex;
        align-items: center;

        text-align: left;

        padding: 14px 16px;

        border: 1px solid rgba(132, 163, 226, 0.65);
        border-radius: 10px;

        background: rgba(11, 24, 48, 0.72);
    }

    .cta-icon {
        width: 43px;
        height: 43px;

        flex-shrink: 0;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: rgba(85, 126, 207, 0.25);

        color: white;
        font-size: 21px;

        margin-right: 13px;
    }

    .cta-info {
        flex: 1;
    }

    .cta-small-title {
        color: white;
        font-size: 12px;
        font-weight: 750;
    }

    .cta-small-text {
        color: #aebed8;
        font-size: 10px;
        margin-top: 4px;
    }

    .cta-button {
        padding: 9px 20px;

        border-radius: 8px;

        color: white;
        text-decoration: none;

        font-size: 11px;
        font-weight: 700;

        border: 1px solid rgba(164, 186, 236, 0.65);

        white-space: nowrap;
    }

    .cta-button.primary {
        border: none;

        background:
            linear-gradient(
                135deg,
                #5a8dff,
                #a15ae9
            );
    }


    /* ---------- RESPONSIVE ---------- */

    @media (max-width: 1000px) {

        .cards {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .steps {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }

        .hero-note {
            display: none;
        }

    }

    @media (max-width: 700px) {

        .cards,
        .steps,
        .cta-cards {
            grid-template-columns: 1fr;
        }

        .hero {
            padding: 45px 6%;
        }

        .hero-title {
            font-size: 40px;
        }

        .section {
            padding: 35px 6%;
        }

    }

</style>
""")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html("""
    <div style="
        padding: 25px 10px 20px 10px;
        border-bottom: 1px solid rgba(160,180,220,0.20);
        margin-bottom: 18px;
    ">

        <div style="
            display:flex;
            align-items:center;
            gap:12px;
        ">

            <div style="
                width:48px;
                height:48px;
                border:2px solid #7da5ff;
                border-radius:14px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:24px;
                background:rgba(91,126,215,0.12);
            ">
                🛡️
            </div>

            <div>
                <div style="
                    color:white;
                    font-size:18px;
                    font-weight:750;
                ">
                    ScholarShield
                </div>

                <div style="
                    color:#b8c7df;
                    font-size:10px;
                    line-height:1.5;
                    margin-top:4px;
                ">
                    Context-Aware Academic<br>
                    Similarity Analyzer
                </div>
            </div>

        </div>

    </div>
    """)

    # Native Streamlit navigation
    selected_page = st.radio(
        "Navigation",
        [
            "Home",
            "How It Works",
            "About"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.session_state.page = selected_page

    # Sidebar footer
    st.html("""
    <div style="
        position: fixed;
        bottom: 25px;
        left: 24px;
        width: 190px;
        color:#b9c8e2;
    ">

        <div style="
            font-size:25px;
            margin-bottom:8px;
        ">
            🎓
        </div>

        <div style="
            font-family:Georgia,serif;
            font-style:italic;
            font-size:13px;
            line-height:1.5;
        ">
            Smarter Analysis.<br>
            Fairer Learning.
        </div>

        <div style="
            width:80px;
            height:1px;
            background:#33466b;
            margin-top:20px;
        ">
        </div>

    </div>
    """)


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    st.html("""
    <div class="main-page">

        <!-- ================= HERO ================= -->

        <section class="hero">

            <div class="hero-content">

                <div class="eyebrow">
                    AI-POWERED ACADEMIC ANALYSIS
                </div>

                <h1 class="hero-title">
                    Understand similarity.<br>
                    <span class="gradient">
                        Beyond the words.
                    </span>
                </h1>

                <p class="hero-description">
                    ScholarShield analyzes academic documents using
                    lexical, syntactic and semantic language analysis
                    to identify meaningful similarities and explain
                    the context behind them.
                </p>

                <div class="hero-buttons">

                    <a
    class="hero-btn-primary"
    href="?auth=register"
>
    Get Started&nbsp; →
</a>

                    <a
                        class="hero-btn-secondary"
                        href="#how-it-works"
                    >
                        Learn More
                    </a>

                </div>

            </div>

            <div class="hero-note">
                Better Insights<br>
                for a Fairer<br>
                Academic World
            </div>

        </section>


        <!-- ================= CAPABILITIES ================= -->

        <section class="section capabilities">

            <div class="section-label">
                KEY CAPABILITIES
            </div>

            <h2 class="section-title">
                More than just word matching
            </h2>

            <p class="section-description">
                ScholarShield combines multiple NLP techniques to go
                beyond surface-level matches and understand the true
                meaning and context of your documents.
            </p>


            <div class="cards">

                <div class="capability-card">

                    <div class="capability-icon">
                        📄
                    </div>

                    <div class="capability-title">
                        Lexical Analysis
                    </div>

                    <div class="capability-text">
                        Identifies shared words and phrases while
                        accounting for normalized word forms.
                    </div>

                </div>


                <div class="capability-card">

                    <div class="capability-icon">
                        ⚖
                    </div>

                    <div class="capability-title">
                        Syntactic Analysis
                    </div>

                    <div class="capability-text">
                        Examines sentence structure and dependency
                        relationships to detect syntactic similarities.
                    </div>

                </div>


                <div class="capability-card">

                    <div class="capability-icon">
                        🧠
                    </div>

                    <div class="capability-title">
                        Semantic Analysis
                    </div>

                    <div class="capability-text">
                        Compares the meaning and context of passages,
                        even when their wording differs.
                    </div>

                </div>


                <div class="capability-card">

                    <div class="capability-icon">
                        ✨
                    </div>

                    <div class="capability-title">
                        Explainable Results
                    </div>

                    <div class="capability-text">
                        Not just a score — get clear explanations
                        of why passages are considered similar.
                    </div>

                </div>

            </div>

        </section>


        <!-- ================= PROCESS ================= -->

        <section
            class="section process"
            id="how-it-works"
        >

            <div class="section-label">
                THE PROCESS
            </div>

            <h2 class="section-title">
                From document to insight
            </h2>

            <p class="section-description">
                A structured NLP pipeline that analyzes your documents
                at multiple levels of language understanding.
            </p>


            <div class="steps">

                <div class="step">

                    <div class="step-number">
                        1
                    </div>

                    <div>
                        <div class="step-title">
                            Upload
                        </div>

                        <div class="step-text">
                            Upload your document and
                            reference files.
                        </div>
                    </div>

                </div>


                <div class="step">

                    <div class="step-number">
                        2
                    </div>

                    <div>
                        <div class="step-title">
                            Analyze
                        </div>

                        <div class="step-text">
                            Process language, structure,
                            context and meaning.
                        </div>
                    </div>

                </div>


                <div class="step">

                    <div class="step-number">
                        3
                    </div>

                    <div>
                        <div class="step-title">
                            Compare
                        </div>

                        <div class="step-text">
                            Measure lexical, syntactic
                            and semantic similarity.
                        </div>
                    </div>

                </div>


                <div class="step">

                    <div class="step-number">
                        4
                    </div>

                    <div>
                        <div class="step-title">
                            Explain
                        </div>

                        <div class="step-text">
                            View similar passages and
                            understand why they match.
                        </div>
                    </div>

                </div>

            </div>

        </section>


        <!-- ================= CTA ================= -->

        <section
            class="cta"
            id="get-started"
        >

            <div class="cta-content">

                <h2 class="cta-title">
                    Ready to get started?
                </h2>

                <div class="cta-description">
                    Join ScholarShield and analyze your academic
                    documents with the power of AI.
                </div>


                <div class="cta-cards">

                    <div class="cta-card">

                        <div class="cta-icon">
                            👤
                        </div>

                        <div class="cta-info">

                            <div class="cta-small-title">
                                New to ScholarShield?
                            </div>

                            <div class="cta-small-text">
                                Create an account and get started.
                            </div>

                        </div>

                        <a
                         class="cta-button primary"
                        href="?auth=register"
                    >
                        Register&nbsp; →
                    </a>

                    </div>


                    <div class="cta-card">

                        <div class="cta-icon">
                            ⇥
                        </div>

                        <div class="cta-info">

                            <div class="cta-small-title">
                                Already a Scholar?
                            </div>

                            <div class="cta-small-text">
                                Sign in to access your documents
                                and analyses.
                            </div>

                        </div>

                        <a
    class="cta-button"
    href="?auth=login"
>
    Login&nbsp; →
</a>

                    </div>

                </div>

            </div>

        </section>

    </div>
    """)


# =========================================================
# HOW IT WORKS PAGE
# =========================================================

elif st.session_state.page == "How It Works":

    st.html("""
    <style>

        .how-page {
            min-height: 100vh;
            background:
                radial-gradient(
                    circle at 85% 5%,
                    rgba(90,130,255,0.10),
                    transparent 30%
                ),
                #f5f8fd;

            padding: 55px 7%;
        }

        .how-header {
            max-width: 780px;
            margin-bottom: 40px;
        }

        .how-label {
            color: #568cff;
            font-size: 13px;
            font-weight: 750;
            letter-spacing: 1.7px;
            text-transform: uppercase;
        }

        .how-title {
            color: #14284d;
            font-size: 42px;
            line-height: 1.15;
            margin: 10px 0 12px;
            font-weight: 750;
        }

        .how-intro {
            color: #52698e;
            font-size: 16px;
            line-height: 1.8;
        }

        .how-flow {
            display: grid;
            grid-template-columns:
                repeat(4, minmax(0, 1fr));

            gap: 17px;
            margin-top: 30px;
        }

        .how-card {
            position: relative;

            padding: 25px 22px;

            min-height: 235px;

            border-radius: 15px;

            background: white;

            border: 1px solid #dce7f7;

            box-shadow:
                0 10px 30px rgba(41,70,120,0.07);

            transition:
                transform .2s ease,
                box-shadow .2s ease;
        }

        .how-card:hover {
            transform: translateY(-5px);

            box-shadow:
                0 16px 35px rgba(41,70,120,0.12);
        }

        .how-number {
            width: 43px;
            height: 43px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 12px;

            color: white;

            font-weight: 750;
            font-size: 15px;

            background:
                linear-gradient(
                    135deg,
                    #4d9aff,
                    #695ff0
                );

            margin-bottom: 20px;
        }

        .how-card:nth-child(2) .how-number {
            background:
                linear-gradient(
                    135deg,
                    #7658ff,
                    #a157e8
                );
        }

        .how-card:nth-child(3) .how-number {
            background:
                linear-gradient(
                    135deg,
                    #12a993,
                    #32b891
                );
        }

        .how-card:nth-child(4) .how-number {
            background:
                linear-gradient(
                    135deg,
                    #6658ec,
                    #9d5de8
                );
        }

        .how-card-title {
            color: #172c52;
            font-size: 18px;
            font-weight: 750;
            margin-bottom: 10px;
        }

        .how-card-text {
            color: #607596;
            font-size: 13.5px;
            line-height: 1.7;
        }

        .how-detail {
            margin-top: 28px;

            padding: 28px 30px;

            border-radius: 15px;

            background:
                linear-gradient(
                    135deg,
                    #0d1931,
                    #15294b
                );

            color: white;

            box-shadow:
                0 12px 35px rgba(16,35,69,0.15);
        }

        .how-detail-title {
            font-size: 21px;
            font-weight: 750;
            margin-bottom: 9px;
        }

        .how-detail-text {
            color: #c8d5e9;
            font-size: 14px;
            line-height: 1.75;
            max-width: 900px;
        }

        @media (max-width: 1000px) {
            .how-flow {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 650px) {
            .how-flow {
                grid-template-columns: 1fr;
            }
        }

    </style>


    <div class="how-page">

        <div class="how-header">

            <div class="how-label">
                THE SCHOLARSHIELD PIPELINE
            </div>

            <div class="how-title">
                From document to meaningful insight.
            </div>

            <div class="how-intro">
                ScholarShield follows a structured Natural Language
                Processing pipeline to examine academic documents
                at multiple levels — from individual words to
                sentence structure, context and meaning.
            </div>

        </div>


        <div class="how-flow">

            <div class="how-card">

                <div class="how-number">
                    01
                </div>

                <div class="how-card-title">
                    Upload
                </div>

                <div class="how-card-text">
                    Upload the academic document you want to analyze
                    along with one or more reference documents.
                    ScholarShield extracts the textual content
                    before analysis begins.
                </div>

            </div>


            <div class="how-card">

                <div class="how-number">
                    02
                </div>

                <div class="how-card-title">
                    Analyze
                </div>

                <div class="how-card-text">
                    The system preprocesses the text and performs
                    morphological and syntactic analysis to
                    understand words, sentences and their
                    grammatical relationships.
                </div>

            </div>


            <div class="how-card">

                <div class="how-number">
                    03
                </div>

                <div class="how-card-title">
                    Compare
                </div>

                <div class="how-card-text">
                    Lexical, syntactic and semantic techniques
                    compare the documents to identify similarities
                    even when the wording or sentence structure
                    differs.
                </div>

            </div>


            <div class="how-card">

                <div class="how-number">
                    04
                </div>

                <div class="how-card-title">
                    Explain
                </div>

                <div class="how-card-text">
                    ScholarShield highlights similar passages,
                    provides similarity measurements and explains
                    the linguistic or semantic relationship behind
                    the detected similarity.
                </div>

            </div>

        </div>


        <div class="how-detail">

            <div class="how-detail-title">
                Why multiple levels of analysis?
            </div>

            <div class="how-detail-text">
                Two passages can express a similar idea without using
                the same words. ScholarShield therefore combines
                lexical, syntactic and semantic analysis instead of
                relying on simple word matching alone. This produces
                a more informative view of how two academic passages
                are related.
            </div>

        </div>

    </div>
    """)
# =========================================================
# ABOUT PAGE
# =========================================================

elif st.session_state.page == "About":

    st.html("""
    <style>

        .about-page {
            min-height: 100vh;

            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(91,119,255,0.10),
                    transparent 30%
                ),
                #f5f8fd;

            padding: 55px 7%;
        }

        .about-header {
            max-width: 800px;
        }

        .about-label {
            color: #568cff;
            font-size: 13px;
            font-weight: 750;
            letter-spacing: 1.7px;
        }

        .about-title {
            color: #14284d;
            font-size: 42px;
            line-height: 1.15;
            font-weight: 750;
            margin: 10px 0 14px;
        }

        .about-intro {
            color: #52698e;
            font-size: 16px;
            line-height: 1.8;
        }

        .about-grid {
            display: grid;
            grid-template-columns:
                1.35fr 1fr;

            gap: 22px;

            margin-top: 38px;
        }

        .about-main,
        .about-side {
            background: white;

            border: 1px solid #dce7f7;

            border-radius: 15px;

            padding: 28px;

            box-shadow:
                0 10px 30px rgba(41,70,120,0.06);
        }

        .about-main-title {
            color: #172c52;
            font-size: 21px;
            font-weight: 750;
            margin-bottom: 12px;
        }

        .about-main-text {
            color: #607596;
            font-size: 14px;
            line-height: 1.8;
        }

        .about-feature {
            display: flex;
            gap: 14px;

            padding: 15px 0;

            border-bottom: 1px solid #e8eef7;
        }

        .about-feature:last-child {
            border-bottom: none;
        }

        .about-feature-icon {
            width: 40px;
            height: 40px;

            flex-shrink: 0;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 10px;

            background: #edf4ff;

            font-size: 19px;
        }

        .about-feature-title {
            color: #172c52;
            font-size: 14px;
            font-weight: 750;
        }

        .about-feature-text {
            color: #687b99;
            font-size: 12.5px;
            line-height: 1.55;
            margin-top: 4px;
        }

        .about-values {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 16px;

            margin-top: 22px;
        }

        .value-card {
            padding: 22px;

            border-radius: 14px;

            background:
                linear-gradient(
                    145deg,
                    #ffffff,
                    #f7faff
                );

            border: 1px solid #dce7f7;
        }

        .value-icon {
            font-size: 23px;
            margin-bottom: 10px;
        }

        .value-title {
            color: #172c52;
            font-size: 15px;
            font-weight: 750;
            margin-bottom: 7px;
        }

        .value-text {
            color: #607596;
            font-size: 12.5px;
            line-height: 1.65;
        }

        .about-note {
            margin-top: 24px;

            padding: 23px 27px;

            border-radius: 14px;

            background:
                linear-gradient(
                    135deg,
                    #0c172d,
                    #15294b
                );

            color: #d5e0f1;

            font-size: 13px;
            line-height: 1.7;
        }

        .about-note strong {
            color: white;
        }

        @media (max-width: 850px) {

            .about-grid {
                grid-template-columns: 1fr;
            }

            .about-values {
                grid-template-columns: 1fr;
            }

        }

    </style>


    <div class="about-page">

        <div class="about-header">

            <div class="about-label">
                ABOUT SCHOLARSHIELD
            </div>

            <div class="about-title">
                Understanding similarity beyond
                identical words.
            </div>

            <div class="about-intro">
                ScholarShield is a context-aware academic similarity
                analyzer built using Natural Language Processing.
                It examines how academic passages relate through
                vocabulary, sentence structure, context and meaning.
            </div>

        </div>


        <div class="about-grid">

            <div class="about-main">

                <div class="about-main-title">
                    What makes ScholarShield different?
                </div>

                <div class="about-main-text">
                    Traditional similarity checks can focus heavily
                    on matching words or phrases. ScholarShield
                    approaches the problem from a linguistic
                    perspective.

                    <br><br>

                    The system analyzes documents at multiple levels,
                    combining lexical analysis, syntactic analysis,
                    semantic similarity, word context and meaning
                    representation.

                    <br><br>

                    The objective is not simply to produce a number,
                    but to provide an understandable explanation of
                    what makes two passages similar.
                </div>

            </div>


            <div class="about-side">

                <div class="about-feature">

                    <div class="about-feature-icon">
                        📚
                    </div>

                    <div>

                        <div class="about-feature-title">
                            Academic Focus
                        </div>

                        <div class="about-feature-text">
                            Designed specifically for comparing
                            academic documents and reference material.
                        </div>

                    </div>

                </div>


                <div class="about-feature">

                    <div class="about-feature-icon">
                        🧠
                    </div>

                    <div>

                        <div class="about-feature-title">
                            NLP Driven
                        </div>

                        <div class="about-feature-text">
                            Uses multiple levels of language analysis
                            to understand document relationships.
                        </div>

                    </div>

                </div>


                <div class="about-feature">

                    <div class="about-feature-icon">
                        🔍
                    </div>

                    <div>

                        <div class="about-feature-title">
                            Explainable
                        </div>

                        <div class="about-feature-text">
                            Shows why passages are considered similar
                            instead of presenting only a final score.
                        </div>

                    </div>

                </div>

            </div>

        </div>


        <div class="about-values">

            <div class="value-card">

                <div class="value-icon">
                    📝
                </div>

                <div class="value-title">
                    Lexical Understanding
                </div>

                <div class="value-text">
                    Identifies shared vocabulary and normalized
                    word forms between documents.
                </div>

            </div>


            <div class="value-card">

                <div class="value-icon">
                    🌐
                </div>

                <div class="value-title">
                    Semantic Understanding
                </div>

                <div class="value-text">
                    Looks beyond exact wording to examine whether
                    passages convey related meanings.
                </div>

            </div>


            <div class="value-card">

                <div class="value-icon">
                    💡
                </div>

                <div class="value-title">
                    Meaningful Insights
                </div>

                <div class="value-text">
                    Presents interpretable results so users can
                    understand the relationship between passages.
                </div>

            </div>

        </div>


        <div class="about-note">

            <strong>Important:</strong>
            A similarity score indicates a linguistic or semantic
            relationship between documents. Similarity alone does
            not establish plagiarism or academic misconduct.
            ScholarShield is designed to support human review and
            interpretation.

        </div>

    </div>
    """)