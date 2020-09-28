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

- `dateutil_parse(text)` - returns an ISO8601 date string parsed from the text, or `null` if the input could not be parsed. `dateutil_parse("10 october 2020 3pm")` returns `2020-10-10T15:00:00`.
- `dateutil_parse_fuzzy(text)` - same as `dateutil_parse()` but this also works against strings that contain a date somewhere within them - that date will be returned, or `null` if no dates could be found. `dateutil_parse_fuzzy("This is due 10 september")` returns `2020-09-10T00:00:00` (but will start returning the 2021 version of that if the year is 2021).
- `dateutil_easter(year)` - returns the date for Easter in that year, for example `dateutil_easter("2020")` returns `2020-04-12`.

The `dateutil_parse()` and `dateutil_parse_fuzzy()` functions both follow the American convention of assuming that `1/2/2020` lists the month first, evaluating this example to the 2nd of January.

If you want to assume that the day comes first, use these two functions instead:

- `dateutil_parse_dayfirst(text)`
- `dateutil_parse_fuzzy_dayfirst(text)`

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
