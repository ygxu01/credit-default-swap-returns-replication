
# Credit Default Swap Returns Replication

## Project Overview  
This project aims to **replicate the Credit Default Swap (CDS) columns** from the dataset used in **He, Kelly, and Manela (2017)**, following the methodology described in **Palhares (2013)**.  
The goal is to construct and validate CDS returns using WRDS data (Markit, Compustat, CRSP) and perform analysis on both historical and updated CDS return series.

### Key Steps

1. **Pull All Daily CDS Data**  
   - We connect to WRDS, query the Markit CDS tables for each year, and fetch the 5‐year CDS spreads (bid, ask, par, or composite).  
   - We merge duplicate quotes on the same day by taking an average or using the composite mid.

2. **Compute a Daily Mid Spread**  
   - We unify bid/ask to a single “midspread” each trading day.  
   - Ensure spreads are consistently in basis points (bps) or decimals.

3. **Calculate Daily Short‐CDS Returns**  
   - For each ticker (or redcode) and each day, apply the formula:


$$
CDS^{ret}_t = \frac{CDS_t}{250}+ \Delta CDS_t \times RD_t.
$$


$$
RD_t = \frac{1}{4} \sum_{j=1}^{4M} e^{-\lambda j/4} - e^{-\left(\lambda + j\delta\right)/4},
$$

4. **Aggregate Daily to Monthly**  
   - We group each entity’s daily returns by calendar month and **compound**:
     $R = \prod (1 + r_{\text{daily}}) - 1$
   - The result is a single monthly short‐CDS return for each name.


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
**Although specific tasks are assigned to individual team members, we work collaboratively as a team. Each member actively reviews and provides feedback on others' code and writing to ensure accuracy, clarity, and consistency. We also assist each other in debugging and refining our work.**

## Project Task Breakdown

| **Category**                  | **Related File**             | **Task Description**                                                                                                                 | **Person Responsible** | **Status** |
|--------------------------------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|------------------------|------------|
| **LaTeX Report**               | `./reports/Final_Project.tex`| Compile a comprehensive LaTeX document that summarizes the replication project. Include methodology, data sources, all generated tables/charts, key findings, and challenges. | Sania & Yangge         |            |
|                                |                              | Provide a high-level overview of the replication process, covering data extraction, cleaning, and analysis steps.                                                          | Sania                  |            |
|                                |                              | Discuss primary results, notable obstacles or limitations, and how they were resolved or remain open.                                                                       | Sania                  |            |
|                                |                              | Detail the various data sources (e.g., Markit, WRDS, etc.) and how they integrate into the replication project.                                                             | Sania                  |            |
| **LaTeX Automation**           | `dodo.py`                    | Automate the conversion of summary tables, figures, and statistics into LaTeX format for direct inclusion in the final report.                                              | Sania & Yangge         |            |
| **Jupyter Notebooks**          | `./src/Final_Project.ipynb`  | Develop a single interactive notebook that illustrates the cleaned data, shows code snippets of the main analysis steps, and summarizes key outputs and findings.           | Sania                  | One notebook is sufficient as datasets are interconnected. |
| **Data Processing & Cleaning** | `./src/pull_markit_cds.py`   | Extract and preprocess CDS data from WRDS Markit. Clean, validate, and structure it for downstream computations.                                                           |  Sania & Yangge          |            |
|                                | `./src/pull_interest_rates_data.py` | Pull and clean interest rate data. Ensure consistent date formatting, remove duplicates, and handle missing values.                                                          | Yangge                 |            |
|                                | `./src/pull_cds_return_data.py`     | Combine relevant fields (e.g., spreads, hazard rates if needed) and merge them into a workable daily or monthly returns dataset.                                             | Yangge                 |            |
|                                | `./src/calc_cds_daily_return.py`    | Implement the short-CDS daily return formula (carry + capital gain) and confirm units (bps vs decimals). Validate correctness of calculations.                               | Yangge                 |            |
|                                | `./src/create_portfolio.py`         | Create and manage portfolio construction logic (e.g., sorting by spread levels), yielding monthly or quarterly portfolio returns.                                            | Yangge                 |            |
| **Unit Testing**               | `./src/test_.py`             | Write and maintain unit tests for the data transformation functions. Ensure correctness of data merges, returns calculations, and portfolio generation.                     | Yangge                 |            |
| **Updates & Enhancements**     |                              | Integrate newly available data or refined techniques to update analysis results. Document any improvements, bug fixes, or alternative methods tested.                        |   Sania & Yangge                     |            |
| **Summary Statistics & Charts**| `./reports/SummaryStats.tex` | Generate descriptive statistics (e.g., mean, std dev) and produce visualizations (histograms, line plots) to highlight key findings and data distributions.                 | Sania & Yangge         |            |
| **Automation & Project Setup** | `dodo.py`                    | Manage the overall workflow with PyDoit (e.g., data pulls, cleaning, table generation). Streamline reproducibility through consistent commands.                              |  Sania & Yangge         |            |
|                                | `.env.example`               | Provide a template for environment variables to ensure smooth local setup and integration with WRDS credentials, data paths, etc.                                           |  Sania & Yangge          |            |
|                                | `requirements.txt`           | Maintain an up-to-date list of dependencies for Python packages necessary to run scripts and notebooks.                                                                     |  Sania & Yangge          |            |
| **Code Formatting & Documentation** |                          | Enforce PEP 8 (or chosen style) for all Python scripts. Include concise docstrings that describe inputs, outputs, and functionality.                                        | Sania                  |            |
|                                | *Function Naming Conventions*| Use descriptive function names for clarity (e.g., `calc_daily_cds_return`), and be consistent across files and modules.                                                     | Sania & Yangge          |            |



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

## **Team Members**
- **Sania Zeb** 
- **Yangge Xu** 
