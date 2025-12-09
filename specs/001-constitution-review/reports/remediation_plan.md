# Remediation Plan

Total remediation steps: 100

## Priority: HIGH

### STEP-001: Fix missing_return_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\conftest.py
**Estimated Effort**: 2.2 hours
**Violations**: 27

Fix 27 violation(s) of type 'missing_return_type_annotation' in tests\conftest.py

Suggested fix: Add return type annotation to function 'loguru_sink' (e.g., -> int, -> str, -> None)

### STEP-002: Fix missing_parameter_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\conftest.py
**Estimated Effort**: 2.2 hours
**Violations**: 26

Fix 26 violation(s) of type 'missing_parameter_type_annotation' in tests\conftest.py

Suggested fix: Add type annotation to parameter 'message' in function 'loguru_sink'

### STEP-003: Fix missing_return_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 15 minutes
**Violations**: 3

Fix 3 violation(s) of type 'missing_return_type_annotation' in tests\fixtures\ui_client.py

Suggested fix: Add return type annotation to function 'ui_client_with_browser' (e.g., -> int, -> str, -> None)

### STEP-004: Fix missing_parameter_type_annotation in ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\fixtures\ui_client.py
**Estimated Effort**: 30 minutes
**Violations**: 6

Fix 6 violation(s) of type 'missing_parameter_type_annotation' in tests\fixtures\ui_client.py

Suggested fix: Add type annotation to parameter 'ui_client_with_config' in function 'ui_client_with_browser'

### STEP-005: Fix missing_return_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\conftest.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_return_type_annotation' in tests\integration\conftest.py

Suggested fix: Add return type annotation to function 'integration_config' (e.g., -> int, -> str, -> None)

### STEP-006: Fix missing_parameter_type_annotation in conftest.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\conftest.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in tests\integration\conftest.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'integration_config'

### STEP-007: Fix missing_return_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_return_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add return type annotation to function 'check_kafka_available' (e.g., -> int, -> str, -> None)

### STEP-008: Fix missing_parameter_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_parameter_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_connect_to_real_kafka'

### STEP-009: Fix missing_method_return_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_method_return_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add return type annotation to method 'TestKafkaClientIntegration.test_connect_to_real_kafka'

### STEP-010: Fix missing_method_parameter_type_annotation in test_kafka_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_kafka_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_method_parameter_type_annotation' in tests\integration\test_kafka_client_integration.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestKafkaClientIntegration.test_connect_to_real_kafka'

### STEP-011: Fix missing_return_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.3 hours
**Violations**: 16

Fix 16 violation(s) of type 'missing_return_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add return type annotation to function 'check_rabbitmq_available' (e.g., -> int, -> str, -> None)

### STEP-012: Fix missing_parameter_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_parameter_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_connect_to_real_rabbitmq'

### STEP-013: Fix missing_method_return_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_method_return_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add return type annotation to method 'TestRabbitMQClientIntegration.test_connect_to_real_rabbitmq'

### STEP-014: Fix missing_method_parameter_type_annotation in test_rabbitmq_client_integration.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\integration\test_rabbitmq_client_integration.py
**Estimated Effort**: 1.2 hours
**Violations**: 14

Fix 14 violation(s) of type 'missing_method_parameter_type_annotation' in tests\integration\test_rabbitmq_client_integration.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestRabbitMQClientIntegration.test_connect_to_real_rabbitmq'

### STEP-015: Fix missing_return_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_return_type_annotation' in tests\unit\test_config.py

Suggested fix: Add return type annotation to function 'test_config_validation_invalid_maximal_retry_count' (e.g., -> int, -> str, -> None)

### STEP-016: Fix missing_parameter_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\test_config.py

Suggested fix: Add type annotation to parameter 'invalid_config_data_maximal_retry_count' in function 'test_config_validation_invalid_maximal_retry_count'

### STEP-017: Fix missing_method_return_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\test_config.py

Suggested fix: Add return type annotation to method 'TestConfigInit.test_config_validation_invalid_maximal_retry_count'

### STEP-018: Fix missing_method_parameter_type_annotation in test_config.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\test_config.py

