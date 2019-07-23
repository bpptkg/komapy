import datetime

from .client import fetch_bma_as_dataframe
from .processing import dataframe_or_empty
from .utils import resolve_timestamp


def plot_explosion_line(axis, starttime, endtime, **options):
    """
    Plot Merapi explosion line on current axis.

    Exposion date is fetched from seismic bulletin database. All event dates
    are treated as local timezone, i.e. Asia/Jakarta.
    """
    handle = None

    params = {
        'eventtype': 'EXPLOSION',
        'nolimit': True,
    }
    data = fetch_bma_as_dataframe('bulletin', params)

    eventdate = resolve_timestamp(dataframe_or_empty(data, 'eventdate'))
    if eventdate.empty:
        return handle
    else:
        eventdate = eventdate.dt.tz_localize(None).dt.to_pydatetime()

    for timestamp in eventdate:
        if starttime <= timestamp and timestamp <= endtime:
            handle = axis.axvline(timestamp, label='Letusan', **options)

    return handle


def plot_dome_appearance(axis, starttime, endtime, **options):
    """
    Plot Merapi dome appearance on current axis.

    Merapi dome appears at 2018-08-01 Asia/Jakarta timezone.
    """
    handle = None

    timestamp = datetime.datetime(2018, 8, 1)
    if starttime <= timestamp and timestamp >= endtime:
        handle = axis.axvline(timestamp, **options)
    return handle
