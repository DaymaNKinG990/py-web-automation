"""
Unit tests for plugins module.
"""

from unittest.mock import patch

import allure
import pytest

from py_web_automation.metrics import Metrics
from py_web_automation.plugins import (
    HookContext,
    HookType,
    LoggingPlugin,
    MetricsPlugin,
    Plugin,
    PluginManager,
)

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class MockPlugin(Plugin):
    """Test plugin implementation."""

    def get_name(self) -> str:
        """Get plugin name."""
        return "test_plugin"

    def on_before_request(self, context: HookContext) -> None:
        """Handle before request hook."""
        context.metadata["called"] = True


@pytest.mark.unit
class TestPluginManager:
    """Test PluginManager class."""

    @allure.title("TC-PL-001: PluginManager - инициализация")
    @allure.description("Test PluginManager initialization. TC-PL-001")
    def test_plugin_manager_init(self):
        """Test PluginManager initialization."""
        with allure.step("Create PluginManager"):
            manager = PluginManager()

        with allure.step("Verify _plugins and _hooks initialized"):
            assert manager._plugins == {}
            assert len(manager._hooks) == len(HookType)

    @allure.title("TC-PL-002: PluginManager - register")
    @allure.description("Test plugin registration. TC-PL-002")
    def test_plugin_manager_register(self):
        """Test plugin registration."""
        with allure.step("Create PluginManager and Plugin"):
            manager = PluginManager()
            plugin = MockPlugin()

        with allure.step("Register plugin"):
            result = manager.register(plugin)

        with allure.step("Verify plugin stored and hooks registered"):
            assert "test_plugin" in manager._plugins
            assert manager._plugins["test_plugin"] == plugin
            assert result is manager  # Method chaining

    @allure.title("TC-PL-003: PluginManager - register дубликат")
    @allure.description("Test error on duplicate registration. TC-PL-003")
    def test_plugin_manager_register_duplicate(self):
        """Test error on duplicate registration."""
        with allure.step("Create PluginManager and register plugin"):
            manager = PluginManager()
            plugin = MockPlugin()
            manager.register(plugin)

        with allure.step("Register same plugin again and expect ValueError"):
            with pytest.raises(ValueError, match="already registered"):
                manager.register(plugin)

    @allure.title("TC-PL-004: PluginManager - unregister")
    @allure.description("Test plugin unregistration. TC-PL-004")
    def test_plugin_manager_unregister(self):
        """Test plugin unregistration."""
        with allure.step("Create PluginManager and register plugin"):
            manager = PluginManager()
            plugin = MockPlugin()
            manager.register(plugin)

        with allure.step("Unregister plugin"):
            result = manager.unregister("test_plugin")

        with allure.step("Verify plugin removed and hooks cleared"):
            assert "test_plugin" not in manager._plugins
            assert result is manager  # Method chaining

    @allure.title("TC-PL-005: PluginManager - unregister несуществующий")
    @allure.description("Test no error on unregistering non-existent plugin. TC-PL-005")
    def test_plugin_manager_unregister_not_found(self):
        """Test no error on unregistering non-existent plugin."""
        with allure.step("Create PluginManager without plugins"):
            manager = PluginManager()

        with allure.step("Unregister non-existent plugin"):
            result = manager.unregister("nonexistent")

        with allure.step("Verify no error, method chaining works"):
            assert result is manager

    @pytest.mark.asyncio
    @allure.title("TC-PL-006: PluginManager - execute_hook")
    @allure.description("Test hook execution. TC-PL-006")
    async def test_plugin_manager_execute_hook(self):
        """Test hook execution."""
        with allure.step("Create PluginManager and register plugin"):
            manager = PluginManager()
            plugin = MockPlugin()
            manager.register(plugin)

        with allure.step("Execute hook"):
            context = HookContext(hook_type=HookType.BEFORE_REQUEST, data={"method": "GET", "url": "/test"})
            await manager.execute_hook(HookType.BEFORE_REQUEST, context)

        with allure.step("Verify handler called"):
            assert context.metadata.get("called") is True

    @pytest.mark.asyncio
    @allure.title("TC-PL-007: PluginManager - execute_hook обработка ошибок")
    @allure.description("Test error handling in hooks. TC-PL-007")
    async def test_plugin_manager_execute_hook_error_handling(self):
        """Test error handling in hooks."""
        with allure.step("Create PluginManager and plugin that raises error"):
            manager = PluginManager()

            class ErrorPlugin(Plugin):
                def get_name(self) -> str:
                    return "error_plugin"

                def on_before_request(self, context: HookContext) -> None:
                    raise ValueError("test error")

            plugin = ErrorPlugin()
            manager.register(plugin)

        with allure.step("Execute hook and verify error logged"):
            context = HookContext(hook_type=HookType.BEFORE_REQUEST)
            with patch("loguru.logger.error") as mock_log:
                await manager.execute_hook(HookType.BEFORE_REQUEST, context)
                mock_log.assert_called_once()

    @allure.title("TC-PL-008: PluginManager - get_plugin")
    @allure.description("Test getting plugin by name. TC-PL-008")
    def test_plugin_manager_get_plugin(self):
        """Test getting plugin by name."""
        with allure.step("Create PluginManager and register plugin"):
            manager = PluginManager()
            plugin = MockPlugin()
            manager.register(plugin)

        with allure.step("Get plugin by name"):
            retrieved_plugin = manager.get_plugin("test_plugin")

        with allure.step("Verify plugin returned"):
            assert retrieved_plugin == plugin

    @allure.title("TC-PL-009: PluginManager - get_plugin не найден")
    @allure.description("Test None returned when plugin not found. TC-PL-009")
    def test_plugin_manager_get_plugin_not_found(self):
        """Test None returned when plugin not found."""
        with allure.step("Create PluginManager without plugins"):
            manager = PluginManager()

        with allure.step("Get non-existent plugin"):
            plugin = manager.get_plugin("nonexistent")

        with allure.step("Verify None returned"):
            assert plugin is None

    @allure.title("TC-PL-010: PluginManager - list_plugins")
    @allure.description("Test listing all plugins. TC-PL-010")
    def test_plugin_manager_list_plugins(self):
        """Test listing all plugins."""
        with allure.step("Create PluginManager and register 3 plugins"):
            manager = PluginManager()
            for i in range(3):
                plugin = MockPlugin()
                plugin.get_name = lambda idx=i: f"plugin_{idx}"  # Capture i in closure
                manager.register(plugin)

        with allure.step("List plugins"):
            plugins = manager.list_plugins()

        with allure.step("Verify list of plugin names returned"):
            assert len(plugins) == 3
            assert all(f"plugin_{i}" in plugins for i in range(3))


