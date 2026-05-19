import streamlit as st
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    PrivateFormat,
    NoEncryption,
)

st.set_page_config(page_title="Snowflake Connection Test", layout="centered")

st.title("Snowflake Connection Test")
st.markdown(
    "Credentials (username & private key) are loaded from Streamlit Secrets. "
    "Fill in the connection parameters below and click **Connect & Test**."
)

with st.form("connection_form"):
    account = st.text_input(
        "Account Identifier",
        placeholder="orgname-accountname  or  xy12345.us-east-1",
        help="Found in your Snowflake URL: https://<account>.snowflakecomputing.com",
    )
    warehouse = st.text_input("Warehouse (optional)", placeholder="COMPUTE_WH")
    database = st.text_input("Database (optional)", placeholder="MY_DATABASE")
    schema = st.text_input("Schema (optional)", placeholder="PUBLIC")
    role = st.text_input("Role (optional)", placeholder="MY_ROLE")

    submitted = st.form_submit_button("Connect & Test", type="primary")

if submitted:
    if not account.strip():
        st.error("Account identifier is required.")
        st.stop()

    # Load credentials from Streamlit Secrets
    try:
        sf = st.secrets["snowflake"]
        user = sf["user"]
        private_key_pem = sf["private_key"]
        passphrase = sf.get("private_key_passphrase", None)
        if passphrase:
            passphrase = passphrase.encode()
    except KeyError as e:
        st.error(f"Missing secret key: {e}. Check your Streamlit Secrets configuration.")
        st.stop()

    # Parse PEM private key into DER bytes required by the connector
    try:
        private_key_obj = load_pem_private_key(
            private_key_pem.encode(),
            password=passphrase,
            backend=default_backend(),
        )
        private_key_der = private_key_obj.private_bytes(
            encoding=Encoding.DER,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        )
    except Exception as e:
        st.error(f"Failed to parse private key: {e}")
        st.stop()

    conn_kwargs = {
        "account": account.strip(),
        "user": user,
        "private_key": private_key_der,
    }
    if warehouse.strip():
        conn_kwargs["warehouse"] = warehouse.strip()
    if database.strip():
        conn_kwargs["database"] = database.strip()
    if schema.strip():
        conn_kwargs["schema"] = schema.strip()
    if role.strip():
        conn_kwargs["role"] = role.strip()

    with st.spinner("Connecting to Snowflake…"):
        try:
            conn = snowflake.connector.connect(**conn_kwargs)
            cur = conn.cursor()
            cur.execute(
                "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), "
                "CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_VERSION()"
            )
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
