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
@pytest.mark.parametrize("sql,expected", [
    ("select dateutil_parse('1st october 2009')", "2009-10-01T00:00:00"),
    ("select dateutil_parse('invalid')", None),
    ("select dateutil_parse('due on 1st october 2009')", None),
    ("select dateutil_parse_fuzzy('due on 1st october 2009')", "2009-10-01T00:00:00"),
    ("select dateutil_parse_fuzzy('due on')", None),
    ("select dateutil_parse_dayfirst('1/2/2020')", "2020-02-01T00:00:00"),
    ("select dateutil_parse('1/2/2020')", "2020-01-02T00:00:00"),
    ("select dateutil_parse_fuzzy('due on 1/2/2003')", "2003-01-02T00:00:00"),
    ("select dateutil_parse_fuzzy_dayfirst('due on 1/2/2003')", "2003-02-01T00:00:00"),
    ("select dateutil_easter(2020)", "2020-04-12"),
    ("select dateutil_easter('invalid')", None),
])
async def test_dateutil_sql_functions(sql, expected):
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/:memory:.json", params={
            "sql": sql,
            "_shape": "array",
        })
        assert 200 == response.status_code
        actual = list(response.json()[0].values())[0]
        assert actual == expected
