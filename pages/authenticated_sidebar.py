import streamlit as st


def inject_sidebar_styles():

    st.html("""
    <style>

    /* =========================================================
       SIDEBAR BASE
    ========================================================= */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #f4f7fc 0%,
                #edf3fb 55%,
                #e7eef8 100%
            ) !important;

        border-right: 1px solid #d5dfed !important;

        overflow: hidden !important;
    }


    /* =========================================================
       FIXED SIDEBAR VIEWPORT
    ========================================================= */

    [data-testid="stSidebar"] > div:first-child {
        height: 100vh !important;
        max-height: 100vh !important;

        overflow: hidden !important;
    }

    [data-testid="stSidebarContent"] {
        height: 100vh !important;
        max-height: 100vh !important;

        overflow: hidden !important;
    }


    /* =========================================================
       FIXED INNER CONTENT AREA
    ========================================================= */

    [data-testid="stSidebar"] .block-container {

        height: 100vh !important;
        min-height: 100vh !important;

        max-height: 100vh !important;

        box-sizing: border-box !important;

        padding-top: 27px !important;
        padding-left: 17px !important;
        padding-right: 17px !important;
        padding-bottom: 18px !important;

        overflow: hidden !important;
    }


    /* =========================================================
       NORMALIZE STREAMLIT VERTICAL SPACING
    ========================================================= */

    [data-testid="stSidebar"] .stVerticalBlock {
        gap: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    [data-testid="stSidebar"] .element-container {
        margin-bottom: 0 !important;
    }


    /* =========================================================
       REMOVE EXTRA TOP/BOTTOM SPACING FROM WIDGETS
    ========================================================= */

    [data-testid="stSidebar"] [data-testid="stRadio"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    [data-testid="stSidebar"] .stButton {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }


    /* =========================================================
       BRAND
    ========================================================= */

    .sidebar-brand {
        padding: 2px 4px 20px 4px;
    }

    .sidebar-logo {
        color: #183968;

        font-size: 18px;
        font-weight: 850;

        letter-spacing: 1.5px;
    }

    .sidebar-brand-accent {
        width: 40px;
        height: 3px;

        margin-top: 8px;

        border-radius: 4px;

        background:
            linear-gradient(
                90deg,
                #426dc1,
                #8ca8e6
            );
    }


    /* =========================================================
       USER CARD
    ========================================================= */

    .sidebar-user {

        padding: 13px 14px;

        margin-bottom: 20px;

        background: #ffffff;

        border: 1px solid #d8e2ef;

        border-radius: 12px;

        box-shadow:
            0 4px 12px rgba(37, 70, 120, 0.06);
    }

    .sidebar-user-name {

        color: #17345f;

        font-size: 13px;

        font-weight: 750;

        margin-bottom: 4px;

        white-space: nowrap;

        overflow: hidden;

        text-overflow: ellipsis;
    }

    .sidebar-user-email {

        color: #657791;

        font-size: 11px;

        line-height: 1.4;

        word-break: break-word;
    }


    /* =========================================================
       WORKSPACE LABEL
    ========================================================= */

    .sidebar-section-label {

        color: #6680a7;

        font-size: 10px;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 1.3px;

        margin: 0 4px 8px 4px;
    }


    /* =========================================================
       NAVIGATION
    ========================================================= */

    [data-testid="stSidebar"] [data-testid="stRadio"] {

        margin: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div {

        gap: 4px !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {

        min-height: 36px;

        padding: 8px 10px;

        border-radius: 9px;

        box-sizing: border-box;

        color: #43546e;

        font-size: 12.5px;

        font-weight: 550;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {

        background: #e3ecf8;

        color: #234d83;
    }

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    label[data-checked="true"] {

        background:
            linear-gradient(
                90deg,
                #d7e5f8,
                #e5edf9
            );

        color: #183d70;

        font-weight: 750;

        border-left: 3px solid #426dc1;

        padding-left: 7px;
    }


    /* =========================================================
       HIDE RADIO CIRCLES
    ========================================================= */

    [data-testid="stSidebar"]
    [data-testid="stRadio"]
    div[role="radiogroup"] > label > div:first-child {

        display: none !important;
    }


    /* =========================================================
       DIVIDER
    ========================================================= */

    .sidebar-divider {

        height: 1px;

        background: #d2ddea;

        margin: 18px 0 13px 0;
    }


    /* =========================================================
       LOGOUT
    ========================================================= */

    [data-testid="stSidebar"] .stButton {

        margin: 0 !important;
    }

    [data-testid="stSidebar"] .stButton button {

        min-height: 37px;

        border-radius: 9px;

        border: 1px solid #cfdbea;

        background: #ffffff;

        color: #4b6383;

        font-size: 12.5px;

        font-weight: 650;
    }

    [data-testid="stSidebar"] .stButton button:hover {

        background: #eaf1fb;

        border-color: #a9bdd9;

        color: #244e84;
    }


    /* =========================================================
       REMOVE SCROLLBAR
    ========================================================= */

    [data-testid="stSidebar"] ::-webkit-scrollbar {

        width: 0 !important;
        height: 0 !important;
    }

    [data-testid="stSidebar"] {

        scrollbar-width: none !important;
    }

    </style>
    """)


def show_authenticated_sidebar():

    inject_sidebar_styles()

    if "dashboard_page" not in st.session_state:
        st.session_state.dashboard_page = "Dashboard"

    with st.sidebar:

        # =====================================================
        # BRAND
        # =====================================================

        st.html("""
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                SCHOLARSHIELD
            </div>

            <div class="sidebar-brand-accent"></div>

        </div>
        """)


        # =====================================================
        # USER
        # =====================================================

        st.html(f"""
        <div class="sidebar-user">

            <div class="sidebar-user-name">
                👤 &nbsp; {st.session_state.get("user_name", "User")}
            </div>

            <div class="sidebar-user-email">
                {st.session_state.get("user_email", "")}
            </div>

        </div>
        """)


        # =====================================================
        # WORKSPACE
        # =====================================================

        st.html("""
        <div class="sidebar-section-label">
            Workspace
        </div>
        """)


        # =====================================================
        # NAVIGATION
        # =====================================================

        page_options = {
            "▣  Dashboard": "Dashboard",
            "↑  Upload Document": "Upload Document",
            "▤  My Library": "My Library",
            "⌕  Analysis": "Analysis",
            "▧  Reports": "Reports",
            "◎  Profile": "Profile"
        }

        current_page = st.session_state.dashboard_page

        current_label = next(
            (
                label
                for label, page in page_options.items()
                if page == current_page
            ),
            "▣  Dashboard"
        )

        selected_label = st.radio(
            "Navigation",
            list(page_options.keys()),
            index=list(page_options.keys()).index(current_label),
            label_visibility="collapsed",
            key="workspace_navigation"
        )

        selected_page = page_options[selected_label]


        # =====================================================
        # LOGOUT
        # =====================================================

        st.html("""
        <div class="sidebar-divider"></div>
        """)

        if st.button(
            "↪  Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.pop("user_id", None)
            st.session_state.pop("user_name", None)
            st.session_state.pop("user_email", None)

            st.session_state.dashboard_page = "Dashboard"
            st.session_state.page = "Home"

            st.query_params.clear()

            st.rerun()


        # =====================================================
        # NAVIGATION CHANGE
        # =====================================================

        if selected_page != current_page:

            st.session_state.dashboard_page = selected_page

            st.rerun()