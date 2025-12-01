# Query Builder Module - Unit Test Cases

## Overview
Tests for `py_web_automation.query_builder` module - fluent SQL query builder.

## Test Categories

### 1. SELECT Query Tests

#### TC-QB-001: QueryBuilder - select
- **Purpose**: Verify SELECT query building
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call select("id", "name", "email")
  3. Call from_table("users")
  4. Call build()
  5. Verify SQL: "SELECT id, name, email FROM users"
- **Expected Result**: SELECT query built correctly
- **Coverage**: `QueryBuilder.select` method

#### TC-QB-002: QueryBuilder - select *
- **Purpose**: Verify SELECT * query
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call select("*")
  3. Call from_table("users")
  4. Call build()
  5. Verify SQL: "SELECT * FROM users"
- **Expected Result**: SELECT * query built
- **Coverage**: `QueryBuilder.select` method - wildcard

#### TC-QB-003: QueryBuilder - from_table
- **Purpose**: Verify FROM clause
- **Preconditions**: QueryBuilder with select
- **Test Steps**:
  1. Create QueryBuilder
  2. Call select("*").from_table("users")
  3. Call build()
  4. Verify FROM clause in SQL
- **Expected Result**: FROM clause added
- **Coverage**: `QueryBuilder.from_table` method

#### TC-QB-004: QueryBuilder - where
- **Purpose**: Verify WHERE clause
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call select("*").from_table("users").where("active", "=", True)
  3. Call build()
  4. Verify WHERE clause and parameters
- **Expected Result**: WHERE clause added, params={"where_0": True}
- **Coverage**: `QueryBuilder.where` method

#### TC-QB-005: QueryBuilder - multiple where
- **Purpose**: Verify multiple WHERE conditions
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call where("active", "=", True).where("age", ">=", 18)
  3. Call build()
  4. Verify both conditions in WHERE with AND
- **Expected Result**: Both conditions in WHERE, joined with AND
- **Coverage**: `QueryBuilder.where` method - multiple

#### TC-QB-006: QueryBuilder - order_by
- **Purpose**: Verify ORDER BY clause
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call order_by("name", "ASC")
  3. Call build()
  4. Verify ORDER BY clause in SQL
- **Expected Result**: ORDER BY name ASC added
- **Coverage**: `QueryBuilder.order_by` method

#### TC-QB-007: QueryBuilder - order_by DESC
- **Purpose**: Verify ORDER BY DESC
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call order_by("created_at", "DESC")
  3. Call build()
  4. Verify ORDER BY created_at DESC
- **Expected Result**: ORDER BY DESC added
- **Coverage**: `QueryBuilder.order_by` method - DESC

#### TC-QB-008: QueryBuilder - multiple order_by
- **Purpose**: Verify multiple ORDER BY columns
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call order_by("status", "ASC").order_by("name", "ASC")
  3. Call build()
  4. Verify both columns in ORDER BY
- **Expected Result**: Multiple ORDER BY columns
- **Coverage**: `QueryBuilder.order_by` method - multiple

#### TC-QB-009: QueryBuilder - limit
- **Purpose**: Verify LIMIT clause
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call limit(10)
  3. Call build()
  4. Verify LIMIT 10 in SQL
- **Expected Result**: LIMIT 10 added
- **Coverage**: `QueryBuilder.limit` method

#### TC-QB-010: QueryBuilder - offset
- **Purpose**: Verify OFFSET clause
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call offset(20)
  3. Call build()
  4. Verify OFFSET 20 in SQL
- **Expected Result**: OFFSET 20 added
- **Coverage**: `QueryBuilder.offset` method

#### TC-QB-011: QueryBuilder - limit и offset вместе
- **Purpose**: Verify LIMIT and OFFSET together
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call limit(10).offset(20)
  3. Call build()
  4. Verify LIMIT 10 OFFSET 20 in SQL
- **Expected Result**: Both LIMIT and OFFSET added
- **Coverage**: `QueryBuilder.limit` and `offset` methods

#### TC-QB-012: QueryBuilder - join
- **Purpose**: Verify JOIN clause
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call join("orders", "users.id", "orders.user_id", "LEFT")
  3. Call build()
  4. Verify LEFT JOIN clause in SQL
- **Expected Result**: LEFT JOIN added
- **Coverage**: `QueryBuilder.join` method

#### TC-QB-013: QueryBuilder - multiple joins
- **Purpose**: Verify multiple JOINs
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call join("orders", ...).join("products", ...)
  3. Call build()
  4. Verify both JOINs in SQL
- **Expected Result**: Multiple JOINs added
- **Coverage**: `QueryBuilder.join` method - multiple

#### TC-QB-014: QueryBuilder - group_by
- **Purpose**: Verify GROUP BY clause
- **Preconditions**: QueryBuilder with select and from_table
- **Test Steps**:
  1. Create QueryBuilder
  2. Call group_by("status", "category")
  3. Call build()
  4. Verify GROUP BY clause in SQL
- **Expected Result**: GROUP BY added
- **Coverage**: `QueryBuilder.group_by` method

