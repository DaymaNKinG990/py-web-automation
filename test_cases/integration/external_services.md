# External Services Integration Test Cases

## Overview
Tests for integration with external services: HTTP endpoints and browser automation.

## Test Categories

### 1. HTTP API Integration

#### TC-INTEGRATION-EXT-001: Test real HTTP endpoint
- **Purpose**: Verify HTTP requests to real endpoints
- **Preconditions**:
  - Real HTTP endpoint URL (use httpbin.org or local mock server)
  - Endpoint is accessible
- **Test Steps**:
  1. Create `ApiClient` with base URL from fixture or environment variable
     - Default: `http://httpbin.org` (or `http://localhost:8000` for local mock server)
     - Use `MOCK_SERVER_URL` environment variable if available for CI
  2. Call `make_request("/get")` to httpbin.org/get endpoint
  3. Verify response is received
  4. Verify response status code is 200
  5. Verify response data matches expected schema:
     ```json
     {
       "url": "http://httpbin.org/get",
       "headers": {...},
       "args": {}
     }
     ```
     - Verify `url` field exists and matches request URL
     - Verify `headers` field exists and is a dictionary
- **Expected Result**: Real HTTP request succeeds with status 200 and valid JSON response
- **Coverage**: Real HTTP integration
- **Dependencies**: Real HTTP endpoint (httpbin.org or mock server)
- **Notes**:
  - For CI/CD, use `MOCK_SERVER_URL` environment variable to point to a provided mock server fixture
  - Local development can use httpbin.org or start a local mock server on port 8000

#### TC-INTEGRATION-EXT-002: Test HTTPS endpoint
- **Purpose**: Verify HTTPS requests work correctly
- **Preconditions**: HTTPS endpoint with valid SSL certificate
- **Test Steps**:
  1. Create `ApiClient` with HTTPS URL: `https://httpbin.org`
  2. Call `make_request("/get")` to https://httpbin.org/get endpoint
  3. Verify SSL/TLS handshake succeeds
  4. Verify response is received with status code 200
  5. Verify response contains valid JSON data
