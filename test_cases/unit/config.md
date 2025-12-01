# Config Class - Unit Test Cases

## Overview
Tests for `py_web_automation.config.Config` class - configuration management for web automation testing framework.

## Test Categories

### 1. Initialization Tests

#### TC-CONFIG-001: Create Config with valid parameters
- **Purpose**: Verify Config can be created with all valid parameters
- **Preconditions**: Valid configuration data
- **Test Steps**:
  1. Create Config with all optional parameters
  2. Verify all attributes are set correctly
- **Expected Result**: Config object created successfully with all attributes set
- **Coverage**: `__init__`, `__post_init__`

#### TC-CONFIG-002: Create Config with minimal parameters (defaults)
- **Purpose**: Verify Config can be created with no parameters (all defaults)
- **Preconditions**: None
- **Test Steps**:
  1. Create Config with no parameters
  2. Verify default values are applied
- **Expected Result**: Config created with defaults (timeout=30, retry_count=3, retry_delay=1.0, log_level="INFO", browser_headless=True, browser_timeout=30000)
- **Coverage**: Default parameter values

#### TC-CONFIG-003: Create Config with base_url
- **Purpose**: Verify Config accepts base_url
- **Preconditions**: Valid base_url
- **Test Steps**:
  1. Create Config with base_url
  2. Verify base_url is set
- **Expected Result**: Config created with base_url
- **Coverage**: base_url parameter

### 2. Validation Tests

#### TC-CONFIG-004: Reject Config with invalid timeout (too low)
- **Purpose**: Verify validation rejects timeout < 1
- **Preconditions**: timeout = 0
- **Test Steps**:
  1. Attempt to create Config with timeout = 0
- **Expected Result**: ValueError raised: "timeout must be between 1 and 300 seconds"
- **Coverage**: `__post_init__` timeout validation (lower bound)

#### TC-CONFIG-005: Reject Config with invalid timeout (too high)
- **Purpose**: Verify validation rejects timeout > 300
- **Preconditions**: timeout = 301
- **Test Steps**:
  1. Attempt to create Config with timeout = 301
- **Expected Result**: ValueError raised: "timeout must be between 1 and 300 seconds"
- **Coverage**: `__post_init__` timeout validation (upper bound)

#### TC-CONFIG-006: Accept Config with valid timeout boundaries
- **Purpose**: Verify validation accepts boundary timeout values
- **Preconditions**: timeout = 1, timeout = 300
- **Test Steps**:
  1. Create Config with timeout = 1
  2. Create Config with timeout = 300
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` timeout validation (boundaries)

#### TC-CONFIG-007: Reject Config with invalid retry_count (too low)
- **Purpose**: Verify validation rejects retry_count < 0
- **Preconditions**: retry_count = -1
- **Test Steps**:
  1. Attempt to create Config with retry_count = -1
- **Expected Result**: ValueError raised: "retry_count must be between 0 and 10"
- **Coverage**: `__post_init__` retry_count validation (lower bound)

#### TC-CONFIG-008: Reject Config with invalid retry_count (too high)
- **Purpose**: Verify validation rejects retry_count > 10
- **Preconditions**: retry_count = 11
- **Test Steps**:
  1. Attempt to create Config with retry_count = 11
- **Expected Result**: ValueError raised: "retry_count must be between 0 and 10"
- **Coverage**: `__post_init__` retry_count validation (upper bound)

#### TC-CONFIG-009: Accept Config with valid retry_count boundaries
- **Purpose**: Verify validation accepts boundary retry_count values
- **Preconditions**: retry_count = 0, retry_count = 10
- **Test Steps**:
  1. Create Config with retry_count = 0
  2. Create Config with retry_count = 10
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` retry_count validation (boundaries)

#### TC-CONFIG-010: Reject Config with invalid retry_delay (too low)
- **Purpose**: Verify validation rejects retry_delay < 0.1
- **Preconditions**: retry_delay = 0.05
- **Test Steps**:
  1. Attempt to create Config with retry_delay = 0.05
- **Expected Result**: ValueError raised: "retry_delay must be between 0.1 and 10.0 seconds"
- **Coverage**: `__post_init__` retry_delay validation (lower bound)

#### TC-CONFIG-011: Reject Config with invalid retry_delay (too high)
- **Purpose**: Verify validation rejects retry_delay > 10.0
- **Preconditions**: retry_delay = 10.1
- **Test Steps**:
  1. Attempt to create Config with retry_delay = 10.1
