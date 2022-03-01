from datasette.app import Datasette
import pytest
import httpx


@pytest.mark.asyncio
async def test_plugin_is_installed():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/plugins.json")
        assert 200 == response.status_code
        installed_plugins = {p["name"] for p in response.json()}
        assert "datasette-dateutil" in installed_plugins


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sql,expected",
    [
        # dateutil_parse variants with one argument
        ("select dateutil_parse('1st october 2009')", "2009-10-01T00:00:00"),
        ("select dateutil_parse('invalid')", None),
        ("select dateutil_parse('due on 1st october 2009')", None),
        (
            "select dateutil_parse_fuzzy('due on 1st october 2009')",
            "2009-10-01T00:00:00",
        ),
        ("select dateutil_parse_fuzzy('due on')", None),
        ("select dateutil_parse_dayfirst('1/2/2020')", "2020-02-01T00:00:00"),
        ("select dateutil_parse('1/2/2020')", "2020-01-02T00:00:00"),
        ("select dateutil_parse_fuzzy('due on 1/2/2003')", "2003-01-02T00:00:00"),
        (
            "select dateutil_parse_fuzzy_dayfirst('due on 1/2/2003')",
            "2003-02-01T00:00:00",
        ),
        # dateutil_parse variants with the optional second default datetime argument
        (
            "select dateutil_parse('1st october 2009', '10th september 2020')",
            "2009-10-01T00:00:00",
        ),
        (
            "select dateutil_parse('1st october', '10th september 2020')",
            "2020-10-01T00:00:00",
        ),
        (
            "select dateutil_parse_fuzzy('due on 1st october', '2020-01-01')",
            "2020-10-01T00:00:00",
        ),
        ("select dateutil_parse_dayfirst('1/2', '1981-01-01')", "1981-02-01T00:00:00"),
        (
            "select dateutil_parse_fuzzy_dayfirst('due on 1/2', '1765-01-01')",
            "1765-02-01T00:00:00",
        ),
        # dateutil_easter
        ("select dateutil_easter(2020)", "2020-04-12"),
        ("select dateutil_easter('invalid')", None),
        # dateutil_rrule
        (
            "select dateutil_rrule('DTSTART:20200101\nFREQ=DAILY;INTERVAL=10;COUNT=5')",
            '["2020-01-01T00:00:00", "2020-01-11T00:00:00", "2020-01-21T00:00:00", "2020-01-31T00:00:00", "2020-02-10T00:00:00"]',
        ),
        (
            "select dateutil_rrule('FREQ=DAILY;INTERVAL=10;COUNT=5', '2020-01-01')",
            '["2020-01-01T00:00:00", "2020-01-11T00:00:00", "2020-01-21T00:00:00", "2020-01-31T00:00:00", "2020-02-10T00:00:00"]',
        ),
        (
            "select dateutil_rrule_date('DTSTART:20200101\nFREQ=DAILY;INTERVAL=10;COUNT=5')",
            '["2020-01-01", "2020-01-11", "2020-01-21", "2020-01-31", "2020-02-10"]',
        ),
        (
            "select dateutil_rrule_date('FREQ=DAILY;INTERVAL=10;COUNT=5', '2020-01-01')",
            '["2020-01-01", "2020-01-11", "2020-01-21", "2020-01-31", "2020-02-10"]',
        ),
        # dateutil_dates_between
        (
            "select dateutil_dates_between('1 january 2020', '5 jan 2020', 0)",
            '["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"]',
        ),
        (
            "select dateutil_dates_between('1 january 2020', '5 jan 2020')",
            '["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05"]',
        ),
    ],
)
async def test_dateutil_sql_functions(sql, expected):
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://localhost/_memory.json",
            params={
                "sql": sql,
                "_shape": "array",
            },
        )
        assert 200 == response.status_code
        actual = list(response.json()[0].values())[0]
        assert actual == expected


@pytest.mark.asyncio
async def test_dateutil_unbounded_rrule_error():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get(
            "http://localhost/_memory.json",
            params={
                "sql": "select dateutil_rrule('FREQ=DAILY;INTERVAL=10')",
                "_shape": "array",
            },
        )
        assert 400 == response.status_code
