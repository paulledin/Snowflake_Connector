import streamlit as st
import snowflake.connector

st.set_page_config(page_title="Snowflake Connection Test", layout="centered")

st.title("Snowflake Connection Test")
st.markdown("Enter your Snowflake connection details below. Authentication uses SSO (browser-based).")

with st.form("connection_form"):
    account = st.text_input(
        "Account Identifier",
        placeholder="orgname-accountname  or  xy12345.us-east-1",
        help="Found in Snowflake URL: https://<account>.snowflakecomputing.com",
    )
    username = st.text_input("Username / Email", placeholder="you@example.com")
    warehouse = st.text_input("Warehouse (optional)", placeholder="COMPUTE_WH")
    database = st.text_input("Database (optional)", placeholder="MY_DATABASE")
    schema = st.text_input("Schema (optional)", placeholder="PUBLIC")
    role = st.text_input("Role (optional)", placeholder="MY_ROLE")

    submitted = st.form_submit_button("Connect & Test", type="primary")

if submitted:
    if not account or not username:
        st.error("Account identifier and username are required.")
        st.stop()

    conn_kwargs = {
        "account": account.strip(),
        "user": username.strip(),
        "authenticator": "externalbrowser",
    }
    if warehouse.strip():
        conn_kwargs["warehouse"] = warehouse.strip()
    if database.strip():
        conn_kwargs["database"] = database.strip()
    if schema.strip():
        conn_kwargs["schema"] = schema.strip()
    if role.strip():
        conn_kwargs["role"] = role.strip()

    with st.spinner("Opening browser for SSO login — complete the login, then return here…"):
        try:
            conn = snowflake.connector.connect(**conn_kwargs)
            cur = conn.cursor()

            cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_VERSION()")
            row = cur.fetchone()

            st.success("Connection successful!")
            st.table(
                {
                    "Property": ["User", "Role", "Warehouse", "Database", "Schema", "Snowflake Version"],
                    "Value": [str(v) if v is not None else "—" for v in row],
                }
            )

            cur.close()
            conn.close()

        except Exception as e:
            st.error(f"Connection failed: {e}")
