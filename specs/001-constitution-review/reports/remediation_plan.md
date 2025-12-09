# Remediation Plan

Total remediation steps: 747

## Priority: CRITICAL

### STEP-570: Fix missing_context_manager in kafka_client.py

**Principle/Standard**: Resource Management
**Affected Files**: py_web_automation\clients\broker_clients\kafka_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in py_web_automation\clients\broker_clients\kafka_client.py

Suggested fix: Implement context manager methods in class 'KafkaClient' for proper resource cleanup

### STEP-571: Fix missing_context_manager in rabbitmq_client.py

**Principle/Standard**: Resource Management
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Implement context manager methods in class 'RabbitMQClient' for proper resource cleanup

### STEP-572: Fix missing_context_manager in mysql_client.py

**Principle/Standard**: Resource Management
**Affected Files**: py_web_automation\clients\db_clients\mysql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in py_web_automation\clients\db_clients\mysql_client.py

Suggested fix: Implement context manager methods in class 'MySQLClient' for proper resource cleanup

### STEP-573: Fix missing_context_manager in postgresql_client.py

**Principle/Standard**: Resource Management
**Affected Files**: py_web_automation\clients\db_clients\postgresql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in py_web_automation\clients\db_clients\postgresql_client.py

Suggested fix: Implement context manager methods in class 'PostgreSQLClient' for proper resource cleanup

### STEP-574: Fix missing_context_manager in sqlite_client.py

**Principle/Standard**: Resource Management
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Implement context manager methods in class 'SQLiteClient' for proper resource cleanup

### STEP-575: Fix missing_context_manager in test_kafka_client_integration.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\integration\test_kafka_client_integration.py

Suggested fix: Implement context manager methods in class 'TestKafkaClientIntegration' for proper resource cleanup

### STEP-576: Fix missing_context_manager in test_rabbitmq_client_integration.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Implement context manager methods in class 'TestRabbitMQClientIntegration' for proper resource cleanup

### STEP-577: Fix missing_context_manager in test_kafka_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_context_manager' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Implement context manager methods in class 'TestKafkaClientInit' for proper resource cleanup

### STEP-578: Fix missing_context_manager in test_rabbitmq_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_context_manager' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Implement context manager methods in class 'TestRabbitMQClientInit' for proper resource cleanup

### STEP-579: Fix missing_context_manager in test_db_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_context_manager' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Implement context manager methods in class 'TestDBClientInit' for proper resource cleanup

### STEP-580: Fix missing_context_manager in test_async_ui_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 1.1 hours
**Violations**: 13

Fix 13 violation(s) of type 'missing_context_manager' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Implement context manager methods in class 'TestUiClientInit' for proper resource cleanup

### STEP-581: Fix missing_context_manager in test_graphql_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Implement context manager methods in class 'TestGraphQLClient' for proper resource cleanup

### STEP-582: Fix missing_context_manager in test_grpc_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Implement context manager methods in class 'TestGrpcClient' for proper resource cleanup

### STEP-583: Fix missing_context_manager in test_grpc_client_additional.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Implement context manager methods in class 'TestGrpcClientAdditional' for proper resource cleanup

### STEP-584: Fix missing_context_manager in test_http_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_context_manager' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Implement context manager methods in class 'TestApiClientInit' for proper resource cleanup

### STEP-585: Fix missing_context_manager in test_soap_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Implement context manager methods in class 'TestSoapClient' for proper resource cleanup

### STEP-586: Fix missing_context_manager in test_websocket_client.py

**Principle/Standard**: Resource Management
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_context_manager' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Implement context manager methods in class 'TestWebSocketClient' for proper resource cleanup

## Priority: HIGH

### STEP-001: Fix missing_parameter_type_annotation in config.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\config.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\config.py

Suggested fix: Add type annotation to parameter 'cls' in function 'from_env'

### STEP-002: Fix missing_method_parameter_type_annotation in config.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\config.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\config.py

Suggested fix: Add type annotation to parameter 'cls' in method 'Config.from_env'

### STEP-003: Fix missing_parameter_type_annotation in broker_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\broker_clients\broker_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\broker_clients\broker_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-004: Fix missing_method_parameter_type_annotation in broker_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\broker_clients\broker_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\broker_clients\broker_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'BrokerClient.connect'

### STEP-005: Fix missing_parameter_type_annotation in kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\broker_clients\kafka_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\broker_clients\kafka_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-006: Fix missing_method_parameter_type_annotation in kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\broker_clients\kafka_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\broker_clients\kafka_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'KafkaClient.connect'

### STEP-007: Fix missing_parameter_type_annotation in rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-008: Fix missing_method_parameter_type_annotation in rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'RabbitMQClient.connect'

### STEP-009: Fix missing_parameter_type_annotation in db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\db_client.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\db_clients\db_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-010: Fix missing_method_parameter_type_annotation in db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\db_client.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\db_clients\db_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'DBClient.connect'

### STEP-011: Fix missing_parameter_type_annotation in mysql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\mysql_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\db_clients\mysql_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-012: Fix missing_method_parameter_type_annotation in mysql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\mysql_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\db_clients\mysql_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'MySQLClient.connect'

### STEP-013: Fix missing_parameter_type_annotation in postgresql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\postgresql_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\db_clients\postgresql_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-014: Fix missing_method_parameter_type_annotation in postgresql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\postgresql_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\db_clients\postgresql_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'PostgreSQLClient.connect'

### STEP-015: Fix missing_parameter_type_annotation in query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\query_builder.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\db_clients\query_builder.py

Suggested fix: Add type annotation to parameter 'self' in function 'select'

### STEP-016: Fix missing_parameter_type_annotation in sqlite_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-017: Fix missing_method_parameter_type_annotation in sqlite_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'SQLiteClient.connect'

### STEP-018: Fix missing_parameter_type_annotation in visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\visual_testing.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\ui_clients\visual_testing.py

Suggested fix: Add type annotation to parameter 'self' in function 'compare'

### STEP-019: Fix missing_method_parameter_type_annotation in visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\visual_testing.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\ui_clients\visual_testing.py

Suggested fix: Add type annotation to parameter 'self' in method 'VisualComparator.compare'

### STEP-020: Fix missing_parameter_type_annotation in graphql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\graphql_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'close'

### STEP-021: Fix missing_method_parameter_type_annotation in graphql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\graphql_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'GraphQLClient.close'

### STEP-022: Fix missing_parameter_type_annotation in graphql_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\graphql_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'raise_for_errors'

### STEP-023: Fix missing_method_parameter_type_annotation in graphql_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\graphql_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'GraphQLResult.raise_for_errors'

### STEP-024: Fix missing_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'record_request'

### STEP-025: Fix missing_method_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'Metrics.record_request'

### STEP-026: Fix missing_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'acquire'

### STEP-027: Fix missing_method_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimiter.acquire'

### STEP-028: Fix missing_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\retry.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in function 'calculate_delay'

### STEP-029: Fix missing_method_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\retry.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryConfig.calculate_delay'

### STEP-030: Fix missing_parameter_type_annotation in grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\grpc_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-031: Fix missing_method_parameter_type_annotation in grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\grpc_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'GrpcClient.connect'

### STEP-032: Fix missing_parameter_type_annotation in grpc_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\grpc_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'raise_for_error'

### STEP-033: Fix missing_method_parameter_type_annotation in grpc_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\grpc_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'GrpcResult.raise_for_error'

### STEP-034: Fix missing_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'record_request'

### STEP-035: Fix missing_method_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'Metrics.record_request'

### STEP-036: Fix missing_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'acquire'

### STEP-037: Fix missing_method_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimiter.acquire'

### STEP-038: Fix missing_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\retry.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in function 'calculate_delay'

### STEP-039: Fix missing_method_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\retry.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryConfig.calculate_delay'

### STEP-040: Fix missing_parameter_type_annotation in http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'close'

### STEP-041: Fix missing_method_parameter_type_annotation in http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'HttpClient.close'

### STEP-042: Fix missing_parameter_type_annotation in http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_result.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\http_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'json'

### STEP-043: Fix missing_method_parameter_type_annotation in http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_result.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\http_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'HttpResult.json'

### STEP-044: Fix missing_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\metrics.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'record_request'

### STEP-045: Fix missing_method_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\metrics.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'Metrics.record_request'

### STEP-046: Fix missing_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'acquire'

### STEP-047: Fix missing_method_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimiter.acquire'

### STEP-048: Fix missing_parameter_type_annotation in request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\request_builder.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\request_builder.py

Suggested fix: Add type annotation to parameter 'self' in function 'get_endpoint'

### STEP-049: Fix missing_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in function 'to_dict'

### STEP-050: Fix missing_method_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryConfig.to_dict'

### STEP-051: Fix missing_parameter_type_annotation in validator.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\validator.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\validator.py

Suggested fix: Add type annotation to parameter 'self' in function 'validate'

### STEP-052: Fix missing_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'record_request'

### STEP-053: Fix missing_method_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'Metrics.record_request'

### STEP-054: Fix missing_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'acquire'

### STEP-055: Fix missing_method_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimiter.acquire'

### STEP-056: Fix missing_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in function 'to_dict'

### STEP-057: Fix missing_method_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryConfig.to_dict'

### STEP-058: Fix missing_parameter_type_annotation in soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\soap_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'close'

### STEP-059: Fix missing_method_parameter_type_annotation in soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\soap_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'SoapClient.close'

### STEP-060: Fix missing_parameter_type_annotation in soap_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\soap_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'raise_for_fault'

### STEP-061: Fix missing_method_parameter_type_annotation in soap_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\soap_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'SoapResult.raise_for_fault'

### STEP-062: Fix missing_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'update_token'

### STEP-063: Fix missing_method_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'AuthMiddleware.update_token'

### STEP-064: Fix missing_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-065: Fix missing_method_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'LoggingMiddleware.process_request'

### STEP-066: Fix missing_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-067: Fix missing_method_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'MetricsMiddleware.process_request'

### STEP-068: Fix missing_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-069: Fix missing_method_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'Middleware.process_request'

### STEP-070: Fix missing_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-071: Fix missing_method_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimitMiddleware.process_request'

### STEP-072: Fix missing_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-073: Fix missing_method_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryMiddleware.process_request'

### STEP-074: Fix missing_parameter_type_annotation in validation_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-075: Fix missing_method_parameter_type_annotation in validation_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'ValidationMiddleware.process_request'

### STEP-076: Fix missing_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'update_token'

### STEP-077: Fix missing_method_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'AuthMiddleware.update_token'

### STEP-078: Fix missing_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-079: Fix missing_method_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'LoggingMiddleware.process_request'

### STEP-080: Fix missing_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-081: Fix missing_method_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'MetricsMiddleware.process_request'

### STEP-082: Fix missing_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-083: Fix missing_method_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'Middleware.process_request'

### STEP-084: Fix missing_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-085: Fix missing_method_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimitMiddleware.process_request'

### STEP-086: Fix missing_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-087: Fix missing_method_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryMiddleware.process_request'

### STEP-088: Fix missing_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'update_token'

### STEP-089: Fix missing_method_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'AuthMiddleware.update_token'

### STEP-090: Fix missing_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-091: Fix missing_method_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'LoggingMiddleware.process_request'

### STEP-092: Fix missing_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-093: Fix missing_method_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'MetricsMiddleware.process_request'

