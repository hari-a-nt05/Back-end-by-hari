# Fastapi Local Environment Setup

# Prerequisites
- Python 3.10+ (recommended)
- PostgreSQL (running locally)
- Git

## Steps

# Clone the repository
    ```bash
    git clone <repository-url>
    cd fastapi/
    ```

# Create and activate a virtual environment
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

# Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Configure environment variables
    
# Create a .env file in the fastapi directory with the following (adjust as needed):
    ```bash
    DATABASE_URL=postgresql://postgres:yourpassword@localhost/yourdb
    ```    
# Run database migrations
    ```bash
    alembic upgrade head
    ```
# Start the FastAPI server
    ```bash
    uvicorn app.main:app --reload
    ```
# Access the API
    Open http://localhost:8000/docs for Swagger UI.

## Microsoft Graph / Outlook integration

To enable fetching Outlook (Microsoft) mails you must register an application in Azure AD and provide the app credentials to the backend.

1. Register an app in Azure AD (App registrations) and note the Tenant ID and Client ID.
2. Under "Certificates & secrets" create a Client Secret and copy its value.
3. Under "API permissions" add Microsoft Graph -> Application permissions -> Mail.Read (or Mail.ReadWrite) and click "Grant admin consent".
4. In your backend `.env` or environment, set the following variables:

```bash
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>
# Optional: userPrincipalName or user id to query
AZURE_MAILBOX=example@yourdomain.com
```

5. Restart the backend. Use the secured endpoint to query mails:

GET /api/v1/mail/outlook/messages?mailbox=example@yourdomain.com&subject=Engineer&top=5

Notes:
- The current implementation uses client credentials (app-only). For app-only tokens you must specify the mailbox to query (userPrincipalName or id) and the app must have appropriate Application permissions and admin consent.
- If you need delegated access (on-behalf-of a user) you'll need to implement OAuth2 authorization code flow instead.
