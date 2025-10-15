"""
eqserver_tools.downloader
-------------------------

Utilities for downloading waveform and metadata archives
from EqServer instances (e.g. AGOSLOG or MEIPROC).
"""

import os
import time
from datetime import datetime
from urllib.parse import urlencode
from zipfile import ZipFile
import requests
from requests.auth import HTTPBasicAuth

def download_eqserver_waveform(
    start_time: datetime,
    duration: int,
    destination: str,
    sitelist: str,
    server_url: str,
    auth_username: str = None,
    auth_password: str = None,
    fileformat: str = "mszip",
    unzip: bool = True,
    verify_ssl: bool = True,
    retries: int = 3,
    retry_delay: float = 2.0,
) -> str:
    """
    Download waveform data from an EqServer instance.

    Parameters
    ----------
    start_time : datetime
        UTC datetime for the start of the waveform window.
    duration : int
        Duration in minutes (max 1440).
    destination : str
        Directory where the file will be saved.
    sitelist : str
        Comma-separated station list (e.g., "GECK1,GECK2").
    server_url : str
        Base EqServer extractor URL.
    auth_username, auth_password : str, optional
        Basic auth credentials if required.
    fileformat : str
        Usually 'mszip' or 'miniseed'.
    unzip : bool
        If True and fileformat is 'mszip', extract after download.
    verify_ssl : bool
        Disable for internal self-signed certs (use with caution).
    """

    os.makedirs(destination, exist_ok=True)

    params = {
        "year": start_time.year,
        "month": start_time.month,
        "day": start_time.day,
        "hour": start_time.hour,
        "minute": start_time.minute,
        "duration": duration,
        "servernum": 0,
        "conttrig": 0,
        "sitechoice": "list",
        "sitelist": sitelist,
        "siteradius": "",
        "closesite": "",
        "radius": "",
        "latitude": "",
        "longitude": "",
        "fileformat": fileformat,
    }

    query = urlencode(params)
    url = f"{server_url}?{query}&getwave=Get+Waveform"

    print(f"Requesting: {url}")

    auth = None
    if auth_username and auth_password:
        auth = HTTPBasicAuth(auth_username, auth_password)

    for attempt in range(retries):
        try:
            r = requests.get(url, auth=auth, timeout=120, verify=verify_ssl)
            r.raise_for_status()
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(retry_delay)
    else:
        raise ConnectionError("Failed to download after retries.")

    # Save file
    fname = f"{start_time.strftime('%Y%m%d_%H%M')}_{sitelist}.{fileformat}"
    fpath = os.path.join(destination, fname)
    with open(fpath, "wb") as f:
        f.write(r.content)

    print(f"Saved: {fpath}")

    # Optionally unzip
    if unzip and fileformat == "mszip":
        extract_dir = os.path.splitext(fpath)[0]
        with ZipFile(fpath, "r") as z:
            z.extractall(extract_dir)
        print(f"Extracted to: {extract_dir}")
        return extract_dir

    return fpath