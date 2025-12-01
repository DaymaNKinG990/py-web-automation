"""
Plugin system usage example.

This example demonstrates how to use the plugin system to extend
framework functionality with custom plugins.
"""

import asyncio

from py_web_automation.metrics import Metrics
from py_web_automation.plugins import (
    HookContext,
    HookType,
    LoggingPlugin,
    MetricsPlugin,
    Plugin,
    PluginManager,
)


class CustomLoggingPlugin(Plugin):
    """Custom logging plugin."""

    def get_name(self) -> str:
        return "custom_logging"

    def on_before_request(self, context: HookContext) -> None:
        method = context.data.get("method", "UNKNOWN")
        url = context.data.get("url", "UNKNOWN")
        print(f"   [Custom Plugin] Before request: {method} {url}")

    def on_after_request(self, context: HookContext) -> None:
        status = context.data.get("status_code", "UNKNOWN")
        print(f"   [Custom Plugin] After request: Status {status}")


class ErrorTrackingPlugin(Plugin):
    """Plugin for tracking errors."""

    def __init__(self):
        self.error_count = 0
        self.errors = []

    def get_name(self) -> str:
        return "error_tracking"

    def on_error(self, context: HookContext) -> None:
        self.error_count += 1
        error_type = context.data.get("error_type", "Unknown")
        error_message = context.data.get("error_message", "No message")
        self.errors.append({"type": error_type, "message": error_message})
        print(f"   [Error Tracker] Error #{self.error_count}: {error_type} - {error_message}")

    def get_error_summary(self) -> dict:
        return {
            "total_errors": self.error_count,
            "errors": self.errors,
        }


async def main():
    """Main function demonstrating plugins usage."""

    try:
        print("=== Plugins Examples ===\n")

        # Example 1: Using Built-in Plugins
        print("1. Using built-in plugins...")
        manager = PluginManager()
        manager.register(LoggingPlugin())
        manager.register(MetricsPlugin(Metrics()))

        # In real usage, plugins would be registered with ApiClient
        # api_client._plugin_manager = manager

        print("   Registered LoggingPlugin and MetricsPlugin")

        # Example 2: Custom Plugin
        print("\n2. Creating custom plugin...")
        custom_plugin = CustomLoggingPlugin()
        manager = PluginManager()
        manager.register(custom_plugin)

        print(f"   Registered plugin: {custom_plugin.get_name()}")

        # Example 3: Error Tracking Plugin
        print("\n3. Error tracking plugin...")
        error_plugin = ErrorTrackingPlugin()
        manager = PluginManager()
        manager.register(error_plugin)

        # Simulate error hook
        error_context = HookContext(
            hook_type=HookType.ON_ERROR,
            data={"error_type": "ConnectionError", "error_message": "Connection failed"},
        )
        error_plugin.on_error(error_context)

        summary = error_plugin.get_error_summary()
        print(f"   Error summary: {summary}")

        # Example 4: Multiple Plugins
        print("\n4. Using multiple plugins...")
        manager = PluginManager()
        manager.register(LoggingPlugin())
        manager.register(MetricsPlugin(Metrics()))
        manager.register(CustomLoggingPlugin())
        manager.register(ErrorTrackingPlugin())

        print(f"   Registered {len(manager._plugins)} plugins")

        # Example 5: Plugin Hook Execution
        print("\n5. Executing plugin hooks...")
        manager = PluginManager()
        manager.register(CustomLoggingPlugin())

        # Simulate before_request hook
        before_context = HookContext(
            hook_type=HookType.BEFORE_REQUEST,
            data={"method": "GET", "url": "/api/users"},
        )
        manager.execute_hook(HookType.BEFORE_REQUEST, before_context)

        # Simulate after_request hook
        after_context = HookContext(
            hook_type=HookType.AFTER_REQUEST,
            data={"status_code": 200, "response_time": 0.5},
        )
        manager.execute_hook(HookType.AFTER_REQUEST, after_context)

        # Example 6: Plugin Management
        print("\n6. Plugin management...")
        manager = PluginManager()
        plugin1 = CustomLoggingPlugin()
        plugin2 = ErrorTrackingPlugin()

        manager.register(plugin1)
        manager.register(plugin2)

        # Get plugin
        retrieved = manager.get_plugin("custom_logging")
        print(f"   Retrieved plugin: {retrieved.get_name() if retrieved else 'None'}")

        # Unregister plugin
        manager.unregister("error_tracking")
        print("   Unregistered error_tracking plugin")

        # Check if plugin exists
        exists = manager.get_plugin("error_tracking")
        print(f"   Plugin exists: {exists is not None}")

        # Example 7: Plugin with Metrics
        print("\n7. Plugin with metrics integration...")
        metrics = Metrics()
        metrics_plugin = MetricsPlugin(metrics)
        manager = PluginManager()
        manager.register(metrics_plugin)

        # Simulate request hooks
        for i in range(3):
            before_context = HookContext(
                hook_type=HookType.BEFORE_REQUEST,
                data={"method": "GET", "url": f"/api/endpoint-{i}"},
            )
            manager.execute_hook(HookType.BEFORE_REQUEST, before_context)

            after_context = HookContext(
                hook_type=HookType.AFTER_REQUEST,
                data={"status_code": 200, "response_time": 0.5},
            )
            manager.execute_hook(HookType.AFTER_REQUEST, after_context)

        print(f"   Metrics - Requests: {metrics.request_count}")

        print("\n=== Plugins Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
