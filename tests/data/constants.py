"""
Test data constants for TMA Framework tests.
"""

# API result test data
VALID_API_RESULT_DATA = {
    "endpoint": "/api/status",
    "method": "GET",
    "status_code": 200,
    "response_time": 0.5,
    "success": True,
    "redirect": False,
    "client_error": False,
    "server_error": False,
    "informational": False,
    "headers": {"content-type": "application/json"},
    "body": b'{"status": "ok"}',
    "content_type": "application/json",
    "reason": "OK",
    "error_message": None,
}

ERROR_API_RESULT_DATA = {
    "endpoint": "/api/error",
    "method": "POST",
    "status_code": 400,
    "response_time": 0.2,
    "success": False,
    "redirect": False,
    "client_error": True,
    "server_error": False,
    "informational": False,
    "headers": {"content-type": "application/json"},
    "body": b'{"error": "Bad Request"}',
    "content_type": "application/json",
    "reason": "Bad Request",
    "error_message": "Bad Request",
}

TIMEOUT_API_RESULT_DATA = {
    "endpoint": "/api/timeout",
    "method": "GET",
    "status_code": 408,
    "response_time": 30.0,
    "success": False,
    "redirect": False,
    "client_error": True,
    "server_error": False,
    "informational": False,
    "headers": {},
    "body": b"",
    "content_type": None,
    "reason": "Request Timeout",
    "error_message": "Request timeout",
}

REDIRECT_API_RESULT_DATA = {
    "endpoint": "/api/redirect",
    "method": "GET",
    "status_code": 301,
    "response_time": 0.1,
    "success": False,
    "redirect": True,
    "client_error": False,
    "server_error": False,
    "informational": False,
    "headers": {"location": "https://example.com/new"},
    "body": b"",
    "content_type": None,
    "reason": "Moved Permanently",
    "error_message": None,
}

SERVER_ERROR_API_RESULT_DATA = {
    "endpoint": "/api/server-error",
    "method": "POST",
    "status_code": 500,
    "response_time": 1.5,
    "success": False,
    "redirect": False,
    "client_error": False,
    "server_error": True,
    "informational": False,
    "headers": {"content-type": "text/html"},
    "body": b"Internal Server Error",
    "content_type": "text/html",
    "reason": "Internal Server Error",
    "error_message": "Internal Server Error",
}

INFORMATIONAL_API_RESULT_DATA = {
    "endpoint": "/api/info",
    "method": "GET",
    "status_code": 101,
    "response_time": 0.05,
    "success": False,
    "redirect": False,
    "client_error": False,
    "server_error": False,
    "informational": True,
    "headers": {},
    "body": b"",
    "content_type": None,
    "reason": "Switching Protocols",
    "error_message": None,
}