@pytest.mark.unit
class TestPlugin:
    """Test Plugin base class."""

    @allure.title("TC-PL-011: Plugin - get_name")
    @allure.description("Test plugin name retrieval. TC-PL-011")
    def test_plugin_get_name(self):
        """Test plugin name retrieval."""
        with allure.step("Create Plugin subclass"):
            plugin = MockPlugin()

        with allure.step("Call get_name"):
            name = plugin.get_name()

        with allure.step("Verify name returned"):
            assert name == "test_plugin"

    @allure.title("TC-PL-012: Plugin - hook методы")
    @allure.description("Test hook methods can be overridden. TC-PL-012")
    def test_plugin_hook_methods(self):
        """Test hook methods can be overridden."""
        with allure.step("Create Plugin subclass with hook override"):
            plugin = MockPlugin()

        with allure.step("Call hook method"):
            context = HookContext(hook_type=HookType.BEFORE_REQUEST)
            plugin.on_before_request(context)

        with allure.step("Verify method can be called"):
            assert context.metadata.get("called") is True

    @allure.title("TC-PL-HOOKS-001: Plugin - проверка вызова всех hook методов")
    @allure.description("Test all hook methods can be called on Plugin base class. TC-PL-HOOKS-001")
    def test_plugin_all_hook_methods(self):
        """Test all hook methods can be called on Plugin base class."""
        with allure.step("Create Plugin subclass"):
            plugin = MockPlugin()

        with allure.step("Create HookContext"):
            context = HookContext(hook_type=HookType.BEFORE_REQUEST)

        with allure.step("Call all hook methods and verify no exceptions raised"):
            # Test all hook methods from Plugin base class
            plugin.on_before_request(context)
            plugin.on_after_request(context)
            plugin.on_error(context)
            plugin.on_before_validation(context)
            plugin.on_after_validation(context)
            plugin.on_before_ui_action(context)
            plugin.on_after_ui_action(context)

        with allure.step("Verify all methods can be called (default pass implementation)"):
            # If we get here without exceptions, all methods work
            assert True