Suggested fix: Add type annotation to parameter 'invalid_config_data_maximal_retry_count' in method 'TestConfigInit.test_config_validation_invalid_maximal_retry_count'

### STEP-019: Fix missing_return_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 2.6 hours
**Violations**: 31

Fix 31 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add return type annotation to function 'test_init_with_valid_url' (e.g., -> int, -> str, -> None)

### STEP-020: Fix missing_parameter_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 4.2 hours
**Violations**: 51

Fix 51 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_init_with_valid_url'

### STEP-021: Fix missing_method_return_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add return type annotation to method 'TestKafkaClientInit.test_init_with_valid_url'

### STEP-022: Fix missing_method_parameter_type_annotation in test_kafka_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_kafka_client.py
**Estimated Effort**: 4.2 hours
**Violations**: 50

Fix 50 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\broker_clients\test_kafka_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestKafkaClientInit.test_init_with_valid_url'

### STEP-023: Fix missing_return_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 4.7 hours
**Violations**: 56

Fix 56 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add return type annotation to function 'test_init_with_valid_url' (e.g., -> int, -> str, -> None)

### STEP-024: Fix missing_parameter_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 4.6 hours
**Violations**: 55

Fix 55 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_init_with_valid_url'

### STEP-025: Fix missing_method_return_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 2.6 hours
**Violations**: 31

Fix 31 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add return type annotation to method 'TestRabbitMQClientInit.test_init_with_valid_url'

### STEP-026: Fix missing_method_parameter_type_annotation in test_rabbitmq_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\broker_clients\test_rabbitmq_client.py
**Estimated Effort**: 4.5 hours
**Violations**: 54

Fix 54 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\broker_clients\test_rabbitmq_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestRabbitMQClientInit.test_init_with_valid_url'

### STEP-027: Fix missing_return_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 3.6 hours
**Violations**: 43

Fix 43 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add return type annotation to function 'test_init_with_connection_string' (e.g., -> int, -> str, -> None)

### STEP-028: Fix missing_parameter_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add type annotation to parameter 'mocker' in function 'test_close_calls_disconnect'

### STEP-029: Fix missing_method_return_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 3.4 hours
**Violations**: 41

Fix 41 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add return type annotation to method 'TestDBClientInit.test_init_with_connection_string'

### STEP-030: Fix missing_method_parameter_type_annotation in test_db_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_db_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\db_clients\test_db_client.py

Suggested fix: Add type annotation to parameter 'mocker' in method 'TestDBClientConnection.test_close_calls_disconnect'

### STEP-031: Fix missing_return_type_annotation in test_query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add return type annotation to function 'test_query_builder_select' (e.g., -> int, -> str, -> None)

### STEP-032: Fix missing_method_return_type_annotation in test_query_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\db_clients\test_query_builder.py
**Estimated Effort**: 2.3 hours
**Violations**: 28

Fix 28 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\db_clients\test_query_builder.py

Suggested fix: Add return type annotation to method 'TestQueryBuilderSelect.test_query_builder_select'

### STEP-033: Fix missing_return_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5.8 hours
**Violations**: 70

Fix 70 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add return type annotation to function 'test_init_with_config_none_uses_default' (e.g., -> int, -> str, -> None)

### STEP-034: Fix missing_parameter_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 1.8 days
**Violations**: 168

Fix 168 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_init_with_url_and_config'

### STEP-035: Fix missing_method_return_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 5.8 hours
**Violations**: 70

Fix 70 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add return type annotation to method 'TestUiClientInit.test_init_with_config_none_uses_default'

### STEP-036: Fix missing_method_parameter_type_annotation in test_async_ui_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_async_ui_client.py
**Estimated Effort**: 1.8 days
**Violations**: 168

Fix 168 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\ui_clients\test_async_ui_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestUiClientInit.test_init_with_url_and_config'

### STEP-037: Fix missing_return_type_annotation in test_page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add return type annotation to function 'test_base_page_init' (e.g., -> int, -> str, -> None)

### STEP-038: Fix missing_method_return_type_annotation in test_page_objects.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_page_objects.py
**Estimated Effort**: 1.8 hours
**Violations**: 22

