"""
Additional unit tests for GrpcClient.
"""

from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from py_web_automation.clients.grpc_client import GrpcClientImpl

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.grpc]


class TestGrpcClientAdditional:
    """Additional test cases for GrpcClient class."""

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-006: set_metadata устанавливает metadata")
    @allure.description("Test set_metadata sets metadata. TC-GRPC-006")
    async def test_set_metadata(self, valid_config):
        """Test set_metadata sets metadata."""
        with allure.step("Create GrpcClientImpl instance"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

        with allure.step("Set metadata for authorization"):
            client.set_metadata("authorization", "Bearer token123")
            assert client._metadata["authorization"] == "Bearer token123"

        with allure.step("Set metadata for custom header"):
            client.set_metadata("custom-header", "value")
            assert client._metadata["custom-header"] == "value"

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-007: clear_metadata очищает metadata")
    @allure.description("Test clear_metadata clears metadata. TC-GRPC-007")
    async def test_clear_metadata(self, valid_config):
        """Test clear_metadata clears metadata."""
        with allure.step("Create GrpcClientImpl and set metadata"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            client.set_metadata("authorization", "Bearer token123")
            assert len(client._metadata) > 0

        with allure.step("Clear metadata"):
            client.clear_metadata()

        with allure.step("Verify metadata is empty"):
            assert len(client._metadata) == 0

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-008: _merge_metadata объединяет default и call metadata")
    @allure.description("Test _merge_metadata merges default and call metadata. TC-GRPC-008")
    async def test_merge_metadata(self, valid_config):
        """Test _merge_metadata merges default and call metadata."""
        with allure.step("Create GrpcClientImpl and set default metadata"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            client.set_metadata("authorization", "Bearer default-token")
            client.set_metadata("x-request-id", "default-id")

        with allure.step("Merge with call metadata"):
            call_metadata = {"x-request-id": "call-id", "x-custom": "value"}
            merged = client._merge_metadata(call_metadata)

        with allure.step("Verify merged metadata"):
            assert merged["authorization"] == "Bearer default-token"
            assert merged["x-request-id"] == "call-id"  # Call metadata overrides default
            assert merged["x-custom"] == "value"

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-009: _merge_metadata использует только default если call metadata нет")
    @allure.description("Test _merge_metadata uses only default if call metadata is None. TC-GRPC-009")
    async def test_merge_metadata_no_call_metadata(self, valid_config):
        """Test _merge_metadata uses only default if call metadata is None."""
        with allure.step("Create GrpcClientImpl and set default metadata"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            client.set_metadata("authorization", "Bearer token")

        with allure.step("Merge with None call metadata"):
            merged = client._merge_metadata(None)

        with allure.step("Verify only default metadata returned"):
            assert merged == {"authorization": "Bearer token"}

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-010: _merge_metadata перезаписывает default call metadata")
    @allure.description("Test _merge_metadata overwrites default with call metadata. TC-GRPC-010")
    async def test_merge_metadata_overwrites(self, valid_config):
        """Test _merge_metadata overwrites default with call metadata."""
        with allure.step("Create GrpcClientImpl and set default metadata"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            client.set_metadata("authorization", "Bearer default-token")

        with allure.step("Merge with call metadata that overwrites default"):
            call_metadata = {"authorization": "Bearer call-token"}
            merged = client._merge_metadata(call_metadata)

        with allure.step("Verify call metadata overwrites default"):
            assert merged["authorization"] == "Bearer call-token"

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-011: close очищает metadata")
    @allure.description("Test close clears metadata. TC-GRPC-011")
    async def test_close_clears_metadata(self, mocker, valid_config):
        """Test close clears metadata."""
        with allure.step("Create GrpcClientImpl and set metadata"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            client.set_metadata("authorization", "Bearer token")
            assert len(client._metadata) > 0

        with allure.step("Mock disconnect and call close"):
            # Mock disconnect to avoid actual gRPC connection
            client.disconnect = AsyncMock()  # type: ignore[method-assign]

            await client.close()

        with allure.step("Verify metadata is cleared"):
            assert len(client._metadata) == 0

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-012: server_streaming_call выбрасывает NotImplementedError")
    @allure.description("Test server_streaming_call raises NotImplementedError. TC-GRPC-012")
    async def test_server_streaming_call_not_implemented(self, mocker, valid_config):
        """Test server_streaming_call raises NotImplementedError."""
        with allure.step("Create GrpcClientImpl and setup mock channel"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            mock_channel = AsyncMock()
            client._channel = mock_channel

            mock_request = MagicMock()

        with allure.step("Call server_streaming_call and expect NotImplementedError"):
            # server_streaming_call returns a coroutine that raises NotImplementedError
            with pytest.raises(NotImplementedError):
                await client.server_streaming_call("Service", "Method", mock_request)

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-013: server_streaming_call выбрасывает RuntimeError если не подключен")
    @allure.description("Test server_streaming_call raises RuntimeError if not connected. TC-GRPC-013")
    async def test_server_streaming_call_not_connected(self, valid_config):
        """Test server_streaming_call raises RuntimeError if not connected."""
        with allure.step("Create GrpcClientImpl without connection"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            mock_request = MagicMock()

        with allure.step("Call server_streaming_call and expect RuntimeError"):
            # server_streaming_call returns a coroutine that raises RuntimeError
            with pytest.raises(RuntimeError, match="Not connected"):
                await client.server_streaming_call("Service", "Method", mock_request)

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-014: __aenter__ вызывает connect")
    @allure.description("Test __aenter__ calls connect. TC-GRPC-014")
    async def test_aenter_calls_connect(self, mocker, valid_config):
        """Test __aenter__ calls connect."""
        with allure.step("Create GrpcClientImpl and mock connect"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            connect_mock = mocker.patch.object(client, "connect", new_callable=AsyncMock)

        with allure.step("Use client as context manager"):
            try:
                async with client:
                    pass
            except (RuntimeError, NotImplementedError, ImportError, ModuleNotFoundError):
                # Expected if grpc module is not available
                pass

        with allure.step("Verify connect was called"):
            # connect should have been called
            assert connect_mock.called

    @pytest.mark.asyncio
    @allure.title("TC-GRPC-015: __aexit__ вызывает close")
    @allure.description("Test __aexit__ calls close. TC-GRPC-015")
    async def test_aexit_calls_close(self, mocker, valid_config):
        """Test __aexit__ calls close."""
        with allure.step("Create GrpcClientImpl and mock close and connect"):
            url = "https://api.example.com:50051"
            client = GrpcClientImpl(url, valid_config)

            close_mock = mocker.patch.object(client, "close", new_callable=AsyncMock)
            mocker.patch.object(client, "connect", new_callable=AsyncMock)

        with allure.step("Use client as context manager"):
            try:
                async with client:
                    pass
            except (RuntimeError, NotImplementedError, ImportError, ModuleNotFoundError):
                # Expected if grpc module is not available
                pass

        with allure.step("Verify close was called"):
            # close should have been called
            assert close_mock.called
