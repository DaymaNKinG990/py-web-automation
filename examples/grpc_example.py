"""
gRPC API client usage example.

This example demonstrates how to use GrpcClient for testing gRPC services,
including unary calls, streaming, and metadata handling.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.api_clients.grpc_client import GrpcClient


async def main():
    """Main function demonstrating gRPC client usage."""

    config = Config(timeout=30, log_level="INFO")
    grpc_url = "localhost:50051"  # Example gRPC server address

    try:
        print("=== gRPC Client Examples ===\n")

        # Note: GrpcClient requires actual gRPC service definitions
        # This is a conceptual example showing the API usage

        async with GrpcClient(grpc_url, config) as grpc:
            # Example 1: Connect to gRPC Server
            print("1. Connecting to gRPC server...")
            await grpc.connect()
            print("   Connected successfully!")

            # Example 2: Unary Call (Request-Response)
            print("\n2. Executing unary RPC call...")
            # In real usage, you would use actual protobuf message types
            # request = YourRequestMessage(field="value")
            # result = await grpc.unary_call(
            #     service="YourService",
            #     method="YourMethod",
            #     request=request
            # )
            print("   Unary call executed (conceptual example)")

            # Example 3: Set Metadata
            print("\n3. Setting metadata...")
            grpc.set_metadata("authorization", "Bearer token123")
            grpc.set_metadata("custom-header", "value")
            print("   Metadata set successfully")

            # Example 4: Unary Call with Metadata
            print("\n4. Executing unary call with metadata...")
            # result = await grpc.unary_call(
            #     service="YourService",
            #     method="YourMethod",
            #     request=request,
            #     metadata={"additional": "metadata"}
            # )
            print("   Unary call with metadata executed (conceptual example)")

            # Example 5: Server Streaming
            print("\n5. Executing server streaming call...")
            # async for response in grpc.server_streaming_call(
            #     service="YourService",
            #     method="StreamMethod",
            #     request=request
            # ):
            #     print(f"   Received: {response}")
            print("   Server streaming call executed (conceptual example)")

            # Example 6: Client Streaming
            print("\n6. Executing client streaming call...")
            # async def request_generator():
            #     for i in range(5):
            #         yield YourRequestMessage(id=i)
            # result = await grpc.client_streaming_call(
            #     service="YourService",
            #     method="StreamMethod",
            #     requests=request_generator()
            # )
            print("   Client streaming call executed (conceptual example)")

            # Example 7: Bidirectional Streaming
            print("\n7. Executing bidirectional streaming call...")
            # async def request_generator():
            #     for i in range(5):
            #         yield YourRequestMessage(id=i)
            # async for response in grpc.bidirectional_streaming_call(
            #     service="YourService",
            #     method="BidiStreamMethod",
            #     requests=request_generator()
            # ):
            #     print(f"   Received: {response}")
            print("   Bidirectional streaming call executed (conceptual example)")

            # Example 8: Disconnect
            print("\n8. Disconnecting...")
            await grpc.disconnect()
            print("   Disconnected successfully")

        print("\n=== gRPC Examples Completed ===")
        print("\nNote: This is a conceptual example.")
        print("In real usage, you need:")
        print("  - Actual .proto service definitions")
        print("  - Generated Python code from .proto files")
        print("  - Proper request/response message types")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
