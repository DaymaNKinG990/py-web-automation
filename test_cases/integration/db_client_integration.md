# DBClient Integration Test Cases

## Overview
Tests for integration between `DBClient` and other framework components (`ApiClient`, `UiClient`).

## Test Categories

### 1. ApiClient + DBClient Integration

#### TC-INTEGRATION-DB-001: ApiClient reads data from database via API
- **Purpose**: Verify integration between `ApiClient` and `DBClient` - API reads data that was stored via DBClient
- **Preconditions**: 
  - Web application with API endpoints that query database
  - Database connection available (SQLite, PostgreSQL, or MySQL)
  - Database schema prepared
  - Test data in database
- **Test Steps**:
  1. Create `DBClient` instance using `DBClient.create()` with appropriate database type
  2. Connect to database using `connect()`
  3. Store test data in database via `DBClient.execute_command()` (INSERT)
  4. Create `ApiClient` with application base URL
  5. Query data via API using `ApiClient.make_request()` (GET endpoint that queries database)
  6. Verify API returns data from database
  7. Verify API response matches database data via `DBClient.execute_query()`
  8. Clean up test data from database
  9. Disconnect from database
- **Expected Result**: API successfully retrieves data stored via DBClient
- **Coverage**: `DBClient.connect()`, `DBClient.execute_command()`, `DBClient.execute_query()`, `ApiClient.make_request()`, `DBClient.disconnect()`
- **Dependencies**: Web application with database-backed API, database connection, database schema

#### TC-INTEGRATION-DB-002: ApiClient writes data to database via API
- **Purpose**: Verify data written via API (POST) is accessible and verifiable via DBClient (SELECT)
- **Preconditions**: 
  - Web application with API endpoints that write to database
  - Database connection available
- **Test Steps**:
  1. Create `ApiClient` and `DBClient`
  2. Connect `DBClient` to database
  3. Create data via API using `ApiClient.make_request()` (POST endpoint)
  4. Query database directly via `DBClient.execute_query()` (SELECT)
  5. Verify data written via API is present in database
  6. Verify data integrity and format
  7. Clean up test data
- **Expected Result**: Data written via API is correctly stored in database and accessible via DBClient
- **Coverage**: `ApiClient.make_request()` POST, `DBClient.execute_query()`
- **Dependencies**: Web application with write API endpoints, database connection

#### TC-INTEGRATION-DB-003: RequestBuilder + DBClient integration
- **Purpose**: Verify RequestBuilder works with database-backed API
- **Preconditions**: 
  - Web application with database-backed API
  - Database connection available
- **Test Steps**:
  1. Create `DBClient` and seed test data
  2. Create `ApiClient` with base URL
  3. Use `build_request()` to create RequestBuilder
  4. Build and execute request: `.get("/users").params(page=1).execute()`
  5. Verify response contains database data
  6. Validate response using `validate_api_result()`
  7. Clean up test data
- **Expected Result**: RequestBuilder works correctly with database-backed API
- **Coverage**: `RequestBuilder` + `DBClient` integration
- **Dependencies**: Web application with database-backed API

### 2. UiClient + DBClient Integration

#### TC-INTEGRATION-DB-004: UiClient + DBClient Integration
- **Purpose**: Verify integration between `UiClient` and `DBClient` for database-backed UI testing
- **Preconditions**: 
  - Web application with UI that displays database data
  - Database connection available
  - Test data in database
- **Test Steps**:
  1. Create `DBClient` instance and connect
  2. Store test data in database via `DBClient.execute_command()` (INSERT)
  3. Create `UiClient` with application base URL
  4. Setup browser using `setup_browser()`
  5. Navigate to application UI
  6. Verify UI displays data from database (check text content, elements)
  7. Verify data matches database content via `DBClient.execute_query()`
  8. Clean up test data
  9. Close browser
- **Expected Result**: UI successfully displays data stored via DBClient
- **Coverage**: `DBClient.execute_command()`, `DBClient.execute_query()`, `UiClient` UI interactions
- **Dependencies**: Web application with database-backed UI, database connection, browser setup

#### TC-INTEGRATION-DB-005: UiClient writes to database via UI
- **Purpose**: Verify data written via UI form is accessible via DBClient
- **Preconditions**: 
  - Web application with UI form that writes to database
  - Database connection available
- **Test Steps**:
  1. Create `UiClient` and `DBClient`
  2. Connect `DBClient` to database
  3. Setup browser and navigate to form
  4. Fill form fields using `UiClient` methods
  5. Submit form through UI
  6. Query database directly via `DBClient.execute_query()` (SELECT)
  7. Verify data written via UI is present in database
  8. Verify data integrity
  9. Clean up test data