### STEP-094: Fix missing_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-095: Fix missing_method_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'Middleware.process_request'

### STEP-096: Fix missing_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-097: Fix missing_method_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimitMiddleware.process_request'

### STEP-098: Fix missing_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-099: Fix missing_method_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryMiddleware.process_request'

### STEP-100: Fix missing_parameter_type_annotation in validation_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-101: Fix missing_method_parameter_type_annotation in validation_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'ValidationMiddleware.process_request'

### STEP-102: Fix missing_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'update_token'

### STEP-103: Fix missing_method_parameter_type_annotation in auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'AuthMiddleware.update_token'

### STEP-104: Fix missing_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-105: Fix missing_method_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'LoggingMiddleware.process_request'

### STEP-106: Fix missing_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-107: Fix missing_method_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'MetricsMiddleware.process_request'

### STEP-108: Fix missing_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-109: Fix missing_method_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'Middleware.process_request'

### STEP-110: Fix missing_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-111: Fix missing_method_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimitMiddleware.process_request'

### STEP-112: Fix missing_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_request'

### STEP-113: Fix missing_method_parameter_type_annotation in retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryMiddleware.process_request'

### STEP-114: Fix missing_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'record_request'

### STEP-115: Fix missing_method_parameter_type_annotation in metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\metrics.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'Metrics.record_request'

### STEP-116: Fix missing_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'acquire'

### STEP-117: Fix missing_method_parameter_type_annotation in rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimiter.acquire'

### STEP-118: Fix missing_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in function 'to_dict'

### STEP-119: Fix missing_method_parameter_type_annotation in retry.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\retry.py

Suggested fix: Add type annotation to parameter 'self' in method 'RetryConfig.to_dict'

### STEP-120: Fix missing_parameter_type_annotation in websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'connect'

### STEP-121: Fix missing_method_parameter_type_annotation in websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'WebSocketClient.connect'

### STEP-122: Fix missing_parameter_type_annotation in websocket_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'raise_for_error'

### STEP-123: Fix missing_method_parameter_type_annotation in websocket_result.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'WebSocketResult.raise_for_error'

### STEP-124: Fix missing_parameter_type_annotation in connection_retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_message'

### STEP-125: Fix missing_method_parameter_type_annotation in connection_retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'ConnectionRetryMiddleware.process_message'

### STEP-126: Fix missing_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_message'

### STEP-127: Fix missing_method_parameter_type_annotation in logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'LoggingMiddleware.process_message'

### STEP-128: Fix missing_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_message'

### STEP-129: Fix missing_method_parameter_type_annotation in metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'MetricsMiddleware.process_message'

### STEP-130: Fix missing_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_message'

### STEP-131: Fix missing_method_parameter_type_annotation in middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'Middleware.process_message'

### STEP-132: Fix missing_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'process_message'

### STEP-133: Fix missing_method_parameter_type_annotation in rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'RateLimitMiddleware.process_message'

### STEP-134: Fix missing_parameter_type_annotation in page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\page_objects.py
**Estimated Effort**: 1.6 hours
**Violations**: 19

Fix 19 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\ui_clients\async_ui_client\page_objects.py

Suggested fix: Add type annotation to parameter 'self' in function 'navigate'

### STEP-135: Fix missing_method_parameter_type_annotation in page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\page_objects.py
**Estimated Effort**: 1.6 hours
**Violations**: 19

Fix 19 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\ui_clients\async_ui_client\page_objects.py

Suggested fix: Add type annotation to parameter 'self' in method 'BasePage.navigate'

### STEP-136: Fix missing_parameter_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'setup_browser'

### STEP-137: Fix missing_method_parameter_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'UiClient.setup_browser'

### STEP-138: Fix missing_parameter_type_annotation in page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py
**Estimated Effort**: 1.6 hours
**Violations**: 19

Fix 19 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py

Suggested fix: Add type annotation to parameter 'self' in function 'navigate'

### STEP-139: Fix missing_method_parameter_type_annotation in page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py
**Estimated Effort**: 1.6 hours
**Violations**: 19

Fix 19 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py

Suggested fix: Add type annotation to parameter 'self' in method 'BasePage.navigate'

### STEP-140: Fix missing_parameter_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_parameter_type_annotation' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'setup_browser'

### STEP-141: Fix missing_method_parameter_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_method_parameter_type_annotation' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'UiClient.setup_browser'

### STEP-142: Fix missing_return_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\conftest.py
**Estimated Effort**: 2.2 hours
**Violations**: 27

Fix 27 violation(s) of type 'missing_return_type_annotation' in tests\conftest.py

Suggested fix: Add return type annotation to function 'loguru_sink' (e.g., -> int, -> str, -> None)

### STEP-143: Fix missing_parameter_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\conftest.py
**Estimated Effort**: 2.2 hours
**Violations**: 26

Fix 26 violation(s) of type 'missing_parameter_type_annotation' in tests\conftest.py

Suggested fix: Add type annotation to parameter 'message' in function 'loguru_sink'

### STEP-144: Fix missing_return_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_return_type_annotation' in tests\fixtures\ui_client.py

Suggested fix: Add return type annotation to function 'ui_client_with_browser' (e.g., -> int, -> str, -> None)

### STEP-145: Fix missing_parameter_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_parameter_type_annotation' in tests\fixtures\ui_client.py

Suggested fix: Add type annotation to parameter 'ui_client_with_config' in function 'ui_client_with_browser'

### STEP-146: Fix missing_return_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\conftest.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_return_type_annotation' in tests\integration\conftest.py

Suggested fix: Add return type annotation to function 'integration_config' (e.g., -> int, -> str, -> None)

### STEP-147: Fix missing_parameter_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\conftest.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in tests\integration\conftest.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'integration_config'

### STEP-148: Fix missing_return_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_return_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add return type annotation to function 'check_kafka_available' (e.g., -> int, -> str, -> None)

### STEP-149: Fix missing_parameter_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_parameter_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_connect_to_real_kafka'

### STEP-150: Fix missing_method_return_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_method_return_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add return type annotation to method 'TestKafkaClientIntegration.test_connect_to_real_kafka'

### STEP-151: Fix missing_method_parameter_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_method_parameter_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestKafkaClientIntegration.test_connect_to_real_kafka'

### STEP-152: Fix missing_return_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_return_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add return type annotation to function 'check_rabbitmq_available' (e.g., -> int, -> str, -> None)

### STEP-153: Fix missing_parameter_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_parameter_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_connect_to_real_rabbitmq'

### STEP-154: Fix missing_method_return_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_method_return_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add return type annotation to method 'TestRabbitMQClientIntegration.test_connect_to_real_rabbitmq'

### STEP-155: Fix missing_method_parameter_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_method_parameter_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRabbitMQClientIntegration.test_connect_to_real_rabbitmq'

### STEP-156: Fix missing_parameter_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 1.1 days
**Violations**: 109

Fix 109 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\test_config.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_valid_config_creation'

### STEP-157: Fix missing_return_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_return_type_annotation' in tests\unit\test_config.py

Suggested fix: Add return type annotation to function 'test_config_validation_invalid_maximal_retry_count' (e.g., -> int, -> str, -> None)

### STEP-158: Fix missing_method_parameter_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 1.1 days
**Violations**: 109

Fix 109 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\test_config.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestConfigInit.test_valid_config_creation'

### STEP-159: Fix missing_method_return_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\test_config.py

Suggested fix: Add return type annotation to method 'TestConfigInit.test_config_validation_invalid_maximal_retry_count'

### STEP-160: Fix missing_return_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 2.6 hours
**Violations**: 31

Fix 31 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add return type annotation to function 'test_init_with_valid_url' (e.g., -> int, -> str, -> None)

### STEP-161: Fix missing_parameter_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 6.7 hours
**Violations**: 80

Fix 80 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init_with_valid_url'

### STEP-162: Fix missing_method_return_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 2.6 hours
**Violations**: 31

Fix 31 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add return type annotation to method 'TestKafkaClientInit.test_init_with_valid_url'

### STEP-163: Fix missing_method_parameter_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 6.7 hours
**Violations**: 80

Fix 80 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestKafkaClientInit.test_init_with_valid_url'

### STEP-164: Fix missing_return_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 4.7 hours
**Violations**: 56

Fix 56 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add return type annotation to function 'test_init_with_valid_url' (e.g., -> int, -> str, -> None)

### STEP-165: Fix missing_parameter_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 7.2 hours
**Violations**: 86

Fix 86 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init_with_valid_url'

### STEP-166: Fix missing_method_return_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 4.7 hours
**Violations**: 56

Fix 56 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add return type annotation to method 'TestRabbitMQClientInit.test_init_with_valid_url'

### STEP-167: Fix missing_method_parameter_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 7.2 hours
**Violations**: 86

Fix 86 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRabbitMQClientInit.test_init_with_valid_url'

### STEP-168: Fix missing_return_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 3.6 hours
**Violations**: 43

Fix 43 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add return type annotation to function 'test_init_with_connection_string' (e.g., -> int, -> str, -> None)

### STEP-169: Fix missing_parameter_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 4.2 hours
**Violations**: 51

Fix 51 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init_with_connection_string'

### STEP-170: Fix missing_method_return_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 3.6 hours
**Violations**: 43

Fix 43 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add return type annotation to method 'TestDBClientInit.test_init_with_connection_string'

### STEP-171: Fix missing_method_parameter_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 4.2 hours
**Violations**: 51

Fix 51 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestDBClientInit.test_init_with_connection_string'

### STEP-172: Fix missing_return_type_annotation in test_query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add return type annotation to function 'test_query_builder_select' (e.g., -> int, -> str, -> None)

### STEP-173: Fix missing_parameter_type_annotation in test_query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_query_builder_select'

### STEP-174: Fix missing_method_return_type_annotation in test_query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add return type annotation to method 'TestQueryBuilderSelect.test_query_builder_select'

### STEP-175: Fix missing_method_parameter_type_annotation in test_query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestQueryBuilderSelect.test_query_builder_select'

### STEP-176: Fix missing_return_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5.8 hours
**Violations**: 70

Fix 70 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add return type annotation to function 'test_init_with_config_none_uses_default' (e.g., -> int, -> str, -> None)

### STEP-177: Fix missing_parameter_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 2.5 days
**Violations**: 238

Fix 238 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init_with_config_none_uses_default'

### STEP-178: Fix missing_method_return_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5.8 hours
**Violations**: 70

Fix 70 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add return type annotation to method 'TestUiClientInit.test_init_with_config_none_uses_default'

### STEP-179: Fix missing_method_parameter_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 2.5 days
**Violations**: 238

Fix 238 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestUiClientInit.test_init_with_config_none_uses_default'

### STEP-180: Fix missing_parameter_type_annotation in test_page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.9 hours
**Violations**: 23

Fix 23 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add type annotation to parameter 'self' in function 'is_loaded'

### STEP-181: Fix missing_return_type_annotation in test_page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add return type annotation to function 'test_base_page_init' (e.g., -> int, -> str, -> None)

### STEP-182: Fix missing_method_return_type_annotation in test_page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add return type annotation to method 'TestBasePage.test_base_page_init'

### STEP-183: Fix missing_method_parameter_type_annotation in test_page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestBasePage.test_base_page_init'

### STEP-184: Fix missing_return_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add return type annotation to function 'test_visual_comparator_init' (e.g., -> int, -> str, -> None)