Fix 22 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\ui_clients\test_page_objects.py

Suggested fix: Add return type annotation to method 'TestBasePage.test_base_page_init'

### STEP-039: Fix missing_return_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add return type annotation to function 'test_visual_comparator_init' (e.g., -> int, -> str, -> None)

### STEP-040: Fix missing_parameter_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add type annotation to parameter 'tmp_path' in function 'test_visual_comparator_compare_identical'

### STEP-041: Fix missing_method_return_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add return type annotation to method 'TestVisualComparator.test_visual_comparator_init'

### STEP-042: Fix missing_method_parameter_type_annotation in test_visual_testing.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\ui_clients\test_visual_testing.py
**Estimated Effort**: 35 minutes
**Violations**: 7

Fix 7 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\ui_clients\test_visual_testing.py

Suggested fix: Add type annotation to parameter 'tmp_path' in method 'TestVisualComparator.test_visual_comparator_compare_identical'

### STEP-043: Fix missing_parameter_type_annotation in test_graphql_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Add type annotation to parameter 'request_context' in function 'delayed_error'

### STEP-044: Fix missing_parameter_type_annotation in test_graphql_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add type annotation to parameter 'mock_graphql_execute_operation' in function 'test_graphql_result_no_errors'

### STEP-045: Fix missing_method_parameter_type_annotation in test_graphql_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_result.py
**Estimated Effort**: 10 minutes
**Violations**: 2

Fix 2 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\test_graphql_result.py

Suggested fix: Add type annotation to parameter 'mock_graphql_execute_operation' in method 'TestGraphQLResult.test_graphql_result_no_errors'

### STEP-046: Fix missing_return_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add return type annotation to function 'test_init' (e.g., -> int, -> str, -> None)

### STEP-047: Fix missing_parameter_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_init'

### STEP-048: Fix missing_method_return_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 25 minutes
**Violations**: 5

Fix 5 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add return type annotation to method 'TestGrpcClient.test_init'

### STEP-049: Fix missing_method_parameter_type_annotation in test_grpc_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestGrpcClient.test_init'

### STEP-050: Fix missing_return_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add return type annotation to function 'test_set_metadata' (e.g., -> int, -> str, -> None)

### STEP-051: Fix missing_parameter_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add type annotation to parameter 'valid_config' in function 'test_set_metadata'

### STEP-052: Fix missing_method_return_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add return type annotation to method 'TestGrpcClientAdditional.test_set_metadata'

### STEP-053: Fix missing_method_parameter_type_annotation in test_grpc_client_additional.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\grpc_client\test_grpc_client_additional.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestGrpcClientAdditional.test_set_metadata'

### STEP-054: Fix missing_return_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 3.9 hours
**Violations**: 47

Fix 47 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add return type annotation to function 'test_init_with_url_and_config' (e.g., -> int, -> str, -> None)

### STEP-055: Fix missing_parameter_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 1.3 days
**Violations**: 125

Fix 125 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add type annotation to parameter 'mocker' in function 'test_init_with_url_and_config'

### STEP-056: Fix missing_method_return_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 3.9 hours
**Violations**: 47

Fix 47 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add return type annotation to method 'TestApiClientInit.test_init_with_url_and_config'

### STEP-057: Fix missing_method_parameter_type_annotation in test_http_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 1.3 days
**Violations**: 125

Fix 125 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Add type annotation to parameter 'mocker' in method 'TestApiClientInit.test_init_with_url_and_config'

### STEP-058: Fix missing_return_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 3.4 hours
**Violations**: 41

Fix 41 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add return type annotation to function 'test_valid_api_result_creation' (e.g., -> int, -> str, -> None)

### STEP-059: Fix missing_parameter_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add type annotation to parameter 'status_code' in function 'test_api_result_status_codes'

### STEP-060: Fix missing_method_return_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 3.4 hours
**Violations**: 41

Fix 41 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add return type annotation to method 'TestHttpResult.test_valid_api_result_creation'

### STEP-061: Fix missing_method_parameter_type_annotation in test_http_result.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Add type annotation to parameter 'status_code' in method 'TestHttpResult.test_api_result_status_codes'