- **Expected Result**: ValueError raised: "retry_delay must be between 0.1 and 10.0 seconds"
- **Coverage**: `__post_init__` retry_delay validation (upper bound)

#### TC-CONFIG-012: Accept Config with valid retry_delay boundaries
- **Purpose**: Verify validation accepts boundary retry_delay values
- **Preconditions**: retry_delay = 0.1, retry_delay = 10.0
- **Test Steps**:
  1. Create Config with retry_delay = 0.1
  2. Create Config with retry_delay = 10.0
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` retry_delay validation (boundaries)

#### TC-CONFIG-013: Reject Config with invalid browser_timeout (too low)
- **Purpose**: Verify validation rejects browser_timeout < 1000
- **Preconditions**: browser_timeout = 999
- **Test Steps**:
  1. Attempt to create Config with browser_timeout = 999
- **Expected Result**: ValueError raised: "browser_timeout must be between 1000 and 300000 milliseconds"
- **Coverage**: `__post_init__` browser_timeout validation (lower bound)

#### TC-CONFIG-014: Reject Config with invalid browser_timeout (too high)
- **Purpose**: Verify validation rejects browser_timeout > 300000
- **Preconditions**: browser_timeout = 300001
- **Test Steps**:
  1. Attempt to create Config with browser_timeout = 300001
- **Expected Result**: ValueError raised: "browser_timeout must be between 1000 and 300000 milliseconds"
- **Coverage**: `__post_init__` browser_timeout validation (upper bound)

#### TC-CONFIG-015: Accept Config with valid browser_timeout boundaries
- **Purpose**: Verify validation accepts boundary browser_timeout values
- **Preconditions**: browser_timeout = 1000, browser_timeout = 300000
- **Test Steps**:
  1. Create Config with browser_timeout = 1000
  2. Create Config with browser_timeout = 300000
- **Expected Result**: Both Configs created successfully
- **Coverage**: `__post_init__` browser_timeout validation (boundaries)

#### TC-CONFIG-016: Reject Config with invalid log_level
- **Purpose**: Verify validation rejects invalid log_level
- **Preconditions**: log_level = "INVALID"
- **Test Steps**:
  1. Attempt to create Config with log_level = "INVALID"
- **Expected Result**: ValueError raised: "Invalid log level: INVALID. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
- **Coverage**: `__post_init__` log_level validation

#### TC-CONFIG-017: Accept Config with all valid log_levels
- **Purpose**: Verify validation accepts all valid log_level values
- **Preconditions**: log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
- **Test Steps**:
  1. Create Config with each valid log_level
- **Expected Result**: All Configs created successfully
- **Coverage**: `__post_init__` log_level validation (all values)

### 3. from_env() Tests

#### TC-CONFIG-018: Create Config from environment variables
- **Purpose**: Verify Config.from_env() reads from environment
- **Preconditions**: Environment variables set (WA_BASE_URL, WA_TIMEOUT, etc.)
- **Test Steps**:
  1. Set environment variables
  2. Call Config.from_env()
  3. Verify Config created with correct values
- **Expected Result**: Config created from environment variables
- **Coverage**: `from_env()` method

#### TC-CONFIG-019: Create Config from_env with all optional variables
- **Purpose**: Verify from_env() reads all optional environment variables
- **Preconditions**: All WA_* environment variables set
- **Test Steps**:
  1. Set all environment variables
  2. Call Config.from_env()
  3. Verify all values are read correctly
- **Expected Result**: Config created with all optional values from environment
- **Coverage**: `from_env()` with all parameters

#### TC-CONFIG-020: Create Config from_env with defaults
- **Purpose**: Verify from_env() uses defaults for missing optional variables
- **Preconditions**: No environment variables set
- **Test Steps**:
  1. Unset all WA_* environment variables
  2. Call Config.from_env()
  3. Verify defaults are used
- **Expected Result**: Config created with default values for optional parameters
- **Coverage**: `from_env()` default values

#### TC-CONFIG-021: Reject from_env() with invalid WA_TIMEOUT type
- **Purpose**: Verify from_env() fails when WA_TIMEOUT cannot be converted to int
- **Preconditions**: WA_TIMEOUT = "invalid"
- **Test Steps**:
  1. Set WA_TIMEOUT = "invalid"
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "WA_TIMEOUT must be a valid integer: ..."
- **Coverage**: `from_env()` type conversion

#### TC-CONFIG-022: Reject from_env() with invalid WA_RETRY_COUNT type
- **Purpose**: Verify from_env() fails when WA_RETRY_COUNT cannot be converted to int
- **Preconditions**: WA_RETRY_COUNT = "invalid"
- **Test Steps**:
  1. Set WA_RETRY_COUNT = "invalid"
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "WA_RETRY_COUNT must be a valid integer: ..."
- **Coverage**: `from_env()` type conversion

#### TC-CONFIG-023: Reject from_env() with invalid WA_RETRY_DELAY type
- **Purpose**: Verify from_env() fails when WA_RETRY_DELAY cannot be converted to float
- **Preconditions**: WA_RETRY_DELAY = "invalid"
- **Test Steps**:
  1. Set WA_RETRY_DELAY = "invalid"
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "WA_RETRY_DELAY must be a valid float: ..."
- **Coverage**: `from_env()` type conversion

#### TC-CONFIG-024: Reject from_env() with invalid WA_BROWSER_TIMEOUT type
- **Purpose**: Verify from_env() fails when WA_BROWSER_TIMEOUT cannot be converted to int
- **Preconditions**: WA_BROWSER_TIMEOUT = "invalid"
- **Test Steps**:
  1. Set WA_BROWSER_TIMEOUT = "invalid"
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "WA_BROWSER_TIMEOUT must be a valid integer: ..."
- **Coverage**: `from_env()` type conversion

#### TC-CONFIG-025: Reject from_env() with invalid WA_LOG_LEVEL
- **Purpose**: Verify from_env() fails when WA_LOG_LEVEL is invalid
- **Preconditions**: WA_LOG_LEVEL = "INVALID"
- **Test Steps**:
  1. Set WA_LOG_LEVEL = "INVALID"
  2. Call Config.from_env()
- **Expected Result**: ValueError raised: "Invalid log level: INVALID. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
- **Coverage**: `from_env()` log_level validation

#### TC-CONFIG-026: Verify from_env() handles WA_BROWSER_HEADLESS correctly
- **Purpose**: Verify from_env() converts WA_BROWSER_HEADLESS to boolean
- **Preconditions**: WA_BROWSER_HEADLESS set to various values
- **Test Steps**:
  1. Set WA_BROWSER_HEADLESS = "true", verify browser_headless = True
  2. Set WA_BROWSER_HEADLESS = "false", verify browser_headless = False
  3. Set WA_BROWSER_HEADLESS = "1", verify browser_headless = True
  4. Set WA_BROWSER_HEADLESS = "0", verify browser_headless = False
- **Expected Result**: browser_headless converted correctly from string
- **Coverage**: `from_env()` browser_headless conversion

### 4. from_yaml() Tests

#### TC-CONFIG-027: Create Config from valid YAML file
- **Purpose**: Verify Config.from_yaml() reads from YAML file
- **Preconditions**: Valid YAML file exists
- **Test Steps**:
  1. Create valid YAML file with config data
  2. Call Config.from_yaml(file_path)
  3. Verify Config created with correct values
- **Expected Result**: Config created from YAML file
- **Coverage**: `from_yaml()` method

#### TC-CONFIG-028: Create Config from_yaml with all parameters
- **Purpose**: Verify from_yaml() reads all parameters from YAML
- **Preconditions**: YAML file with all config parameters
- **Test Steps**:
  1. Create YAML with all parameters
  2. Call Config.from_yaml()
  3. Verify all values are read
- **Expected Result**: Config created with all parameters from YAML
- **Coverage**: `from_yaml()` with all parameters

#### TC-CONFIG-029: Create Config from_yaml with minimal parameters
- **Purpose**: Verify from_yaml() works with minimal YAML
- **Preconditions**: YAML file with only some parameters
- **Test Steps**:
  1. Create minimal YAML
  2. Call Config.from_yaml()
  3. Verify defaults are applied
- **Expected Result**: Config created with defaults for missing parameters
- **Coverage**: `from_yaml()` with defaults

#### TC-CONFIG-030: Reject from_yaml() with invalid file path
- **Purpose**: Verify from_yaml() fails with non-existent file
- **Preconditions**: File does not exist
- **Test Steps**:
  1. Call Config.from_yaml("nonexistent.yaml")
- **Expected Result**: FileNotFoundError or similar exception
- **Coverage**: `from_yaml()` error handling

#### TC-CONFIG-031: Reject from_yaml() with invalid YAML format
- **Purpose**: Verify from_yaml() fails with malformed YAML
- **Preconditions**: Invalid YAML file exists
- **Test Steps**:
  1. Create file with invalid YAML syntax
  2. Call Config.from_yaml()
- **Expected Result**: YAML parsing error
- **Coverage**: `from_yaml()` error handling

#### TC-CONFIG-032: Reject from_yaml() with invalid data
- **Purpose**: Verify from_yaml() fails when YAML data doesn't pass validation
- **Preconditions**: YAML file with invalid config values
- **Test Steps**:
  1. Create YAML with invalid timeout
  2. Call Config.from_yaml()
- **Expected Result**: ValueError raised in __post_init__
- **Coverage**: `from_yaml()` validation

#### TC-CONFIG-033: Reject from_yaml() with non-dict YAML
- **Purpose**: Verify from_yaml() fails when YAML is not a dictionary
- **Preconditions**: YAML file with list or string
- **Test Steps**:
  1. Create YAML file with list or string
  2. Call Config.from_yaml()
- **Expected Result**: ValueError raised: "YAML file must contain a dictionary"
- **Coverage**: `from_yaml()` validation

#### TC-CONFIG-YAML-001: Reject from_yaml() with missing PyYAML
- **Purpose**: Verify from_yaml() fails when PyYAML is not installed
- **Preconditions**: PyYAML library not installed
- **Test Steps**:
  1. Mock import to raise ImportError for yaml module
  2. Call Config.from_yaml("config.yaml")
- **Expected Result**: ImportError raised: "PyYAML is required for YAML config. Install it with: uv add pyyaml"
- **Coverage**: `from_yaml()` ImportError handling

#### TC-CONFIG-LOGGING-001: Fallback logging configuration with AttributeError
- **Purpose**: Verify fallback logging configuration when AttributeError occurs
- **Preconditions**: Logger handlers check raises AttributeError
- **Test Steps**:
  1. Mock logger._core.handlers to raise AttributeError
  2. Create Config instance
  3. Verify logger.remove() and logger.add() called (fallback path)
- **Expected Result**: Fallback logging configuration applied
- **Coverage**: `__post_init__` fallback logging (AttributeError)

#### TC-CONFIG-LOGGING-002: Fallback logging configuration with TypeError
- **Purpose**: Verify fallback logging configuration when TypeError occurs
- **Preconditions**: Logger handlers check raises TypeError
- **Test Steps**:
  1. Mock logger._core.handlers to raise TypeError
  2. Create Config instance
  3. Verify logger.remove() and logger.add() called (fallback path)
- **Expected Result**: Fallback logging configuration applied
- **Coverage**: `__post_init__` fallback logging (TypeError)

### 5. Immutability Tests

#### TC-CONFIG-034: Verify Config is frozen (immutable)
- **Purpose**: Verify Config objects cannot be modified after creation
- **Preconditions**: Valid Config object created
- **Test Steps**:
  1. Create Config
  2. Attempt to modify an attribute
- **Expected Result**: AttributeError raised: "immutable type: 'Config'"
- **Coverage**: Frozen struct behavior

#### TC-CONFIG-035: Verify Config can be used in sets/dicts
- **Purpose**: Verify Config is hashable (can be used as dict key)
- **Preconditions**: Two Config objects with same values
- **Test Steps**:
  1. Create two Config objects with identical values
  2. Verify hash(config1) == hash(config2)
  3. Use Config as dict key
- **Expected Result**: Config is hashable and can be used in sets/dicts
- **Coverage**: Hashable behavior

### 6. Edge Cases

#### TC-CONFIG-036: Create Config with None base_url
- **Purpose**: Verify Config accepts None for base_url
- **Preconditions**: base_url = None
- **Test Steps**:
  1. Create Config with base_url=None
- **Expected Result**: Config created successfully
- **Coverage**: Optional None handling

#### TC-CONFIG-037: Create Config with empty base_url
- **Purpose**: Verify Config accepts empty string for base_url
- **Preconditions**: base_url = ""
- **Test Steps**:
  1. Create Config with base_url=""
- **Expected Result**: Config created successfully
- **Coverage**: Empty string handling

#### TC-CONFIG-038: Create Config with special characters in base_url
- **Purpose**: Verify Config handles special characters
- **Preconditions**: base_url with unicode, special chars
- **Test Steps**:
  1. Create Config with unicode in base_url
  2. Create Config with special characters
- **Expected Result**: Configs created successfully
- **Coverage**: Special character handling