### STEP-185: Fix missing_parameter_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_visual_comparator_init'

### STEP-186: Fix missing_method_return_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add return type annotation to method 'TestVisualComparator.test_visual_comparator_init'

### STEP-187: Fix missing_method_parameter_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestVisualComparator.test_visual_comparator_init'

### STEP-188: Fix missing_parameter_type_annotation in test_graphql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5.7 hours
**Violations**: 68

Fix 68 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init'

### STEP-189: Fix missing_method_parameter_type_annotation in test_graphql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5.7 hours
**Violations**: 68

Fix 68 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestGraphQLClient.test_init'

### STEP-190: Fix missing_parameter_type_annotation in test_graphql_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_graphql_result_contains_errors'

### STEP-191: Fix missing_method_parameter_type_annotation in test_graphql_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestGraphQLResult.test_graphql_result_contains_errors'

### STEP-192: Fix missing_parameter_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_metrics_record_successful_request'

### STEP-193: Fix missing_method_parameter_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestMetrics.test_metrics_record_successful_request'

### STEP-194: Fix missing_parameter_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 1.1 hours
**Violations**: 13

Fix 13 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_rate_limit_config_init'

### STEP-195: Fix missing_method_parameter_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 1.1 hours
**Violations**: 13

Fix 13 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRateLimitConfig.test_rate_limit_config_init'

### STEP-196: Fix missing_parameter_type_annotation in test_retry.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_retry_config_init'

### STEP-197: Fix missing_method_parameter_type_annotation in test_retry.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRetryConfig.test_retry_config_init'

### STEP-198: Fix missing_return_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add return type annotation to function 'test_init' (e.g., -> int, -> str, -> None)

### STEP-199: Fix missing_parameter_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init'

### STEP-200: Fix missing_method_return_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add return type annotation to method 'TestGrpcClient.test_init'

### STEP-201: Fix missing_method_parameter_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestGrpcClient.test_init'

### STEP-202: Fix missing_return_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add return type annotation to function 'test_set_metadata' (e.g., -> int, -> str, -> None)

### STEP-203: Fix missing_parameter_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 2.1 hours
**Violations**: 25

Fix 25 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_set_metadata'

### STEP-204: Fix missing_method_return_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add return type annotation to method 'TestGrpcClientAdditional.test_set_metadata'

### STEP-205: Fix missing_method_parameter_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 2.1 hours
**Violations**: 25

Fix 25 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestGrpcClientAdditional.test_set_metadata'

### STEP-206: Fix missing_return_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 3.9 hours
**Violations**: 47

Fix 47 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add return type annotation to function 'test_init_with_url_and_config' (e.g., -> int, -> str, -> None)

### STEP-207: Fix missing_parameter_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 1.8 days
**Violations**: 172

Fix 172 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init_with_url_and_config'

### STEP-208: Fix missing_method_return_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 4.0 hours
**Violations**: 48

Fix 48 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add return type annotation to method 'TestApiClientInit.test_init_with_url_and_config'

### STEP-209: Fix missing_method_parameter_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 1.8 days
**Violations**: 173

Fix 173 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestApiClientInit.test_init_with_url_and_config'

### STEP-210: Fix missing_return_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 3.4 hours
**Violations**: 41

Fix 41 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add return type annotation to function 'test_valid_api_result_creation' (e.g., -> int, -> str, -> None)

### STEP-211: Fix missing_parameter_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 3.5 hours
**Violations**: 42

Fix 42 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_valid_api_result_creation'

### STEP-212: Fix missing_method_return_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 3.4 hours
**Violations**: 41

Fix 41 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add return type annotation to method 'TestHttpResult.test_valid_api_result_creation'

### STEP-213: Fix missing_method_parameter_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 3.5 hours
**Violations**: 42

Fix 42 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestHttpResult.test_valid_api_result_creation'

### STEP-214: Fix missing_return_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add return type annotation to function 'test_metrics_record_request_success' (e.g., -> int, -> str, -> None)

### STEP-215: Fix missing_parameter_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 2.5 hours
**Violations**: 30

Fix 30 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_metrics_record_request_success'

### STEP-216: Fix missing_method_return_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add return type annotation to method 'TestMetricsRecordRequest.test_metrics_record_request_success'

### STEP-217: Fix missing_method_parameter_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 2.5 hours
**Violations**: 30

Fix 30 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestMetricsRecordRequest.test_metrics_record_request_success'

### STEP-218: Fix missing_return_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 3.0 hours
**Violations**: 36

Fix 36 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add return type annotation to function 'test_middleware_chain_add' (e.g., -> int, -> str, -> None)

### STEP-219: Fix missing_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 6.1 hours
**Violations**: 73

Fix 73 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_middleware_chain_add'

### STEP-220: Fix missing_method_return_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 3.8 hours
**Violations**: 45

Fix 45 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add return type annotation to method 'TestMiddlewareChain.test_middleware_chain_add'

### STEP-221: Fix missing_method_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 7.8 hours
**Violations**: 94

Fix 94 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestMiddlewareChain.test_middleware_chain_add'

### STEP-222: Fix missing_return_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add return type annotation to function 'test_rate_limiter_acquire_success' (e.g., -> int, -> str, -> None)

### STEP-223: Fix missing_parameter_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_rate_limiter_acquire_success'

### STEP-224: Fix missing_method_return_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add return type annotation to method 'TestRateLimiter.test_rate_limiter_acquire_success'

### STEP-225: Fix missing_method_parameter_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRateLimiter.test_rate_limiter_acquire_success'

### STEP-226: Fix missing_return_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add return type annotation to function 'test_init' (e.g., -> int, -> str, -> None)

### STEP-227: Fix missing_parameter_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 5.3 hours
**Violations**: 64

Fix 64 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init'

### STEP-228: Fix missing_method_return_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add return type annotation to method 'TestRequestBuilder.test_init'

### STEP-229: Fix missing_method_parameter_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 5.3 hours
**Violations**: 64

Fix 64 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRequestBuilder.test_init'

### STEP-230: Fix missing_return_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add return type annotation to function 'mock_zeep_client' (e.g., -> int, -> str, -> None)

### STEP-231: Fix missing_parameter_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 1.6 hours
**Violations**: 19

Fix 19 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add type annotation to parameter 'mocker' in function 'mock_zeep_client'

### STEP-232: Fix missing_method_return_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add return type annotation to method 'TestSoapClient.test_init'

### STEP-233: Fix missing_method_parameter_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 1.5 hours
**Violations**: 18

Fix 18 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestSoapClient.test_init'

### STEP-234: Fix missing_parameter_type_annotation in test_auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_auth_middleware_sets_token'

### STEP-235: Fix missing_method_parameter_type_annotation in test_auth_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestAuthMiddleware.test_auth_middleware_sets_token'

### STEP-236: Fix missing_parameter_type_annotation in test_context.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_request_context_init'

### STEP-237: Fix missing_method_parameter_type_annotation in test_context.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestGraphQLRequestContext.test_request_context_init'

### STEP-238: Fix missing_parameter_type_annotation in test_logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_logging_middleware_logs_request'

### STEP-239: Fix missing_method_parameter_type_annotation in test_logging_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestLoggingMiddleware.test_logging_middleware_logs_request'

### STEP-240: Fix missing_parameter_type_annotation in test_metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_metrics_middleware_records_success'

### STEP-241: Fix missing_method_parameter_type_annotation in test_metrics_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestMetricsMiddleware.test_metrics_middleware_records_success'

### STEP-242: Fix missing_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 3.9 hours
**Violations**: 47

Fix 47 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_middleware_process_request_modifies_context'

### STEP-243: Fix missing_method_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 7.2 hours
**Violations**: 86

Fix 86 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestMiddlewareChain.test_middleware_process_request_modifies_context'

### STEP-244: Fix missing_parameter_type_annotation in test_rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_rate_limit_middleware_acquires_permission'

### STEP-245: Fix missing_method_parameter_type_annotation in test_rate_limit_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRateLimitMiddleware.test_rate_limit_middleware_acquires_permission'

### STEP-246: Fix missing_parameter_type_annotation in test_retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_retry_middleware_retries'

### STEP-247: Fix missing_method_parameter_type_annotation in test_retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestRetryMiddleware.test_retry_middleware_retries'

### STEP-248: Fix missing_parameter_type_annotation in test_validation_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_validation_middleware_validates_valid_query'

### STEP-249: Fix missing_method_parameter_type_annotation in test_validation_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestValidationMiddleware.test_validation_middleware_validates_valid_query'

### STEP-250: Fix missing_return_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5.3 hours
**Violations**: 64

Fix 64 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add return type annotation to function 'test_init' (e.g., -> int, -> str, -> None)

### STEP-251: Fix missing_parameter_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 7.9 hours
**Violations**: 95

Fix 95 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add type annotation to parameter 'self' in function 'test_init'

### STEP-252: Fix missing_method_return_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5.3 hours
**Violations**: 64

Fix 64 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add return type annotation to method 'TestWebSocketClient.test_init'

### STEP-253: Fix missing_method_parameter_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 7.9 hours
**Violations**: 95

Fix 95 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add type annotation to parameter 'self' in method 'TestWebSocketClient.test_init'

### STEP-569: Fix invalid_exception_hierarchy in test_http_client.py

**Principle/Standard**: Error Handling
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'invalid_exception_hierarchy' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Make 'ElapsedWithError' inherit from WebAutomationError or its subclasses

## Priority: MEDIUM

### STEP-254: Fix missing_testcase_decorator in test_kafka_client_integration.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_testcase_decorator' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_connect_to_real_kafka'

### STEP-255: Fix missing_pytest_marker in test_kafka_client_integration.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_pytest_marker' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_connect_to_real_kafka'

### STEP-256: Fix missing_allure_steps in test_kafka_client_integration.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_allure_steps' in tests\integration\test_kafka_client_integration.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_connect_to_real_kafka'

### STEP-257: Fix missing_testcase_decorator in test_rabbitmq_client_integration.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_testcase_decorator' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_connect_to_real_rabbitmq'

### STEP-258: Fix missing_pytest_marker in test_rabbitmq_client_integration.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_pytest_marker' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_connect_to_real_rabbitmq'

### STEP-259: Fix missing_allure_steps in test_rabbitmq_client_integration.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_allure_steps' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_connect_to_real_rabbitmq'

### STEP-260: Fix missing_testcase_decorator in test_config.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 1.8 days
**Violations**: 176

Fix 176 violation(s) of type 'missing_testcase_decorator' in tests\unit\test_config.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_valid_config_creation'

### STEP-261: Fix missing_pytest_marker in test_config.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 1.8 days
**Violations**: 176

Fix 176 violation(s) of type 'missing_pytest_marker' in tests\unit\test_config.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_valid_config_creation'

### STEP-262: Fix missing_allure_steps in test_config.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_allure_steps' in tests\unit\test_config.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_config_fallback_logging_attribute_error'

### STEP-263: Fix missing_testcase_decorator in test_kafka_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 4.8 hours
**Violations**: 58

Fix 58 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init_with_valid_url'

### STEP-264: Fix missing_pytest_marker in test_kafka_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 4.8 hours
**Violations**: 58

Fix 58 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init_with_valid_url'

### STEP-265: Fix missing_allure_steps in test_kafka_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 4.8 hours
**Violations**: 58

Fix 58 violation(s) of type 'missing_allure_steps' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_init_with_valid_url'

