# Setting Up Secrets in Streamlit Cloud

When deploying your app to Streamlit Cloud, you need to securely manage sensitive information like API keys, database credentials, and other secrets. Here's how to do it properly:

## Steps to Set Up Secrets in Streamlit Cloud

1. **Go to your app dashboard** in Streamlit Cloud.
2. **Click on your app**.
3. **Go to "Settings" > "Secrets"**.
4. **Add your secrets** in TOML format as shown below:

```toml
# Example secrets.toml format (don't add brackets around strings)
OPENAI_API_KEY = "your_actual_openai_api_key"

# Firebase Configuration
FIREBASE_API_KEY = "AIzaSyCPmEys0ywMIKcAluSdrBzd5FdtFUHiP1E"
FIREBASE_AUTH_DOMAIN = "law-enforcement-ai-training.firebaseapp.com"
FIREBASE_PROJECT_ID = "law-enforcement-ai-training"
FIREBASE_STORAGE_BUCKET = "law-enforcement-ai-training.firebasestorage.app"
FIREBASE_MESSAGING_SENDER_ID = "155395185769"
FIREBASE_APP_ID = "1:155395185769:web:ab27715c057731aa1396f8"
FIREBASE_MEASUREMENT_ID = "G-7Y6KX0NDXS"

# Firebase Service Account
FIREBASE_PRIVATE_KEY_ID = "your_private_key_id"
FIREBASE_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
YOUR_ACTUAL_PRIVATE_KEY_WITH_NEWLINES
-----END PRIVATE KEY-----"""
FIREBASE_CLIENT_EMAIL = "firebase-adminsdk-fbsvc@law-enforcement-ai-training.iam.gserviceaccount.com"
FIREBASE_CLIENT_ID = "106260104666258014774"
FIREBASE_CLIENT_CERT_URL = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40law-enforcement-ai-training.iam.gserviceaccount.com"
```

## Accessing Secrets in Your Code

In your Streamlit app, access these secrets using:

```python
import streamlit as st

# Access API key
api_key = st.secrets["OPENAI_API_KEY"]

# Access nested configurations (if you organized them that way)
# firebase_api_key = st.secrets["firebase"]["api_key"]
```

## Important Notes

1. **Never commit actual API keys** or secrets to your GitHub repository.
2. **Use placeholders in your `.env` file** for local development.
3. **Make sure `.env` is in your `.gitignore`** to prevent accidental commits.
4. For multiline secrets like private keys, use triple quotes (""") in the TOML format.
5. Streamlit Cloud automatically handles environment variables, so you don't need to configure ports, addresses, etc.

## Local Development vs. Deployment

- **Local development**: Use the `.env` file.
- **Streamlit Cloud**: Use the secrets management as described above.

## Testing Your Configuration

Add a simple check in your app to verify secrets are loaded:

```python
if "OPENAI_API_KEY" in st.secrets:
    st.success("API key configuration loaded!")
else:
    st.error("API key not found in secrets.")
``` 