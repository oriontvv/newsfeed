"""Application test fixtures."""

from pytest import fixture

from newsfeed.app import application


@fixture
def web_app():
    """Create test web application."""
    app = application.Application()
    web_app = app.create_web_app()

    return web_app


@fixture
async def web_client(aiohttp_client, web_app):
    """Create test application client."""
    return await aiohttp_client(web_app)