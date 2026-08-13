# run.py

"""
- queries conklin loaners notion db
- update date notified property if email property ends in rundlecollege.ca
- notion automation sends email when date notified is updated
- run every weekday @ 15:00 using launchctl
"""

from dotenv import load_dotenv
import os
import datetime
import requests
import certifi
import tempfile
import json
from pathlib import Path

load_dotenv()
TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = os.getenv("DB_ID")
HEADERS = {
  "Authorization": f"Bearer {TOKEN}",
  "Content-Type": "application/json",
  "Accept": "application/json",
  "Notion-Version": "2025-09-03",
}


def get_ca_bundle():
  # merge the default trust store with the cloudflare gateway root cert
  # (if present) rather than replacing it, so this works both on machines
  # behind a TLS-inspecting gateway and machines with a direct connection
  cert_path = Path(__file__).parent / "cert.pem"
  if not cert_path.exists():
    print(f"Warning: CA bundle not found at {cert_path} — using default trust store")
    return certifi.where()

  combined_path = Path(tempfile.gettempdir()) / "loaner_notify_ca_bundle.pem"
  default_bundle = Path(certifi.where()).read_bytes()
  gateway_cert = cert_path.read_bytes()
  combined_path.write_bytes(default_bundle + b"\n" + gateway_cert)
  print(f"Using merged CA bundle ({cert_path.name} + certifi) for SSL verification")
  return str(combined_path)


CA_BUNDLE = get_ca_bundle()



def get_timestamp():
  # format as YYYY-MM-DDTHH:mm:ss.sss+HH:MM
  mst = datetime.timezone(datetime.timedelta(hours=-7))
  now_mst = datetime.datetime.now(tz=mst)
  offset = now_mst.strftime("%z")      # "-0700"
  offset = offset[:-2] + ":" + offset[-2:]  # "-07:00"
  mst_iso_ms = f"{now_mst.strftime('%Y-%m-%dT%H:%M:%S')}.{now_mst.microsecond//1000:03d}{offset}"
  # print(f"Sending timestamp {mst_iso_ms}")
  return mst_iso_ms

def update_page(page_id):
  global HEADERS

  entry_url = f"https://api.notion.com/v1/pages/{page_id}"
  headers = HEADERS
  payload = {
    "in_trash": False,
    "erase_content": False,
    "properties": {
      "Date Notified": {
        "id": "FJio",
        "type": "date",
        "date": {
          "start": get_timestamp(),
          "end": None,
          "time_zone": None,
        }
      }
    }
  }
  response = requests.patch(entry_url, json=payload, headers=headers, verify=CA_BUNDLE)
  print(response.json())
  return response.json()



def main():
  global DB_ID, HEADERS

  db_url = f"https://api.notion.com/v1/data_sources/{DB_ID}/query"
  headers = HEADERS
  payload = {
    "filter": {
      "property": "Email",
      "rich_text": {
        "ends_with": "rundlecollege.ca"
      }
    }
  }
  response = requests.post(db_url, json=payload, headers=headers, verify=CA_BUNDLE)

  # update pages from db query
  results = []
  for page in response.json()["results"]:
    current_id = page["id"]
    response = update_page(current_id)
    results.append(response["properties"])

  with open("result.json", "w") as f:
    json.dump(results, f, indent=2)



if __name__ == "__main__":
  # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  main()
