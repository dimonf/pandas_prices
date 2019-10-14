import pytest

from Prices import Prices

_data =  {'date':['2019-01-01','2010-01-05','2019-01-15'],
         'amount':[142.32, 442.30, 40123.40],
         'curr':['eur','usd','eur'],
         'usd':[145.17, 442.30, 41327.10],
        }

_rates = {
        ('EUR:USD','2019-01-01'): 145.17 / 142.32,
        ('EUR:USD','2019-01-15'): 41327.10 / 40123.40,
        }


@pytest.fixture
def test_df():
    """
    create sample set of currency rates
    date
    """
    import pandas as pd
    df = pd.DataFrame(_data)
    return df

def test_correct_calculation(test_df):
    p = Prices(test_df)
    for k,v in _rates.items():
        assert p.prices.loc[k] == v
