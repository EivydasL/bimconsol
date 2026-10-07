"""Create the top-level folder structure in the BIMConSol site's default "Documents" library.

Idempotent: a folder that already exists is skipped, never an error. Safe to re-run
from any machine.

    py sharepoint/provision_structure.py --dry-run
    py sharepoint/provision_structure.py

Auth is the same client-credentials flow as bim-crm/sharepoint_client.py (MSAL +
Graph .default scope). Needs Sites.ReadWrite.All (application) — creating folders is
ordinary drive CRUD, so Sites.Manage.All is not required.
"""
import argparse
import os
import sys

import msal
import requests
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

# override=True on purpose, same as bim-crm/config.py: a stale TENANT_ID / SITE_PATH
# left in the user environment by another project must not beat this folder's .env.
load_dotenv(override=True)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]

# Folder names are ASCII on purpose: they end up in URLs and in scripts.
FOLDERS = ["Marketing-Brand", "Templates", "Knowledge", "Governance"]


def _require(name):
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"Missing {name} — copy .env.example to .env and fill it in.")
    return value


TENANT_ID = _require("TENANT_ID")
CLIENT_ID = _require("CLIENT_ID")
CLIENT_SECRET = _require("CLIENT_SECRET")
SITE_HOSTNAME = _require("SITE_HOSTNAME")
SITE_PATH = _require("SITE_PATH")

_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET,
)


def _headers():
    result = _app.acquire_token_silent(GRAPH_SCOPE, account=None)
    if not result:
        result = _app.acquire_token_for_client(scopes=GRAPH_SCOPE)
    if "access_token" not in result:
        raise RuntimeError(f"Auth failed: {result.get('error_description', result)}")
    return {"Authorization": f"Bearer {result['access_token']}"}


def get_site():
    resp = requests.get(f"{GRAPH_BASE}/sites/{SITE_HOSTNAME}:{SITE_PATH}", headers=_headers())
    resp.raise_for_status()
    return resp.json()


def get_drive(site_id):
    """The site's default document library ("Documents")."""
    resp = requests.get(f"{GRAPH_BASE}/sites/{site_id}/drive", headers=_headers())
    resp.raise_for_status()
    return resp.json()


def folder_exists(drive_id, name):
    resp = requests.get(f"{GRAPH_BASE}/drives/{drive_id}/root:/{name}", headers=_headers())
    if resp.status_code == 404:
        return False
    resp.raise_for_status()
    # A file with the same name would block the folder; treat that as an error, not "exists".
    if "folder" not in resp.json():
        raise RuntimeError(f"'{name}' exists in the library but is a file, not a folder.")
    return True


def create_folder(drive_id, name):
    """Returns True if created, False if it already existed (including a race)."""
    resp = requests.post(
        f"{GRAPH_BASE}/drives/{drive_id}/root/children",
        headers=_headers(),
        json={
            "name": name,
            "folder": {},
            # "fail" turns a duplicate into 409 instead of silently renaming to "Name 1".
            "@microsoft.graph.conflictBehavior": "fail",
        },
    )
    if resp.status_code == 409:
        return False
    resp.raise_for_status()
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="show what would be created, change nothing")
    args = parser.parse_args()

    site = get_site()
    drive = get_drive(site["id"])
    print(f"Site:    {site.get('displayName')}  ({site['webUrl']})")
    print(f"Library: {drive.get('name')}")
    print()

    created, existed = [], []
    for name in FOLDERS:
        if folder_exists(drive["id"], name):
            existed.append(name)
            print(f"  = exists   {name}")
        elif args.dry_run:
            print(f"  + would create  {name}")
        elif create_folder(drive["id"], name):
            created.append(name)
            print(f"  + created  {name}")
        else:
            existed.append(name)
            print(f"  = exists   {name}")

    print()
    if args.dry_run:
        print("Dry run — nothing was changed.")
    else:
        print(f"Created: {len(created)}   Already existed: {len(existed)}")


if __name__ == "__main__":
    main()
