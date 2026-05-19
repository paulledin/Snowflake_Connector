# Snowflake Connector

A Streamlit application for establishing and testing a connection to Snowflake using key-pair authentication. Designed to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

## Features

- Input form for Snowflake connection parameters (account, warehouse, database, schema, role)
- Key-pair authentication — no passwords; credentials stored securely in Streamlit Secrets
- On successful connection, displays current user, role, warehouse, database, schema, and Snowflake version

## Requirements

- Python 3.8+
- A Snowflake account with key-pair authentication configured for your user

## Snowflake Setup — Generate a Key Pair

Run these commands once to generate your RSA key pair:

```bash
# Generate unencrypted private key
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# Generate matching public key
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Then register the public key with your Snowflake user:

```sql
ALTER USER your_username SET RSA_PUBLIC_KEY='<contents of rsa_key.pub, header/footer removed>';
```

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

3. **Configure secrets**

   Copy the example secrets file and fill in your values:

   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

   Edit `.streamlit/secrets.toml`:

   ```toml
   [snowflake]
   user = "your_snowflake_username"
   private_key = """
   -----BEGIN PRIVATE KEY-----
   <your private key content>
   -----END PRIVATE KEY-----
   """
   ```

4. **Run the app**

   ```bash
   streamlit run SnowFlake_Connector.py
   ```

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub (already done)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account
3. Select the `paulledin/Snowflake_Connector` repo and set the main file to `SnowFlake_Connector.py`
4. Under **Advanced settings → Secrets**, paste your `[snowflake]` secrets block (same format as `secrets.toml.example`)
5. Click **Deploy**

> **Note:** `.streamlit/secrets.toml` is excluded from git via `.gitignore` — never commit your actual secrets.

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `snowflake-connector-python` | Snowflake Python connector |
| `cryptography` | RSA private key parsing |
