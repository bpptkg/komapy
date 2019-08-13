"""
KomaPy data transforms module.
"""

import pandas as pd

from .client import fetch_bma_as_dataframe

SUPPORTED_TRANSFORMS = {
    'slope_correction': 'slope_correction',
}


def slope_correction(data, config):
    """
    Apply EDM slope distance correction.
    """
    if config.name != 'edm':
        return data

    timestamp__gte = config.query_params.get(
        'timestamp__gte') or config.query_params.get('start_at')
    timestamp__lt = config.query_params.get(
        'timestamp__lt') or config.query_params.get('end_at')

    err_data = fetch_bma_as_dataframe('slope', {
        'timestamp__gte': timestamp__gte,
        'timestamp__lt': timestamp__lt,
        'benchmark': config.query_params['benchmark'],
        'reflector': config.query_params['reflector'],
    })
    if err_data.empty:
        return data

    slope_data = pd.DataFrame()
    for item in data:
        slope_data.join(item)

    corrected_data = slope_data.apply(
        lambda item: item.slope_distance + err_data.where(
            err_data.timestamp > item.timestamp).deviation.sum(), axis=1)
    return [data[0], corrected_data]
