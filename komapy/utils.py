from dateutil import parser


def resolve_timestamp(data):
    """
    Resolve data timestamp.
    """
    if data.empty:
        return data

    data = data.astype('datetime64[s]')
    return data


def to_pydatetime(*args, **kwargs):
    """
    Convert date string to Python non-aware datetime.
    """
    date_obj = parser.parse(*args, **kwargs)
    return date_obj
