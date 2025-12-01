# Quick Start Guide

Get up and running with the Web Automation Framework in just a few minutes.

## Basic Setup

### 1. Import the Framework

```python
import asyncio
from py_web_automation import ApiClient, UiClient, Config
```

### 2. Create Configuration

```python
# Using environment variables
config = Config.from_env()

# Or create manually
config = Config(
    timeout=30,
    retry_count=3,
    log_level="INFO"
)
```

### 3. API Testing Example

```python
async def test_api():
    config = Config(timeout=30)
    
    async with ApiClient("https://api.example.com", config) as api:
        # Test GET endpoint
        result = await api.make_request("/api/status", method="GET")
        print(f"Status: {result.status_code}")
        print(f"Success: {result.success}")

        # Test POST endpoint
        result = await api.make_request(
            "/api/data",
            method="POST",
            data={"key": "value"}
        )
        print(f"Response: {result.response_time:.3f}s")

asyncio.run(test_api())
```

## UI Testing

Test your web application's user interface:

```python
async def test_ui():
    config = Config(timeout=30)
    
    async with UiClient("https://example.com", config) as ui:
        # Setup browser and navigate
        await ui.setup_browser()
        await ui.page.goto("https://example.com", wait_until="networkidle")

        # Basic interactions
        await ui.fill_input("#username", "test_user")
        await ui.click_element("#submit-button")

        # Take screenshot
        await ui.take_screenshot("test_result.png")

        # Get page information
        title = await ui.get_page_title()
        url = await ui.get_page_url()
        print(f"Page: {title} - {url}")

asyncio.run(test_ui())
```

## Complete Example

Here's a complete example that combines API and UI testing:

```python
import asyncio
from py_web_automation import ApiClient, UiClient, Config

async def complete_example():
    # Setup
    config = Config(timeout=30, log_level="INFO")

    # API Testing
    print("\n=== API Testing ===")
    async with ApiClient("https://api.example.com", config) as api:
        result = await api.make_request("/api/health", method="GET")
        print(f"Health check: {'✅ OK' if result.success else '❌ FAILED'}")

    # UI Testing
    print("\n=== UI Testing ===")
    async with UiClient("https://example.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://example.com", wait_until="networkidle")

        # Test form interaction
        await ui.fill_input("#email", "test@example.com")
        await ui.click_element("#submit")
        await ui.take_screenshot("form_test.png")

        print("UI test completed")

    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(complete_example())
```

## Environment Variables

Set up your environment variables (optional):

```bash
# Optional configuration
export WEB_AUTOMATION_TIMEOUT="30"
export WEB_AUTOMATION_RETRY_COUNT="3"
export WEB_AUTOMATION_LOG_LEVEL="INFO"
export WEB_AUTOMATION_BROWSER_HEADLESS="true"
```

## Next Steps

1. **Explore Examples**: Check out the `examples/` directory for more detailed examples
2. **Read API Reference**: See [API Reference](api-reference.md) for complete method documentation
3. **Configuration**: Learn about all configuration options in [Configuration Guide](installation.md)
4. **Advanced Usage**: Discover advanced patterns in [Examples](examples.md)

## Common Patterns

### Error Handling

```python
async def robust_testing():
    config = Config.from_env()

    try:
        async with ApiClient("https://api.example.com", config) as api:
            result = await api.make_request("/api/test", method="GET")

            if result.success:
                print("✅ API test passed")
            else:
                print(f"❌ API test failed: {result.error_message}")

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
```

### Retry Logic

```python
async def retry_test():
    config = Config.from_env()

    for attempt in range(3):
        try:
            async with ApiClient("https://api.example.com", config) as api:
                result = await api.make_request("/api/test", method="GET")
                if result.success:
                    print("✅ Test passed")
                    break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                await asyncio.sleep(1)
```

### Context Managers

Always use context managers for proper resource cleanup:

```python
# ✅ Good
async with ApiClient(url, config) as api:
    result = await api.make_request("/api/test", method="GET")

# ❌ Avoid
api = ApiClient(url, config)
result = await api.make_request("/api/test", method="GET")
# Don't forget to call await api.close()
```

## Tips

1. **Use async/await**: All framework methods are async
2. **Context managers**: Use `async with` for automatic cleanup
3. **Error handling**: Always handle exceptions in your tests
4. **Logging**: Use the built-in logging for debugging
5. **Screenshots**: Take screenshots for visual verification
6. **Timeouts**: Set appropriate timeouts for your tests

Ready to dive deeper? Check out the [Examples](examples.md) for more advanced use cases!
