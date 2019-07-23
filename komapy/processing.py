import numpy as np
import pandas as pd
from matplotlib import cm


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


def get_rgb_color(num_sample, index, colormap='tab10'):
    """
    Get RGB color at current index for number of sample from matplotlib
    color map.
    """
    space = np.linspace(0, 1, num_sample)
    cmap = cm.get_cmap(colormap)
    return cmap(space[index])
