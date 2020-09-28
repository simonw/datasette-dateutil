from datasette import hookimpl
from dateutil.parser import parse, ParserError
from dateutil.easter import easter


def _dateutil_parse_shared(s, **kwargs):
    if not kwargs.get("dayfirst"):
        kwargs["dayfirst"] = False
    if not s:
        return None
    try:
        return parse(s, **kwargs).isoformat()
    except ParserError:
        return None


def dateutil_parse(s):
    return _dateutil_parse_shared(s)


def dateutil_parse_fuzzy(s):
    return _dateutil_parse_shared(s, fuzzy=True)


def dateutil_parse_dayfirst(s):
    return _dateutil_parse_shared(s, dayfirst=True)


def dateutil_parse_fuzzy_dayfirst(s):
    return _dateutil_parse_shared(s, fuzzy=True, dayfirst=True)


def dateutil_easter(year):
    year = str(year) if year else None
    if not year or not year.isdigit():
        return None
    try:
        return easter(int(year)).isoformat()
    except Exception as e:
        return None


@hookimpl
def prepare_connection(conn):
    conn.create_function("dateutil_parse", 1, dateutil_parse)
    conn.create_function("dateutil_parse_fuzzy", 1, dateutil_parse_fuzzy)
    conn.create_function("dateutil_parse_dayfirst", 1, dateutil_parse_dayfirst)
    conn.create_function(
        "dateutil_parse_fuzzy_dayfirst", 1, dateutil_parse_fuzzy_dayfirst
    )
    conn.create_function("dateutil_easter", 1, dateutil_easter)
