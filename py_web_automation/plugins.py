"""
Plugin system for extending framework functionality.

This module provides a plugin system that allows extending framework
functionality through hooks and event handlers.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .metrics import Metrics


class HookType(Enum):
    """Types of hooks available in the plugin system."""

    BEFORE_REQUEST = "before_request"
    AFTER_REQUEST = "after_request"
    ON_ERROR = "on_error"
    BEFORE_VALIDATION = "before_validation"
    AFTER_VALIDATION = "after_validation"
    BEFORE_UI_ACTION = "before_ui_action"
    AFTER_UI_ACTION = "after_ui_action"


@dataclass
class HookContext:
    """
    Context object passed to hook handlers.

    Attributes:
        hook_type: Type of hook being executed
        data: Hook-specific data dictionary
        metadata: Additional metadata for hook communication
    """

    hook_type: HookType
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class Plugin(ABC):
    """
    Base class for framework plugins.

    Plugins can hook into various framework events to extend functionality.
    Implement specific hook methods to handle events.

    Example:
        >>> class LoggingPlugin(Plugin):
        ...     def on_before_request(self, context: HookContext) -> None:
        ...         print(f"Request: {context.data.get('method')} {context.data.get('url')}")
        ...     def on_after_request(self, context: HookContext) -> None:
        ...         print(f"Response: {context.data.get('status_code')}")
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Get plugin name.

        Returns:
            Plugin name
        """
        pass

    def on_before_request(self, context: HookContext) -> None:
        """Called before making HTTP request."""
        pass

    def on_after_request(self, context: HookContext) -> None:
        """Called after receiving HTTP response."""
        pass

    def on_error(self, context: HookContext) -> None:
        """Called when an error occurs."""
        pass

    def on_before_validation(self, context: HookContext) -> None:
        """Called before response validation."""
        pass

    def on_after_validation(self, context: HookContext) -> None:
        """Called after response validation."""
        pass

    def on_before_ui_action(self, context: HookContext) -> None:
        """Called before UI action (click, fill, etc.)."""
        pass

    def on_after_ui_action(self, context: HookContext) -> None:
        """Called after UI action."""
        pass


class PluginManager:
    """
    Manager for framework plugins.

    Registers and executes plugins for various framework hooks.

    Attributes:
        _plugins: Dictionary of registered plugins by name
        _hooks: Dictionary of hook handlers by hook type

    Example:
        >>> manager = PluginManager()
        >>> manager.register(LoggingPlugin())
        >>> manager.register(MetricsPlugin())
        >>> # Plugins are automatically called on relevant events
    """

    def __init__(self) -> None:
        """Initialize plugin manager."""
        self._plugins: dict[str, Plugin] = {}
        self._hooks: dict[HookType, list[Callable[[HookContext], None]]] = {hook_type: [] for hook_type in HookType}

    def register(self, plugin: Plugin) -> "PluginManager":
        """
        Register a plugin.

        Args:
            plugin: Plugin instance to register

        Returns:
            Self for method chaining

        Example:
            >>> manager.register(MyPlugin())
        """
        name = plugin.get_name()
        if name in self._plugins:
            raise ValueError(f"Plugin '{name}' is already registered")

        self._plugins[name] = plugin

        # Register hook handlers
        if hasattr(plugin, "on_before_request"):
            self._hooks[HookType.BEFORE_REQUEST].append(plugin.on_before_request)
        if hasattr(plugin, "on_after_request"):
            self._hooks[HookType.AFTER_REQUEST].append(plugin.on_after_request)
        if hasattr(plugin, "on_error"):
            self._hooks[HookType.ON_ERROR].append(plugin.on_error)
        if hasattr(plugin, "on_before_validation"):
            self._hooks[HookType.BEFORE_VALIDATION].append(plugin.on_before_validation)
        if hasattr(plugin, "on_after_validation"):
            self._hooks[HookType.AFTER_VALIDATION].append(plugin.on_after_validation)
        if hasattr(plugin, "on_before_ui_action"):
            self._hooks[HookType.BEFORE_UI_ACTION].append(plugin.on_before_ui_action)
        if hasattr(plugin, "on_after_ui_action"):
            self._hooks[HookType.AFTER_UI_ACTION].append(plugin.on_after_ui_action)

        return self

    def unregister(self, plugin_name: str) -> "PluginManager":
        """
        Unregister a plugin.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            Self for method chaining
        """
        if plugin_name not in self._plugins:
            return self

        plugin = self._plugins[plugin_name]
        del self._plugins[plugin_name]

        # Remove hook handlers
        for hook_type in HookType:
            hook_handlers = self._hooks[hook_type]
            # Remove plugin's hook methods
            if hook_type == HookType.BEFORE_REQUEST and hasattr(plugin, "on_before_request"):
                if plugin.on_before_request in hook_handlers:
                    hook_handlers.remove(plugin.on_before_request)
            elif hook_type == HookType.AFTER_REQUEST and hasattr(plugin, "on_after_request"):
                if plugin.on_after_request in hook_handlers:
                    hook_handlers.remove(plugin.on_after_request)
            elif hook_type == HookType.ON_ERROR and hasattr(plugin, "on_error"):
                if plugin.on_error in hook_handlers:
                    hook_handlers.remove(plugin.on_error)
            elif hook_type == HookType.BEFORE_VALIDATION and hasattr(plugin, "on_before_validation"):
                if plugin.on_before_validation in hook_handlers:
                    hook_handlers.remove(plugin.on_before_validation)
            elif hook_type == HookType.AFTER_VALIDATION and hasattr(plugin, "on_after_validation"):
                if plugin.on_after_validation in hook_handlers:
                    hook_handlers.remove(plugin.on_after_validation)
            elif hook_type == HookType.BEFORE_UI_ACTION and hasattr(plugin, "on_before_ui_action"):
                if plugin.on_before_ui_action in hook_handlers:
                    hook_handlers.remove(plugin.on_before_ui_action)
            elif hook_type == HookType.AFTER_UI_ACTION and hasattr(plugin, "on_after_ui_action"):
                if plugin.on_after_ui_action in hook_handlers:
                    hook_handlers.remove(plugin.on_after_ui_action)

        return self

    async def execute_hook(self, hook_type: HookType, context: HookContext) -> None:
        """
        Execute all handlers for a hook.

        Args:
            hook_type: Type of hook to execute
            context: Hook context with data
        """
        handlers = self._hooks.get(hook_type, [])
        for handler in handlers:
            try:
                handler(context)
            except Exception as e:
                # Log error but don't stop other handlers
                from loguru import logger

                logger.error(f"Plugin hook error: {e}")

    def get_plugin(self, name: str) -> Plugin | None:
        """
        Get registered plugin by name.

        Args:
            name: Plugin name

        Returns:
            Plugin instance if found, None otherwise
        """
        return self._plugins.get(name)

    def list_plugins(self) -> list[str]:
        """
        List all registered plugin names.

        Returns:
            List of plugin names
        """
        return list(self._plugins.keys())


# Built-in plugins


class LoggingPlugin(Plugin):
    """Built-in plugin for request/response logging."""

    def get_name(self) -> str:
        """Get plugin name."""
        return "logging"

    def on_before_request(self, context: HookContext) -> None:
        """Log request details."""
        from loguru import logger

        method = context.data.get("method", "UNKNOWN")
        url = context.data.get("url", "UNKNOWN")
        logger.info(f"Plugin: Request {method} {url}")

    def on_after_request(self, context: HookContext) -> None:
        """Log response details."""
        from loguru import logger

        status = context.data.get("status_code", 0)
        logger.info(f"Plugin: Response {status}")


class MetricsPlugin(Plugin):
    """Built-in plugin for collecting metrics."""

    def __init__(self, metrics: Optional["Metrics"] = None) -> None:
        """
        Initialize metrics plugin.

        Args:
            metrics: Metrics object to use (creates new one if None)
        """
        if metrics is None:
            from .metrics import Metrics

            metrics = Metrics()
        self.metrics = metrics

    def get_name(self) -> str:
        """Get plugin name."""
        return "metrics"

    def on_after_request(self, context: HookContext) -> None:
        """Record request metrics."""
        success = context.data.get("success", False)
        latency = context.data.get("latency", 0.0)
        error_type = context.data.get("error_type")
        self.metrics.record_request(success=success, latency=latency, error_type=error_type)