### STEP-266: Fix missing_testcase_decorator in test_rabbitmq_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 5.2 hours
**Violations**: 62

Fix 62 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init_with_valid_url'

### STEP-267: Fix missing_pytest_marker in test_rabbitmq_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 5.2 hours
**Violations**: 62

Fix 62 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init_with_valid_url'

### STEP-268: Fix missing_allure_steps in test_rabbitmq_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 5.2 hours
**Violations**: 62

Fix 62 violation(s) of type 'missing_allure_steps' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_init_with_valid_url'

### STEP-269: Fix missing_testcase_decorator in test_db_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 6.8 hours
**Violations**: 82

Fix 82 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init_with_connection_string'

### STEP-270: Fix missing_pytest_marker in test_db_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 6.8 hours
**Violations**: 82

Fix 82 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init_with_connection_string'

### STEP-271: Fix missing_testcase_decorator in test_query_builder.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 4.7 hours
**Violations**: 56

Fix 56 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_query_builder_select'

### STEP-272: Fix missing_pytest_marker in test_query_builder.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 4.7 hours
**Violations**: 56

Fix 56 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_query_builder_select'

### STEP-273: Fix missing_testcase_decorator in test_async_ui_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 1.5 days
**Violations**: 140

Fix 140 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init_with_config_none_uses_default'

### STEP-274: Fix missing_pytest_marker in test_async_ui_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 1.5 days
**Violations**: 140

Fix 140 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init_with_config_none_uses_default'

### STEP-275: Fix missing_testcase_decorator in test_page_objects.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 3.7 hours
**Violations**: 44

Fix 44 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_base_page_init'

### STEP-276: Fix missing_pytest_marker in test_page_objects.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 3.7 hours
**Violations**: 44

Fix 44 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_base_page_init'

### STEP-277: Fix missing_testcase_decorator in test_visual_testing.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 1.5 hours
**Violations**: 18

Fix 18 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_visual_comparator_init'

### STEP-278: Fix missing_pytest_marker in test_visual_testing.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 1.5 hours
**Violations**: 18

Fix 18 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_visual_comparator_init'

### STEP-279: Fix missing_testcase_decorator in test_graphql_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 1.4 days
**Violations**: 134

Fix 134 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init'

### STEP-280: Fix missing_pytest_marker in test_graphql_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 1.4 days
**Violations**: 134

Fix 134 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init'

### STEP-281: Fix missing_allure_steps in test_graphql_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 1.4 days
**Violations**: 134

Fix 134 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_init'

### STEP-282: Fix missing_testcase_decorator in test_graphql_result.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_graphql_result_contains_errors'

### STEP-283: Fix missing_pytest_marker in test_graphql_result.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_graphql_result_contains_errors'

### STEP-284: Fix missing_allure_steps in test_graphql_result.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_graphql_result_contains_errors'

### STEP-285: Fix missing_testcase_decorator in test_metrics.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_metrics_record_successful_request'

### STEP-286: Fix missing_pytest_marker in test_metrics.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_metrics_record_successful_request'

### STEP-287: Fix missing_allure_steps in test_metrics.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_metrics_record_successful_request'

### STEP-288: Fix missing_testcase_decorator in test_rate_limit.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 2.2 hours
**Violations**: 26

Fix 26 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_rate_limit_config_init'

### STEP-289: Fix missing_pytest_marker in test_rate_limit.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 2.2 hours
**Violations**: 26

Fix 26 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_rate_limit_config_init'

### STEP-290: Fix missing_allure_steps in test_rate_limit.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 2.2 hours
**Violations**: 26

Fix 26 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_rate_limit_config_init'

### STEP-291: Fix missing_testcase_decorator in test_retry.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_retry_config_init'

### STEP-292: Fix missing_pytest_marker in test_retry.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_retry_config_init'

### STEP-293: Fix missing_allure_steps in test_retry.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_retry_config_init'

### STEP-294: Fix missing_testcase_decorator in test_grpc_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init'

### STEP-295: Fix missing_pytest_marker in test_grpc_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init'

### STEP-296: Fix missing_testcase_decorator in test_grpc_client_additional.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_set_metadata'

### STEP-297: Fix missing_pytest_marker in test_grpc_client_additional.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_set_metadata'

### STEP-298: Fix missing_testcase_decorator in test_http_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 7.7 hours
**Violations**: 92

Fix 92 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init_with_url_and_config'

### STEP-299: Fix missing_pytest_marker in test_http_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 7.7 hours
**Violations**: 92

Fix 92 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init_with_url_and_config'

### STEP-300: Fix missing_testcase_decorator in test_http_result.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 6.8 hours
**Violations**: 82

Fix 82 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_valid_api_result_creation'

### STEP-301: Fix missing_pytest_marker in test_http_result.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 6.8 hours
**Violations**: 82

Fix 82 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_valid_api_result_creation'

### STEP-302: Fix missing_testcase_decorator in test_metrics.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 2.5 hours
**Violations**: 30

Fix 30 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_metrics_record_request_success'

### STEP-303: Fix missing_pytest_marker in test_metrics.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 2.5 hours
**Violations**: 30

Fix 30 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_metrics_record_request_success'

### STEP-304: Fix missing_testcase_decorator in test_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 4.5 hours
**Violations**: 54

Fix 54 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_middleware_chain_add'

### STEP-305: Fix missing_pytest_marker in test_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 4.5 hours
**Violations**: 54

Fix 54 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_middleware_chain_add'

### STEP-306: Fix missing_testcase_decorator in test_rate_limit.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_rate_limiter_acquire_success'

### STEP-307: Fix missing_pytest_marker in test_rate_limit.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_rate_limiter_acquire_success'

### STEP-308: Fix missing_testcase_decorator in test_request_builder.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 3.5 hours
**Violations**: 42

Fix 42 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init'

### STEP-309: Fix missing_pytest_marker in test_request_builder.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 3.5 hours
**Violations**: 42

Fix 42 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init'

### STEP-310: Fix missing_allure_steps in test_request_builder.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 2.8 hours
**Violations**: 34

Fix 34 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_init'

### STEP-311: Fix missing_testcase_decorator in test_soap_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init'

### STEP-312: Fix missing_pytest_marker in test_soap_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init'

### STEP-313: Fix missing_allure_steps in test_soap_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_init'

### STEP-314: Fix missing_testcase_decorator in test_auth_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 1.0 hours
**Violations**: 12

Fix 12 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_auth_middleware_sets_token'

### STEP-315: Fix missing_pytest_marker in test_auth_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 1.0 hours
**Violations**: 12

Fix 12 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_auth_middleware_sets_token'

### STEP-316: Fix missing_allure_steps in test_auth_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 1.0 hours
**Violations**: 12

Fix 12 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_auth_middleware_sets_token'

### STEP-317: Fix missing_testcase_decorator in test_context.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_request_context_init'

### STEP-318: Fix missing_pytest_marker in test_context.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_request_context_init'

### STEP-319: Fix missing_allure_steps in test_context.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_request_context_init'

### STEP-320: Fix missing_testcase_decorator in test_logging_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_logging_middleware_logs_request'

### STEP-321: Fix missing_pytest_marker in test_logging_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_logging_middleware_logs_request'

### STEP-322: Fix missing_allure_steps in test_logging_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_logging_middleware_logs_request'

### STEP-323: Fix missing_testcase_decorator in test_metrics_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_metrics_middleware_records_success'

### STEP-324: Fix missing_pytest_marker in test_metrics_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_metrics_middleware_records_success'

### STEP-325: Fix missing_allure_steps in test_metrics_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_metrics_middleware_records_success'

### STEP-326: Fix missing_testcase_decorator in test_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_middleware_process_request_modifies_context'

### STEP-327: Fix missing_pytest_marker in test_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_middleware_process_request_modifies_context'

### STEP-328: Fix missing_allure_steps in test_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_middleware_process_request_modifies_context'

### STEP-329: Fix missing_testcase_decorator in test_rate_limit_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_rate_limit_middleware_acquires_permission'

### STEP-330: Fix missing_pytest_marker in test_rate_limit_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_rate_limit_middleware_acquires_permission'

### STEP-331: Fix missing_allure_steps in test_rate_limit_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_rate_limit_middleware_acquires_permission'

### STEP-332: Fix missing_testcase_decorator in test_retry_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_retry_middleware_retries'

### STEP-333: Fix missing_pytest_marker in test_retry_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_retry_middleware_retries'

### STEP-334: Fix missing_allure_steps in test_retry_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_retry_middleware_retries'

### STEP-335: Fix missing_testcase_decorator in test_validation_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_validation_middleware_validates_valid_query'

### STEP-336: Fix missing_pytest_marker in test_validation_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_validation_middleware_validates_valid_query'

### STEP-337: Fix missing_allure_steps in test_validation_middleware.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_allure_steps' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_validation_middleware_validates_valid_query'

### STEP-338: Fix missing_testcase_decorator in test_websocket_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 4.8 hours
**Violations**: 58

Fix 58 violation(s) of type 'missing_testcase_decorator' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add @allure.testcase('TC-XXX-XXX-XXX') decorator to test function 'test_init'

### STEP-339: Fix missing_pytest_marker in test_websocket_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 4.8 hours
**Violations**: 58

Fix 58 violation(s) of type 'missing_pytest_marker' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add @pytest.mark.unit or @pytest.mark.integration decorator to 'test_init'

### STEP-340: Fix missing_allure_steps in test_websocket_client.py

**Principle/Standard**: Testing Standards
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 4.5 hours
**Violations**: 54

Fix 54 violation(s) of type 'missing_allure_steps' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Wrap test actions in allure.step() context manager in function 'test_init'

### STEP-434: Fix missing_args_section in test_kafka_client_integration.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_args_section' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add Args section to docstring for function 'test_connect_to_real_kafka'

### STEP-435: Fix missing_docstring in test_kafka_client_integration.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_docstring' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add Google-style docstring to function 'handler'

### STEP-436: Fix missing_args_section in test_rabbitmq_client_integration.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_args_section' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add Args section to docstring for function 'test_connect_to_real_rabbitmq'

### STEP-437: Fix missing_docstring in test_rabbitmq_client_integration.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_docstring' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add Google-style docstring to function 'handler'

### STEP-440: Fix missing_args_section in test_kafka_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_args_section' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add Args section to docstring for function 'test_init_with_valid_url'

### STEP-441: Fix missing_docstring in test_kafka_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_docstring' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add Google-style docstring to function 'mock_consume'

### STEP-442: Fix missing_args_section in test_rabbitmq_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 2.5 hours
**Violations**: 30

Fix 30 violation(s) of type 'missing_args_section' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add Args section to docstring for function 'test_init_with_valid_url'

### STEP-443: Fix missing_docstring in test_rabbitmq_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 2.1 hours
**Violations**: 25

Fix 25 violation(s) of type 'missing_docstring' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add Google-style docstring to function 'mock_connect_robust'

### STEP-444: Fix missing_args_section in test_db_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_args_section' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add Args section to docstring for function 'test_close_calls_disconnect'

### STEP-445: Fix missing_docstring in test_db_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_docstring' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add Google-style docstring to function 'mock_connect_impl'

### STEP-446: Fix missing_args_section in test_async_ui_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5.8 hours
**Violations**: 69

Fix 69 violation(s) of type 'missing_args_section' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add Args section to docstring for function 'test_init_with_url_and_config'

