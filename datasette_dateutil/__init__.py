from datasette import hookimpl
from dateutil.parser import parse, ParserError
from dateutil.rrule import rrulestr
from dateutil.easter import easter
import datetime
import itertools
import json


RRULE_MAX = 10_000


def _dateutil_parse_shared(s, **kwargs):
    default = kwargs.get("default")
    if default is not None:
        kwargs["default"] = parse(kwargs["default"])
    if not kwargs.get("dayfirst"):
        kwargs["dayfirst"] = False
    if not s:
        return None
    try:
        return parse(s, **kwargs).isoformat()
    except ParserError:
        return None


def dateutil_parse(s, default=None):
    return _dateutil_parse_shared(s, default=default)


def dateutil_parse_fuzzy(s, default=None):
    return _dateutil_parse_shared(s, fuzzy=True, default=default)


def dateutil_parse_dayfirst(s, default=None):
    return _dateutil_parse_shared(s, dayfirst=True, default=default)


def dateutil_parse_fuzzy_dayfirst(s, default=None):
    return _dateutil_parse_shared(s, fuzzy=True, dayfirst=True, default=default)


def dateutil_easter(year):
    year = str(year) if year else None
    if not year or not year.isdigit():
        return None
    try:
        return easter(int(year)).isoformat()
    except Exception as e:
        return None


class TooManyError(Exception):
    pass


def dateutil_rrule(rrule, dtstart=None, date=False):
    dtstart = dtstart and parse(dtstart) or None
    kwargs = {}
    if dtstart:
        kwargs["dtstart"] = dtstart
    results = list(itertools.islice(rrulestr(rrule, **kwargs), 0, RRULE_MAX + 1))
    if len(results) > RRULE_MAX:
        raise TooManyError(
            "More than {} results returned by '{}'".format(RRULE_MAX, rrule)
        )
    if date:
        results = [d.date() for d in results]
    return json.dumps([d.isoformat() for d in results])


def dateutil_rrule_date(rrule, dtstart=None):
    return dateutil_rrule(rrule, dtstart, date=True)


def _between(dt_start, dt_end, inclusive=True):
    if dt_start >= dt_end:
        return []
    current = dt_start
    while current < dt_end:
        yield current.isoformat()
        current += datetime.timedelta(days=1)
    if inclusive:
        yield current.isoformat()


def dateutil_dates_between(start, end, inclusive=True):
    dt_start = parse(start).date()
    dt_end = parse(end).date()
    results = list(
        itertools.islice(_between(dt_start, dt_end, inclusive), 0, RRULE_MAX + 1)
    )
    if len(results) > RRULE_MAX:
        raise TooManyError(
            "More than {} dates between '{}' and '{}".format(RRULE_MAX, start, end)
        )
    return json.dumps(results)


@hookimpl
def prepare_connection(conn):
    conn.create_function("dateutil_parse", 1, dateutil_parse)
    conn.create_function("dateutil_parse_fuzzy", 1, dateutil_parse_fuzzy)
    conn.create_function("dateutil_parse_dayfirst", 1, dateutil_parse_dayfirst)
    conn.create_function(
        "dateutil_parse_fuzzy_dayfirst", 1, dateutil_parse_fuzzy_dayfirst
    )
    # The two argument version of these (default date is second argument)
    conn.create_function("dateutil_parse", 2, dateutil_parse)
    conn.create_function("dateutil_parse_fuzzy", 2, dateutil_parse_fuzzy)
    conn.create_function("dateutil_parse_dayfirst", 2, dateutil_parse_dayfirst)
    conn.create_function(
        "dateutil_parse_fuzzy_dayfirst", 2, dateutil_parse_fuzzy_dayfirst
    )
    conn.create_function("dateutil_easter", 1, dateutil_easter)
    conn.create_function("dateutil_rrule", 1, dateutil_rrule)
    conn.create_function("dateutil_rrule", 2, dateutil_rrule)
    conn.create_function("dateutil_rrule_date", 1, dateutil_rrule_date)
    conn.create_function("dateutil_rrule_date", 2, dateutil_rrule_date)
    conn.create_function("dateutil_dates_between", 2, dateutil_dates_between)
    conn.create_function("dateutil_dates_between", 3, dateutil_dates_between)
