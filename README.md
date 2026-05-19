# Snowflake Connector

A Streamlit application for establishing and testing a connection to Snowflake using SSO (browser-based) authentication.

## Features

- Input form for Snowflake connection parameters (account, username, warehouse, database, schema, role)
- SSO / ExternalBrowser authentication — no passwords stored
- On successful connection, displays current user, role, warehouse, database, schema, and Snowflake version

## Requirements

- Python 3.8+
- A Snowflake account with SSO enabled

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/paulledin/Snowflake_Connector.git
   cd Snowflake_Connector
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run SnowFlake_Connector.py
   ```

## Usage

1. Enter your **Snowflake Account Identifier** (e.g. `orgname-accountname` or `xy12345.us-east-1`)
2. Enter your **Username / Email**
3. Optionally specify a Warehouse, Database, Schema, and Role
4. Click **Connect & Test** — your browser will open for SSO login
5. After authenticating, return to the app to see your connection details

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `snowflake-connector-python` | Snowflake Python connector |
