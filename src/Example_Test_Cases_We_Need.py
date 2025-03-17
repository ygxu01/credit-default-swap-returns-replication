# Test Case 1: for test_calc_cds_daily_return.py

import pytest
import pandas as pd
import numpy as np
from calc_cds_daily_return import calc_RD, calc_cds_daily_return

def test_calc_RD():
    """Test that Risky Duration (RD) is calculated correctly with realistic values."""
    mock_cds_data = pd.DataFrame({
        'trade_date': pd.date_range(start='2020-01-01', periods=5, freq='D'),
        'spread': [0.01, 0.012, 0.013, 0.014, 0.015],
        'ticker': ['A', 'B', 'C', 'D', 'E']
    })
    
    mock_risk_free_data = pd.DataFrame(np.random.rand(5, 60), index=mock_cds_data['trade_date'])
    
    result = calc_RD(mock_cds_data, mock_risk_free_data)
    
    assert 'RD' in result.columns
    assert not result['RD'].isnull().all()
    assert result.shape[0] > 0  # Ensure rows exist

def test_calc_cds_daily_return():
    """Test that CDS daily returns are computed correctly."""
    mock_rd_data = pd.DataFrame({
        'spread_prev': [0.01, 0.012, 0.013, 0.014, 0.015],
        'spread': [0.011, 0.013, 0.014, 0.016, 0.018],
        'RD_prev': [0.9, 0.85, 0.8, 0.75, 0.7]
    })

    result = calc_cds_daily_return(mock_rd_data)

    assert 'daily_return' in result.columns
    assert not result['daily_return'].isnull().all()
    assert result['daily_return'].dtype in [np.float64, np.float32]  # Ensure numeric values


#Test Case 2: test_pull_cds_return_data.py

import pytest
import pandas as pd
from pull_cds_return_data import pull_real_cds_return, load_read_cds_return
from pathlib import Path
from settings import config

DATA_DIR = Path(config("DATA_DIR"))

def test_pull_real_cds_return():
    """Test that historical CDS returns are loaded correctly."""
    df = pull_real_cds_return()
    assert not df.empty
    assert list(df.columns) == ['yyyymm'] + [f'CDS_{i:02d}' for i in range(1, 21)]
    assert df.dtypes['yyyymm'] == 'int64'

def test_load_read_cds_return():
    """Ensure that stored CDS return files exist and are loadable."""
    path = DATA_DIR / "actual_cds_return.parquet"
    if path.exists():
        df = load_read_cds_return()
        assert not df.empty
        assert 'CDS_01' in df.columns
    else:
        pytest.skip("Parquet file does not exist, skipping test.")


#Test Case 3: for test_pull_markit.py

import pytest
import pandas as pd
from pull_markit import pull_markit_data, pull_markit_sector

def test_pull_markit_data(mocker):
    """Mock WRDS connection and ensure Markit CDS data is pulled properly."""
    mocker.patch('pull_markit.pd.DataFrame', return_value=pd.DataFrame({
        'trade_date': pd.date_range(start='2020-01-01', periods=3, freq='D'),
        'ticker': ['A', 'B', 'C'],
        'spread': [0.01, 0.012, 0.015]
    }))

    df = pull_markit_data(2020, 2020)
    assert not df.empty
    assert 'spread' in df.columns
    assert df['trade_date'].dtype == '<M8[ns]'

def test_pull_markit_sector(mocker):
    """Ensure sector data is correctly retrieved."""
    mocker.patch('pull_markit.pd.DataFrame', return_value=pd.DataFrame({
        'ticker': ['A', 'B', 'C'],
        'sector': ['Tech', 'Finance', 'Energy']
    }))
    
    df = pull_markit_sector(2020, 2020)
    assert not df.empty
    assert 'sector' in df.columns
    assert df['sector'].nunique() > 1

# Test Case 4: for test_pull_rf_data.py

import pytest
import pandas as pd
from pull_rf_data import pull_fed_yield_curve, pull_swap_rates

def test_pull_fed_yield_curve():
    """Test that Fed yield curve data is pulled and contains expected columns."""
    df = pull_fed_yield_curve()
    assert not df.empty
    assert all(col in df.columns for col in ['SVENY01', 'SVENY02', 'SVENY03'])
    assert df.index.dtype == 'datetime64[ns]'

def test_pull_swap_rates():
    """Ensure swap rates are pulled and properly structured."""
    df = pull_swap_rates()
    assert not df.empty
    assert all(col in df.columns for col in ['DGS3MO', 'DGS6MO'])
    assert df.index.dtype == 'datetime64[ns]'
