from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.auth import get_current_user
from app.utils.logging_utils import setup_logger
from app.utils.outlook_client import get_outlook_client

logger = setup_logger(__name__)

router = APIRouter()


class OutlookMessageOut(dict):
    """Lightweight dict-like model for response (we keep simple to avoid Pydantic overhead)."""


@router.get("/outlook/messages", response_model=List[dict])
def get_outlook_messages(
    subject: Optional[str] = Query(
        None, description="Filter messages where subject contains this string"
    ),
    from_address: Optional[str] = Query(
        None, description="Filter messages from this email address"
    ),
    mailbox: Optional[str] = Query(
        None, description="Mailbox userPrincipalName or id to query"
    ),
    top: int = Query(10, ge=1, le=50),
    user=Depends(get_current_user),
):
    """Return recent messages from an Outlook mailbox using Microsoft Graph (app-only).

    Requires AZURE_* settings configured in the backend environment. For app-only tokens
    the mailbox param must be a valid userPrincipalName or id that the app has access to.
    """
    client = get_outlook_client()
    try:
        messages = client.get_recent_messages(
            mailbox=mailbox,
            top=top,
            subject_contains=subject,
            from_address=from_address,
        )
    except ValueError as ve:
        logger.error(
            "Invalid request parameters: %s, params: mailbox=%s subject=%s from=%s",
            str(ve),
            mailbox,
            subject,
            from_address,
        )
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(
            "Failed to fetch messages: %s, params: mailbox=%s subject=%s from=%s",
            str(e),
            mailbox,
            subject,
            from_address,
        )
        raise HTTPException(status_code=502, detail=f"Failed to fetch messages: {e}")

    logger.info(
        "Successfully fetched %d messages for mailbox=%s subject=%s from=%s",
        len(messages),
        mailbox,
        subject,
        from_address,
    )
    # Return relevant fields only
    out = []
    for m in messages:
        out.append(
            {
                "id": m.get("id"),
                "subject": m.get("subject"),
                "from": m.get("from", {}).get("emailAddress", {}),
                "receivedDateTime": m.get("receivedDateTime"),
                "bodyPreview": m.get("bodyPreview"),
            }
        )
    return out
