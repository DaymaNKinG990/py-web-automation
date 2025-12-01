# Installation Guide

This guide will help you install and set up the Web Automation Framework.

## Prerequisites

- Python 3.13 (required)
- pip or uv package manager
- Git (for cloning the repository)

## Installation Methods

### Method 1: Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/py-web-automation.git
cd py-web-automation

# Install dependencies using uv
uv sync

# Install Playwright browsers
uv run playwright install
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/your-org/py-web-automation.git
cd py-web-automation

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install
```

## Dependencies

The framework requires the following packages:

### Core Dependencies
- `httpx` - HTTP client for API testing
- `playwright` - Browser automation for UI testing
- `msgspec` - High-performance data validation and serialization
- `loguru` - Logging framework
- `pyyaml` - YAML configuration support
- `aiofiles` - Async file operations
- `websockets` - WebSocket client support
- `aiosqlite` - SQLite database adapter (for DBClient)

### Optional Protocol Dependencies
- `grpclib` - gRPC client support (for GrpcClient)
- `zeep` - SOAP client support (for SoapClient)
- `graphql-core` - GraphQL support (for GraphQLClient)

### Optional Database Dependencies (for DBClient)
- `asyncpg` or `psycopg` - PostgreSQL adapter
- `aiomysql` or `pymysql` - MySQL adapter

### Development Dependencies
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support
- `pytest-playwright` - Playwright testing integration

## Environment Setup

### 1. Configuration

Create a `.env` file in your project root (optional):

```bash
# Optional configuration
WEB_AUTOMATION_BASE_URL="https://api.example.com"
WEB_AUTOMATION_TIMEOUT="30"
WEB_AUTOMATION_RETRY_COUNT="3"
WEB_AUTOMATION_RETRY_DELAY="1.0"
WEB_AUTOMATION_LOG_LEVEL="INFO"
WEB_AUTOMATION_BROWSER_HEADLESS="true"
WEB_AUTOMATION_BROWSER_TIMEOUT="30000"
```

### 2. YAML Configuration (Alternative)

Create a `config.yaml` file:

```yaml
base_url: "https://api.example.com"
timeout: 30
retry_count: 3
retry_delay: 1.0
log_level: "INFO"
browser_headless: true
browser_timeout: 30000
```

## Verification

Test your installation:

```bash
# Run basic API client example
uv run python examples/basic_usage.py

# Run UI client example
uv run python examples/ui_only_usage.py

# Run API-only example
uv run python examples/api_only_usage.py

# Run error handling examples
uv run python examples/error_handling.py
```

## Troubleshooting

### Common Issues

1. **Playwright browser installation fails**
   ```bash
   # Try installing browsers manually
   uv run playwright install chromium
   ```

2. **Import errors**
   - Make sure you're using the correct Python version (3.13+)
   - Verify all dependencies are installed correctly
   - Check that you're in the correct virtual environment

3. **Database connection issues**
   - Ensure the required database adapter is installed
   - Verify connection string format
   - Check database server is running and accessible

4. **WebSocket connection issues**
   - Verify WebSocket URL is correct (ws:// or wss://)
   - Check firewall and network settings
   - Ensure WebSocket server is running

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the [Examples](examples.md) for working code
3. Open an issue on the project repository

## Next Steps

After successful installation:
1. Read the [Quick Start Guide](quickstart.md)
2. Explore the [Examples](examples.md)
3. Check the [API Reference](api-reference.md) for detailed documentation
