"""
UI Client for web automation testing.

This module provides both synchronous and asynchronous UI clients
for browser automation using Playwright.

Classes:
    AsyncUiClient: Asynchronous UI client (main, for production)
    SyncUiClient: Synchronous UI client (for simple cases)
    UiClient: Alias for AsyncUiClient (default)

Page Objects:
    BasePage, Component, PageFactory: Async page objects (from page_objects)
    SyncBasePage, SyncComponent, SyncPageFactory: Sync page objects (from sync_page_objects)
"""

from .async_ui_client.page_objects import BasePage as AsyncBasePage
from .async_ui_client.page_objects import Component as AsyncComponent
from .async_ui_client.page_objects import PageFactory as AsyncPageFactory
from .async_ui_client.ui_client import UiClient as AsyncUiClient
from .sync_ui_client.page_objects import BasePage as SyncBasePage
from .sync_ui_client.page_objects import Component as SyncComponent
from .sync_ui_client.page_objects import PageFactory as SyncPageFactory
from .sync_ui_client.ui_client import UiClient as SyncUiClient

# Default export is async version (recommended for production)
UiClient = AsyncUiClient

__all__ = [
    "AsyncUiClient",
    "SyncUiClient",
    # Async page objects
    "AsyncBasePage",
    "AsyncComponent",
    "AsyncPageFactory",
    # Sync page objects
    "SyncBasePage",
    "SyncComponent",
    "SyncPageFactory",
]