### STEP-447: Fix missing_class_docstring in test_async_ui_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_class_docstring' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add Google-style docstring to class 'CustomUiClient'

### STEP-450: Fix missing_args_section in test_graphql_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5.2 hours
**Violations**: 63

Fix 63 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add Args section to docstring for function 'test_init'

### STEP-451: Fix missing_returns_section in test_graphql_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5.6 hours
**Violations**: 67

Fix 67 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add Returns section to docstring for function 'test_init'

### STEP-452: Fix missing_docstring in test_graphql_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_docstring' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add Google-style docstring to function 'failing_close'

### STEP-460: Fix missing_args_section in test_http_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 3.8 hours
**Violations**: 46

Fix 46 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add Args section to docstring for function 'test_init_with_url_and_config'

### STEP-461: Fix missing_docstring in test_http_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_docstring' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add Google-style docstring to function 'total_seconds'

### STEP-464: Fix missing_args_section in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 1.4 hours
**Violations**: 17

Fix 17 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add Args section to docstring for function 'test_middleware_chain_add'

### STEP-465: Fix missing_docstring in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_docstring' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add Google-style docstring to function 'process_request'

### STEP-466: Fix missing_class_docstring in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_class_docstring' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add Google-style docstring to class 'TrackingMiddleware'

### STEP-475: Fix missing_args_section in test_metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add Args section to docstring for function 'test_metrics_middleware_records_success'

### STEP-476: Fix missing_returns_section in test_metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_metrics_middleware_records_success'

### STEP-477: Fix missing_docstring in test_metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_docstring' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Add Google-style docstring to function 'mock_create_success_result'

### STEP-478: Fix missing_args_section in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add Args section to docstring for function 'test_middleware_process_request_modifies_context'

### STEP-479: Fix missing_returns_section in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_middleware_process_request_modifies_context'

### STEP-480: Fix missing_docstring in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.5 hours
**Violations**: 18

Fix 18 violation(s) of type 'missing_docstring' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add Google-style docstring to function 'process_request'

### STEP-481: Fix missing_class_docstring in test_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_class_docstring' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add Google-style docstring to class 'TestMiddleware'

### STEP-484: Fix missing_args_section in test_retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add Args section to docstring for function 'test_retry_middleware_retries'

### STEP-485: Fix missing_returns_section in test_retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_retry_middleware_retries'

### STEP-486: Fix missing_docstring in test_retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_docstring' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add Google-style docstring to function 'mock_execute_with_retry'

### STEP-489: Fix missing_args_section in test_websocket_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_args_section' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add Args section to docstring for function 'test_init'

### STEP-490: Fix missing_docstring in test_websocket_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 2.9 hours
**Violations**: 35

Fix 35 violation(s) of type 'missing_docstring' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add Google-style docstring to function 'mock_connect'

### STEP-492: Fix ruff_violation in sqlite_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'ruff_violation' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\db_clients\sqlite_client.py' to auto-fix

### STEP-493: Fix line_too_long in sqlite_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Break line 25 into multiple lines or refactor

### STEP-494: Fix ruff_violation in graphql_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'ruff_violation' in py_web_automation\clients\api_clients\graphql_client\graphql_client.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\api_clients\graphql_client\graphql_client.py' to auto-fix

### STEP-495: Fix ruff_violation in retry.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'ruff_violation' in py_web_automation\clients\api_clients\graphql_client\retry.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\api_clients\graphql_client\retry.py' to auto-fix

### STEP-496: Fix ruff_violation in http_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'ruff_violation' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\api_clients\http_client\http_client.py' to auto-fix

### STEP-497: Fix line_too_long in http_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Break line 66 into multiple lines or refactor

### STEP-498: Fix ruff_violation in request_builder.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\api_clients\http_client\request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'ruff_violation' in py_web_automation\clients\api_clients\http_client\request_builder.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\api_clients\http_client\request_builder.py' to auto-fix

### STEP-499: Fix ruff_violation in validation_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'ruff_violation' in py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py' to auto-fix

### STEP-500: Fix ruff_violation in retry.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\retry.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'ruff_violation' in py_web_automation\clients\streaming_clients\websocket_client\retry.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\streaming_clients\websocket_client\retry.py' to auto-fix

### STEP-501: Fix ruff_violation in websocket_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'ruff_violation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Run 'uv run ruff check --fix py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py' to auto-fix

### STEP-503: Fix ruff_violation in conftest.py

**Principle/Standard**: Code Style
**Affected Files**: tests\conftest.py
**Estimated Effort**: 6.4 hours
**Violations**: 77

Fix 77 violation(s) of type 'ruff_violation' in tests\conftest.py

Suggested fix: Run 'uv run ruff check --fix tests\conftest.py' to auto-fix

### STEP-504: Fix line_too_long in conftest.py

**Principle/Standard**: Code Style
**Affected Files**: tests\conftest.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'line_too_long' in tests\conftest.py

Suggested fix: Break line 111 into multiple lines or refactor

### STEP-505: Fix ruff_violation in api_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\fixtures\api_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'ruff_violation' in tests\fixtures\api_client.py

Suggested fix: Run 'uv run ruff check --fix tests\fixtures\api_client.py' to auto-fix

### STEP-506: Fix line_too_long in api_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\fixtures\api_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'line_too_long' in tests\fixtures\api_client.py

Suggested fix: Break line 130 into multiple lines or refactor

### STEP-507: Fix ruff_violation in config.py

**Principle/Standard**: Code Style
**Affected Files**: tests\fixtures\config.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'ruff_violation' in tests\fixtures\config.py

Suggested fix: Run 'uv run ruff check --fix tests\fixtures\config.py' to auto-fix

### STEP-508: Fix line_too_long in config.py

**Principle/Standard**: Code Style
**Affected Files**: tests\fixtures\config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in tests\fixtures\config.py

Suggested fix: Break line 662 into multiple lines or refactor

### STEP-509: Fix ruff_violation in middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\fixtures\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'ruff_violation' in tests\fixtures\middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\fixtures\middleware.py' to auto-fix

### STEP-510: Fix ruff_violation in ui_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'ruff_violation' in tests\fixtures\ui_client.py

Suggested fix: Run 'uv run ruff check --fix tests\fixtures\ui_client.py' to auto-fix

### STEP-511: Fix ruff_violation in test_kafka_client_integration.py

**Principle/Standard**: Code Style
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 2.8 hours
**Violations**: 33

Fix 33 violation(s) of type 'ruff_violation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Run 'uv run ruff check --fix tests\integration\test_kafka_client_integration.py' to auto-fix

### STEP-512: Fix line_too_long in test_kafka_client_integration.py

**Principle/Standard**: Code Style
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'line_too_long' in tests\integration\test_kafka_client_integration.py

Suggested fix: Break line 58 into multiple lines or refactor

### STEP-513: Fix ruff_violation in test_rabbitmq_client_integration.py

**Principle/Standard**: Code Style
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 2.7 hours
**Violations**: 32

Fix 32 violation(s) of type 'ruff_violation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Run 'uv run ruff check --fix tests\integration\test_rabbitmq_client_integration.py' to auto-fix

### STEP-514: Fix line_too_long in test_rabbitmq_client_integration.py

**Principle/Standard**: Code Style
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'line_too_long' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Break line 69 into multiple lines or refactor

### STEP-515: Fix ruff_violation in test_config.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 2.7 days
**Violations**: 258

Fix 258 violation(s) of type 'ruff_violation' in tests\unit\test_config.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\test_config.py' to auto-fix

### STEP-516: Fix line_too_long in test_config.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 7.1 hours
**Violations**: 85

Fix 85 violation(s) of type 'line_too_long' in tests\unit\test_config.py

Suggested fix: Break line 49 into multiple lines or refactor

### STEP-517: Fix ruff_violation in test_kafka_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 4.2 hours
**Violations**: 51

Fix 51 violation(s) of type 'ruff_violation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\broker_clients\test_kafka_client.py' to auto-fix

### STEP-518: Fix line_too_long in test_kafka_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'line_too_long' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Break line 66 into multiple lines or refactor

### STEP-519: Fix ruff_violation in test_rabbitmq_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 3.7 hours
**Violations**: 44

Fix 44 violation(s) of type 'ruff_violation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\broker_clients\test_rabbitmq_client.py' to auto-fix

### STEP-520: Fix line_too_long in test_rabbitmq_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'line_too_long' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Break line 63 into multiple lines or refactor

### STEP-521: Fix ruff_violation in test_db_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 7.1 hours
**Violations**: 85

Fix 85 violation(s) of type 'ruff_violation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\db_clients\test_db_client.py' to auto-fix

### STEP-522: Fix line_too_long in test_db_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'line_too_long' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Break line 225 into multiple lines or refactor

### STEP-523: Fix ruff_violation in test_query_builder.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 7.6 hours
**Violations**: 91

Fix 91 violation(s) of type 'ruff_violation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\db_clients\test_query_builder.py' to auto-fix

### STEP-524: Fix line_too_long in test_query_builder.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'line_too_long' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Break line 90 into multiple lines or refactor

### STEP-525: Fix ruff_violation in test_async_ui_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5.3 hours
**Violations**: 64

Fix 64 violation(s) of type 'ruff_violation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\ui_clients\test_async_ui_client.py' to auto-fix

### STEP-526: Fix line_too_long in test_async_ui_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 2.2 hours
**Violations**: 27

Fix 27 violation(s) of type 'line_too_long' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Break line 207 into multiple lines or refactor

### STEP-527: Fix ruff_violation in test_page_objects.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'ruff_violation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\ui_clients\test_page_objects.py' to auto-fix

### STEP-528: Fix line_too_long in test_page_objects.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'line_too_long' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Break line 12 into multiple lines or refactor

### STEP-529: Fix ruff_violation in test_visual_testing.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 1.4 hours
**Violations**: 17

Fix 17 violation(s) of type 'ruff_violation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\ui_clients\test_visual_testing.py' to auto-fix

### STEP-530: Fix line_too_long in test_visual_testing.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Break line 101 into multiple lines or refactor

### STEP-531: Fix ruff_violation in test_graphql_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 1.8 days
**Violations**: 175

Fix 175 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\test_graphql_client.py' to auto-fix

### STEP-532: Fix line_too_long in test_graphql_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 3.9 hours
**Violations**: 47

Fix 47 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Break line 16 into multiple lines or refactor

### STEP-533: Fix ruff_violation in test_graphql_result.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\test_graphql_result.py' to auto-fix

### STEP-534: Fix ruff_violation in test_metrics.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 4.2 hours
**Violations**: 50

Fix 50 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\test_metrics.py' to auto-fix

### STEP-535: Fix ruff_violation in test_rate_limit.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 2.2 hours
**Violations**: 26

Fix 26 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\test_rate_limit.py' to auto-fix

### STEP-536: Fix ruff_violation in test_retry.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 2.8 hours
**Violations**: 33

Fix 33 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\test_retry.py' to auto-fix

### STEP-537: Fix ruff_violation in test_grpc_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\grpc_client\test_grpc_client.py' to auto-fix

### STEP-538: Fix line_too_long in test_grpc_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Break line 48 into multiple lines or refactor

### STEP-539: Fix ruff_violation in test_grpc_client_additional.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 1.5 hours
**Violations**: 18

Fix 18 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py' to auto-fix

