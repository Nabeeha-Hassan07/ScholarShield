import streamlit as st
from html import escape
from datetime import datetime

from database.database import (
    get_user_profile,
    get_user_profile_stats
)

from pages.authenticated_sidebar import (
    show_authenticated_sidebar
)


# =========================================================
# HELPERS
# =========================================================

def format_date(date_value):

    if not date_value:
        return "Unknown"

    try:

        date_obj = datetime.strptime(
            str(date_value),
            "%Y-%m-%d %H:%M:%S"
        )

        return date_obj.strftime(
            "%d %B %Y"
        )

    except (ValueError, TypeError):

        return str(date_value)


def format_percentage(value):

    if value is None:
        return "—"

    return f"{float(value):.0f}%"


# =========================================================
# PROFILE PAGE
# =========================================================

def profile_page():

    # -----------------------------------------------------
    # AUTHENTICATION CHECK
    # -----------------------------------------------------

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.warning(
            "Please log in to view your profile."
        )

        return


    # -----------------------------------------------------
    # USER INFORMATION
    # -----------------------------------------------------

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:

        st.error(
            "User information could not be loaded."
        )

        return


    # -----------------------------------------------------
    # LOAD PROFILE DATA
    # -----------------------------------------------------

    profile = get_user_profile(
        user_id
    )

    profile_stats = get_user_profile_stats(
        user_id
    )


    if not profile:

        st.error(
            "Profile information could not be found."
        )

        return


    user_name = escape(
        str(profile["name"])
    )

    user_email = escape(
        str(profile["email"])
    )

    joined_date = format_date(
        profile["created_at"]
    )

    total_documents = profile_stats[
        "total_documents"
    ]

    total_analyses = profile_stats[
        "total_analyses"
    ]

    average_similarity = format_percentage(
        profile_stats["average_similarity"]
    )


    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    show_authenticated_sidebar()


    # =====================================================
    # PAGE STYLING
    # =====================================================

    st.html(
        """
        <style>

        /* =================================================
       HIDE STREAMLIT TOP TOOLBAR
        ================================================= */

        [data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        /* =================================================
           PAGE BACKGROUND
        ================================================= */

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


        .block-container {

            padding:
                30px 52px 65px 52px !important;

            max-width:
                1540px !important;
        }


        /* =================================================
           SIDEBAR
        ================================================= */

        [data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    #eef2f7 0%,
                    #e9edf3 100%
                ) !important;

            border-right:
                1px solid #d9e0ea !important;
        }


        [data-testid="stSidebarNav"] {

            display: none !important;
        }


        /* =================================================
           PAGE HEADER
        ================================================= */

        .profile-header {

            position: relative;

            display: flex;

            align-items: flex-start;

            justify-content: space-between;

            gap: 30px;

            margin-bottom: 28px;
        }


        .profile-kicker {

            color: #5579cf;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 2px;

            text-transform: uppercase;

            margin-bottom: 7px;
        }


        .profile-title {

            color: #12264b;

            font-size: 40px;

            font-weight: 850;

            letter-spacing: -1.2px;

            line-height: 1.1;

            margin: 0;
        }


        .profile-title span {

            color: #4f73c8;
        }


        .profile-description {

            color: #65748c;

            font-size: 15px;

            line-height: 1.7;

            margin-top: 10px;

            max-width: 690px;
        }


        /* =================================================
           PROFILE HERO
        ================================================= */

        .profile-hero {

            position: relative;

            overflow: hidden;

            min-height: 190px;

            padding: 30px 34px;

            border-radius: 21px;

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
                rgba(27, 57, 105, 0.17);

            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 30px;
        }


        .profile-hero-content {

            position: relative;

            z-index: 2;
        }


        .profile-avatar {

            width: 76px;

            height: 76px;

            border-radius: 50%;

            background:
                rgba(255,255,255,0.15);

            border:
                1px solid
                rgba(255,255,255,0.25);

            display: flex;

            align-items: center;

            justify-content: center;

            color: #ffffff;

            font-size: 29px;

            font-weight: 800;

            box-shadow:
                0 10px 25px
                rgba(0,0,0,0.12);

            flex-shrink: 0;
        }


        .profile-hero-label {

            color:
                rgba(255,255,255,0.68);

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 1.8px;

            text-transform: uppercase;

            margin-bottom: 6px;
        }


        .profile-hero-name {

            color: #ffffff;

            font-size: 28px;

            font-weight: 800;

            line-height: 1.2;

            margin: 0;
        }


        .profile-hero-email {

            color:
                rgba(255,255,255,0.72);

            font-size: 13px;

            margin-top: 7px;
        }


        .profile-hero-decoration {

            position: absolute;

            width: 190px;

            height: 190px;

            border-radius: 50%;

            border:
                1px solid
                rgba(255,255,255,0.08);

            right: -60px;

            top: -70px;
        }


        .profile-hero-decoration::after {

            content: "";

            position: absolute;

            width: 115px;

            height: 115px;

            border-radius: 50%;

            border:
                1px solid
                rgba(255,255,255,0.08);

            right: 35px;

            top: 37px;
        }


        /* =================================================
           SECTION
        ================================================= */

        .section-block {

            margin-top: 30px;

            margin-bottom: 17px;
        }


        .section-heading {

            color: #17294d;

            font-size: 20px;

            font-weight: 800;

            line-height: 1.2;
        }


        .section-subheading {

            color: #78869b;

            font-size: 12.5px;

            margin-top: 5px;
        }


        .section-accent {

            width: 42px;

            height: 3px;

            border-radius: 20px;

            background:
                linear-gradient(
                    90deg,
                    #426dc1,
                    #8ca8e6
                );

            margin-top: 10px;
        }


        /* =================================================
           INFORMATION CARDS
        ================================================= */

        .info-card {

            background: #ffffff;

            border:
                1px solid #dee6f1;

            border-radius: 17px;

            padding: 21px;

            min-height: 120px;

            box-shadow:
                0 9px 24px
                rgba(35, 58, 95, 0.055);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }


        .info-card:hover {

            transform:
                translateY(-2px);

            box-shadow:
                0 14px 28px
                rgba(35, 58, 95, 0.09);
        }


        .info-icon {

            width: 42px;

            height: 42px;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #eef4ff,
                    #dfeaff
                );

            display: flex;

            align-items: center;

            justify-content: center;

            color: #315f9f;

            font-size: 18px;

            font-weight: 700;

            margin-bottom: 15px;
        }


        .info-label {

            color: #8491a4;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 0.8px;

            text-transform: uppercase;
        }


        .info-value {

            color: #17294d;

            font-size: 17px;

            font-weight: 750;

            margin-top: 6px;

            word-break: break-word;
        }


        .info-description {

            color: #8995a7;

            font-size: 12px;

            margin-top: 5px;
        }


        /* =================================================
           STATISTICS
        ================================================= */

        .stat-card {

            background: #ffffff;

            border:
                1px solid #dee6f1;

            border-radius: 17px;

            padding: 21px;

            min-height: 145px;

            box-shadow:
                0 9px 24px
                rgba(35, 58, 95, 0.055);

            position: relative;

            overflow: hidden;
        }


        .stat-card::after {

            content: "";

            position: absolute;

            left: 0;

            right: 0;

            bottom: 0;

            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    #426dc1,
                    #8ca8e6
                );
        }


        .stat-icon {

            width: 42px;

            height: 42px;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #eef4ff,
                    #dfeaff
                );

            display: flex;

            align-items: center;

            justify-content: center;

            color: #315f9f;

            font-size: 17px;

            margin-bottom: 13px;
        }


        .stat-label {

            color: #7d8ba0;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 0.7px;

            text-transform: uppercase;
        }


        .stat-value {

            color: #17294d;

            font-size: 29px;

            font-weight: 850;

            line-height: 1.1;

            margin-top: 5px;
        }


        .stat-subtitle {

            color: #8a96a8;

            font-size: 11.5px;

            margin-top: 5px;
        }


        /* =================================================
           ACCOUNT CARD
        ================================================= */

        .account-card {

            background:
                linear-gradient(
                    135deg,
                    #ffffff 0%,
                    #f8faff 100%
                );

            border:
                1px solid #dee6f1;

            border-radius: 17px;

            padding: 25px 26px;

            box-shadow:
                0 9px 24px
                rgba(35, 58, 95, 0.055);
        }


        .account-title {

            color: #17294d;

            font-size: 16px;

            font-weight: 800;

            margin-bottom: 5px;
        }


        .account-description {

            color: #7d8ba0;

            font-size: 12.5px;

            line-height: 1.6;
        }


        .account-row {

            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 20px;

            padding: 14px 0;

            border-bottom:
                1px solid #edf1f6;
        }


        .account-row:last-child {

            border-bottom: none;

            padding-bottom: 0;
        }


        .account-row-label {

            color: #8290a5;

            font-size: 12px;

            font-weight: 700;
        }


        .account-row-value {

            color: #24385b;

            font-size: 12.5px;

            font-weight: 700;

            text-align: right;
        }


        /* =================================================
           FOOTER
        ================================================= */

        .profile-footer {

            margin-top: 42px;

            padding-top: 20px;

            border-top:
                1px solid #e1e6ee;

            text-align: center;

            color: #98a3b3;

            font-size: 11px;
        }

        </style>
        """
    )


    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.html(
        """
        <div class="profile-header">

            <div>

                <div class="profile-kicker">
                    ACCOUNT
                </div>

                <div class="profile-title">
                    My <span>Profile</span>
                </div>

                <div class="profile-description">
                    View your ScholarShield account information
                    and analysis activity.
                </div>

            </div>

        </div>
        """
    )


    # =====================================================
    # PROFILE HERO
    # =====================================================

    initials = "".join(
        part[0]
        for part in str(profile["name"]).split()
        if part
    )[:2].upper()

    initials = escape(initials)

    st.html(
        f"""
        <div class="profile-hero">

            <div
                style="
                    display:flex;
                    align-items:center;
                    gap:22px;
                    position:relative;
                    z-index:2;
                "
            >

                <div class="profile-avatar">
                    {initials}
                </div>

                <div class="profile-hero-content">

                    <div class="profile-hero-label">
                        ScholarShield Account
                    </div>

                    <div class="profile-hero-name">
                        {user_name}
                    </div>

                    <div class="profile-hero-email">
                        {user_email}
                    </div>

                </div>

            </div>

            <div class="profile-hero-decoration"></div>

        </div>
        """
    )


    # =====================================================
    # PROFILE INFORMATION
    # =====================================================

    st.html(
        """
        <div class="section-block">

            <div class="section-heading">
                Profile Information
            </div>

            <div class="section-subheading">
                Your registered account details.
            </div>

            <div class="section-accent"></div>

        </div>
        """
    )


    info_col1, info_col2 = st.columns(2)


    with info_col1:

        st.html(
            f"""
            <div class="info-card">

                <div class="info-icon">
                    ♙
                </div>

                <div class="info-label">
                    Full Name
                </div>

                <div class="info-value">
                    {user_name}
                </div>

                <div class="info-description">
                    Name associated with your ScholarShield account.
                </div>

            </div>
            """
        )


    with info_col2:

        st.html(
            f"""
            <div class="info-card">

                <div class="info-icon">
                    @
                </div>

                <div class="info-label">
                    Email Address
                </div>

                <div class="info-value">
                    {user_email}
                </div>

                <div class="info-description">
                    Your registered account email address.
                </div>

            </div>
            """
        )


    # =====================================================
    # ACCOUNT STATISTICS
    # =====================================================

    st.html(
        """
        <div class="section-block">

            <div class="section-heading">
                Your Activity
            </div>

            <div class="section-subheading">
                A summary of your ScholarShield workspace.
            </div>

            <div class="section-accent"></div>

        </div>
        """
    )


    stat_col1, stat_col2, stat_col3 = st.columns(3)


    with stat_col1:

        st.html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ▤
                </div>

                <div class="stat-label">
                    Documents
                </div>

                <div class="stat-value">
                    {total_documents}
                </div>

                <div class="stat-subtitle">
                    Documents uploaded
                </div>

            </div>
            """
        )


    with stat_col2:

        st.html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ◈
                </div>

                <div class="stat-label">
                    Analyses
                </div>

                <div class="stat-value">
                    {total_analyses}
                </div>

                <div class="stat-subtitle">
                    Completed analyses
                </div>

            </div>
            """
        )


    with stat_col3:

        st.html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    %
                </div>

                <div class="stat-label">
                    Average Similarity
                </div>

                <div class="stat-value">
                    {average_similarity}
                </div>

                <div class="stat-subtitle">
                    Across completed analyses
                </div>

            </div>
            """
        )


    # =====================================================
    # ACCOUNT DETAILS
    # =====================================================

    st.html(
        """
        <div class="section-block">

            <div class="section-heading">
                Account Details
            </div>

            <div class="section-subheading">
                Basic information about your ScholarShield account.
            </div>

            <div class="section-accent"></div>

        </div>
        """
    )


    st.html(
        f"""
        <div class="account-card">

            <div class="account-title">
                Account Information
            </div>

            <div class="account-description">
                Your account was created when you registered
                with ScholarShield.
            </div>


            <div class="account-row">

                <div class="account-row-label">
                    Account Name
                </div>

                <div class="account-row-value">
                    {user_name}
                </div>

            </div>


            <div class="account-row">

                <div class="account-row-label">
                    Email Address
                </div>

                <div class="account-row-value">
                    {user_email}
                </div>

            </div>


            <div class="account-row">

                <div class="account-row-label">
                    Member Since
                </div>

                <div class="account-row-value">
                    {escape(joined_date)}
                </div>

            </div>


            <div class="account-row">

                <div class="account-row-label">
                    Account Status
                </div>

                <div class="account-row-value">
                    Active
                </div>

            </div>

        </div>
        """
    )


    # =====================================================
    # FOOTER
    # =====================================================

    st.html(
        """
        <div class="profile-footer">
            ScholarShield · Context-Aware Academic Similarity Analyzer
        </div>
        """
    )