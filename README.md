**# Spool to Excel Converter**

A command-line utility to convert a spool file containing multiple SQL query results into Excel file(s). Each query result can be exported to a separate sheet (in a single Excel file) or a separate Excel file. Optionally, a summary of row counts for each query can be included.

---

**## 📆 Features**

- Convert spool files to Excel format
- Export results to:

  - A single Excel file with multiple sheets
  - Multiple Excel files (one per query)

- Optional summary of row counts
- Verbose mode for step-by-step logging
- Smart default output naming based on input file
- Optional installer available (no need to install Python)

---

**## 🛠️ Setup Instructions**

### 🔧 Option 1: Using Source Code

1. **Clone the repository** (or copy the script):

   ```bash
   git clone <repo-url>
   cd spool-to-excel
   ```

2. **Set up virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### 🖥️ Option 2: Using Installer (No Python Needed)

An executable installer is available for Windows.
Simply download and run the installer from the [Releases](repo-release-page) section.

Once installed, use the following command from any terminal:

```bash
splexcel <input_file> [options]
```

### ✅ Installed CLI Examples

Convert to a single Excel file with multiple sheets:

```bash
splexcel spool_file.spl
```

Convert each query to a separate Excel file inside a folder:

```bash
splexcel spool_file.spl --separate
```

Specify a custom output file or folder:

```bash
splexcel spool_file.spl -d my_output.xlsx
```

Enable verbose mode and include summary sheet:

```bash
splexcel spool_file.spl --verbose --showstats
```

---

**## 📄 Usage (Source Version)**

```bash
python main.py <input_file> [options]
```

### ✅ Source CLI Examples

Convert to a single Excel file with multiple sheets:

```bash
python main.py spool_file.spl
```

Convert each query to a separate Excel file inside a folder:

```bash
python main.py spool_file.spl --separate
```

Specify a custom output file or folder:

```bash
python main.py spool_file.spl -d my_output.xlsx
```

Enable verbose mode and include summary sheet:

```bash
python main.py spool_file.spl --verbose --showstats
```

---

**## ⚙️ Options**

| Option                | Description                                                                         |
| --------------------- | ----------------------------------------------------------------------------------- |
| `input_file`          | Path to the input spool file (required)                                             |
| `-d`, `--destination` | Output file (single Excel) or folder name (multiple files). Defaults to input name. |
| `-s`, `--separate`    | Export each query to a separate Excel file                                          |
| `-v`, `--verbose`     | Enable verbose logging                                                              |
| `-st`, `--showstats`  | Include a summary sheet or file with query names and row counts                     |

---

**## 📋 Requirements**

- Python 3.6+
- pandas
- openpyxl

---

**## 📁 File Structure**

```
main.py
parser.py
excel_export.py
utils.py
requirements.txt
README.md
CL_account_data.SPL (sample spool file)
```

---

**## 📜 License**

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