- **Expected Result**: HTTPS request succeeds with status 200
- **Coverage**: HTTPS integration
- **Dependencies**: HTTPS endpoint (https://httpbin.org)
- **Notes**: Uses httpbin.org for testing SSL/TLS handshake

#### TC-INTEGRATION-EXT-003: Test HTTP endpoint with authentication
- **Purpose**: Verify authenticated HTTP requests
- **Preconditions**:
  - HTTP endpoint requiring authentication (use httpbin.org/bearer or mock server)
  - Valid auth token
- **Test Steps**:
  1. Create `ApiClient` with base URL: `https://httpbin.org`
  2. Set authentication token: `api.set_auth_token("test_token_12345abcdef")`
  3. Call `make_request("/bearer")` endpoint
  4. Verify authenticated request succeeds with status 200
  5. Verify response contains `authenticated: true` in JSON body
  6. Clear authentication: `api.clear_auth_token()`
  7. Try request without auth headers to `/bearer`
  8. Verify unauthenticated request returns status 401 or 403
- **Expected Result**:
  - Authenticated request succeeds (status 200, `authenticated: true`)
  - Unauthenticated request fails (status 401 or 403)
- **Coverage**: HTTP authentication
- **Dependencies**: Authenticated endpoint (httpbin.org/bearer or mock server with auth)
- **Notes**:
  - For CI/CD, use mock server fixture that supports Bearer token authentication
  - Token can be provided via `TEST_AUTH_TOKEN` environment variable

#### TC-INTEGRATION-EXT-004: Handle HTTP errors (4xx, 5xx)
- **Purpose**: Verify handling of HTTP error responses
- **Preconditions**: Endpoints that return specific error codes
- **Test Steps**:
  1. Create `ApiClient` with base URL: `https://httpbin.org`
  2. Call `make_request("/status/404")` to endpoint returning 404
  3. Verify ApiResult has:
     - `status_code = 404`
     - `client_error = True`
     - `success = False`
     - `server_error = False`
  4. Call `make_request("/status/500")` to endpoint returning 500
  5. Verify ApiResult has:
     - `status_code = 500`
     - `server_error = True`
     - `success = False`
     - `client_error = False`
  6. Optionally verify error response body structure
- **Expected Result**:
  - 404 error correctly identified as client_error (status 404, client_error=True)
  - 500 error correctly identified as server_error (status 500, server_error=True)
- **Coverage**: HTTP error handling
- **Dependencies**: Endpoints returning errors (httpbin.org/status/{code} or mock server)
- **Notes**: httpbin.org provides `/status/{code}` endpoints for testing various status codes

#### TC-INTEGRATION-EXT-005: Handle HTTP timeouts
- **Purpose**: Verify handling of HTTP timeouts
- **Preconditions**: Slow or unresponsive endpoint
- **Test Steps**:
  1. Create `ApiClient` with timeout set to 2 seconds
  2. Call `make_request("/delay/5")` to httpbin.org/delay/5 endpoint (which delays 5 seconds)
  3. Verify timeout is detected within 2-3 seconds
  4. Verify ApiResult indicates timeout:
     - `success = False`
     - `error_message` contains "timeout" or "timed out"
     - `status_code` may be None or 408 (Request Timeout)
- **Expected Result**: HTTP timeout detected correctly within specified timeout period (2 seconds)
- **Coverage**: HTTP timeout handling
- **Dependencies**: Slow endpoint (httpbin.org/delay/{seconds} or mock server with delay)
- **Notes**:
  - Timeout threshold: 2 seconds
  - For CI/CD, use mock server fixture with configurable delay endpoint
  - Alternative: use httpbin.org/delay/{seconds} where seconds > timeout value

### 2. Browser Automation Integration

**Note on Test Fixtures**: Browser integration tests use local HTML fixtures located in `tests/data/html_fixtures/` to ensure reproducibility and avoid fragile external dependencies. These fixtures are served via a local HTTP server or accessed via `file://` protocol. For production-like testing, stable external URLs (e.g., `https://example.com`, `https://httpbin.org/html`) can be used as fallback, but local fixtures are preferred for CI/CD environments.

#### TC-INTEGRATION-EXT-006: Launch real browser
- **Purpose**: Verify Playwright browser launches correctly
- **Preconditions**: Playwright installed
- **Test Steps**:
  1. Create `UiClient` with base URL
  2. Call `setup_browser()`
  3. Verify browser is launched
  4. Verify page is created
  5. Verify browser is accessible
- **Expected Result**: Browser launches successfully
- **Coverage**: Browser launch integration
- **Dependencies**: Playwright installation

#### TC-INTEGRATION-EXT-007: Navigate to real URL
- **Purpose**: Verify navigation to real web page
- **Preconditions**:
  - Test fixture URL or stable external URL (e.g., `file:///path/to/tests/data/html_fixtures/test_page.html` or `https://example.com`)
  - Browser setup
- **Test Steps**:
  1. Create `UiClient` with test URL: `file:///path/to/tests/data/html_fixtures/test_page.html` (or `https://example.com` as fallback)
  2. Setup browser using `setup_browser()`
  3. Navigate to URL explicitly using `navigate()`
  4. Wait for page load using `wait_for_element()` or page load state
  5. Verify page loads by checking page URL matches expected URL
  6. Verify page title using `get_page_title()` equals expected title
- **Expected Result**: Navigation to URL succeeds, page loads correctly
- **Coverage**: Real URL navigation
- **Dependencies**: Local HTML fixture at `tests/data/html_fixtures/test_page.html` or stable external URL
- **Test Fixture**: `tests/data/html_fixtures/test_page.html`

#### TC-INTEGRATION-EXT-008: Interact with real web page
- **Purpose**: Verify interaction with real web page elements
- **Preconditions**:
  - Test fixture URL: `file:///path/to/tests/data/html_fixtures/interactive_page.html` (or `https://httpbin.org/forms/post` as fallback)
  - Browser setup
- **Test Steps**:
  1. Navigate to test page: `file:///path/to/tests/data/html_fixtures/interactive_page.html`
  2. Wait for element `#test-input` using `wait_for_element("#test-input")`
  3. Fill input field using `fill_input("#test-input", "test value")`
  4. Click button using `click_element("#test-button")`
  5. Wait for output element `#output` to appear
  6. Verify interactions work by checking `#output` element text contains expected value
  7. Fill input again: `fill_input("#test-input", "form submission")`
  8. Click submit button: `click_element("#submit-button")`
  9. Verify output updated with submitted value
- **Expected Result**: Real page interactions work correctly
- **Coverage**: Real page interaction
- **Dependencies**: Local HTML fixture at `tests/data/html_fixtures/interactive_page.html` with elements:
  - `#test-input` - text input field
  - `#test-button` - clickable button
  - `#submit-button` - submit button
  - `#output` - output div element
- **Test Fixture**: `tests/data/html_fixtures/interactive_page.html`

#### TC-INTEGRATION-EXT-009: Handle browser errors
- **Purpose**: Verify handling of browser errors
- **Preconditions**:
  - Test fixture URL: `file:///path/to/tests/data/html_fixtures/error_page.html` (local fixture with intentional errors)
  - Browser setup
- **Test Steps**:
  1. Navigate to error test page: `file:///path/to/tests/data/html_fixtures/error_page.html`
  2. Wait for page load
  3. Verify JavaScript console errors are logged (check browser console)
  4. Try to interact with element `#error-button` using `click_element("#error-button")`
  5. Verify errors are caught and logged (check error logs)
  6. Verify test continues execution after error handling
  7. Verify page still accessible after errors
- **Expected Result**: Browser errors handled gracefully, errors logged, test continues
- **Coverage**: Browser error handling
- **Dependencies**: Local HTML fixture at `tests/data/html_fixtures/error_page.html` containing:
  - Intentional JavaScript errors (undefined function calls)
  - Missing resource references (404 errors)
  - Error button element `#error-button`
- **Test Fixture**: `tests/data/html_fixtures/error_page.html`

#### TC-INTEGRATION-EXT-010: Test browser with JavaScript disabled
- **Purpose**: Verify framework works without JavaScript
- **Preconditions**:
  - Test fixture URL: `file:///path/to/tests/data/html_fixtures/no_js_page.html` (page that works without JavaScript)
  - Browser setup with JavaScript disabled
- **Test Steps**:
  1. Setup browser context with JavaScript disabled using Playwright API
  2. Navigate to no-JS test page: `file:///path/to/tests/data/html_fixtures/no_js_page.html`
  3. Wait for page load
  4. Verify page loads (check page title)
  5. Fill input field using `fill_input("#test-input", "test without js")`
  6. Verify input value was set correctly
  7. Click submit button using `click_element("#test-button")`
  8. Verify form interaction works without JavaScript
- **Expected Result**: Works without JavaScript, basic interactions succeed
- **Coverage**: JavaScript independence
- **Dependencies**:
  - Local HTML fixture at `tests/data/html_fixtures/no_js_page.html` (pure HTML form, no JS required)
  - Playwright browser context with `js_enabled=False` parameter
- **Test Fixture**: `tests/data/html_fixtures/no_js_page.html`

### 3. Network Integration

#### TC-INTEGRATION-EXT-011: Handle network interruptions
- **Purpose**: Verify handling of network interruptions with retry mechanism
- **Preconditions**:
  - Network that can be interrupted
  - Docker installed (for network namespace control)
  - OR iptables available (Linux) / netsh (Windows)
  - OR pytest-httpx for HTTP client mocking
- **Test Steps**:
  1. Create `ApiClient` with test endpoint URL
  2. **Method A (Docker network namespace)**:
     - Start test container with network namespace
     - Create `ApiClient` inside container
     - Execute: `docker network disconnect bridge <container_id>` to interrupt
     - Attempt HTTP request via `make_request()`
     - Verify `ApiResult.error_message` contains network error
     - Execute: `docker network connect bridge <container_id>` to restore
     - Retry request within 5 seconds after restore
     - Verify request succeeds with `ApiResult.success=True`
  3. **Method B (iptables - Linux only)**:
     - Execute: `iptables -A OUTPUT -d <target_host> -j DROP` to block traffic
     - Attempt HTTP request via `make_request()`
     - Verify `ApiResult.error_message` contains network error
     - Execute: `iptables -D OUTPUT -d <target_host> -j DROP` to restore
     - Retry request within 5 seconds after restore
     - Verify request succeeds
  4. **Method C (pytest-httpx mock)**:
     - Use `httpx_mock` fixture to simulate `httpx.ConnectError` or `httpx.NetworkError`
     - Attempt HTTP request via `make_request()`
     - Verify `ApiResult.error_message` contains network error
     - Configure mock to return successful response on retry
     - Retry request (if framework implements automatic retry)
     - Verify request succeeds
- **Expected Result**: Network interruptions detected, logged, and retry succeeds after restoration
- **Coverage**: Network error handling and retry mechanism
- **Dependencies**: Docker OR iptables (Linux) OR pytest-httpx

#### TC-INTEGRATION-EXT-012: Test with proxy
- **Purpose**: Verify framework works with HTTP/HTTPS proxy server
- **Preconditions**:
  - Proxy server available (Squid or mitmproxy)
  - Proxy accessible from test environment
- **Test Steps**:
  1. Start proxy server (Squid or mitmproxy)
  2. Configure proxy in httpx client (if supported)
  3. Create `ApiClient` with proxy configuration
  4. Make HTTP request via `make_request("/api/status")`
  5. Verify request routed through proxy (check proxy logs or headers)
  6. Verify response received successfully
  7. Test with authentication (if proxy requires auth)
- **Expected Result**: Proxy integration works correctly, requests routed through proxy, responses received
- **Coverage**: Proxy support for HTTP/HTTPS requests
- **Dependencies**: Squid proxy server OR mitmproxy, Docker (optional for containerized Squid)

#### TC-INTEGRATION-EXT-013: Test with different network conditions
- **Purpose**: Verify framework behavior under various network conditions (bandwidth, latency, packet loss)
- **Preconditions**: Network throttling tool available
- **Test Steps**:
  1. **Baseline (Fast Network)**:
     - Make HTTP request via `make_request("/api/status")`
     - Measure `ApiResult.response_time`
     - Verify request completes within 2 seconds
  2. **Apply network throttling** (using tc, Docker+netem, or Playwright)
  3. **Test each profile**:
     - **Slow 3G**: Request completes within 10 seconds OR triggers timeout/retry
     - **Fast 3G**: Request completes within 5 seconds
     - **High Latency (500ms)**: Request completes within 3 seconds
     - **Packet Loss (5%)**: Request may require retry, completes within retry attempts
  4. Verify response times recorded in `ApiResult.response_time` reflect network conditions
- **Expected Result**: Framework handles various network conditions correctly, with appropriate timeouts and retries
- **Coverage**: Network condition handling, timeout behavior, retry logic
- **Dependencies**: Playwright OR tc+iproute2 (Linux) OR Docker+netem

### 4. Security Integration

#### TC-INTEGRATION-EXT-014: Verify SSL certificate validation
- **Purpose**: Verify SSL certificate validation works with various certificate scenarios
- **Preconditions**:
  - HTTPS test server capability (e.g., local test server with certificate control)
  - Certificate fixtures prepared
- **Test Steps**:
  1. Create `ApiClient` with default SSL validation enabled
  2. Make request to HTTPS endpoint with **valid certificate** (baseline)
     - Verify request succeeds, status 200, no SSL errors
  3. Make request to endpoint with **self-signed certificate**
     - Verify connection rejected with SSL certificate verification error
  4. Make request to endpoint with **expired certificate**
     - Verify connection rejected with certificate expiration error
  5. Make request to endpoint with **hostname mismatch certificate**
     - Verify connection rejected with hostname verification error
  6. (Optional) Test with SSL validation disabled
     - Verify all requests succeed regardless of certificate validity (security test)
- **Expected Result**:
  - Valid certificates accepted
  - Invalid certificates (self-signed, expired, hostname mismatch) rejected with appropriate error codes
  - Error messages clearly indicate certificate validation failure reason
- **Coverage**: SSL/TLS security with comprehensive certificate validation scenarios
- **Dependencies**: HTTPS test server with certificate fixture control

#### TC-INTEGRATION-EXT-015: Test with different user agents
- **Purpose**: Verify user agent handling with explicit verification methods
- **Preconditions**:
  - Browser setup (Playwright)
  - Test page/server that can verify user agent
- **Test Steps**:
  1. Setup browser with custom user agent string (e.g., `"CustomTestAgent/1.0"`)
  2. Navigate to test page that verifies user agent
  3. **Verify user agent is set correctly (server-side)**:
     - Check server logs or make request to endpoint that returns User-Agent header
     - Verify HTTP request header `User-Agent` equals configured value
  4. **Verify user agent is set correctly (client-side)**:
     - Execute JavaScript in page context: `user_agent = await page.evaluate("() => navigator.userAgent")`
     - Verify `navigator.userAgent` equals configured value
  5. **Verify page responds to user agent**:
     - Verify page loads successfully
     - Verify page content/behavior matches expected response for given user agent
- **Expected Result**:
  - User agent is correctly set in HTTP request headers
  - `navigator.userAgent` in browser context matches configured value
  - Page/server correctly receives and responds to user agent
- **Coverage**: User agent support with explicit verification across server, client, and network layers
- **Dependencies**: Test page/server with user agent verification capability

### 5. Performance Integration

#### TC-INTEGRATION-EXT-016: Measure API response times
- **Purpose**: Verify API response time measurement with concrete performance criteria
- **Preconditions**:
  - API endpoint accessible and stable
  - Network conditions are consistent
- **Test Steps**:
  1. Create `ApiClient` with target endpoint
  2. Execute 100 sequential HTTP requests to the same endpoint
  3. For each request, capture response time from `ApiResult.response_time`
  4. Calculate statistics from all 100 measurements:
     - Mean (arithmetic average)
     - Median (50th percentile)
     - 95th percentile (p95)
     - 99th percentile (p99)
  5. Verify all times are recorded in ApiResult objects
  6. Evaluate performance budget:
     - Pass if: p95 < 500ms AND mean < 300ms
     - Fail if: p95 >= 500ms OR mean >= 300ms
- **Expected Result**:
  - All 100 requests complete successfully
  - Response times are measured and recorded
  - Performance budget is met (p95 < 500ms and mean < 300ms)
- **Coverage**: Performance measurement with deterministic criteria
- **Dependencies**: Stable API endpoint

#### TC-INTEGRATION-EXT-017: Measure page load times
- **Purpose**: Verify page load time measurement with concrete performance criteria
- **Preconditions**:
  - Web page URL accessible and stable
  - Browser environment is consistent
  - Network conditions are stable
- **Test Steps**:
  1. Setup browser (fresh instance for each run)
  2. Execute 10 navigation runs:
     - For each run:
       - Start timer before `navigate()` call
       - Wait for page load complete using Playwright's `page.wait_for_load_state("networkidle")`
       - Stop timer after load state is reached
       - Record elapsed time
       - Close browser instance
  3. Calculate statistics from all 10 measurements:
     - Median (50th percentile)
     - Mean (arithmetic average)
     - Standard deviation
     - Coefficient of variation (CV) = (standard_deviation / mean) * 100%
  4. Evaluate acceptance criteria:
     - Pass if: median < 2.0s AND coefficient_of_variation < 10%
     - Fail if: median >= 2.0s OR coefficient_of_variation >= 10%
- **Expected Result**:
  - All 10 navigation runs complete successfully
  - Load times are measured consistently
  - Performance criteria are met (median < 2s and CV < 10%)
- **Coverage**: Page load performance with deterministic criteria
- **Dependencies**: Stable web page and consistent browser environment

### 6. Compatibility Integration

#### TC-INTEGRATION-EXT-018: Test with different browsers
- **Purpose**: Verify framework works correctly across different browser engines
- **Preconditions**:
  - Playwright installed with all browsers: `uv run playwright install chromium firefox webkit`
  - Test fixtures available: `tests/data/html_fixtures/test_page.html`, `tests/data/html_fixtures/interactive_page.html`
- **Test Steps**:
  1. **For Chromium**:
     - Configure Playwright to use Chromium
     - Execute browser automation test cases
     - Record results
  2. **For Firefox**:
     - Configure Playwright to use Firefox
     - Execute the same test cases
     - Record results
  3. **For WebKit**:
     - Configure Playwright to use WebKit
     - Execute the same test cases
     - Record results
  4. **Compare Results**:
     - Create comparison matrix: Browser × Test Case × Result
     - Verify all test steps pass on each browser
     - Compare execution times across browsers
- **Expected Result**:
  - All test executions pass on all browsers
  - Framework functionality is consistent across all browser engines
  - Results comparison matrix shows identical behavior across browsers
- **Coverage**: Browser compatibility across Chromium, Firefox, and WebKit engines
- **Dependencies**:
  - Playwright with all browsers installed
  - Test fixtures in `tests/data/html_fixtures/`

## Summary

- **Total test cases**: 18
- **Categories**: 6 (HTTP API, Browser Automation, Network, Security, Performance, Compatibility)
- **Coverage**: Complete integration testing with external services
