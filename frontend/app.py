import streamlit as st


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Admin", "Super Admin"]


def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

super_admin = st.Page(
    "super-admin/super-admin_1.py",
    title="Super Admin",
    icon=":material/healing:",
    default=(role == "Super Admin"),
)

dashboard = st.Page(
    "./pages/dashboard.py",
    title="Dashboard",
    icon=":material/home:",
)

modelling = st.Page(
    "./pages/modelling.py",
    title="Prediction",
    icon=":material/home:",
)

route_history = st.Page(
    "./pages/route_history.py",
    title="Bin Location",
    icon=":material/healing:",
)

truck_status = st.Page(
    "./pages/truck_status.py",
    title="Truck Status",
    # icon=":materiral/account",
)

history = st.Page(
    "./pages/history.py",
    title="History",
    # icon=":materiral/account",
)

account_pages = [logout_page, settings]
admin_pages = [admin_1, admin_2]
super_admin_pages = [super_admin]
menu_pages = [dashboard, modelling, route_history]


# st.title("Request manager")
st.logo("images/logo_bg.png",size= "large", icon_image="images/icon_broom.png")

page_dict = {}
if st.session_state.role in ["Admin", "Super Admin"]:
    page_dict["Admin"] = admin_pages
    page_dict["Menu"] = menu_pages

if st.session_state.role == "Super Admin":
    page_dict["Super Admin"] = super_admin_pages
    page_dict["Menu"] = menu_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
    
else:
    pg = st.navigation([st.Page(login)])

pg.run()
