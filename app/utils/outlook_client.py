"""Simple Microsoft Graph client for fetching mail using client credentials.

This module implements a minimal client that obtains an app-only access token
from Azure AD and calls the Microsoft Graph /users/{mailbox}/mailFolders/Inbox/messages
endpoint to fetch recent messages. It supports simple filtering by subject and
sender and returns a structured list.

Notes:
- Requires the application to be registered in Azure AD with the Mail.Read
  application permission (Application type) and admin consent granted.
- Uses client credentials (client id + secret + tenant id).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from app.core.config import settings
from app.utils.logging_utils import setup_logger

logger = setup_logger(__name__)


class OutlookClient:
    TOKEN_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    GRAPH_BASE = "https://graph.microsoft.com/v1.0"

    def __init__(
        self,
        *,
        tenant_id: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        self.tenant_id = tenant_id or settings.AZURE_TENANT_ID
        self.client_id = client_id or settings.AZURE_CLIENT_ID
        self.client_secret = client_secret or settings.AZURE_CLIENT_SECRET
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            logger.warning("Azure AD credentials are not fully configured in settings")

    def _get_token(self) -> Optional[str]:
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            return None
        url = self.TOKEN_URL.format(tenant=self.tenant_id)
        data = {
            "client_id": self.client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        resp = requests.post(url, data=data)
        if resp.status_code != 200:
            logger.error(
                "Failed to obtain token from Azure AD: status=%s, response=%s, data=%s",
                resp.status_code,
                resp.text,
                {
                    k: v for k, v in data.items() if k != "client_secret"
                },  # Log data without secret
            )
            return None
        token = resp.json().get("access_token")
        return token

    def get_recent_messages(
        self,
        mailbox: Optional[str] = None,
        top: int = 10,
        subject_contains: Optional[str] = None,
        from_address: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch recent messages from the mailbox Inbox.

        Returns a list of messages with keys: id, subject, from, receivedDateTime, bodyPreview
        """
        token = self._get_token()
        if token is None:
            raise RuntimeError("Unable to get access token for Microsoft Graph")

        mailbox = mailbox or settings.AZURE_MAILBOX
        if not mailbox:
            # If no mailbox is specified, use the /me endpoint (not valid for app-only tokens).
            # For app-only tokens you must specify a user id or userPrincipalName: /users/{id|userPrincipalName}
            raise ValueError(
                "Mailbox must be provided when using app-only tokens. Set AZURE_MAILBOX or pass mailbox parameter."
            )

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        # Build query parameters
        params = {
            "$top": str(top),
            "$select": "id,subject,from,receivedDateTime,bodyPreview",
        }

        # OData filter construction (server-side filtering limited for body/subject contains)
        filters: List[str] = []
        if subject_contains:
            # use contains on subject
            safe_subject = subject_contains.replace("'", "''")
            filters.append(f"contains(subject,'{safe_subject}')")
        if from_address:
            safe_from = from_address.replace("'", "''")
            filters.append(f"from/emailAddress/address eq '{safe_from}'")
        if filters:
            params["$filter"] = " and ".join(filters)

        url = f"{self.GRAPH_BASE}/users/{mailbox}/mailFolders/Inbox/messages"
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            logger.error(
                "Graph messages request failed: status=%s, url=%s, params=%s, response=%s",
                resp.status_code,
                url,
                params,
                resp.text,
            )
            raise RuntimeError(
                f"Graph API error: {resp.status_code} - {resp.text[:200]}"
            )

        data = resp.json()
        messages = data.get("value", [])
        return messages


def get_outlook_client() -> OutlookClient:
    return OutlookClient()
