import pandas as pd


def dataframe_from_dictionary(entry):
    """Create Pandas DataFrame from list of dictionary."""
    return pd.DataFrame(entry)


def empty_dataframe():
    """Create empty Pandas DataFrame."""
    return pd.DataFrame()


def dataframe_or_empty(data, name):
    """Get DataFrame column name or return empty DataFrame."""
    return data.get(name, empty_dataframe())


def read_csv(*args, **kwargs):
    """Read csv file."""
    return pd.read_csv(*args, **kwargs)


def read_excel(*args, **kwargs):
    """Read excel file."""
    return pd.read_excel(*args, **kwargs)
