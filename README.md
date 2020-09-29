# datasette-dateutil

[![PyPI](https://img.shields.io/pypi/v/datasette-dateutil.svg)](https://pypi.org/project/datasette-dateutil/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-dateutil?include_prereleases&label=changelog)](https://github.com/simonw/datasette-dateutil/releases)
[![Tests](https://github.com/simonw/datasette-dateutil/workflows/Test/badge.svg)](https://github.com/simonw/datasette-dateutil/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-dateutil/blob/main/LICENSE)

dateutil functions for Datasette

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-dateutil

## Usage

This function adds custom SQL functions that expose functionality from the [dateutil](https://dateutil.readthedocs.io/) Python library.

Once installed, the following SQL functions become available:

### Parsing date strings

- `dateutil_parse(text)` - returns an ISO8601 date string parsed from the text, or `null` if the input could not be parsed. `dateutil_parse("10 october 2020 3pm")` returns `2020-10-10T15:00:00`.
- `dateutil_parse_fuzzy(text)` - same as `dateutil_parse()` but this also works against strings that contain a date somewhere within them - that date will be returned, or `null` if no dates could be found. `dateutil_parse_fuzzy("This is due 10 september")` returns `2020-09-10T00:00:00` (but will start returning the 2021 version of that if the year is 2021).

The `dateutil_parse()` and `dateutil_parse_fuzzy()` functions both follow the American convention of assuming that `1/2/2020` lists the month first, evaluating this example to the 2nd of January.

If you want to assume that the day comes first, use these two functions instead:

- `dateutil_parse_dayfirst(text)`
- `dateutil_parse_fuzzy_dayfirst(text)`

Here's a query demonstrating these functions:

```sql
select
  dateutil_parse("10 october 2020 3pm"),
  dateutil_parse_fuzzy("This is due 10 september"),
  dateutil_parse("1/2/2020"),
  dateutil_parse("2020-03-04"),
  dateutil_parse_dayfirst("2020-03-04");
```

[Try that query](https://latest-with-plugins.datasette.io/fixtures?sql=select%0D%0A++dateutil_parse%28%2210+october+2020+3pm%22%29%2C%0D%0A++dateutil_parse_fuzzy%28%22This+is+due+10+september%22%29%2C%0D%0A++dateutil_parse%28%221%2F2%2F2020%22%29%2C%0D%0A++dateutil_parse%28%222020-03-04%22%29%2C%0D%0A++dateutil_parse_dayfirst%28%222020-03-04%22%29%3B)

### Calculating Easter

- `dateutil_easter(year)` - returns the date for Easter in that year, for example `dateutil_easter("2020")` returns `2020-04-12`.

[Example Easter query](https://latest-with-plugins.datasette.io/fixtures?sql=select%0D%0A++dateutil_easter%282019%29%2C%0D%0A++dateutil_easter%282020%29%2C%0D%0A++dateutil_easter%282021%29)

### JSON arrays of dates

Several functions return JSON arrays of date strings. These can be used with SQLite's `json_each()` function to perform joins against dates from a specific date range or recurrence rule.

These functions can return up to 10,000 results. They will return an error if more than 10,000 dates would be returned - this is to protect against denial of service attacks.

- `dateutil_dates_between('1 january 2020', '5 jan 2020')` - given two dates (in any format that can be handled by `dateutil_parse()`) this function returns a JSON string containing the dates between those two days, inclusive. This example returns `["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05"]`.
- `dateutil_dates_between('1 january 2020', '5 jan 2020', 0)` - set the optional third argument to `0` to specify that you would like this to be exclusive of the last day. This example returns `["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"]`.

[Try these queries](https://latest-with-plugins.datasette.io/fixtures?sql=select%0D%0A++dateutil_dates_between%28%271+january+2020%27%2C+%275+jan+2020%27%29%2C%0D%0A++dateutil_dates_between%28%271+january+2020%27%2C+%275+jan+2020%27%2C+0%29)

The `dateutil_rrule()` and `dateutil_rrule_date()` functions accept the iCalendar standard ``rrule` format - see [the dateutil documentation](https://dateutil.readthedocs.io/en/stable/rrule.html#rrulestr-examples) for more examples.

This format lets you specify recurrence rules such as "the next four last mondays of the month".

- `dateutil_rrule(rrule, optional_dtsart)` - given an rrule returns a JSON array of ISO datetimes. The second argument is optional and will be treated as the start date for the rule.
- `dateutil_rrule_date(rrule, optional_dtsart)` - same as `dateutil_rrule()` but returns ISO dates.

Example query:

```sql
select
  dateutil_rrule('FREQ=HOURLY;COUNT=5'),
  dateutil_rrule_date(
    'FREQ=DAILY;COUNT=3',
    '1st jan 2020'
  );
```
[Try the rrule example query](https://latest-with-plugins.datasette.io/fixtures?sql=select%0D%0A++dateutil_rrule('FREQ%3DHOURLY%3BCOUNT%3D5')%2C%0D%0A++dateutil_rrule_date(%0D%0A++++'FREQ%3DDAILY%3BCOUNT%3D3'%2C%0D%0A++++'1st+jan+2020'%0D%0A++)%3B)

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-dateutil
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
