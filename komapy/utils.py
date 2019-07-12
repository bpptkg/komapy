
def resolve_timestamp(data):
    """
    Resolve data timestamp.
    """
    if data.empty:
        return data

    data = data.astype('datetime64[s]')
    return data