### STEP-540: Fix line_too_long in test_grpc_client_additional.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Break line 76 into multiple lines or refactor

### STEP-541: Fix ruff_violation in test_http_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 2.0 days
**Violations**: 195

Fix 195 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\http_client\test_http_client.py' to auto-fix

### STEP-542: Fix line_too_long in test_http_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 6.5 hours
**Violations**: 78

Fix 78 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Break line 156 into multiple lines or refactor

### STEP-543: Fix ruff_violation in test_http_result.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 1.3 days
**Violations**: 125

Fix 125 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\http_client\test_http_result.py' to auto-fix

### STEP-544: Fix line_too_long in test_http_result.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Break line 128 into multiple lines or refactor

### STEP-545: Fix ruff_violation in test_metrics.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 2.9 hours
**Violations**: 35

Fix 35 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\http_client\test_metrics.py' to auto-fix

### STEP-546: Fix ruff_violation in test_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 4.8 hours
**Violations**: 58

Fix 58 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\http_client\test_middleware.py' to auto-fix

### STEP-547: Fix line_too_long in test_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Break line 89 into multiple lines or refactor

### STEP-548: Fix ruff_violation in test_rate_limit.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 1.4 hours
**Violations**: 17

Fix 17 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\http_client\test_rate_limit.py' to auto-fix

### STEP-549: Fix line_too_long in test_rate_limit.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Break line 11 into multiple lines or refactor

### STEP-550: Fix ruff_violation in test_request_builder.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 4.2 hours
**Violations**: 51

Fix 51 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\http_client\test_request_builder.py' to auto-fix

### STEP-551: Fix line_too_long in test_request_builder.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 2.0 hours
**Violations**: 24

Fix 24 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Break line 12 into multiple lines or refactor

### STEP-552: Fix ruff_violation in test_soap_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\soap_client\test_soap_client.py' to auto-fix

### STEP-553: Fix line_too_long in test_soap_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Break line 113 into multiple lines or refactor

### STEP-554: Fix ruff_violation in test_auth_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 2.0 hours
**Violations**: 24

Fix 24 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py' to auto-fix

### STEP-555: Fix line_too_long in test_auth_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Break line 13 into multiple lines or refactor

### STEP-556: Fix ruff_violation in test_context.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_context.py' to auto-fix

### STEP-557: Fix ruff_violation in test_logging_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py' to auto-fix

### STEP-558: Fix ruff_violation in test_metrics_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py' to auto-fix

### STEP-559: Fix line_too_long in test_metrics_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Break line 121 into multiple lines or refactor

### STEP-560: Fix ruff_violation in test_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.7 hours
**Violations**: 20

Fix 20 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py' to auto-fix

### STEP-561: Fix ruff_violation in test_rate_limit_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py' to auto-fix

### STEP-562: Fix ruff_violation in test_retry_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py' to auto-fix

### STEP-563: Fix line_too_long in test_retry_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Break line 58 into multiple lines or refactor

### STEP-564: Fix ruff_violation in test_validation_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 1.0 hours
**Violations**: 12

Fix 12 violation(s) of type 'ruff_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py' to auto-fix

### STEP-565: Fix line_too_long in test_validation_middleware.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'line_too_long' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Break line 137 into multiple lines or refactor

### STEP-566: Fix ruff_violation in test_websocket_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5.8 hours
**Violations**: 69

Fix 69 violation(s) of type 'ruff_violation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Run 'uv run ruff check --fix tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py' to auto-fix

### STEP-567: Fix line_too_long in test_websocket_client.py

**Principle/Standard**: Code Style
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 2.6 hours
**Violations**: 31

Fix 31 violation(s) of type 'line_too_long' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Break line 11 into multiple lines or refactor

### STEP-568: Fix missing_exception_chaining in validator.py

**Principle/Standard**: Error Handling
**Affected Files**: py_web_automation\clients\api_clients\http_client\validator.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_exception_chaining' in py_web_automation\clients\api_clients\http_client\validator.py

Suggested fix: Use 'raise NewException from e' for exception chaining

### STEP-588: Fix imports_not_at_top in config.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\config.py

Suggested fix: Move all imports to the top of the file

### STEP-589: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-590: Fix imports_not_at_top in broker_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\broker_clients\broker_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\broker_clients\broker_client.py

Suggested fix: Move all imports to the top of the file

### STEP-591: Fix incorrect_import_order in broker_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\broker_clients\broker_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\broker_clients\broker_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-592: Fix imports_not_at_top in kafka_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\broker_clients\kafka_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\broker_clients\kafka_client.py

Suggested fix: Move all imports to the top of the file

### STEP-593: Fix incorrect_import_order in kafka_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\broker_clients\kafka_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\broker_clients\kafka_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-594: Fix imports_not_at_top in rabbitmq_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Move all imports to the top of the file

### STEP-595: Fix incorrect_import_order in rabbitmq_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-596: Fix imports_not_at_top in db_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\db_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\db_clients\db_client.py

Suggested fix: Move all imports to the top of the file

### STEP-597: Fix incorrect_import_order in db_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\db_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\db_clients\db_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-598: Fix imports_not_at_top in mysql_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\mysql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\db_clients\mysql_client.py

Suggested fix: Move all imports to the top of the file

### STEP-599: Fix imports_not_at_top in postgresql_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\postgresql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\db_clients\postgresql_client.py

Suggested fix: Move all imports to the top of the file

### STEP-600: Fix imports_not_at_top in query_builder.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\query_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\db_clients\query_builder.py

Suggested fix: Move all imports to the top of the file

### STEP-601: Fix imports_not_at_top in sqlite_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Move all imports to the top of the file

### STEP-602: Fix incorrect_import_order in sqlite_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-603: Fix imports_not_at_top in types.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\db_clients\types.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\db_clients\types.py

Suggested fix: Move all imports to the top of the file

### STEP-604: Fix imports_not_at_top in visual_testing.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\visual_testing.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\ui_clients\visual_testing.py

Suggested fix: Move all imports to the top of the file

### STEP-605: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\ui_clients\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-606: Fix imports_not_at_top in graphql_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\graphql_client.py

Suggested fix: Move all imports to the top of the file

### STEP-607: Fix incorrect_import_order in graphql_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\graphql_client\graphql_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-608: Fix imports_not_at_top in graphql_result.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\graphql_result.py

Suggested fix: Move all imports to the top of the file

### STEP-609: Fix imports_not_at_top in metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-610: Fix imports_not_at_top in rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-611: Fix imports_not_at_top in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\retry.py

Suggested fix: Move all imports to the top of the file

### STEP-612: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-613: Fix imports_not_at_top in grpc_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\grpc_client.py

Suggested fix: Move all imports to the top of the file

### STEP-614: Fix incorrect_import_order in grpc_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\grpc_client\grpc_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-615: Fix imports_not_at_top in grpc_result.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\grpc_result.py

Suggested fix: Move all imports to the top of the file

### STEP-616: Fix imports_not_at_top in metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-617: Fix imports_not_at_top in rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-618: Fix imports_not_at_top in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\retry.py

Suggested fix: Move all imports to the top of the file

### STEP-619: Fix incorrect_import_order in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\grpc_client\retry.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-620: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-621: Fix imports_not_at_top in exceptions.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\exceptions.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\exceptions.py

Suggested fix: Move all imports to the top of the file

### STEP-622: Fix imports_not_at_top in http_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Move all imports to the top of the file

### STEP-623: Fix incorrect_import_order in http_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-624: Fix imports_not_at_top in http_result.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\http_result.py

Suggested fix: Move all imports to the top of the file

### STEP-625: Fix incorrect_import_order in http_result.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_result.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\http_client\http_result.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-626: Fix imports_not_at_top in metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-627: Fix imports_not_at_top in rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-628: Fix imports_not_at_top in request_builder.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\request_builder.py

Suggested fix: Move all imports to the top of the file

### STEP-629: Fix imports_not_at_top in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\retry.py

Suggested fix: Move all imports to the top of the file

### STEP-630: Fix imports_not_at_top in validator.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\validator.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\validator.py

Suggested fix: Move all imports to the top of the file

### STEP-631: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-632: Fix imports_not_at_top in metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-633: Fix imports_not_at_top in rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-634: Fix imports_not_at_top in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\retry.py

Suggested fix: Move all imports to the top of the file

### STEP-635: Fix incorrect_import_order in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\soap_client\retry.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-636: Fix imports_not_at_top in soap_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\soap_client.py

Suggested fix: Move all imports to the top of the file

### STEP-637: Fix incorrect_import_order in soap_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\api_clients\soap_client\soap_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-638: Fix imports_not_at_top in soap_result.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\soap_result.py

Suggested fix: Move all imports to the top of the file

### STEP-639: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-640: Fix imports_not_at_top in auth_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-641: Fix imports_not_at_top in context.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\context.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\context.py

Suggested fix: Move all imports to the top of the file

### STEP-642: Fix imports_not_at_top in logging_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-643: Fix imports_not_at_top in metrics_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-644: Fix imports_not_at_top in middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-645: Fix imports_not_at_top in rate_limit_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-646: Fix imports_not_at_top in retry_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-647: Fix imports_not_at_top in validation_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-648: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\graphql_client\middleware\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-649: Fix imports_not_at_top in auth_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-650: Fix imports_not_at_top in context.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\context.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\context.py

Suggested fix: Move all imports to the top of the file

### STEP-651: Fix imports_not_at_top in logging_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-652: Fix imports_not_at_top in metrics_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-653: Fix imports_not_at_top in middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-654: Fix imports_not_at_top in rate_limit_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-655: Fix imports_not_at_top in retry_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-656: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\grpc_client\middleware\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-657: Fix imports_not_at_top in auth_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-658: Fix imports_not_at_top in context.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\context.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\context.py

Suggested fix: Move all imports to the top of the file

### STEP-659: Fix imports_not_at_top in logging_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-660: Fix imports_not_at_top in metrics_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-661: Fix imports_not_at_top in middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-662: Fix imports_not_at_top in rate_limit_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-663: Fix imports_not_at_top in retry_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-664: Fix imports_not_at_top in validation_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-665: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\http_client\middleware\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-666: Fix imports_not_at_top in auth_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-667: Fix imports_not_at_top in context.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\context.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\context.py

Suggested fix: Move all imports to the top of the file

### STEP-668: Fix imports_not_at_top in logging_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-669: Fix imports_not_at_top in metrics_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-670: Fix imports_not_at_top in middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-671: Fix imports_not_at_top in rate_limit_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-672: Fix imports_not_at_top in retry_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-673: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\api_clients\soap_client\middleware\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-674: Fix imports_not_at_top in metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-675: Fix imports_not_at_top in rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-676: Fix imports_not_at_top in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\retry.py

Suggested fix: Move all imports to the top of the file

### STEP-677: Fix incorrect_import_order in retry.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\streaming_clients\websocket_client\retry.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-678: Fix imports_not_at_top in websocket_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Move all imports to the top of the file

### STEP-679: Fix incorrect_import_order in websocket_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-680: Fix imports_not_at_top in websocket_result.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py

Suggested fix: Move all imports to the top of the file

### STEP-681: Fix imports_not_at_top in connection_retry_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-682: Fix imports_not_at_top in context.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\context.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\context.py

Suggested fix: Move all imports to the top of the file

