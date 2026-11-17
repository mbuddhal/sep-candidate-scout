from __future__ import annotations

import json
import os
from typing import Iterable

import gspread
from google.oauth2.service_account import Credentials

from .models import Candidate


HEADERS = ["Name", "Grad signal", "Major / area", "Public signal", "SEP fit angle", "Cutoff status", "Source type", "Source link"]


def _client() -> gspread.Client:
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is required for Sheets writeback")
    info = json.loads(raw)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    return gspread.authorize(Credentials.from_service_account_info(info, scopes=scopes))


def append_new_candidates(candidates: Iterable[Candidate]) -> int:
    spreadsheet_id = os.getenv("SEP_SPREADSHEET_ID")
    if not spreadsheet_id:
        raise RuntimeError("SEP_SPREADSHEET_ID is required for Sheets writeback")
    sheet_name = os.getenv("SEP_SHEET_NAME", "Web Prospects")
    worksheet = _client().open_by_key(spreadsheet_id).worksheet(sheet_name)
    existing = {row[0].strip().lower() for row in worksheet.get_all_values()[1:] if row}
    new_rows = [candidate.sheet_row() for candidate in candidates if candidate.name.strip().lower() not in existing]
    if new_rows:
        worksheet.append_rows(new_rows, value_input_option="USER_ENTERED")
    return len(new_rows)
