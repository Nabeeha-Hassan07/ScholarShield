import streamlit as st

from auth.auth_utils import authenticate_user


def show_login_page():

    # =====================================================
    # PAGE BACKGROUND + STYLING
    # =====================================================

    st.html("""
    <style>

        [data-testid="stAppViewContainer"] {
            background:
                linear-gradient(
                    90deg,
                    rgba(7, 20, 40, 0.88),
                    rgba(12, 28, 55, 0.70)
                ),
                url("https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=2200&q=90");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            padding-top: 55px !important;
            padding-bottom: 45px !important;
        }


        /* ---------- LOGIN INTRO ---------- */

        .login-heading {
            text-align: center;
            margin-bottom: 18px;
        }

        .login-label {
            color: #6fa5ff;
            font-size: 12px;
            font-weight: 750;
            letter-spacing: 1.8px;
        }

        .login-title {
            color: white;
            font-size: 34px;
            font-weight: 750;
            margin-top: 6px;
        }

        .login-description {
            color: #d5e0f1;
            font-size: 14px;
            line-height: 1.6;
            max-width: 520px;
            margin: 8px auto 0;
        }


        /* ---------- FORM ---------- */

        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.97) !important;

            border: 1px solid rgba(210,225,245,0.9) !important;

            border-radius: 16px !important;

            padding: 30px !important;

            box-shadow:
                0 20px 55px rgba(0,0,0,0.25) !important;

            max-width: 500px;

            margin: auto;
        }


        /* ---------- INPUTS ---------- */

        div[data-testid="stForm"] label {
            color: #243858 !important;
            font-size: 13px !important;
            font-weight: 650 !important;
        }

        div[data-testid="stForm"] input {
            border-radius: 9px !important;
            border: 1px solid #d3deed !important;
            background: #f9fbfe !important;
        }


        /* ---------- BUTTON ---------- */

        div[data-testid="stFormSubmitButton"] button {

            background:
                linear-gradient(
                    135deg,
                    #4b91ff,
                    #785be7
                ) !important;

            color: white !important;

            border: none !important;

            border-radius: 9px !important;

            height: 44px !important;

            font-weight: 700 !important;

            margin-top: 8px !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover {

            box-shadow:
                0 7px 20px rgba(81,110,230,0.30);
        }

    </style>


    <div class="login-heading">

        <div class="login-label">
            SCHOLARSHIELD
        </div>

        <div class="login-title">
            Welcome back
        </div>

        <div class="login-description">
            Sign in to access your academic documents,
            similarity analyses and reports.
        </div>

    </div>

    """)


    # =====================================================
    # LOGIN FORM
    # =====================================================

    with st.form("login_form"):

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True
        )


    # =====================================================
    # LOGIN VALIDATION
    # =====================================================

    if submitted:

        if not email.strip():

            st.error(
                "Please enter your email address."
            )

        elif not password:

            st.error(
                "Please enter your password."
            )

        else:

            user = authenticate_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.user_name = user["name"]
                st.session_state.user_email = user["email"]
                st.session_state.page = "Dashboard"

                # Keep a small session marker so refresh restores the dashboard
                st.query_params["session"] = "authenticated"

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )


    # =====================================================
    # BACK BUTTON
    # =====================================================

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "← Back to ScholarShield",
            use_container_width=True
        ):

            st.query_params.clear()
            st.rerun()