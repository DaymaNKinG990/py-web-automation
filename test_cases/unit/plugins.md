# Plugins Module - Unit Test Cases

## Overview
Tests for `py_web_automation.plugins` module - plugin system for extending framework functionality.

## Test Categories

### 1. PluginManager Tests

#### TC-PL-001: PluginManager - инициализация
- **Purpose**: Verify PluginManager initialization
- **Preconditions**: None
- **Test Steps**:
  1. Create PluginManager
  2. Verify _plugins and _hooks initialized
- **Expected Result**: PluginManager initialized correctly
- **Coverage**: `PluginManager.__init__` method

#### TC-PL-002: PluginManager - register
- **Purpose**: Verify plugin registration
- **Preconditions**: PluginManager, Plugin instance
- **Test Steps**:
  1. Create PluginManager
  2. Create Plugin instance
  3. Call register(plugin)
  4. Verify plugin stored and hooks registered
- **Expected Result**: Plugin registered, hooks added
- **Coverage**: `PluginManager.register` method

#### TC-PL-003: PluginManager - register дубликат
- **Purpose**: Verify error on duplicate registration
- **Preconditions**: PluginManager with registered plugin
- **Test Steps**:
  1. Create PluginManager
  2. Register plugin
  3. Register same plugin again
  4. Verify ValueError raised
- **Expected Result**: ValueError: "Plugin 'name' is already registered"
- **Coverage**: `PluginManager.register` method - duplicate

#### TC-PL-004: PluginManager - unregister
- **Purpose**: Verify plugin unregistration
- **Preconditions**: PluginManager with registered plugin
- **Test Steps**:
  1. Create PluginManager
  2. Register plugin
  3. Call unregister(plugin_name)
  4. Verify plugin removed and hooks cleared
- **Expected Result**: Plugin unregistered
- **Coverage**: `PluginManager.unregister` method

#### TC-PL-005: PluginManager - unregister несуществующий
- **Purpose**: Verify no error on unregistering non-existent plugin
- **Preconditions**: PluginManager without plugin
- **Test Steps**:
  1. Create PluginManager
  2. Call unregister("nonexistent")
  3. Verify no error, method chaining works
- **Expected Result**: No error, returns self
- **Coverage**: `PluginManager.unregister` method - not found

#### TC-PL-006: PluginManager - execute_hook
- **Purpose**: Verify hook execution
- **Preconditions**: PluginManager with registered plugin
- **Test Steps**:
  1. Create PluginManager
  2. Register plugin with hook handler
  3. Call execute_hook(HookType.BEFORE_REQUEST, context)
  4. Verify handler called
- **Expected Result**: Hook handler executed
- **Coverage**: `PluginManager.execute_hook` method

#### TC-PL-007: PluginManager - execute_hook обработка ошибок
- **Purpose**: Verify error handling in hooks
- **Preconditions**: PluginManager with plugin that raises error
- **Test Steps**:
  1. Create PluginManager
  2. Register plugin with error-raising handler
  3. Call execute_hook()
  4. Verify error logged but doesn't stop other handlers
- **Expected Result**: Error handled gracefully
- **Coverage**: `PluginManager.execute_hook` method - error handling

#### TC-PL-008: PluginManager - get_plugin
- **Purpose**: Verify getting plugin by name
- **Preconditions**: PluginManager with registered plugin
- **Test Steps**:
  1. Create PluginManager
  2. Register plugin
  3. Call get_plugin(plugin_name)
  4. Verify plugin returned
- **Expected Result**: Plugin returned
- **Coverage**: `PluginManager.get_plugin` method

#### TC-PL-009: PluginManager - get_plugin не найден
- **Purpose**: Verify None returned when plugin not found
- **Preconditions**: PluginManager without plugin
- **Test Steps**:
  1. Create PluginManager
  2. Call get_plugin("nonexistent")
  3. Verify None returned
- **Expected Result**: None returned
- **Coverage**: `PluginManager.get_plugin` method - not found