### STEP-062: Fix missing_return_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add return type annotation to function 'test_metrics_record_request_success' (e.g., -> int, -> str, -> None)

### STEP-063: Fix missing_parameter_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add type annotation to parameter 'metrics' in function 'test_metrics_record_request_success'

### STEP-064: Fix missing_method_return_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add return type annotation to method 'TestMetricsRecordRequest.test_metrics_record_request_success'

### STEP-065: Fix missing_method_parameter_type_annotation in test_metrics.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_metrics.py
**Estimated Effort**: 1.2 hours
**Violations**: 15

Fix 15 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_metrics.py

Suggested fix: Add type annotation to parameter 'metrics' in method 'TestMetricsRecordRequest.test_metrics_record_request_success'

### STEP-066: Fix missing_return_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 3.0 hours
**Violations**: 36

Fix 36 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add return type annotation to function 'test_middleware_chain_add' (e.g., -> int, -> str, -> None)

### STEP-067: Fix missing_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 3.1 hours
**Violations**: 37

Fix 37 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add type annotation to parameter 'middleware_chain' in function 'test_middleware_chain_add'

### STEP-068: Fix missing_method_return_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 3.0 hours
**Violations**: 36

Fix 36 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add return type annotation to method 'TestMiddlewareChain.test_middleware_chain_add'

### STEP-069: Fix missing_method_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_middleware.py
**Estimated Effort**: 3.1 hours
**Violations**: 37

Fix 37 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_middleware.py

Suggested fix: Add type annotation to parameter 'middleware_chain' in method 'TestMiddlewareChain.test_middleware_chain_add'

### STEP-070: Fix missing_return_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add return type annotation to function 'test_rate_limiter_acquire_success' (e.g., -> int, -> str, -> None)

### STEP-071: Fix missing_parameter_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add type annotation to parameter 'rate_limiter' in function 'test_rate_limiter_acquire_success'

### STEP-072: Fix missing_method_return_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add return type annotation to method 'TestRateLimiter.test_rate_limiter_acquire_success'

### STEP-073: Fix missing_method_parameter_type_annotation in test_rate_limit.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_rate_limit.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_rate_limit.py

Suggested fix: Add type annotation to parameter 'rate_limiter' in method 'TestRateLimiter.test_rate_limiter_acquire_success'

### STEP-074: Fix missing_return_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add return type annotation to function 'test_init' (e.g., -> int, -> str, -> None)

### STEP-075: Fix missing_parameter_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 3.6 hours
**Violations**: 43

Fix 43 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add type annotation to parameter 'mocker' in function 'test_init'

### STEP-076: Fix missing_method_return_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add return type annotation to method 'TestRequestBuilder.test_init'

### STEP-077: Fix missing_method_parameter_type_annotation in test_request_builder.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 3.6 hours
**Violations**: 43

Fix 43 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Add type annotation to parameter 'mocker' in method 'TestRequestBuilder.test_init'

### STEP-078: Fix missing_return_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 45 minutes
**Violations**: 9

Fix 9 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add return type annotation to function 'mock_zeep_client' (e.g., -> int, -> str, -> None)

### STEP-079: Fix missing_parameter_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 55 minutes
**Violations**: 11

Fix 11 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add type annotation to parameter 'mocker' in function 'mock_zeep_client'

### STEP-080: Fix missing_method_return_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 40 minutes
**Violations**: 8

Fix 8 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add return type annotation to method 'TestSoapClient.test_init'

### STEP-081: Fix missing_method_parameter_type_annotation in test_soap_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\soap_client\test_soap_client.py
**Estimated Effort**: 50 minutes
**Violations**: 10

Fix 10 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\soap_client\test_soap_client.py

Suggested fix: Add type annotation to parameter 'valid_config' in method 'TestSoapClient.test_init'

### STEP-082: Fix missing_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add type annotation to parameter 'context' in function 'process_request'

### STEP-083: Fix missing_method_parameter_type_annotation in test_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 1.8 hours
**Violations**: 21

Fix 21 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Add type annotation to parameter 'context' in method 'TestMiddleware.process_request'

