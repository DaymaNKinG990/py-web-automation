"""
WebSocket API client usage example.

This example demonstrates how to use WebSocketClient for testing
WebSocket connections, including message sending, receiving, and event handling.
"""

import asyncio

from py_web_automation import Config, WebSocketClient


async def main():
    """Main function demonstrating WebSocket client usage."""

    config = Config(timeout=30, log_level="INFO")
    ws_url = "wss://echo.websocket.org"  # Public echo server for testing

    try:
        print("=== WebSocket Client Examples ===\n")

        async with WebSocketClient(ws_url, config) as ws:
            # Example 1: Connect and Send Message
            print("1. Connecting to WebSocket...")
            await ws.connect()
            print("   Connected successfully!")

            # Example 2: Send and Receive Message
            print("\n2. Sending and receiving messages...")
            test_message = {"type": "ping", "data": "Hello WebSocket!"}
            await ws.send_message(test_message)
            print(f"   Sent: {test_message}")

            received = await ws.receive_message(timeout=5)
            print(f"   Received: {received}")

            # Example 3: Send Multiple Messages
            print("\n3. Sending multiple messages...")
            messages = [
                {"id": 1, "message": "First message"},
                {"id": 2, "message": "Second message"},
                {"id": 3, "message": "Third message"},
            ]

            for msg in messages:
                await ws.send_message(msg)
                print(f"   Sent: {msg}")
                response = await ws.receive_message(timeout=5)
                print(f"   Echo: {response}")

            # Example 4: Register Message Handler
            print("\n4. Using message handlers...")
            received_messages = []

            def message_handler(message: dict) -> None:
                received_messages.append(message)
                print(f"   Handler received: {message}")

            ws.register_message_handler("test", message_handler)
            await ws.send_message({"type": "test", "data": "Handler test"})
            await asyncio.sleep(1)  # Wait for handler to process

            # Example 5: Check Connection Status
            print("\n5. Checking connection status...")
            is_connected = ws.is_connected()
            print(f"   Is connected: {is_connected}")

            # Example 6: Disconnect
            print("\n6. Disconnecting...")
            await ws.disconnect()
            print("   Disconnected successfully")

        print("\n=== WebSocket Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
