# Troubleshooting

This guide helps you resolve common issues when using the Web Automation Framework.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [API Testing Issues](#api-testing-issues)
- [UI Testing Issues](#ui-testing-issues)
- [Database Issues](#database-issues)
- [Performance Issues](#performance-issues)
- [Browser Issues](#browser-issues)
- [Testing Issues](#testing-issues)
- [Common Error Messages](#common-error-messages)
- [Debugging Tips](#debugging-tips)

## Installation Issues

### Python Version Compatibility

**Problem**: Framework doesn't work with Python version

**Solution**: Ensure you're using Python 3.13

```bash
# Check Python version
python --version

# If using older version, upgrade Python
# On Windows: Download from python.org
# On macOS: brew install python@3.13
# On Linux: sudo apt install python3.13
```

### Dependency Installation Failures

**Problem**: `uv sync` or `pip install` fails

**Solutions**:

1. **Update package managers**:
   ```bash
   # Update uv
   uv self update

   # Update pip
   pip install --upgrade pip
   ```

2. **Clear cache**:
   ```bash
   # Clear uv cache
   uv cache clean

   # Clear pip cache
   pip cache purge
   ```

3. **Install with verbose output**:
   ```bash
   uv sync --verbose
   # or
   pip install -e . -v
   ```

### Playwright Browser Installation

**Problem**: Playwright browsers fail to install

**Solutions**:

1. **Install browsers manually**:
   ```bash
   uv run playwright install chromium
   uv run playwright install firefox
   uv run playwright install webkit
   ```

2. **Install with system dependencies**:
   ```bash
   uv run playwright install --with-deps
   ```

3. **Check system requirements**:
   - Windows: Visual Studio Build Tools
   - macOS: Xcode Command Line Tools
   - Linux: Build essentials

## Configuration Problems

### Configuration Validation Errors

**Problem**: `ConfigurationError` or validation errors

**Solutions**:

1. **Check configuration values**:
   ```python
   from py_web_automation import Config

   # Valid configuration
   config = Config(
       timeout=30,  # Must be between 1 and 300
       retry_count=3,  # Must be between 0 and 10
       retry_delay=1.0,  # Must be between 0.1 and 10.0
       log_level="INFO"  # Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL
   )
   ```

2. **Use environment variables**:
   ```bash
   export WEB_AUTOMATION_TIMEOUT="30"
   export WEB_AUTOMATION_RETRY_COUNT="3"
   export WEB_AUTOMATION_LOG_LEVEL="INFO"
   ```

3. **Load from YAML**:
   ```python
   config = Config.from_yaml("config.yaml")
   ```

### Environment Variable Loading

**Problem**: Environment variables not loaded

**Solutions**:

1. **Use .env file**:
   ```bash
   # Create .env file
   echo "WEB_AUTOMATION_TIMEOUT=30" > .env
   echo "WEB_AUTOMATION_RETRY_COUNT=3" >> .env
   echo "WEB_AUTOMATION_LOG_LEVEL=INFO" >> .env
   ```

2. **Load manually**:
   ```python
   import os
   from dotenv import load_dotenv
   from py_web_automation import Config

   load_dotenv()
   config = Config.from_env()
   ```

## API Testing Issues

### Connection Errors

**Problem**: `ConnectionError` when making API requests

**Solutions**:

1. **Check network connectivity**:
   ```python
   import httpx

   async def test_connection(url):
       async with httpx.AsyncClient() as client:
           try:
               response = await client.get(url, timeout=10.0)
               print(f"Status: {response.status_code}")
           except Exception as e:
               print(f"Connection error: {e}")
   ```

2. **Verify URL format**:
   ```python
   # Correct URL format
   url = "https://api.example.com"  # With protocol
   # Not: "api.example.com" or "//api.example.com"
   ```

3. **Check firewall/proxy settings**:
   - Ensure firewall allows outbound connections
   - Configure proxy if needed

### Timeout Errors

**Problem**: `TimeoutError` during API requests

**Solutions**:

1. **Increase timeout**:
   ```python
   config = Config(timeout=60)  # Increase from default 30
   ```

2. **Check server response time**:
   ```python
   import time
   import httpx

   async def check_response_time(url):
       start = time.time()
       async with httpx.AsyncClient() as client:
           response = await client.get(url)
       elapsed = time.time() - start
       print(f"Response time: {elapsed:.2f}s")
   ```

3. **Implement retry logic**:
   ```python
   config = Config(timeout=30, retry_count=5, retry_delay=2.0)
   ```

### Authentication Errors

**Problem**: `AuthenticationError` or 401/403 responses

**Solutions**:

1. **Verify authentication token**:
   ```python
   # Check token format
   token = "Bearer your-token-here"  # Or just "your-token-here"
   headers = {"Authorization": f"Bearer {token}"}
   ```

2. **Test token manually**:
   ```python
   import httpx

   async def test_auth(url, token):
       async with httpx.AsyncClient() as client:
           response = await client.get(
               url,
               headers={"Authorization": f"Bearer {token}"}
           )
           print(f"Status: {response.status_code}")
   ```

3. **Check token expiration**:
   - Ensure token is not expired
   - Refresh token if needed

## UI Testing Issues

### Browser Not Starting

**Problem**: Browser fails to start or crashes

**Solutions**:

1. **Install Playwright browsers**:
   ```bash
   uv run playwright install chromium
   ```

2. **Check browser path**:
   ```python
   from playwright.async_api import async_playwright

   async def check_browser():
       async with async_playwright() as p:
           browser = await p.chromium.launch()
           print(f"Browser launched: {browser.version}")
   ```

3. **Run in headless mode**:
   ```python
   config = Config(browser_headless=True)
   ```

### Element Not Found

**Problem**: `NotFoundError` when trying to interact with elements

**Solutions**:

1. **Wait for element**:
   ```python
   await ui.wait_for_element("#element-id", timeout=10000)
   await ui.click_element("#element-id")
   ```

2. **Check selector**:
   ```python
   # Use browser DevTools to verify selector
   # Try different selectors:
   await ui.click_element("#id")
   await ui.click_element(".class")
   await ui.click_element("button[type='submit']")
   ```

3. **Take screenshot for debugging**:
   ```python
   await ui.take_screenshot("debug.png")
   ```

### Page Navigation Issues

**Problem**: Page doesn't load or navigation fails

**Solutions**:

1. **Wait for network idle**:
   ```python
   await ui.page.goto(url, wait_until="networkidle")
   ```

2. **Increase timeout**:
   ```python
   config = Config(browser_timeout=60000)  # 60 seconds
   ```

3. **Handle redirects**:
   ```python
   await ui.page.goto(url, wait_until="domcontentloaded")
   await ui.wait_for_navigation(timeout=10000)
   ```

## Database Issues

### Connection Errors

**Problem**: Cannot connect to database

**Solutions**:

1. **Verify connection string**:
   ```python
   # PostgreSQL
   connection_string = "postgresql://user:pass@localhost:5432/dbname"
   
   # MySQL
   connection_string = "mysql://user:pass@localhost:3306/dbname"
   
   # SQLite
   connection_string = "sqlite:///path/to/database.db"
   ```

2. **Check database server**:
   - Ensure database server is running
   - Verify network connectivity
   - Check firewall rules

3. **Test connection manually**:
   ```python
   import asyncpg  # For PostgreSQL

   async def test_connection():
       try:
           conn = await asyncpg.connect("postgresql://user:pass@localhost/db")
           print("Connection successful")
           await conn.close()
       except Exception as e:
           print(f"Connection failed: {e}")
   ```

### Query Errors

**Problem**: SQL queries fail or return unexpected results

**Solutions**:

1. **Use parameterized queries**:
   ```python
   # Good: Parameterized
   await db.execute_query(
       "SELECT * FROM users WHERE id = :id",
       {"id": 1}
   )
   
   # Bad: String formatting (SQL injection risk)
   await db.execute_query(f"SELECT * FROM users WHERE id = {user_id}")
   ```

2. **Check query syntax**:
   - Verify SQL syntax for your database type
   - Test queries in database client first

3. **Handle transactions properly**:
   ```python
   async with db.transaction():
       await db.execute_command("INSERT INTO users ...")
       await db.execute_command("UPDATE users ...")
   ```

## Performance Issues

### Slow API Requests

**Problem**: API requests are slow

**Solutions**:

1. **Use connection pooling**:
   ```python
   # Connection pooling is handled automatically by httpx
   # Reuse client instances
   async with ApiClient(url, config) as api:
       # Multiple requests reuse connection
       await api.make_request("/endpoint1")
       await api.make_request("/endpoint2")
   ```

2. **Parallel requests**:
   ```python
   import asyncio

   async def parallel_requests():
       tasks = [
           api.make_request("/endpoint1"),
           api.make_request("/endpoint2"),
           api.make_request("/endpoint3")
       ]
       results = await asyncio.gather(*tasks)
   ```

3. **Optimize timeouts**:
   ```python
   config = Config(timeout=10)  # Reduce if requests are fast
   ```

### Slow Browser Operations

**Problem**: Browser operations are slow

**Solutions**:

1. **Use headless mode**:
   ```python
   config = Config(browser_headless=True)
   ```

2. **Optimize wait conditions**:
   ```python
   # Use specific wait conditions
   await ui.page.goto(url, wait_until="domcontentloaded")  # Faster than networkidle
   ```

3. **Reduce screenshot size**:
   ```python
   await ui.page.screenshot(path="screenshot.png", full_page=False)
   ```

## Common Error Messages

### `'ApiClient' object has no attribute 'method_name'`

**Problem**: Method doesn't exist on client

**Solution**: Check API reference for correct method names

```python
# Correct usage
result = await api.make_request("/endpoint", method="GET")
```

### `ConnectionError: Failed to connect`

**Problem**: Cannot establish connection

**Solution**: Check network, URL, and firewall settings

### `TimeoutError: Operation exceeded timeout`

**Problem**: Operation took too long

**Solution**: Increase timeout or optimize operation

```python
config = Config(timeout=60)  # Increase timeout
```

### `ValidationError: Invalid configuration`

**Problem**: Configuration values are invalid

**Solution**: Check configuration values against allowed ranges

```python
# Valid ranges
timeout: 1-300
retry_count: 0-10
retry_delay: 0.1-10.0
log_level: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Debugging Tips

### Enable Debug Logging

```python
config = Config(log_level="DEBUG")
```

### Use Screenshots

```python
await ui.take_screenshot("debug.png")
```

### Check Response Details

```python
result = await api.make_request("/endpoint", method="GET")
print(f"Status: {result.status_code}")
print(f"Response: {result.response}")
print(f"Error: {result.error_message}")
```

### Test Components Individually

```python
# Test API separately
async with ApiClient(url, config) as api:
    result = await api.make_request("/test")

# Test UI separately
async with UiClient(url, config) as ui:
    await ui.setup_browser()
```

### Use Network Inspection

```python
# Enable network logging
async with ApiClient(url, config) as api:
    # Check network requests in logs
    result = await api.make_request("/endpoint")
```

## Getting Help

If you encounter issues not covered here:

1. Check the [Examples](examples.md) for working code
2. Review the [API Reference](api-reference.md) for method documentation
3. Check the [Architecture](architecture.md) for design decisions
4. Open an issue on the project repository with:
   - Error message
   - Code snippet
   - Configuration details
   - Python version
   - Framework version
