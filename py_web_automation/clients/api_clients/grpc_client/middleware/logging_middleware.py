"""
Logging middleware for gRPC client.

This module provides LoggingMiddleware for automatic gRPC call logging.
"""

# Python imports
from loguru import logger

# Local imports
from ..grpc_result import GrpcResult
from .context import _GrpcRequestContext, _GrpcResponseContext
from .middleware import Middleware


class LoggingMiddleware(Middleware):
    """
    Middleware for automatic gRPC call logging.

    Logs unary RPC calls, their execution time, and results.

    Example:
        >>> from py_web_automation.clients.grpc_client import GrpcClient, MiddlewareChain
        >>> from py_web_automation.clients.grpc_client.middleware import LoggingMiddleware
        >>> logging_middleware = LoggingMiddleware()
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(logging_middleware)
        >>> async with GrpcClient(
        ...     "localhost:50051", config, middleware=middleware_chain
        ... ) as client:
        ...     result = await client.unary_call("UserService", "GetUser", request)
    """

    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        Log gRPC request.

        Args:
            context: Request context
        """
        logger.info(f"gRPC Request: {context.service}.{context.method}")
        if context.metadata:
            logger.debug(f"Metadata: {list(context.metadata.keys())}")

    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        Log gRPC response.

        Args:
            context: Response context
        """
        result = context.result
        if result.success:
            logger.info(
                f"gRPC Response: {result.service}.{result.method} - Success "
                f"(time: {result.response_time:.3f}s)"
            )
        else:
            logger.error(
                f"gRPC Response: {result.service}.{result.method} - Failed "
                f"(time: {result.response_time:.3f}s, status: {result.status_code})"
            )
            if result.error:
                logger.error(f"gRPC Error: {result.error}")

    async def process_error(
        self, context: _GrpcRequestContext, error: Exception
    ) -> GrpcResult | None:
        """
        Log gRPC error.

        Args:
            context: Request context
            error: Exception that occurred
        """
        logger.error(f"gRPC Error: {context.service}.{context.method} - {error}")
        return None
