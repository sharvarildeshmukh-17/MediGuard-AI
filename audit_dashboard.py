
import streamlit as st
import pandas as pd

from services.audit_service import get_audit_logs


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MediGuard AI - Audit Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 MediGuard AI")
st.subheader("Admin Audit Dashboard")

st.caption("Monitor chatbot interactions and safety events.")

# ==========================================
# ADMIN AUTHENTICATION
# ==========================================

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:

    st.markdown("### 🔐 Administrator Login")

    password = st.text_input(
        "Admin Password",
        type="password"
    )

    if st.button("Login", use_container_width=True):

        expected_password = st.secrets.get(
            "AUDIT_DASHBOARD_PASSWORD",
            ""
        )

        if expected_password and password == expected_password:

            st.session_state.admin_authenticated = True
            st.rerun()

        else:
            st.error("Invalid password or missing dashboard configuration.")

    st.stop()


# ==========================================
# LOAD AUDIT DATA
# ==========================================

logs = get_audit_logs(limit=1000)

if not logs:

    st.info("No audit records are available yet.")
    st.stop()

df = pd.DataFrame(logs)

# ==========================================
# DASHBOARD FILTERS
# ==========================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    selected_status = st.selectbox(
        "Filter by status",
        ["ALL"] + sorted(df["response_status"].dropna().unique().tolist())
    )

with col2:

    selected_category = st.selectbox(
        "Filter by category",
        ["ALL"] + sorted(df["category"].dropna().unique().tolist())
    )

filtered_df = df.copy()

if selected_status != "ALL":

    filtered_df = filtered_df[
        filtered_df["response_status"] == selected_status
    ]

if selected_category != "ALL":

    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]


# ==========================================
# METRICS
# ==========================================

st.markdown("### 📈 Interaction Overview")

total = len(df)

successful = int(
    (df["response_status"] == "SUCCESS").sum()
)

blocked = int(
    (df["response_status"] == "BLOCKED").sum()
)

fallback = int(
    (df["response_status"] == "FALLBACK").sum()
)

errors = int(
    (df["response_status"] == "ERROR").sum()
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Events", total)
c2.metric("Successful", successful)
c3.metric("Blocked", blocked)
c4.metric("Fallback", fallback)
c5.metric("Errors", errors)


# ==========================================
# EVENT BREAKDOWN
# ==========================================

st.markdown("---")
st.markdown("### 📊 Event Category Breakdown")

category_counts = (
    df["category"]
    .fillna("UNKNOWN")
    .value_counts()
)

st.bar_chart(category_counts)


# ==========================================
# RECENT AUDIT RECORDS
# ==========================================

st.markdown("---")
st.markdown("### 📋 Recent Audit Records")

display_columns = [
    "id",
    "timestamp",
    "event_type",
    "category",
    "user_message",
    "response_status",
    "error_message"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)


# ==========================================
# CSV EXPORT
# ==========================================

st.markdown("---")
st.markdown("### 📥 Export Audit Records")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Audit Report (CSV)",
    data=csv_data,
    file_name="mediguard_audit_report.csv",
    mime="text/csv",
    use_container_width=True
)


# ==========================================
# ADMIN CONTROLS
# ==========================================

st.markdown("---")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

if st.button("Logout"):
    st.session_state.admin_authenticated = False
    st.rerun()

st.caption(
    "MediGuard AI | Restricted Administrator Dashboard"
)
