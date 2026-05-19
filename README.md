# Snowflake Connector

A Streamlit application for establishing and testing a connection to Snowflake. Protected by Auth0 OIDC login and uses key-pair authentication for Snowflake. Designed to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

## Features

- Auth0 OIDC login gate — only authenticated users can access the app
- Input form for Snowflake connection parameters (account, warehouse, database, schema, role)
- Key-pair authentication for Snowflake — no passwords stored
- On successful connection, displays current user, role, warehouse, database, schema, and Snowflake version

## Requirements

- Python 3.8+
- An [Auth0](https://auth0.com) account (free tier works)
- A Snowflake account with key-pair authentication configured for your user

---

## Auth0 Setup

1. In Auth0, create a new **Regular Web Application**
2. Under **Allowed Callback URLs**, add:
   - Local: `http://localhost:8501/oauth2callback`
   - Cloud: `https://<your-app>.streamlit.app/oauth2callback`
3. Note your **Client ID**, **Client Secret**, and **Domain** (`<tenant>.auth0.com`)

---

## Snowflake Key-Pair Setup

Run these commands once to generate your RSA key pair:

```bash
# Generate unencrypted private key
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# Generate matching public key
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Register the public key with your Snowflake user:

```sql
ALTER USER your_username SET RSA_PUBLIC_KEY='<contents of rsa_key.pub, header/footer removed>';
```

---

## Local Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/paulledin/Snowflake_Connector.git
   cd Snowflake_Connector
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Auth0 credentials** — copy `.env.example` to `.env` and fill in your values:

   ```bash
   cp .env.example .env
   ```

   ```ini
   REDIRECT_URI=http://localhost:8501/oauth2callback
   COOKIE_SECRET=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
   CLIENT_ID=<Auth0 Client ID>
   CLIENT_SECRET=<Auth0 Client Secret>
   AUTH0_METADATA_URL=https://<tenant>.auth0.com/.well-known/openid-configuration
   ```

4. **Configure Snowflake credentials** — copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your values (only the `[snowflake]` section is needed locally):

   ```toml
   [snowflake]
   user = "your_snowflake_username"
   private_key = """
   -----BEGIN PRIVATE KEY-----
   <your private key content>
   -----END PRIVATE KEY-----
   """
   ```

5. **Run the app**

   ```bash
   streamlit run SnowFlake_Connector.py
   ```

---

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub account, and select the `paulledin/Snowflake_Connector` repo with `SnowFlake_Connector.py` as the main file
3. Under **Advanced settings → Secrets**, paste the full contents of `.streamlit/secrets.toml.example` with real values filled in (both `[snowflake]` and `[auth]` sections)
4. Click **Deploy**

> **Note:** `.env` and `.streamlit/secrets.toml` are excluded from git via `.gitignore` — never commit your actual secrets.

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `snowflake-connector-python` | Snowflake Python connector |
| `cryptography` | RSA private key parsing |
| `python-dotenv` | Load Auth0 config from `.env` locally |
