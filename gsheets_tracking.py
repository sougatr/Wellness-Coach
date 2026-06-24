"""
WellMet — Google Sheets Usage Tracking
=======================================
Logs events to a Google Sheet for persistent tracking across deployments.
Events: metawell_page_visited, metawell_form_submitted, layer3_viewed

Requires in Streamlit secrets:
    [gcp_service_account]
    ... (full JSON key contents)
    
    [sheets]
    spreadsheet_id = "..."
    sheet_name = "Sheet1"
"""

import streamlit as st
from datetime import datetime
import uuid


def _get_client():
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes,
    )
    return gspread.authorize(creds)


def _get_sheet():
    client = _get_client()
    spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
    sheet_name = st.secrets["sheets"]["sheet_name"]
    return client.open_by_key(spreadsheet_id).worksheet(sheet_name)


def log_event(event_name: str):
    """Log a single event to Google Sheets. Fails silently."""
    try:
        # Generate or reuse a session ID
        if "session_id" not in st.session_state:
            st.session_state["session_id"] = str(uuid.uuid4())[:8]

        sheet = _get_sheet()
        sheet.append_row([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            event_name,
            st.session_state["session_id"],
        ])
    except Exception:
        pass  # Never break the app due to tracking failure


def get_summary() -> dict:
    """Return event counts as a dictionary."""
    try:
        sheet = _get_sheet()
        rows = sheet.get_all_values()
        # Skip header row
        data_rows = rows[1:] if len(rows) > 1 else []
        summary = {}
        for row in data_rows:
            if len(row) >= 2:
                event = row[1]
                summary[event] = summary.get(event, 0) + 1
        return summary
    except Exception:
        return {}


def get_recent_events(n: int = 20) -> list:
    """Return the last n events as a list of dicts."""
    try:
        sheet = _get_sheet()
        rows = sheet.get_all_values()
        data_rows = rows[1:] if len(rows) > 1 else []
        recent = data_rows[-n:]
        recent.reverse()
        return [
            {"timestamp": r[0], "event": r[1], "session_id": r[2]}
            for r in recent if len(r) >= 3
        ]
    except Exception:
        return []