#### TC-PL-010: PluginManager - list_plugins
- **Purpose**: Verify listing all plugins
- **Preconditions**: PluginManager with multiple plugins
- **Test Steps**:
  1. Create PluginManager
  2. Register 3 plugins
  3. Call list_plugins()
  4. Verify list of 3 plugin names returned
- **Expected Result**: List of plugin names returned
- **Coverage**: `PluginManager.list_plugins` method

### 2. Plugin Tests

#### TC-PL-011: Plugin - get_name
- **Purpose**: Verify plugin name retrieval
- **Preconditions**: Plugin instance
- **Test Steps**:
  1. Create Plugin subclass
  2. Implement get_name()
  3. Call get_name()
  4. Verify name returned
- **Expected Result**: Plugin name returned
- **Coverage**: `Plugin.get_name` method

#### TC-PL-012: Plugin - hook методы
- **Purpose**: Verify hook methods can be overridden
- **Preconditions**: Plugin subclass
- **Test Steps**:
  1. Create Plugin subclass
  2. Override on_before_request
  3. Verify method can be called
- **Expected Result**: Hook methods can be overridden
- **Coverage**: `Plugin` hook methods

### 3. Built-in Plugins Tests

#### TC-PL-013: LoggingPlugin - инициализация и методы
- **Purpose**: Verify LoggingPlugin functionality
- **Preconditions**: LoggingPlugin instance
- **Test Steps**:
  1. Create LoggingPlugin
  2. Call get_name()
  3. Call on_before_request(context)
  4. Verify logging performed
- **Expected Result**: LoggingPlugin works correctly
- **Coverage**: `LoggingPlugin` class

#### TC-PL-014: MetricsPlugin - инициализация и методы
- **Purpose**: Verify MetricsPlugin functionality
- **Preconditions**: MetricsPlugin instance
- **Test Steps**:
  1. Create MetricsPlugin
  2. Call get_name()
  3. Call on_after_request(context)
  4. Verify metrics recorded
- **Expected Result**: MetricsPlugin works correctly
- **Coverage**: `MetricsPlugin` class

#### TC-PL-LOGGING-001: LoggingPlugin - on_after_request
- **Purpose**: Verify LoggingPlugin.on_after_request logs response details
- **Preconditions**: LoggingPlugin instance, HookContext with response data
- **Test Steps**:
  1. Create LoggingPlugin
  2. Create HookContext with status_code in data
  3. Call on_after_request(context)
  4. Verify logger.info called with response status code
- **Expected Result**: Response status logged correctly
- **Coverage**: `LoggingPlugin.on_after_request` method

#### TC-PL-METRICS-001: MetricsPlugin - инициализация с metrics=None
- **Purpose**: Verify MetricsPlugin creates new Metrics when metrics=None
- **Preconditions**: None
- **Test Steps**:
  1. Create MetricsPlugin with metrics=None
  2. Verify new Metrics instance created
  3. Verify metrics attribute set
- **Expected Result**: New Metrics instance created automatically
- **Coverage**: `MetricsPlugin.__init__` with metrics=None

#### TC-PL-METRICS-002: MetricsPlugin - инициализация с переданным metrics
- **Purpose**: Verify MetricsPlugin uses provided Metrics instance
- **Preconditions**: Metrics instance
- **Test Steps**:
  1. Create Metrics instance
  2. Create MetricsPlugin with metrics=metrics_instance
  3. Verify metrics attribute set to provided instance
- **Expected Result**: Provided Metrics instance used
- **Coverage**: `MetricsPlugin.__init__` with provided metrics

#### TC-PL-HOOKS-001: Plugin - проверка вызова всех hook методов
- **Purpose**: Verify all hook methods can be called on Plugin base class
- **Preconditions**: Plugin subclass instance
- **Test Steps**:
  1. Create Plugin subclass
  2. Create HookContext
  3. Call all hook methods: on_before_request, on_after_request, on_error, on_before_validation, on_after_validation, on_before_ui_action, on_after_ui_action
  4. Verify no exceptions raised
- **Expected Result**: All hook methods can be called (default pass implementation)
- **Coverage**: `Plugin` hook methods (default implementations)

