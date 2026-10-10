import re
import streamlit as st

from auth.auth_utils import register_user


def valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def show_register_page():

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
                url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=2200&q=90");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            padding-top: 45px !important;
            padding-bottom: 45px !important;
        }


        /* ---------- FORM INTRO ---------- */

        .register-heading {
            text-align: center;
            margin-bottom: 18px;
        }

        .register-label {
            color: #6fa5ff;
            font-size: 12px;
            font-weight: 750;
            letter-spacing: 1.8px;
        }

        .register-title {
            color: white;
            font-size: 32px;
            font-weight: 750;
            margin-top: 6px;
        }

        .register-description {
            color: #d5e0f1;
            font-size: 14px;
            line-height: 1.6;
            max-width: 520px;
            margin: 8px auto 0;
        }


        /* ---------- FORM AREA ---------- */

        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.97) !important;

            border: 1px solid rgba(210, 225, 245, 0.9) !important;

            border-radius: 16px !important;

            padding: 28px !important;

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


        /* ---------- BACK BUTTON ---------- */

        .back-area {
            text-align: center;
            margin-top: 18px;
        }

    </style>


    <div class="register-heading">

        <div class="register-label">
            SCHOLARSHIELD
        </div>

        <div class="register-title">
            Create your account
        </div>

        <div class="register-description">
            Start analyzing academic documents with
            context-aware Natural Language Processing.
        </div>

    </div>
    """)


    # =====================================================
    # REGISTRATION FORM
    # =====================================================

    with st.form("registration_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )


    # =====================================================
    # VALIDATION
    # =====================================================

    if submitted:

        if not name.strip():

            st.error("Please enter your name.")

        elif not valid_email(email):

            st.error("Please enter a valid email address.")

        elif len(password) < 6:

            st.error(
                "Password must contain at least 6 characters."
            )

        elif password != confirm_password:

            st.error("Passwords do not match.")

        else:

            success, message = register_user(
                name,
                email,
                password
            )

            if success:

                st.success(message)

                st.session_state.registration_success = True

            else:

                st.error(message)


    # =====================================================
    # NAVIGATION
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

        if st.session_state.get(
            "registration_success",
            False
        ):

            if st.button(
                "Continue to Login →",
                use_container_width=True
            ):

                st.session_state.registration_success = False

                st.query_params["auth"] = "login"

                st.rerun()