import pandas as pd
import gdown
import os
import re

SHEET_ID = "1VJ6imjsh1XbJ-T3CzF6z-vtVP_Yyg_BYRKIzdvMSb3c"
# 🔗 Paste your Google Sheet CSV export link here (from File > Share > Anyone with the link)
sheet_csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 📁 Folder to save match files
download_dir = "matches"
os.makedirs(download_dir, exist_ok=True)

# 🧾 Read the Google Sheet
df = pd.read_csv(sheet_csv_url, header=None)
latest_link = df.iloc[-1, 0]

try:
    # 🔍 Extract match number (e.g., match5.xlsx)
    match_num = re.search(r'match(\\d+)', latest_link, re.IGNORECASE)
    if match_num:
        file_number = match_num.group(1)
        filename = f"match{file_number}.xlsx"
    else:
        filename = f"match_latest.xlsx" 

    output_path = os.path.join(download_dir, filename)

    if os.path.exists(output_path):
        print(f"✅ {filename} already exists. No download needed.")
    else:
        file_id = latest_link.split("/d/")[1].split("/")[0]
        url = f"https://drive.google.com/uc?id={file_id}"

        print(f"📥 Downloading {filename} from {url}...")
        gdown.download(url, output_path, quiet=False)
        print(f"✅ {filename} downloaded successfully!")
except Exception as e:
    print(f"❌ Failed to process or download file.\nError: {e}")