- **Expected Result**: Data written via UI is correctly stored in database and accessible via DBClient
- **Coverage**: `UiClient` form interactions, `DBClient.execute_query()`
- **Dependencies**: Web application with form submission, database connection

### 3. Full Workflow Integration

#### TC-INTEGRATION-DB-006: Full Workflow with DBClient
- **Purpose**: Verify complete workflow: DBClient → ApiClient → UiClient
- **Preconditions**: 
  - Complete web application setup with database backend
  - All components available (DBClient, ApiClient, UiClient)
  - Database schema prepared
- **Test Steps**:
  1. Setup database schema via `DBClient.execute_command()` (CREATE TABLE if needed)
  2. Seed test data via `DBClient.execute_command()` (INSERT)
  3. Test API endpoints that use database data via `ApiClient.make_request()`
  4. Test UI that displays database data via `UiClient` interactions
  5. Verify end-to-end data flow: Database → API → UI
  6. Verify data consistency across all layers
  7. Clean up resources
- **Expected Result**: Complete workflow with database integration works correctly
- **Coverage**: Full integration with database across all components
- **Dependencies**: Complete web application with database, all components available

### 4. Transaction Integration

#### TC-INTEGRATION-DB-007: DBClient Transaction Integration
- **Purpose**: Verify database transactions work correctly in integration context
- **Preconditions**: 
  - Database connection available
  - Database with transaction support
  - Web application with transaction-aware operations
- **Test Steps**:
  1. Create `DBClient` and connect
  2. Begin transaction using `begin_transaction()`
  3. Execute multiple commands using `execute_command()` (INSERT, UPDATE)
  4. Test API that uses transaction data (if applicable)
  5. Commit transaction using `commit_transaction()`
  6. Verify all changes persisted to database
  7. Verify API can access committed data
- **Expected Result**: Transactions work correctly in integration, all changes persisted after commit
- **Coverage**: `DBClient.begin_transaction()`, `DBClient.commit_transaction()`, `DBClient.execute_command()` in transaction
- **Dependencies**: Database with transaction support

#### TC-INTEGRATION-DB-008: DBClient Transaction Rollback
- **Purpose**: Verify transaction rollback works correctly in integration
- **Preconditions**: 
  - Database connection available
  - Database with transaction support
- **Test Steps**:
  1. Create `DBClient` and connect
  2. Begin transaction using `begin_transaction()`
  3. Execute commands using `execute_command()` (INSERT, UPDATE)
  4. Rollback transaction using `rollback_transaction()`
  5. Verify changes are NOT persisted to database
  6. Verify database state is unchanged
- **Expected Result**: Transaction rollback works correctly, no changes persisted
- **Coverage**: `DBClient.begin_transaction()`, `DBClient.rollback_transaction()`
- **Dependencies**: Database with transaction support

#### TC-INTEGRATION-DB-009: DBClient Transaction Context Manager
- **Purpose**: Verify transaction context manager works in integration
- **Preconditions**: 
  - Database connection available
  - Database with transaction support
- **Test Steps**:
  1. Create `DBClient` and connect
  2. Use transaction context manager: `async with db_client.transaction():`
  3. Execute commands within context
  4. Verify transaction commits automatically on success
  5. Test with exception within context (should rollback)
  6. Verify rollback works correctly on exception
- **Expected Result**: Transaction context manager works correctly, commits on success, rolls back on exception
- **Coverage**: `DBClient.transaction()` context manager
- **Dependencies**: Database with transaction support

### 5. Multiple Database Types

#### TC-INTEGRATION-DB-010: DBClient with Multiple Database Types
- **Purpose**: Verify `DBClient` works with different database backends in integration
- **Preconditions**: 
  - Multiple database types available (SQLite, PostgreSQL, MySQL)
  - Database adapters installed (aiosqlite, asyncpg/psycopg, aiomysql/pymysql)
- **Test Steps**:
  1. Test SQLite integration: create `DBClient.create('sqlite', ...)`, connect, execute operations
  2. Test PostgreSQL integration (if available): create `DBClient.create('postgresql', ...)`, connect, execute operations
  3. Test MySQL integration (if available): create `DBClient.create('mysql', ...)`, connect, execute operations
  4. Verify same operations work across all types
  5. Verify data format consistency
- **Expected Result**: `DBClient` works with all supported database types in integration
- **Coverage**: `DBClient.create()` with different `db_type` values, all adapters
- **Dependencies**: Multiple database backends, appropriate adapters installed

