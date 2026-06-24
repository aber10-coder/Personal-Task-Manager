import streamlit as st
import requests

API = "http://127.0.0.1:8000"

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="wide"
)

# ── Styling ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
    }
    .task-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #4CAF50;
    }
    .task-card.pending   { border-left-color: #FF9800; }
    .task-card.in_progress { border-left-color: #2196F3; }
    .task-card.done      { border-left-color: #4CAF50; }
    .priority-high   { color: #e53935; font-weight: 600; }
    .priority-medium { color: #FB8C00; font-weight: 600; }
    .priority-low    { color: #43A047; font-weight: 600; }
    .metric-box {
        background: #f0f4ff;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ─────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None
if "page" not in st.session_state:
    st.session_state.page = "login"


# ── Helper: auth header ────────────────────────────────────
def auth_header():
    return {"Authorization": f"Bearer {st.session_state.token}"}


# ── API calls ──────────────────────────────────────────────
def api_register(email, password):
    return requests.post(f"{API}/auth/register", json={"email": email, "password": password})

def api_login(email, password):
    return requests.post(f"{API}/auth/login", json={"email": email, "password": password})

def api_get_tasks(status=None, priority=None):
    params = {}
    if status:   params["status"] = status
    if priority: params["priority"] = priority
    return requests.get(f"{API}/tasks/", headers=auth_header(), params=params)

def api_create_task(title, description, priority, due_date):
    return requests.post(f"{API}/tasks/", headers=auth_header(), json={
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date
    })

def api_update_task(task_id, title, description, priority, status, due_date):
    return requests.put(f"{API}/tasks/{task_id}", headers=auth_header(), json={
        "title": title,
        "description": description,
        "priority": priority,
        "status": status,
        "due_date": due_date
    })

def api_delete_task(task_id):
    return requests.delete(f"{API}/tasks/{task_id}", headers=auth_header())

def api_update_status(task_id, status):
    return requests.patch(f"{API}/tasks/{task_id}/status", headers=auth_header(), json={"status": status})

def api_summary():
    return requests.get(f"{API}/tasks/summary", headers=auth_header())


# ══════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 👋 Welcome back")
        st.markdown("Log in to manage your tasks.")
        st.divider()

        email    = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Login", type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    res = api_login(email, password)
                    if res.status_code == 200:
                        st.session_state.token = res.json()["token"]
                        st.session_state.email = email
                        st.session_state.page  = "dashboard"
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        with col_b:
            if st.button("Create account"):
                st.session_state.page = "register"
                st.rerun()


# ══════════════════════════════════════════════════════════
#  REGISTER PAGE
# ══════════════════════════════════════════════════════════
def show_register():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 📝 Create account")
        st.divider()

        email    = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Register", type="primary"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    res = api_register(email, password)
                    if res.status_code == 201:
                        st.success("Account created! Please log in.")
                        st.session_state.page = "login"
                        st.rerun()
                    elif res.status_code == 400:
                        st.error("Email already exists.")
                    else:
                        st.error("Something went wrong.")

        with col_b:
            if st.button("Back to login"):
                st.session_state.page = "login"
                st.rerun()


# ══════════════════════════════════════════════════════════
#  DASHBOARD PAGE
# ══════════════════════════════════════════════════════════
def show_dashboard():

    # ── Sidebar ───────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### ✅ Task Manager")
        st.markdown(f"Logged in as **{st.session_state.email}**")
        st.divider()

        if st.button("➕  New Task"):
            st.session_state.page = "create"
            st.rerun()

        if st.button("📋  My Tasks"):
            st.session_state.page = "dashboard"
            st.rerun()

        st.divider()

        if st.button("🚪  Logout"):
            st.session_state.token = None
            st.session_state.email = None
            st.session_state.page  = "login"
            st.rerun()

    # ── Summary metrics ───────────────────────────────────
    st.markdown("## 📊 Overview")

    res = api_summary()
    if res.status_code == 200:
        s = res.json()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total",       s["total"])
        c2.metric("Pending",     s["pending"])
        c3.metric("In Progress", s["in_progress"])
        c4.metric("Done",        s["done"])

    st.divider()

    # ── Filters ───────────────────────────────────────────
    st.markdown("## 📋 My Tasks")

    f1, f2 = st.columns(2)
    with f1:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "pending", "in_progress", "done"]
        )
    with f2:
        filter_priority = st.selectbox(
            "Filter by priority",
            ["All", "high", "medium", "low"]
        )

    status_param   = None if filter_status   == "All" else filter_status
    priority_param = None if filter_priority == "All" else filter_priority

    # ── Task list ─────────────────────────────────────────
    res = api_get_tasks(status_param, priority_param)

    if res.status_code != 200:
        st.error("Failed to load tasks.")
        return

    tasks = res.json()

    if not tasks:
        st.info("No tasks found. Create one!")
        return

    for task in tasks:
        status_color = {
            "pending":     "🟠",
            "in_progress": "🔵",
            "done":        "🟢"
        }.get(task["status"], "⚪")

        priority_color = {
            "high":   "🔴",
            "medium": "🟡",
            "low":    "🟢"
        }.get(task["priority"], "⚪")

        with st.expander(f"{status_color} {task['title']}  —  {priority_color} {task['priority'].capitalize()}"):

            col_info, col_actions = st.columns([3, 1])

            with col_info:
                st.markdown(f"**Description:** {task['description'] or '—'}")
                st.markdown(f"**Status:** `{task['status']}`")
                st.markdown(f"**Priority:** `{task['priority']}`")
                st.markdown(f"**Due date:** {task['due_date'] or '—'}")

            with col_actions:
                # Quick status update
                new_status = st.selectbox(
                    "Change status",
                    ["pending", "in_progress", "done"],
                    index=["pending", "in_progress", "done"].index(task["status"]),
                    key=f"status_{task['id']}"
                )
                if st.button("Update status", key=f"upd_{task['id']}"):
                    r = api_update_status(task["id"], new_status)
                    if r.status_code == 200:
                        st.success("Status updated!")
                        st.rerun()
                    else:
                        st.error("Failed to update.")

                if st.button("✏️ Edit", key=f"edit_{task['id']}"):
                    st.session_state.edit_task = task
                    st.session_state.page = "edit"
                    st.rerun()

                if st.button("🗑️ Delete", key=f"del_{task['id']}"):
                    r = api_delete_task(task["id"])
                    if r.status_code == 200:
                        st.success("Task deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete.")


# ══════════════════════════════════════════════════════════
#  CREATE TASK PAGE
# ══════════════════════════════════════════════════════════
def show_create():
    with st.sidebar:
        st.markdown(f"### ✅ Task Manager")
        st.markdown(f"Logged in as **{st.session_state.email}**")
        st.divider()
        if st.button("⬅️  Back to tasks"):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("🚪  Logout"):
            st.session_state.token = None
            st.session_state.email = None
            st.session_state.page  = "login"
            st.rerun()

    st.markdown("## ➕ New Task")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        title       = st.text_input("Title *", placeholder="e.g. Fix login bug")
        description = st.text_area("Description", placeholder="Optional details...")
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        due_date = st.date_input("Due date (optional)")

    due_date_str = str(due_date) if due_date else None

    if st.button("Create Task", type="primary"):
        if not title:
            st.error("Title is required.")
        else:
            res = api_create_task(title, description, priority, due_date_str)
            if res.status_code == 200:
                st.success("Task created!")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Failed to create task.")


# ══════════════════════════════════════════════════════════
#  EDIT TASK PAGE
# ══════════════════════════════════════════════════════════
def show_edit():
    with st.sidebar:
        st.markdown(f"### ✅ Task Manager")
        st.markdown(f"Logged in as **{st.session_state.email}**")
        st.divider()
        if st.button("⬅️  Back to tasks"):
            st.session_state.page = "dashboard"
            st.rerun()
        if st.button("🚪  Logout"):
            st.session_state.token = None
            st.session_state.email = None
            st.session_state.page  = "login"
            st.rerun()

    task = st.session_state.get("edit_task")
    if not task:
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown(f"## ✏️ Edit Task")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        title       = st.text_input("Title",       value=task["title"])
        description = st.text_area("Description",  value=task["description"] or "")
    with col2:
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=["low", "medium", "high"].index(task["priority"])
        )
        status = st.selectbox(
            "Status",
            ["pending", "in_progress", "done"],
            index=["pending", "in_progress", "done"].index(task["status"])
        )
        due_date = st.text_input("Due date", value=task["due_date"] or "")

    if st.button("Save changes", type="primary"):
        if not title:
            st.error("Title is required.")
        else:
            res = api_update_task(
                task["id"], title, description,
                priority, status, due_date or None
            )
            if res.status_code == 200:
                st.success("Task updated!")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Failed to update task.")


# ══════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════
if st.session_state.token is None:
    if st.session_state.page == "register":
        show_register()
    else:
        show_login()
else:
    if st.session_state.page == "create":
        show_create()
    elif st.session_state.page == "edit":
        show_edit()
    else:
        show_dashboard()