import pandas as pd
import pytest

import pandasdmx as sdmx

from .data import specimen


@pytest.fixture(autouse=True)
def compat_rtype():
    """Ensure DEFAULT_RTYPE is 'compat' for all tests in this file."""
    tmp = sdmx.writer.DEFAULT_RTYPE
    sdmx.writer.DEFAULT_RTYPE = 'compat'
    yield
    sdmx.writer.DEFAULT_TYPE = tmp


def pd_obj(name):
    """Return the specimen at *name* read, then converted to pandas."""
    with specimen(name) as f:
        data_msg = sdmx.read_sdmx(f)
    return sdmx.to_pandas(data_msg)


def test_xml():
    """Test that objects have the expected layout with rtype='compat'."""
    # GenericData with non-time Dimension at observation → data frame
    df1 = pd_obj('ng-xs.xml')
    assert isinstance(df1.index, pd.Index) and df1.index.name == 'CURRENCY'
    assert isinstance(df1.columns, pd.MultiIndex)

    # TimeSeriesData → data frame with DatetimeIndex
    df2 = pd_obj('ng-ts.xml')
    assert isinstance(df2.index, pd.DatetimeIndex)
    assert isinstance(df2.columns, pd.MultiIndex)

    # GenericData with AllDimensions at observation → series
    df3 = pd_obj('ng-flat.xml')
    assert isinstance(df3, pd.Series)
    assert isinstance(df3.index, pd.MultiIndex)