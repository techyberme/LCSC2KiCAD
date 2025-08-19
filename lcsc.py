import csv
import subprocess
import os
import pandas as pd

# === Config ===
excel_file = 'ELM_BOARD LCSC.xlsx'
temp_csv_file = 'components_temp.csv'
log_file = 'error_log.txt'
imported_file = 'imported_ids.txt'
output_dir = '.'  # KiCad libs are written to the working directory

# === Step 1: Convert Excel to CSV ===
try:
    df = pd.read_excel(excel_file)
    df.to_csv(temp_csv_file, index=False)
except Exception as e:
    print(f"Failed to read or convert Excel file: {e}")
    exit(1)

# === Step 2: Load Already Imported IDs ===
imported_ids = set()
if os.path.exists(imported_file):
    with open(imported_file, 'r') as f:
        imported_ids = set(line.strip() for line in f if line.strip())

# === Step 3: Process CSV and Fetch Parts ===
with open(temp_csv_file, newline='') as f_csv, \
     open(log_file, 'w') as log, \
     open(imported_file, 'a') as imported_log:

    reader = csv.DictReader(f_csv)

    # Auto-detect LCSC column
    lcsc_col = next((h for h in reader.fieldnames if 'lcsc' in h.lower()), None)
    if not lcsc_col:
        print("No column containing 'LCSC' found in the Excel file.")
        exit(1)

    for row in reader:
        lcsc_id = row.get(lcsc_col, '').strip()
        if not lcsc_id or lcsc_id in imported_ids:
            print(f"Skipping {lcsc_id} (empty or already imported).")
            continue

        print(f"Fetching {lcsc_id}...")
        cmd = ['easyeda2kicad', '--full', f'--lcsc_id={lcsc_id}']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            if 'already in' in result.stderr.lower():
                print(f"{lcsc_id} already present in library. Skipping as successful.")
                imported_log.write(lcsc_id + '\n')
                imported_ids.add(lcsc_id)
            else:
                log.write(f"Error fetching {lcsc_id}:\n{result.stderr}\n\n")
                print(f"Error fetching {lcsc_id}. Logged.")
        else:
            imported_log.write(lcsc_id + '\n')
            imported_ids.add(lcsc_id)


# === Step 4: Optional Cleanup ===
# os.remove(temp_csv_file)