@pytest.mark.unit
class TestBuiltInPlugins:
    """Test built-in plugins."""

    @allure.title("TC-PL-013: LoggingPlugin - инициализация и методы")
    @allure.description("Test LoggingPlugin functionality. TC-PL-013")
    def test_logging_plugin(self):
        """Test LoggingPlugin functionality."""
        with allure.step("Create LoggingPlugin"):
            plugin = LoggingPlugin()

        with allure.step("Call get_name"):
            name = plugin.get_name()

        with allure.step("Call on_before_request"):
            context = HookContext(hook_type=HookType.BEFORE_REQUEST, data={"method": "GET", "url": "/test"})
            with patch("loguru.logger.info") as mock_log:
                plugin.on_before_request(context)
                mock_log.assert_called_once()

        with allure.step("Verify LoggingPlugin works correctly"):
            assert name == "logging"

    @allure.title("TC-PL-014: MetricsPlugin - инициализация и методы")
    @allure.description("Test MetricsPlugin functionality. TC-PL-014")
    def test_metrics_plugin(self):
        """Test MetricsPlugin functionality."""
        with allure.step("Create MetricsPlugin"):
            metrics = Metrics()
            plugin = MetricsPlugin(metrics)

        with allure.step("Call get_name"):
            name = plugin.get_name()

        with allure.step("Call on_after_request"):
            context = HookContext(
                hook_type=HookType.AFTER_REQUEST,
                data={"success": True, "latency": 0.5},
            )
            plugin.on_after_request(context)

        with allure.step("Verify metrics recorded"):
            assert name == "metrics"
            assert metrics.request_count == 1
            assert metrics.success_count == 1

    @allure.title("TC-PL-LOGGING-001: LoggingPlugin - on_after_request")
    @allure.description("Test LoggingPlugin.on_after_request logs response details. TC-PL-LOGGING-001")
    def test_logging_plugin_on_after_request(self):
        """Test LoggingPlugin.on_after_request logs response details."""
        with allure.step("Create LoggingPlugin"):
            plugin = LoggingPlugin()

        with allure.step("Create HookContext with status_code in data"):
            context = HookContext(hook_type=HookType.AFTER_REQUEST, data={"status_code": 200})

        with allure.step("Call on_after_request and verify logger.info called"):
            with patch("loguru.logger.info") as mock_log:
                plugin.on_after_request(context)
                mock_log.assert_called_once()
                # Verify the log message contains status code
                call_args = mock_log.call_args[0][0]
                assert "200" in call_args or "Response" in call_args

    @allure.title("TC-PL-METRICS-001: MetricsPlugin - инициализация с metrics=None")
    @allure.description("Test MetricsPlugin creates new Metrics when metrics=None. TC-PL-METRICS-001")
    def test_metrics_plugin_init_with_none(self):
        """Test MetricsPlugin creates new Metrics when metrics=None."""
        with allure.step("Create MetricsPlugin with metrics=None"):
            plugin = MetricsPlugin(metrics=None)

        with allure.step("Verify new Metrics instance created"):
            assert plugin.metrics is not None
            assert isinstance(plugin.metrics, Metrics)

        with allure.step("Verify metrics attribute set"):
            assert hasattr(plugin, "metrics")

    @allure.title("TC-PL-METRICS-002: MetricsPlugin - инициализация с переданным metrics")
    @allure.description("Test MetricsPlugin uses provided Metrics instance. TC-PL-METRICS-002")
    def test_metrics_plugin_init_with_provided_metrics(self):
        """Test MetricsPlugin uses provided Metrics instance."""
        with allure.step("Create Metrics instance"):
            metrics_instance = Metrics()

        with allure.step("Create MetricsPlugin with metrics=metrics_instance"):
            plugin = MetricsPlugin(metrics=metrics_instance)

        with allure.step("Verify metrics attribute set to provided instance"):
            assert plugin.metrics is metrics_instance
            assert plugin.metrics == metrics_instance
