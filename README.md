
# Credit Default Swap Returns Replication

## Project Overview  
This project aims to **replicate the Credit Default Swap (CDS) columns** from the dataset used in **He, Kelly, and Manela (2017)**, following the methodology described in **Palhares (2013)**.  
The goal is to construct and validate CDS returns using WRDS data (Markit, Compustat, CRSP) and perform analysis on both historical and updated CDS return series.


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
## Project Task Breakdown

| **Category**                  | **Related File**             | **Task Description**                                                              | **Person Responsible** | **Status** |
|--------------------------------|-----------------------------|----------------------------------------------------------------------------------|------------------------|------------|
| **LaTeX Report**               | `report.tex`                | Compile a LaTeX document summarizing the replication project, including all generated tables and charts. | Sania                  |            |
|                                |                             | Provide a high-level overview of the replication process, successes, and challenges. | Sania                  |            |
|                                |                             | Discuss key findings and challenges encountered during the replication.           | Yangge & Sania         |            |
|                                |                             | Explain the data sources used in the project.                                    | Yangge                 |            |
| **LaTeX Automation**           | `.py`                       | Convert tables into LaTeX format automatically for inclusion in the report.      |                        |            |
| **Jupyter Notebooks**          | `notebooks/summary.ipynb`   | Create a Jupyter notebook that provides an overview of the cleaned data and demonstrates key analysis steps. | Yangge & Sania | One notebook should be sufficient as datasets are interconnected. |
| **Data Processing & Cleaning** | `pull_nyfed_dealer.py`      | Extract and preprocess primary dealer data.                                      | Yangge                 | ✅ Completed |
|                                | `dealer_map_helper.csv`     | Manually map company names for consistency.                                     | Yangge                 | ✅ NA stocks finished |
|                                | `pull_comp_fundq.py`        | Process and clean Compustat quarterly data.                                      | Yangge                 |            |
|                                | `pull_crsp_monthly.py`      | Extract and clean monthly CRSP stock data.                                      | Yangge & Sania         |            |
|                                | `pull_datastream.py`        | Extract and process Datastream data.                                            | Sania                  |            |
| **Replication & Unit Testing** | `test_replication.py`       | Verify replication accuracy through unit tests.                                 | Yangge                 | 🔄 In progress |
|                                | `test_summary_stats.py`     | Ensure summary statistics computations are correct.                             | Yangge/Sania           |            |
|                                | `test_cds_returns.py`       | Validate CDS return calculations with unit tests.                              | Yangge/Sania           |            |
|                                | `test_pipeline.py`          | Test the automation pipeline for reliability.                                  | Yangge/Sania           |            |
| **Updates & Enhancements**     |                             | Integrate newly available data to refresh analysis results.                     |                        |            |
| **Summary Statistics & Charts**|                             | Generate summary statistics and visualizations for the dataset.                 | Yangge & Sania         | ❓ Can we base this on a table from the paper? |
| **Automation & Project Setup** | `dodo.py`                   | Automate the project workflow using PyDoit.                                     | Yangge & Sania         |            |
|                                | `.env.example`              | Provide a template `.env` file for environment variables.                        | Yangge & Sania         |            |
|                                | `requirements.txt`          | List all required Python dependencies.                                          | Yangge & Sania         |            |
| **Code Formatting & Documentation** | `settings.py`         | Ensure all Python scripts include clear docstrings.                             | Yangge & Sania         |            |
|                                | Function Naming Conventions | Use clear and descriptive function names for readability.                        | Yangge & Sania         |            |


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
He, Zhiguo, Bryan Kelly, and Asaf Manela, Intermediary Asset Pricing: New Evidence from Many Asset Classes, Journal of Financial Economics, 2017, Vol 126, Issue 1, pp. 1–35
2. **Palhares (2013)** - CDS return calculations  
3. **Markit Data** - Primary data source  

---

## 👥 **Team Members**
- **Sania Zeb** 
- **Yangge Xu** 
