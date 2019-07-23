import base64
import uuid
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


def generate_url_safe_filename(extension='png'):
    """Generate URL-safe random filename based on UUID4."""
    name = uuid.uuid4()
    filename = base64.urlsafe_b64encode(
        name.bytes).decode('utf-8').rstrip('=\n')
    return '{filename}.{extension}'.format(
        filename=filename, extension=extension)
