
# Credit Default Swap Returns Replication

## Project Overview  
This project aims to **replicate the Credit Default Swap (CDS) columns** from the dataset used in **He, Kelly, and Manela (2017)**, following the methodology described in **Palhares (2013)**.  
The goal is to construct and validate CDS returns using **Markit data** and perform analysis on both historical and updated CDS return series.

---

## **Project Structure**
```
cds-returns-replication
├── figures/              # Figures for report and analysis
├── requirements.txt      # Dependencies needed to run the project
├── .gitignore            # Ensures no sensitive files are committed
├── .env.example          # Example environment variable file
├── dodo.py               # Automation pipeline using PyDoit
└── README.md             # Project documentation

[updating]
```


---

## **Setup & Installation**
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/cds-returns-replication.git
cd cds-returns-replication
```

### **2️. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
- Copy `.env.example` to `.env` and fill in necessary details (e.g., API keys, data paths).
- Ensure **raw datasets are stored locally** (`data/raw/`) and not committed.

---

## **Task Assignments**
| **Category**  | **Task Description** | **Person Responsible** | **Related Files** |
|--------------|--------------------|----------------------|----------------|
| **Repository Setup** | Fork `jmbejara/blank_project`, create repo, add teammates | [Your Name] / [Teammate] | `README.md`, `.gitignore` |
| | Add `.env.example` for environment variables | [Your Name] / [Teammate] | `.env.example` |
| | Include `requirements.txt` for dependencies | [Teammate] | `requirements.txt` |
| **LaTeX Report** | Write report, summarize findings | [Your Name] / [Teammate] | `report.tex` |
| **Data Handling** | Clean and preprocess data | [Your Name] | `scripts/data_cleaning.py` |
| | **Write unit tests for data cleaning** | [Teammate] | `tests/test_data_cleaning.py` |
| **CDS Return Calculation** | Implement CDS return formula | [Teammate] | `scripts/cds_returns.py` |
| | **Write unit tests for return calculations** | [Your Name] | `tests/test_cds_returns.py` |
| **Replication & Updates** | Replicate paper's tables & figures | [Your Name] / [Teammate] | `scripts/replication.py` |
| | **Write unit tests for replication accuracy** | [Teammate] | `tests/test_replication.py` |
| | Update analysis with recent data | [Teammate] | `scripts/update_replication.py` |
| | **Write unit tests for updated replication** | [Your Name] | `tests/test_update_replication.py` |
| **Summary Statistics & Visualization** | Generate statistics and visualizations | [Your Name] / [Teammate] | `notebooks/summary.ipynb` |
| | **Write unit tests for summary statistics** | [Teammate] | `tests/test_summary_stats.py` |
| **Automation & Unit Tests** | Automate pipeline with PyDoit | [Your Name] | `dodo.py` |
| | **Write unit tests for automation pipeline** | [Teammate] | `tests/test_pipeline.py` |
| **GitHub & Version Control** | Each team member makes commits and PRs | [Your Name] / [Teammate] | GitHub PRs |
| | Maintain clear Git commit messages | [Your Name] / [Teammate] | GitHub |

---

## **Running Unit Tests**
To ensure correctness, run all tests using `pytest`:
```bash
pytest tests/
```
To run a specific test:
```bash
pytest tests/test_cds_returns.py
```

---

## **Key References**
1. **He, Kelly, and Manela (2017)** - Defines the CDS columns  
2. **Palhares (2013)** - CDS return calculations  
3. **Markit Data** - Primary data source  

---

## 👥 **Team Members**
- **Sania Zeb** 
- **Yangge Xu** 