### STEP-084: Fix missing_parameter_type_annotation in test_retry_middleware.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\api_clients\graphql_client\middleware\test_retry_middleware.py

Suggested fix: Add type annotation to parameter 'request_context' in function 'mock_execute_with_retry'

### STEP-085: Fix missing_return_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5.3 hours
**Violations**: 64

Fix 64 violation(s) of type 'missing_return_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add return type annotation to function 'test_init' (e.g., -> int, -> str, -> None)

### STEP-086: Fix missing_parameter_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5.5 hours
**Violations**: 66

Fix 66 violation(s) of type 'missing_parameter_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add type annotation to parameter 'mocker' in function 'test_init'

### STEP-087: Fix missing_method_return_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 2.4 hours
**Violations**: 29

Fix 29 violation(s) of type 'missing_method_return_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add return type annotation to method 'TestWebSocketClient.test_init'

### STEP-088: Fix missing_method_parameter_type_annotation in test_websocket_client.py

**Principle/Standard**: Type Safety
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5.0 hours
**Violations**: 60

Fix 60 violation(s) of type 'missing_method_parameter_type_annotation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Add type annotation to parameter 'mocker' in method 'TestWebSocketClient.test_init'

## Priority: LOW

### STEP-089: Fix potential_srp_violation in query_builder.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\db_clients\query_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\db_clients\query_builder.py

Suggested fix: Review class '_QueryBuilder' and consider splitting into smaller, focused classes

### STEP-090: Fix potential_srp_violation in request_builder.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\api_clients\http_client\request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\api_clients\http_client\request_builder.py

Suggested fix: Review class '_RequestBuilder' and consider splitting into smaller, focused classes

### STEP-091: Fix potential_srp_violation in websocket_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\streaming_clients\websocket_client\websocket_client.py

Suggested fix: Review class 'WebSocketClient' and consider splitting into smaller, focused classes

### STEP-092: Fix potential_srp_violation in ui_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\ui_clients\async_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\ui_clients\async_ui_client\ui_client.py

Suggested fix: Review class 'UiClient' and consider splitting into smaller, focused classes

### STEP-093: Fix potential_srp_violation in ui_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in py_web_automation\clients\ui_clients\sync_ui_client\ui_client.py

Suggested fix: Review class 'UiClient' and consider splitting into smaller, focused classes

### STEP-094: Fix potential_srp_violation in test_config.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\test_config.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\test_config.py

Suggested fix: Review class 'TestConfigInit' and consider splitting into smaller, focused classes

### STEP-095: Fix potential_srp_violation in test_graphql_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\graphql_client\test_graphql_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\graphql_client\test_graphql_client.py

Suggested fix: Review class 'TestGraphQLClient' and consider splitting into smaller, focused classes

### STEP-096: Fix potential_srp_violation in test_http_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\http_client\test_http_client.py

Suggested fix: Review class 'TestApiClientMakeRequest' and consider splitting into smaller, focused classes

### STEP-097: Fix potential_srp_violation in test_http_result.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\http_client\test_http_result.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\http_client\test_http_result.py

Suggested fix: Review class 'TestHttpResult' and consider splitting into smaller, focused classes

### STEP-098: Fix potential_srp_violation in test_request_builder.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\http_client\test_request_builder.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\http_client\test_request_builder.py

Suggested fix: Review class 'TestRequestBuilder' and consider splitting into smaller, focused classes

### STEP-099: Fix potential_srp_violation in test_middleware.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\api_clients\graphql_client\middleware\test_middleware.py

Suggested fix: Review class 'TestMiddlewareChain' and consider splitting into smaller, focused classes

### STEP-100: Fix potential_srp_violation in test_websocket_client.py

**Principle/Standard**: SOLID Principles
**Affected Files**: tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py
**Estimated Effort**: 5 minutes
**Violations**: 1

Fix 1 violation(s) of type 'potential_srp_violation' in tests\unit\clients\streaming_clients\websocket_client\test_websocket_client.py

Suggested fix: Review class 'TestWebSocketClient' and consider splitting into smaller, focused classes
