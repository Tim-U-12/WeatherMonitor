from ftplib import FTP
from pathlib import Path

def download_bom_forecast():
    """
    Downloads the Melbourne metropolitan (Frankston-inclusive) forecast text
    from the Bureau of Meteorology and saves it to the local data directory.
    """
    # FTP connection details
    ftp_host = "ftp.bom.gov.au"
    ftp_dir = "/anon/gen/fwo"
    filename = "IDV10460.txt"  # Melbourne metro forecast (includes Frankston)

    # Define output path
    data_dir = Path(__file__).resolve().parents[2] / "data"
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / filename

    print(f"Connecting to {ftp_host} ...")
    ftp = FTP(ftp_host)
    ftp.login()

    print(f"Navigating to {ftp_dir} ...")
    ftp.cwd(ftp_dir)

    print(f"Downloading {filename} ...")
    with open(file_path, "wb") as f:
        ftp.retrbinary(f"RETR {filename}", f.write)

    ftp.quit()
    print(f"✅ Downloaded {filename} successfully to {file_path}")

    return file_path