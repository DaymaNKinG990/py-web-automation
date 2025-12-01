# Plugins Integration Test Cases

## Overview
Integration tests for plugin system with ApiClient and other clients.
Tests verify plugin hooks, event handling, and plugin integration.

## Test Categories

### 1. PluginManager with ApiClient

#### TC-INTEGRATION-PLUGINS-001: PluginManager с ApiClient - hook execution
- **Purpose**: Verify PluginManager executes hooks with ApiClient
- **Preconditions**:
  - ApiClient instance
  - PluginManager instance
  - Custom plugin implementing hooks
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create PluginManager instance
  3. Create custom plugin implementing hooks:
     ```python
     class TestPlugin(Plugin):
         def __init__(self):
             self.before_request_called = False
             self.after_request_called = False
         
         async def on_before_request(self, context: HookContext):
             self.before_request_called = True
         
         async def on_after_request(self, context: HookContext):
             self.after_request_called = True
     ```
  4. Register plugin with PluginManager:
     ```python
     plugin = TestPlugin()
     plugin_manager.register(plugin)
     ```
  5. Mock HTTP response (status 200)
  6. Make request using `make_request()`
  7. Verify hooks executed:
     - on_before_request called
     - on_after_request called
     - Hook context contains request data
- **Expected Result**: PluginManager executes hooks correctly with ApiClient
- **Coverage**: `PluginManager.register()`, hook execution, `Plugin.on_before_request()`, `Plugin.on_after_request()`
- **Dependencies**: ApiClient, PluginManager, custom plugin

#### TC-INTEGRATION-PLUGINS-002: PluginManager с GraphQLClient
- **Purpose**: Verify PluginManager works with GraphQLClient
- **Preconditions**:
  - GraphQLClient instance
  - PluginManager instance
  - Custom plugin
  - Mock GraphQL endpoint
- **Test Steps**:
  1. Create GraphQLClient with base URL
  2. Create PluginManager instance
  3. Create and register custom plugin
  4. Mock GraphQL response (status 200)
  5. Execute GraphQL query
  6. Verify hooks executed (if integrated):
     - on_before_request called
     - on_after_request called
- **Expected Result**: PluginManager works with GraphQLClient (if integrated)
- **Coverage**: PluginManager with GraphQLClient
- **Dependencies**: GraphQLClient, PluginManager, custom plugin

#### TC-INTEGRATION-PLUGINS-003: PluginManager с SoapClient
- **Purpose**: Verify PluginManager works with SoapClient
- **Preconditions**:
  - SoapClient instance
  - PluginManager instance
  - Custom plugin
  - Mock SOAP endpoint
- **Test Steps**:
  1. Create SoapClient with base URL
  2. Create PluginManager instance
  3. Create and register custom plugin
  4. Mock SOAP response (status 200)
  5. Execute SOAP call
  6. Verify hooks executed (if integrated):
     - on_before_request called
     - on_after_request called
- **Expected Result**: PluginManager works with SoapClient (if integrated)
- **Coverage**: PluginManager with SoapClient
- **Dependencies**: SoapClient, PluginManager, custom plugin

#### TC-INTEGRATION-PLUGINS-004: PluginManager с WebSocketClient
- **Purpose**: Verify PluginManager works with WebSocketClient
- **Preconditions**:
  - WebSocketClient instance
  - PluginManager instance
  - Custom plugin
  - Mock WebSocket server
- **Test Steps**:
  1. Create WebSocketClient with WebSocket URL
  2. Create PluginManager instance
  3. Create and register custom plugin
  4. Connect to WebSocket
  5. Send message
  6. Verify hooks executed (if integrated):
     - on_before_request called (for send)
     - on_after_request called (for receive)
- **Expected Result**: PluginManager works with WebSocketClient (if integrated)
- **Coverage**: PluginManager with WebSocketClient
- **Dependencies**: WebSocketClient, PluginManager, custom plugin

#### TC-INTEGRATION-PLUGINS-005: PluginManager с UiClient - UI action hooks
- **Purpose**: Verify PluginManager works with UiClient for UI actions
- **Preconditions**:
  - UiClient instance
  - PluginManager instance
  - Custom plugin implementing UI hooks
  - Web page available