#### TC-QB-015: QueryBuilder - having
- **Purpose**: Verify HAVING clause
- **Preconditions**: QueryBuilder with select, from_table, group_by
- **Test Steps**:
  1. Create QueryBuilder
  2. Call group_by("status").having("COUNT(*)", ">", 10)
  3. Call build()
  4. Verify HAVING clause in SQL
- **Expected Result**: HAVING added
- **Coverage**: `QueryBuilder.having` method

### 2. INSERT Query Tests

#### TC-QB-016: QueryBuilder - insert
- **Purpose**: Verify INSERT query building
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call insert("users", name="John", email="john@example.com")
  3. Call build()
  4. Verify INSERT query and parameters
- **Expected Result**: INSERT query built, params contain values
- **Coverage**: `QueryBuilder.insert` method

#### TC-QB-017: QueryBuilder - insert с множеством полей
- **Purpose**: Verify INSERT with multiple fields
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call insert("users", name="John", email="john@example.com", age=30)
  3. Call build()
  4. Verify all fields in INSERT
- **Expected Result**: All fields in INSERT
- **Coverage**: `QueryBuilder.insert` method - multiple fields

### 3. UPDATE Query Tests

#### TC-QB-018: QueryBuilder - update
- **Purpose**: Verify UPDATE query building
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call update("users", name="Jane").where("id", "=", 1)
  3. Call build()
  4. Verify UPDATE query and parameters
- **Expected Result**: UPDATE query built, SET and WHERE clauses correct
- **Coverage**: `QueryBuilder.update` method

#### TC-QB-019: QueryBuilder - update без WHERE
- **Purpose**: Verify UPDATE without WHERE (allowed but dangerous)
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call update("users", name="Jane")
  3. Call build()
  4. Verify UPDATE query without WHERE
- **Expected Result**: UPDATE without WHERE (allowed)
- **Coverage**: `QueryBuilder.update` method - no WHERE

#### TC-QB-020: QueryBuilder - update с множеством полей
- **Purpose**: Verify UPDATE with multiple fields
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call update("users", name="Jane", email="jane@example.com").where("id", "=", 1)
  3. Call build()
  4. Verify all fields in SET
- **Expected Result**: All fields in SET clause
- **Coverage**: `QueryBuilder.update` method - multiple fields

### 4. DELETE Query Tests

#### TC-QB-021: QueryBuilder - delete
- **Purpose**: Verify DELETE query building
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call delete("users").where("id", "=", 1)
  3. Call build()
  4. Verify DELETE query and parameters
- **Expected Result**: DELETE query built, WHERE clause correct
- **Coverage**: `QueryBuilder.delete` method

#### TC-QB-022: QueryBuilder - delete без WHERE
- **Purpose**: Verify DELETE without WHERE (allowed but dangerous)
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Call delete("users")
  3. Call build()
  4. Verify DELETE query without WHERE
- **Expected Result**: DELETE without WHERE (allowed)
- **Coverage**: `QueryBuilder.delete` method - no WHERE

### 5. Error Handling Tests

#### TC-QB-023: QueryBuilder - build без query_type
- **Purpose**: Verify error when build called without query type
- **Preconditions**: Empty QueryBuilder
- **Test Steps**:
  1. Create QueryBuilder
  2. Call build()
  3. Verify ValueError raised
- **Expected Result**: ValueError: "Query type not set"
- **Coverage**: `QueryBuilder.build` method - validation

#### TC-QB-024: QueryBuilder - build без table
- **Purpose**: Verify error when build called without table
- **Preconditions**: QueryBuilder with select
- **Test Steps**:
  1. Create QueryBuilder
  2. Call select("*")
  3. Call build()
  4. Verify ValueError raised
- **Expected Result**: ValueError: "Table name not set"
- **Coverage**: `QueryBuilder.build` method - validation

### 6. Utility Methods Tests

#### TC-QB-025: QueryBuilder - reset
- **Purpose**: Verify builder reset
- **Preconditions**: QueryBuilder with query
- **Test Steps**:
  1. Create QueryBuilder with query
  2. Call reset()
  3. Verify builder is empty
- **Expected Result**: Builder reset to initial state
- **Coverage**: `QueryBuilder.reset` method

#### TC-QB-026: QueryBuilder - method chaining
- **Purpose**: Verify method chaining works
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Chain: select("*").from_table("users").where("active", "=", True).order_by("name")
  3. Call build()
  4. Verify query built correctly
- **Expected Result**: All methods chained, query built
- **Coverage**: Method chaining support

#### TC-QB-027: QueryBuilder - параметры в build
- **Purpose**: Verify parameters returned in build
- **Preconditions**: QueryBuilder with where
- **Test Steps**:
  1. Create QueryBuilder
  2. Call where("id", "=", 1)
  3. Call build()
  4. Verify parameters dict contains {"where_0": 1}
- **Expected Result**: Parameters returned correctly
- **Coverage**: `QueryBuilder.build` method - parameters

#### TC-QB-028: QueryBuilder - сложный запрос
- **Purpose**: Verify complex query building
- **Preconditions**: QueryBuilder instance
- **Test Steps**:
  1. Create QueryBuilder
  2. Build: SELECT with JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET
  3. Call build()
  4. Verify all clauses in correct order
- **Expected Result**: Complex query built correctly
- **Coverage**: Complex query building