### STEP-683: Fix imports_not_at_top in logging_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-684: Fix imports_not_at_top in metrics_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-685: Fix imports_not_at_top in middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-686: Fix imports_not_at_top in rate_limit_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-687: Fix imports_not_at_top in __init__.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\streaming_clients\websocket_client\middleware\__init__.py

Suggested fix: Move all imports to the top of the file

### STEP-688: Fix imports_not_at_top in page_objects.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\page_objects.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\ui_clients\async_ui_client\page_objects.py

Suggested fix: Move all imports to the top of the file

### STEP-689: Fix imports_not_at_top in ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Move all imports to the top of the file

### STEP-690: Fix incorrect_import_order in ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-691: Fix imports_not_at_top in page_objects.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py

Suggested fix: Move all imports to the top of the file

### STEP-692: Fix imports_not_at_top in ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Move all imports to the top of the file

### STEP-693: Fix incorrect_import_order in ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-694: Fix imports_not_at_top in conftest.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\conftest.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\conftest.py

Suggested fix: Move all imports to the top of the file

### STEP-695: Fix imports_not_at_top in api_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\api_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\fixtures\api_client.py

Suggested fix: Move all imports to the top of the file

### STEP-696: Fix imports_not_at_top in metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\fixtures\metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-697: Fix imports_not_at_top in middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\fixtures\middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-698: Fix imports_not_at_top in rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\fixtures\rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-699: Fix imports_not_at_top in streaming_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\streaming_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\fixtures\streaming_client.py

Suggested fix: Move all imports to the top of the file

### STEP-700: Fix imports_not_at_top in ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\fixtures\ui_client.py

Suggested fix: Move all imports to the top of the file

### STEP-701: Fix incorrect_import_order in ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'incorrect_import_order' in tests\fixtures\ui_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-702: Fix imports_not_at_top in conftest.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\integration\conftest.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\integration\conftest.py

Suggested fix: Move all imports to the top of the file

### STEP-703: Fix imports_not_at_top in test_kafka_client_integration.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\integration\test_kafka_client_integration.py

Suggested fix: Move all imports to the top of the file

### STEP-704: Fix imports_not_at_top in test_rabbitmq_client_integration.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Move all imports to the top of the file

### STEP-705: Fix imports_not_at_top in test_config.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\test_config.py

Suggested fix: Move all imports to the top of the file

### STEP-706: Fix incorrect_import_order in test_config.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'incorrect_import_order' in tests\unit\test_config.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-707: Fix imports_not_at_top in test_kafka_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Move all imports to the top of the file

### STEP-708: Fix incorrect_import_order in test_kafka_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-709: Fix imports_not_at_top in test_rabbitmq_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Move all imports to the top of the file

### STEP-710: Fix incorrect_import_order in test_rabbitmq_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-711: Fix imports_not_at_top in test_db_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Move all imports to the top of the file

### STEP-712: Fix incorrect_import_order in test_db_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'incorrect_import_order' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-713: Fix imports_not_at_top in test_query_builder.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Move all imports to the top of the file

### STEP-714: Fix imports_not_at_top in test_async_ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Move all imports to the top of the file

### STEP-715: Fix incorrect_import_order in test_async_ui_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'incorrect_import_order' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-716: Fix imports_not_at_top in test_page_objects.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Move all imports to the top of the file

### STEP-717: Fix incorrect_import_order in test_page_objects.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-718: Fix imports_not_at_top in test_visual_testing.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Move all imports to the top of the file

### STEP-719: Fix incorrect_import_order in test_visual_testing.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'incorrect_import_order' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-720: Fix imports_not_at_top in test_graphql_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Move all imports to the top of the file

### STEP-721: Fix imports_not_at_top in test_graphql_result.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Move all imports to the top of the file

### STEP-722: Fix imports_not_at_top in test_metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-723: Fix imports_not_at_top in test_rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-724: Fix imports_not_at_top in test_retry.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Move all imports to the top of the file

### STEP-725: Fix imports_not_at_top in test_grpc_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Move all imports to the top of the file

### STEP-726: Fix imports_not_at_top in test_grpc_client_additional.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Move all imports to the top of the file

### STEP-727: Fix imports_not_at_top in test_http_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Move all imports to the top of the file

### STEP-728: Fix imports_not_at_top in test_http_result.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Move all imports to the top of the file

### STEP-729: Fix imports_not_at_top in test_metrics.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Move all imports to the top of the file

### STEP-730: Fix imports_not_at_top in test_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-731: Fix incorrect_import_order in test_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'incorrect_import_order' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-732: Fix imports_not_at_top in test_rate_limit.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Move all imports to the top of the file

### STEP-733: Fix imports_not_at_top in test_request_builder.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Move all imports to the top of the file

### STEP-734: Fix incorrect_import_order in test_request_builder.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'incorrect_import_order' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-735: Fix imports_not_at_top in test_soap_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Move all imports to the top of the file

### STEP-736: Fix incorrect_import_order in test_soap_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'incorrect_import_order' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

### STEP-737: Fix imports_not_at_top in test_auth_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-738: Fix imports_not_at_top in test_context.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Move all imports to the top of the file

### STEP-739: Fix imports_not_at_top in test_logging_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-740: Fix imports_not_at_top in test_metrics_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_metrics_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-741: Fix imports_not_at_top in test_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-742: Fix imports_not_at_top in test_rate_limit_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-743: Fix imports_not_at_top in test_retry_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-744: Fix imports_not_at_top in test_validation_middleware.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Move all imports to the top of the file

### STEP-745: Fix imports_not_at_top in test_websocket_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'imports_not_at_top' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Move all imports to the top of the file

### STEP-746: Fix incorrect_import_order in test_websocket_client.py

**Principle/Standard**: Import Organization
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'incorrect_import_order' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Reorder imports: stdlib → third-party → local

## Priority: LOW

### STEP-341: Fix potential_srp_violation in query_builder.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\db_clients\query_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\db_clients\query_builder.py

Suggested fix: Review class '_QueryBuilder' and consider splitting into smaller, focused classes

### STEP-342: Fix potential_srp_violation in request_builder.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\api_clients\http_client\request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\api_clients\http_client\request_builder.py

Suggested fix: Review class '_RequestBuilder' and consider splitting into smaller, focused classes

### STEP-343: Fix potential_srp_violation in websocket_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Review class 'WebSocketClient' and consider splitting into smaller, focused classes

### STEP-344: Fix potential_srp_violation in ui_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Review class 'UiClient' and consider splitting into smaller, focused classes

### STEP-345: Fix potential_srp_violation in ui_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Review class 'UiClient' and consider splitting into smaller, focused classes

### STEP-346: Fix potential_srp_violation in test_config.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\test_config.py

Suggested fix: Review class 'TestConfigInit' and consider splitting into smaller, focused classes

### STEP-347: Fix potential_srp_violation in test_graphql_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Review class 'TestGraphQLClient' and consider splitting into smaller, focused classes

### STEP-348: Fix potential_srp_violation in test_http_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Review class 'TestApiClientMakeRequest' and consider splitting into smaller, focused classes

### STEP-349: Fix potential_srp_violation in test_http_result.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Review class 'TestHttpResult' and consider splitting into smaller, focused classes

### STEP-350: Fix potential_srp_violation in test_request_builder.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Review class 'TestRequestBuilder' and consider splitting into smaller, focused classes

### STEP-351: Fix potential_srp_violation in test_middleware.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Review class 'TestMiddlewareChain' and consider splitting into smaller, focused classes

### STEP-352: Fix potential_srp_violation in test_websocket_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Review class 'TestWebSocketClient' and consider splitting into smaller, focused classes

### STEP-353: Fix missing_args_section in config.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_args_section' in py_web_automation\config.py

Suggested fix: Add Args section to docstring for function 'from_env'

### STEP-354: Fix missing_returns_section in broker_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\broker_clients\broker_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\broker_clients\broker_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-355: Fix missing_returns_section in kafka_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\broker_clients\kafka_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\broker_clients\kafka_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-356: Fix missing_returns_section in rabbitmq_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-357: Fix missing_returns_section in db_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\db_clients\db_client.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_returns_section' in py_web_automation\clients\db_clients\db_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-358: Fix missing_returns_section in mysql_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\db_clients\mysql_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\db_clients\mysql_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-359: Fix missing_returns_section in postgresql_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\db_clients\postgresql_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\db_clients\postgresql_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-360: Fix missing_returns_section in sqlite_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\db_clients\sqlite_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\db_clients\sqlite_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-361: Fix missing_returns_section in graphql_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\graphql_client.py

Suggested fix: Add Returns section to docstring for function 'close'

### STEP-362: Fix missing_returns_section in graphql_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\graphql_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\graphql_result.py

Suggested fix: Add Returns section to docstring for function 'raise_for_errors'

### STEP-363: Fix missing_returns_section in metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\metrics.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\metrics.py

Suggested fix: Add Returns section to docstring for function 'record_request'

### STEP-364: Fix missing_returns_section in rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\rate_limit.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\rate_limit.py

Suggested fix: Add Returns section to docstring for function 'acquire'

### STEP-365: Fix missing_returns_section in grpc_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\grpc_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-366: Fix missing_returns_section in grpc_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\grpc_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\grpc_result.py

Suggested fix: Add Returns section to docstring for function 'raise_for_error'

### STEP-367: Fix missing_returns_section in metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\metrics.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\metrics.py

Suggested fix: Add Returns section to docstring for function 'record_request'

### STEP-368: Fix missing_returns_section in rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\rate_limit.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\rate_limit.py

Suggested fix: Add Returns section to docstring for function 'acquire'

### STEP-369: Fix missing_returns_section in http_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\http_client.py

Suggested fix: Add Returns section to docstring for function 'close'

### STEP-370: Fix missing_returns_section in http_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\http_result.py

Suggested fix: Add Returns section to docstring for function 'raise_for_status'

### STEP-371: Fix missing_returns_section in metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\metrics.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\metrics.py

Suggested fix: Add Returns section to docstring for function 'record_request'

### STEP-372: Fix missing_returns_section in rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\rate_limit.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\rate_limit.py

Suggested fix: Add Returns section to docstring for function 'acquire'

### STEP-373: Fix missing_returns_section in request_builder.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\request_builder.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\request_builder.py

Suggested fix: Add Returns section to docstring for function 'get_endpoint'

### STEP-374: Fix missing_returns_section in validator.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\validator.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\validator.py

Suggested fix: Add Returns section to docstring for function 'validate'

### STEP-375: Fix missing_args_section in validator.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\validator.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_args_section' in py_web_automation\clients\api_clients\http_client\validator.py

Suggested fix: Add Args section to docstring for function 'validate'

### STEP-376: Fix missing_returns_section in metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\metrics.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\metrics.py

Suggested fix: Add Returns section to docstring for function 'record_request'

### STEP-377: Fix missing_returns_section in rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\rate_limit.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\rate_limit.py

Suggested fix: Add Returns section to docstring for function 'acquire'

### STEP-378: Fix missing_returns_section in soap_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\soap_client.py

Suggested fix: Add Returns section to docstring for function 'close'

### STEP-379: Fix missing_returns_section in soap_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\soap_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\soap_result.py

Suggested fix: Add Returns section to docstring for function 'raise_for_fault'

### STEP-380: Fix missing_returns_section in auth_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\auth_middleware.py

Suggested fix: Add Returns section to docstring for function 'update_token'

