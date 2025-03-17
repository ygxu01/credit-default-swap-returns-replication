## Example dodo.py structure with details (to be tested once we complete files)

import sys
import subprocess
import shutil
from os import environ
from pathlib import Path

sys.path.insert(1, "./src/")

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
OS_TYPE = config("OS_TYPE")

# ==================================================
# Jupyter Notebook Execution Helpers
# ==================================================

environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

def jupyter_execute_notebook(notebook):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --log-level WARN --inplace ./src/{notebook}.ipynb"

def jupyter_to_html(notebook, output_dir=OUTPUT_DIR):
    return f"jupyter nbconvert --to html --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"

def jupyter_to_md(notebook, output_dir=OUTPUT_DIR):
    return f"jupytext --to markdown --log-level WARN --output-dir={output_dir} ./src/{notebook}.ipynb"

def jupyter_to_python(notebook, build_dir):
    return f"jupyter nbconvert --log-level WARN --to python ./src/{notebook}.ipynb --output _{notebook}.py --output-dir {build_dir}"

def jupyter_clear_output(notebook):
    return f"jupyter nbconvert --log-level WARN --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace ./src/{notebook}.ipynb"

# ==================================================
# File Copy Helper
# ==================================================

def copy_file(origin_path, destination_path, mkdir=True):
    """Create a Python action for copying a file."""
    def _copy_file():
        origin = Path(origin_path)
        dest = Path(destination_path)
        if mkdir:
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, dest)
    return _copy_file

# ==================================================
# PyDoit Tasks for Data Pipeline
# ==================================================

def task_config():
    """Create empty directories for data and output if they don't exist"""
    return {
        "actions": ["ipython ./src/settings.py"],
        "targets": [DATA_DIR, OUTPUT_DIR],
        "file_dep": ["./src/settings.py"],
        "clean": [],
    }

def task_pull_markit():
    """Extract market data from WRDS and save it to a structured file."""
    return {
        "actions": ["python src/pull_markit.py"],
        "file_dep": ["src/pull_markit.py"],
        "targets": [DATA_DIR / "raw_markit_data.csv"],
        "clean": True,
    }

def task_prepare_cds_analysis():
    """Transform raw CDS data: clean, resample, and categorize into portfolios."""
    return {
        "actions": ["python src/prepare_cds_analysis.py"],
        "file_dep": ["src/prepare_cds_analysis.py", DATA_DIR / "raw_markit_data.csv"],
        "targets": [DATA_DIR / "structured_cds_data.csv"],
        "clean": True,
    }

def task_pull_rf_data():
    """Gather and process risk-free rate data for calculations."""
    return {
        "actions": ["python src/pull_rf_data.py"],
        "file_dep": ["src/pull_rf_data.py"],
        "targets": [DATA_DIR / "market_rates.csv"],
        "clean": True,
    }

def task_calc_cds_daily_return():
    """Compute daily CDS portfolio returns following the research methodology."""
    return {
        "actions": ["python src/calc_cds_daily_return.py"],
        "file_dep": [
            "src/calc_cds_daily_return.py",
            DATA_DIR / "structured_cds_data.csv",
            DATA_DIR / "market_rates.csv",
        ],
        "targets": [DATA_DIR / "computed_cds_daily_returns.csv"],
        "clean": True,
    }


# ==================================================
# Task for Running Tests
# ==================================================

def task_validate_outputs():
    """Run integrity checks on processed data and computed returns."""
    test_scripts = [
        "src/test_cds_source.py",
        "src/test_cds_analysis.py",
        "src/test_rate_inputs.py",
        "src/test_cds_returns.py",
    ]

    def execute_tests():
        for script in test_scripts:
            subprocess.run(["python", script], check=True)

    return {"actions": [execute_tests], "clean": True}

# ==================================================
# Jupyter Notebook Execution Tasks
# ==================================================

notebook_tasks = {
    "01_cds_analysis.ipynb": {
        "file_dep": [
            "./src/pull_cds_source.py",
            "./src/prepare_cds_analysis.py",
        ],
        "targets": [],
    },
}

def task_convert_notebooks_to_scripts():
    """Convert notebooks to script form to detect changes to source code."""
    build_dir = Path(OUTPUT_DIR)
    
    for notebook in notebook_tasks.keys():
        notebook_name = notebook.split(".")[0]
        yield {
            "name": notebook,
            "actions": [
                jupyter_clear_output(notebook_name),
                jupyter_to_python(notebook_name, build_dir),
            ],
            "file_dep": [Path("./src") / notebook],
            "targets": [OUTPUT_DIR / f"_{notebook_name}.py"],
            "clean": True,
        }

def task_run_notebooks():
    """Execute notebooks and convert them into reports."""
    for notebook in notebook_tasks.keys():
        notebook_name = notebook.split(".")[0]
        yield {
            "name": notebook,
            "actions": [
                f"python -c \"import sys; from datetime import datetime; print(f'Start {notebook}: {datetime.now()}', file=sys.stderr)\"",
                jupyter_execute_notebook(notebook_name),
                jupyter_to_html(notebook_name),
                copy_file(
                    Path("./src") / f"{notebook_name}.ipynb",
                    OUTPUT_DIR / f"{notebook_name}.ipynb",
                    mkdir=True,
                ),
                jupyter_clear_output(notebook_name),
                f"python -c \"import sys; from datetime import datetime; print(f'End {notebook}: {datetime.now()}', file=sys.stderr)\"",
            ],
            "file_dep": [
                OUTPUT_DIR / f"_{notebook_name}.py",
                *notebook_tasks[notebook]["file_dep"],
            ],
            "targets": [
                OUTPUT_DIR / f"{notebook_name}.html",
                OUTPUT_DIR / f"{notebook_name}.ipynb",
                *notebook_tasks[notebook]["targets"],
            ],
            "clean": True,
        }

# ==================================================
# Task for Compiling LaTeX Reports
# ==================================================

def task_compile_summary():
    """Compile the final LaTeX report."""
    latex_file = "./reports/Research_Summary.tex"
    output_pdf = "./reports/Research_Summary.pdf"

    return {
        "actions": [
            f"latexmk -xelatex -cd -jobname=Research_Summary {latex_file}",
            f"latexmk -c -cd {latex_file}",
        ],
        "file_dep": [latex_file],
        "targets": [output_pdf],
        "clean": True,
    }

# ==================================================
# PyDoit Configuration
# ==================================================

DOIT_CONFIG = {
    "default_tasks": [
        "config",
        "pull_cds_source",
        "prepare_cds_analysis",
        "collect_rate_inputs",
        "generate_cds_returns",
        "validate_outputs",
        "run_notebooks",
        "compile_summary",
    ]
}


