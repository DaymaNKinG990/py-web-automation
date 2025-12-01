"""
Web automation testing framework clients.

This package provides classes for testing web applications:
- ApiClient: HTTP REST API testing
- GraphQLClient: GraphQL API testing
- GrpcClient: gRPC API testing
- SoapClient: SOAP API testing
- WebSocketClient: WebSocket API testing
- UiClient: Browser-based UI testing with Playwright
- DBClient: Database client with support for multiple backends
"""

from .api_client import ApiClient
from .db_client import DBClient
from .graphql_client import GraphQLClient
from .grpc_client import GrpcClient, GrpcClientImpl
from .models import ApiResult
from .request_builder import RequestBuilder
from .soap_client import SoapClient
from .ui_client import UiClient
from .websocket_client import WebSocketClient

__all__ = [
    "ApiResult",
    "ApiClient",
    "GraphQLClient",
    "GrpcClient",
    "GrpcClientImpl",
    "SoapClient",
    "WebSocketClient",
    "UiClient",
    "DBClient",
    "RequestBuilder",
]