### STEP-381: Fix missing_returns_section in logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\logging_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-382: Fix missing_returns_section in metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\metrics_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-383: Fix missing_returns_section in middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-384: Fix missing_returns_section in rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\rate_limit_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-385: Fix missing_returns_section in retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\retry_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-386: Fix missing_returns_section in validation_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\graphql_client\middleware\validation_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-387: Fix missing_returns_section in auth_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\middleware\auth_middleware.py

Suggested fix: Add Returns section to docstring for function 'update_token'

### STEP-388: Fix missing_returns_section in logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\middleware\logging_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-389: Fix missing_returns_section in metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\middleware\metrics_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-390: Fix missing_returns_section in middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\middleware\middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-391: Fix missing_returns_section in rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\middleware\rate_limit_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-392: Fix missing_returns_section in retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\grpc_client\middleware\retry_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-393: Fix missing_returns_section in auth_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\auth_middleware.py

Suggested fix: Add Returns section to docstring for function 'update_token'

### STEP-394: Fix missing_returns_section in logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\logging_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-395: Fix missing_returns_section in metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\metrics_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-396: Fix missing_returns_section in middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-397: Fix missing_returns_section in rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\rate_limit_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-398: Fix missing_returns_section in retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\retry_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-399: Fix missing_returns_section in validation_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\http_client\middleware\validation_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-400: Fix missing_returns_section in auth_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\middleware\auth_middleware.py

Suggested fix: Add Returns section to docstring for function 'update_token'

### STEP-401: Fix missing_returns_section in logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\middleware\logging_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-402: Fix missing_returns_section in metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\middleware\metrics_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-403: Fix missing_returns_section in middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\middleware\middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-404: Fix missing_returns_section in rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\middleware\rate_limit_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-405: Fix missing_returns_section in retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\api_clients\soap_client\middleware\retry_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_request'

### STEP-406: Fix missing_returns_section in metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\metrics.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\metrics.py

Suggested fix: Add Returns section to docstring for function 'record_request'

### STEP-407: Fix missing_returns_section in rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\rate_limit.py

Suggested fix: Add Returns section to docstring for function 'acquire'

### STEP-408: Fix missing_returns_section in websocket_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Add Returns section to docstring for function 'connect'

### STEP-409: Fix missing_returns_section in websocket_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\websocket_result.py

Suggested fix: Add Returns section to docstring for function 'raise_for_error'

### STEP-410: Fix missing_returns_section in connection_retry_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\middleware\connection_retry_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_message'

### STEP-411: Fix missing_returns_section in logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\middleware\logging_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_message'

### STEP-412: Fix missing_returns_section in metrics_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\middleware\metrics_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_message'

### STEP-413: Fix missing_returns_section in middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\middleware\middleware.py

Suggested fix: Add Returns section to docstring for function 'process_message'

### STEP-414: Fix missing_returns_section in rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in py_web_automation\clients\streaming_clients\websocket_client\middleware\rate_limit_middleware.py

Suggested fix: Add Returns section to docstring for function 'process_message'

### STEP-415: Fix missing_returns_section in page_objects.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\page_objects.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_returns_section' in py_web_automation\clients\ui_clients\async_ui_client\page_objects.py

Suggested fix: Add Returns section to docstring for function 'navigate'

### STEP-416: Fix missing_args_section in page_objects.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\page_objects.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_args_section' in py_web_automation\clients\ui_clients\async_ui_client\page_objects.py

Suggested fix: Add Args section to docstring for function 'click_element'

### STEP-417: Fix missing_returns_section in ui_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_returns_section' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Add Returns section to docstring for function 'close'

### STEP-418: Fix missing_returns_section in page_objects.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_returns_section' in py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py

Suggested fix: Add Returns section to docstring for function 'navigate'

### STEP-419: Fix missing_args_section in page_objects.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_args_section' in py_web_automation\clients\ui_clients\sync_ui_client\page_objects.py

Suggested fix: Add Args section to docstring for function 'click_element'

### STEP-420: Fix missing_returns_section in ui_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_returns_section' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Add Returns section to docstring for function 'close'

### STEP-421: Fix missing_args_section in conftest.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\conftest.py
**Estimated Effort**: 1.4 hours
**Violations**: 17

Fix 17 violation(s) of type 'missing_args_section' in tests\conftest.py

Suggested fix: Add Args section to docstring for function 'loguru_sink'

### STEP-422: Fix missing_returns_section in conftest.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\conftest.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in tests\conftest.py

Suggested fix: Add Returns section to docstring for function 'format_bytes'

### STEP-423: Fix missing_returns_section in api_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\api_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_returns_section' in tests\fixtures\api_client.py

Suggested fix: Add Returns section to docstring for function 'valid_config'

### STEP-424: Fix missing_args_section in api_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\api_client.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_args_section' in tests\fixtures\api_client.py

Suggested fix: Add Args section to docstring for function 'mock_httpx_response_200'

### STEP-425: Fix missing_args_section in config.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\config.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_args_section' in tests\fixtures\config.py

Suggested fix: Add Args section to docstring for function 'mock_environment'

### STEP-426: Fix missing_returns_section in metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\metrics.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in tests\fixtures\metrics.py

Suggested fix: Add Returns section to docstring for function 'metrics'

### STEP-427: Fix missing_returns_section in middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\middleware.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in tests\fixtures\middleware.py

Suggested fix: Add Returns section to docstring for function 'middleware_chain'

### STEP-428: Fix missing_returns_section in rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\rate_limit.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in tests\fixtures\rate_limit.py

Suggested fix: Add Returns section to docstring for function 'rate_limiter'

### STEP-429: Fix missing_args_section in streaming_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\streaming_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_args_section' in tests\fixtures\streaming_client.py

Suggested fix: Add Args section to docstring for function 'mock_websocket_connection'

### STEP-430: Fix missing_returns_section in streaming_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\streaming_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in tests\fixtures\streaming_client.py

Suggested fix: Add Returns section to docstring for function 'mock_websocket_connection'

### STEP-431: Fix missing_args_section in ui_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_args_section' in tests\fixtures\ui_client.py

Suggested fix: Add Args section to docstring for function 'mock_browser'

### STEP-432: Fix missing_returns_section in ui_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in tests\fixtures\ui_client.py

Suggested fix: Add Returns section to docstring for function 'mock_browser'

### STEP-433: Fix missing_args_section in conftest.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\integration\conftest.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_args_section' in tests\integration\conftest.py

Suggested fix: Add Args section to docstring for function 'integration_config'

### STEP-438: Fix missing_returns_section in test_config.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 7.2 hours
**Violations**: 87

Fix 87 violation(s) of type 'missing_returns_section' in tests\unit\test_config.py

Suggested fix: Add Returns section to docstring for function 'test_valid_config_creation'

### STEP-439: Fix missing_args_section in test_config.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 2.7 hours
**Violations**: 32

Fix 32 violation(s) of type 'missing_args_section' in tests\unit\test_config.py

Suggested fix: Add Args section to docstring for function 'test_config_default_values'

### STEP-448: Fix missing_returns_section in test_page_objects.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_returns_section' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add Returns section to docstring for function 'is_loaded'

### STEP-449: Fix missing_args_section in test_visual_testing.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_args_section' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add Args section to docstring for function 'test_visual_comparator_compare_identical'

### STEP-453: Fix missing_args_section in test_graphql_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add Args section to docstring for function 'test_graphql_result_contains_errors'

### STEP-454: Fix missing_returns_section in test_graphql_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add Returns section to docstring for function 'test_graphql_result_contains_errors'

### STEP-455: Fix missing_returns_section in test_metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\test_metrics.py

Suggested fix: Add Returns section to docstring for function 'test_metrics_record_successful_request'

### STEP-456: Fix missing_returns_section in test_rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_rate_limit.py
**Estimated Effort**: 1.1 hours
**Violations**: 13

Fix 13 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\test_rate_limit.py

Suggested fix: Add Returns section to docstring for function 'test_rate_limit_config_init'

### STEP-457: Fix missing_returns_section in test_retry.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_retry.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\test_retry.py

Suggested fix: Add Returns section to docstring for function 'test_retry_config_init'

### STEP-458: Fix missing_args_section in test_grpc_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add Args section to docstring for function 'test_init'

### STEP-459: Fix missing_args_section in test_grpc_client_additional.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add Args section to docstring for function 'test_set_metadata'

### STEP-462: Fix missing_args_section in test_http_result.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add Args section to docstring for function 'test_api_result_status_codes'

### STEP-463: Fix missing_args_section in test_metrics.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add Args section to docstring for function 'test_metrics_record_request_success'

### STEP-467: Fix missing_args_section in test_rate_limit.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add Args section to docstring for function 'test_rate_limiter_acquire_success'

### STEP-468: Fix missing_args_section in test_request_builder.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add Args section to docstring for function 'test_init'

### STEP-469: Fix missing_args_section in test_soap_client.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add Args section to docstring for function 'mock_zeep_client'

### STEP-470: Fix missing_args_section in test_auth_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Add Args section to docstring for function 'test_auth_middleware_sets_token'

### STEP-471: Fix missing_returns_section in test_auth_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_auth_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_auth_middleware_sets_token'

### STEP-472: Fix missing_returns_section in test_context.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_context.py
**Estimated Effort**: 20 minutes
**Violations**: 4

Fix 4 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_context.py

Suggested fix: Add Returns section to docstring for function 'test_request_context_init'

### STEP-473: Fix missing_args_section in test_logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Add Args section to docstring for function 'test_logging_middleware_logs_request'

### STEP-474: Fix missing_returns_section in test_logging_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_logging_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_logging_middleware_logs_request'

### STEP-482: Fix missing_args_section in test_rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Add Args section to docstring for function 'test_rate_limit_middleware_acquires_permission'

### STEP-483: Fix missing_returns_section in test_rate_limit_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_rate_limit_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_rate_limit_middleware_acquires_permission'

### STEP-487: Fix missing_args_section in test_validation_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_args_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Add Args section to docstring for function 'test_validation_middleware_validates_valid_query'

### STEP-488: Fix missing_returns_section in test_validation_middleware.py

**Principle/Standard**: Documentation Standards
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_returns_section' in tests\unit\clients\api_clients\graphql_client\middleware\test_validation_middleware.py

Suggested fix: Add Returns section to docstring for function 'test_validation_middleware_validates_valid_query'

### STEP-491: Fix line_too_long in rabbitmq_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\broker_clients\rabbitmq_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in py_web_automation\clients\broker_clients\rabbitmq_client.py

Suggested fix: Break line 78 into multiple lines or refactor

### STEP-502: Fix line_too_long in ui_client.py

**Principle/Standard**: Code Style
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'line_too_long' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Break line 205 into multiple lines or refactor

### STEP-587: Fix incorrect_module_location in __init__.py

**Principle/Standard**: Separation of Concerns
**Affected Files**: tests\unit\clients\api_clients\__init__.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'incorrect_module_location' in tests\unit\clients\api_clients\__init__.py

Suggested fix: Move file to appropriate client type subdirectory

### STEP-747: Fix invalid_commit_message in .git

**Principle/Standard**: Git Workflow
**Affected Files**: .git
**Estimated Effort**: 1.7 days
**Violations**: 166

Fix 166 violation(s) of type 'invalid_commit_message' in .git

Suggested fix: Use conventional commit format: 'type: description' (e.g., 'feat: add feature', 'fix: fix bug')