### 6. MySQL Adapter Integration with Real Database

#### TC-INTEGRATION-DB-MYSQL-001: MySQL Adapter Integration with pymysql fallback
- **Purpose**: Verify MySQLAdapter works with real MySQL database using pymysql fallback
- **Preconditions**: 
  - MySQL database server available
  - pymysql library installed (aiomysql not available)
  - MySQL connection credentials
- **Test Steps**:
  1. Create MySQLAdapter with connection string or kwargs
  2. Verify _adapter_type is "pymysql"
  3. Connect to real MySQL database
  4. Execute CREATE TABLE if needed
  5. Execute INSERT command via execute_command()
  6. Execute SELECT query via execute_query()
  7. Verify data retrieved correctly
  8. Execute UPDATE and DELETE commands
  9. Test transaction operations (begin, commit, rollback)
  10. Disconnect from database
- **Expected Result**: MySQLAdapter works correctly with real MySQL database using pymysql
- **Coverage**: Full MySQLAdapter functionality with pymysql fallback
- **Dependencies**: MySQL database server, pymysql library

#### TC-INTEGRATION-DB-MYSQL-002: MySQL Adapter Integration with aiomysql
- **Purpose**: Verify MySQLAdapter works with real MySQL database using aiomysql
- **Preconditions**: 
  - MySQL database server available
  - aiomysql library installed
  - MySQL connection credentials
- **Test Steps**:
  1. Create MySQLAdapter with connection string or kwargs
  2. Verify _adapter_type is "aiomysql"
  3. Connect to real MySQL database
  4. Execute CREATE TABLE if needed
  5. Execute INSERT command via execute_command()
  6. Execute SELECT query via execute_query()
  7. Verify data retrieved correctly
  8. Execute UPDATE and DELETE commands
  9. Test transaction operations (begin, commit, rollback)
  10. Disconnect from database
- **Expected Result**: MySQLAdapter works correctly with real MySQL database using aiomysql
- **Coverage**: Full MySQLAdapter functionality with aiomysql
- **Dependencies**: MySQL database server, aiomysql library

### 7. PostgreSQL Adapter Integration with Real Database

#### TC-INTEGRATION-DB-PG-001: PostgreSQL Adapter Integration with psycopg fallback
- **Purpose**: Verify PostgreSQLAdapter works with real PostgreSQL database using psycopg fallback
- **Preconditions**: 
  - PostgreSQL database server available
  - psycopg library installed (asyncpg not available)
  - PostgreSQL connection credentials
- **Test Steps**:
  1. Create PostgreSQLAdapter with connection string or kwargs
  2. Verify _adapter_type is "psycopg"
  3. Connect to real PostgreSQL database
  4. Execute CREATE TABLE if needed
  5. Execute INSERT command via execute_command()
  6. Execute SELECT query via execute_query()
  7. Verify data retrieved correctly
  8. Execute UPDATE and DELETE commands
  9. Test transaction operations (begin, commit, rollback)
  10. Disconnect from database
- **Expected Result**: PostgreSQLAdapter works correctly with real PostgreSQL database using psycopg
- **Coverage**: Full PostgreSQLAdapter functionality with psycopg fallback
- **Dependencies**: PostgreSQL database server, psycopg library

#### TC-INTEGRATION-DB-PG-002: PostgreSQL Adapter Integration with asyncpg
- **Purpose**: Verify PostgreSQLAdapter works with real PostgreSQL database using asyncpg
- **Preconditions**: 
  - PostgreSQL database server available
  - asyncpg library installed
  - PostgreSQL connection credentials
- **Test Steps**:
  1. Create PostgreSQLAdapter with connection string or kwargs
  2. Verify _adapter_type is "asyncpg"
  3. Connect to real PostgreSQL database
  4. Execute CREATE TABLE if needed
  5. Execute INSERT command via execute_command()
  6. Execute SELECT query via execute_query()
  7. Verify data retrieved correctly
  8. Execute UPDATE and DELETE commands
  9. Test transaction operations (begin, commit, rollback)
  10. Disconnect from database
- **Expected Result**: PostgreSQLAdapter works correctly with real PostgreSQL database using asyncpg
- **Coverage**: Full PostgreSQLAdapter functionality with asyncpg
- **Dependencies**: PostgreSQL database server, asyncpg library

## Summary

- **Total test cases**: 14
- **Categories**: 7 (ApiClient integration, UiClient integration, Full workflow, Transactions, Multiple database types, MySQL integration, PostgreSQL integration)
- **Coverage**: Complete integration testing of `DBClient` with all framework components and real database backends