- **Test Steps**:
  1. Create UiClient with base URL
  2. Create PluginManager instance
  3. Create custom plugin implementing UI hooks:
     ```python
     class UIPlugin(Plugin):
         async def on_before_ui_action(self, context: HookContext):
             # Log UI action
             pass
         
         async def on_after_ui_action(self, context: HookContext):
             # Log UI action result
             pass
     ```
  4. Register plugin with PluginManager
  5. Perform UI actions (navigate, click, fill)
  6. Verify hooks executed (if integrated):
     - on_before_ui_action called
     - on_after_ui_action called
- **Expected Result**: PluginManager works with UiClient for UI actions (if integrated)
- **Coverage**: PluginManager with UiClient, UI action hooks
- **Dependencies**: UiClient, PluginManager, custom plugin

### 2. LoggingPlugin Integration

#### TC-INTEGRATION-PLUGINS-006: LoggingPlugin с ApiClient
- **Purpose**: Verify LoggingPlugin logs requests and responses
- **Preconditions**:
  - ApiClient instance
  - LoggingPlugin instance
  - Logger configured to capture logs
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create LoggingPlugin instance
  3. Register LoggingPlugin with PluginManager
  4. Configure logger to capture logs
  5. Mock HTTP response (status 200)
  6. Make request using `make_request()`
  7. Verify LoggingPlugin logged:
     - Request logged (method, URL, headers)
     - Response logged (status code, response time)
     - Logs captured by logger
- **Expected Result**: LoggingPlugin logs requests and responses correctly
- **Coverage**: LoggingPlugin.on_before_request(), LoggingPlugin.on_after_request()
- **Dependencies**: ApiClient, LoggingPlugin, logger

### 3. MetricsPlugin Integration

#### TC-INTEGRATION-PLUGINS-007: MetricsPlugin с ApiClient
- **Purpose**: Verify MetricsPlugin collects metrics automatically
- **Preconditions**:
  - ApiClient instance
  - MetricsPlugin instance with Metrics
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create Metrics instance
  3. Create MetricsPlugin with Metrics
  4. Register MetricsPlugin with PluginManager
  5. Mock HTTP responses:
     - Request 1: status 200, latency 0.3s
     - Request 2: status 200, latency 0.5s
     - Request 3: status 500, latency 0.1s
  6. Make 3 requests using `make_request()`
  7. Verify MetricsPlugin collected metrics:
     - request_count = 3
     - success_count = 2
     - error_count = 1
     - Latency metrics collected
- **Expected Result**: MetricsPlugin collects metrics automatically
- **Coverage**: MetricsPlugin.on_before_request(), MetricsPlugin.on_after_request()
- **Dependencies**: ApiClient, MetricsPlugin, Metrics

### 4. Multiple Plugins

#### TC-INTEGRATION-PLUGINS-008: Multiple plugins в цепочке
- **Purpose**: Verify multiple plugins work together in chain
- **Preconditions**:
  - ApiClient instance
  - PluginManager instance
  - Multiple plugin instances (LoggingPlugin, MetricsPlugin, CustomPlugin)
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create PluginManager instance
  3. Create multiple plugins:
     - LoggingPlugin
     - MetricsPlugin
     - CustomPlugin
  4. Register all plugins with PluginManager
  5. Mock HTTP response (status 200)
  6. Make request using `make_request()`
  7. Verify all plugins executed:
     - LoggingPlugin logged request/response
     - MetricsPlugin collected metrics
     - CustomPlugin executed hooks
     - Plugins executed in registration order
- **Expected Result**: Multiple plugins work together in chain correctly
- **Coverage**: Multiple plugins, plugin chain execution
- **Dependencies**: ApiClient, PluginManager, multiple plugins

### 5. Plugin Error Handling

#### TC-INTEGRATION-PLUGINS-009: Plugin error handling
- **Purpose**: Verify plugin errors are handled gracefully
- **Preconditions**:
  - ApiClient instance
  - PluginManager instance
  - Custom plugin that raises exception
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create PluginManager instance
  3. Create custom plugin that raises exception in hook:
     ```python
     class ErrorPlugin(Plugin):
         async def on_before_request(self, context: HookContext):
             raise Exception("Plugin error")
     ```
  4. Register ErrorPlugin with PluginManager
  5. Mock HTTP response (status 200)
  6. Make request using `make_request()`
  7. Verify error handling:
     - Plugin error caught
     - Error logged (if logging enabled)
     - Request continues (or fails gracefully)
     - Other plugins still execute
- **Expected Result**: Plugin errors handled gracefully, don't break request flow
- **Coverage**: Plugin error handling, error recovery
- **Dependencies**: ApiClient, PluginManager, error-raising plugin

