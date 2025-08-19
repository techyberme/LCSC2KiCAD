# EasyEDA2KiCad Batch Import Tool

This script automates the process of importing component models from LCSC using the [easyeda2kicad](https://github.com/Bouni/easyeda2kicad) CLI tool. You simply provide an Excel file (`LCSC_Board.xlsx`) with a column containing LCSC part numbers, and the script will:

- Convert the Excel file to CSV
- Skip blank or already imported LCSC parts
- Call `easyeda2kicad` for each unique LCSC part
- Log any errors
- Keep track of what has already been imported

## 📁 Folder Structure

```
project/
├── components.xlsx         # Your Excel file with LCSC# column
├── imported_ids.txt        # Auto-generated: keeps track of fetched parts
├── error_log.txt           # Auto-generated: logs warnings/errors
├── components_temp.csv     # Auto-generated: temp converted CSV
├── easyeda2kicad_batch.py  # The main script
```

## 🚀 Usage

### 1. Install Requirements
Make sure you have:
- Python 3.x
- `pandas` installed:  
  ```bash
  pip install pandas
  ```
- `easyeda2kicad` installed and accessible from command line

### 2. Prepare Your Excel File

Create a `.xlsx` file (e.g. `components.xlsx`) with a column containing LCSC part numbers. The column can be named:

- `LCSC`
- `LCSC Part`
- `LCSC#`
- etc. (script will auto-detect)

### 3. Run the Script

```bash
python easyeda2kicad_batch.py
```

The script will:
- Convert `components.xlsx` to CSV
- Automatically detect the column with LCSC numbers
- Fetch and generate symbols/footprints via `easyeda2kicad`
- Track progress and skip previously fetched parts

### 4. Files Created Automatically
- `imported_ids.txt`: stores successfully fetched LCSC#s
- `error_log.txt`: logs any failed fetches
- `components_temp.csv`: temporary intermediate file

---

## 🛠 Configuration

You can modify the following at the top of the script:

```python
excel_file = 'components.xlsx'
temp_csv_file = 'components_temp.csv'
log_file = 'error_log.txt'
imported_file = 'imported_ids.txt'
```

---

## ⚠️ Notes

- If you see messages like:
  ```
  [WARNING] This id is already in ...
  [ERROR] Use --overwrite to update ...
  ```
  These are not treated as fatal errors by the script — the part is considered already imported.

- If you want to force re-import, delete the `imported_ids.txt` or add `--overwrite` to the `easyeda2kicad` command in the script.

---

## 📄 License

MIT

---

## 🧠 Credits

Developed by Javier Bermejo during his internship at [das-Nano](https://www.das-nano.com) as part of a project adapting electronic board designs for LCSC/JLCPCB compatibility.
