"""
Unit tests for visual_testing module.
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import allure
import pytest

from py_web_automation.visual_testing import (
    VisualComparator,
    VisualDiff,
    take_baseline_screenshot,
)

try:
    from PIL import Image

    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.ui]


class TestVisualComparator:
    """Test VisualComparator class."""

    @allure.title("TC-VT-001: VisualComparator - инициализация")
    def test_visual_comparator_init(self):
        """Test VisualComparator initialization."""
        with allure.step("Create VisualComparator with threshold"):
            comparator = VisualComparator(threshold=0.01)

        with allure.step("Verify threshold set correctly"):
            assert comparator.threshold == 0.01

    @allure.title("TC-VT-002: VisualComparator - инициализация без PIL")
    def test_visual_comparator_init_no_pil(self):
        """Test ImportError when PIL not available."""
        with allure.step("Mock HAS_PIL = False"):
            with patch("py_web_automation.visual_testing.HAS_PIL", False):
                with allure.step("Create VisualComparator and expect ImportError"):
                    with pytest.raises(ImportError, match="PIL/Pillow is required"):
                        VisualComparator()

    @pytest.mark.asyncio
    @allure.title("TC-VT-003: VisualComparator - compare идентичные изображения")
    async def test_visual_comparator_compare_identical(self, tmp_path):
        """Test comparison of identical images."""
        with allure.step("Create two identical image files"):
            baseline_path = tmp_path / "baseline.png"
            current_path = tmp_path / "current.png"

            # Create simple test images
            img = Image.new("RGB", (100, 100), color="red")
            img.save(baseline_path)
            img.save(current_path)

        with allure.step("Create VisualComparator and compare"):
            comparator = VisualComparator(threshold=0.01)
            diff = await comparator.compare(str(baseline_path), str(current_path))

        with allure.step("Verify is_different = False"):
            assert diff.is_different is False
            assert diff.diff_percentage == pytest.approx(0.0, abs=0.1)

    @pytest.mark.asyncio
    @allure.title("TC-VT-004: VisualComparator - compare разные изображения")
    async def test_visual_comparator_compare_different(self, tmp_path):
        """Test comparison of different images."""
        with allure.step("Create two different image files"):
            baseline_path = tmp_path / "baseline.png"
            current_path = tmp_path / "current.png"

            # Create different test images
            baseline_img = Image.new("RGB", (100, 100), color="red")
            current_img = Image.new("RGB", (100, 100), color="blue")
            baseline_img.save(baseline_path)
            current_img.save(current_path)

        with allure.step("Create VisualComparator and compare"):
            comparator = VisualComparator(threshold=0.01)
            diff = await comparator.compare(str(baseline_path), str(current_path))

        with allure.step("Verify is_different = True"):
            assert diff.is_different is True
            assert diff.diff_percentage > 0

    @pytest.mark.asyncio
    @allure.title("TC-VT-005: VisualComparator - compare с diff_path")
    async def test_visual_comparator_compare_with_diff_path(self, tmp_path):
        """Test diff image generation."""
        with allure.step("Create two different image files"):
            baseline_path = tmp_path / "baseline.png"
            current_path = tmp_path / "current.png"
            diff_path = tmp_path / "diff.png"

            baseline_img = Image.new("RGB", (100, 100), color="red")
            current_img = Image.new("RGB", (100, 100), color="blue")
            baseline_img.save(baseline_path)
            current_img.save(current_path)

        with allure.step("Create VisualComparator and compare with diff_path"):
            comparator = VisualComparator(threshold=0.01)
            diff = await comparator.compare(str(baseline_path), str(current_path), diff_path=str(diff_path))

        with allure.step("Verify diff_image_path set, file created"):
            assert diff.is_different is True
            assert diff.diff_image_path == str(diff_path)
            assert Path(diff_path).exists()

    @pytest.mark.asyncio
    @allure.title("TC-VT-006: VisualComparator - compare разные размеры")
    async def test_visual_comparator_compare_different_sizes(self, tmp_path):
        """Test handling of different image sizes."""
        with allure.step("Create images with different dimensions"):
            baseline_path = tmp_path / "baseline.png"
            current_path = tmp_path / "current.png"

            baseline_img = Image.new("RGB", (100, 100), color="red")
            current_img = Image.new("RGB", (200, 200), color="red")
            baseline_img.save(baseline_path)
            current_img.save(current_path)

        with allure.step("Create VisualComparator and compare"):
            comparator = VisualComparator(threshold=0.01)
            diff = await comparator.compare(str(baseline_path), str(current_path))

        with allure.step("Verify current image resized to match baseline"):
            # Comparison should succeed (images resized)
            assert isinstance(diff, VisualDiff)

    @allure.title("TC-VT-007: VisualComparator - calculate_hash")
    def test_visual_comparator_calculate_hash(self, tmp_path):
        """Test hash calculation."""
        with allure.step("Create image file"):
            image_path = tmp_path / "image.png"
            img = Image.new("RGB", (100, 100), color="red")
            img.save(image_path)

        with allure.step("Create VisualComparator and calculate hash"):
            comparator = VisualComparator()
            hash_value = comparator.calculate_hash(str(image_path))

        with allure.step("Verify MD5 hash returned"):
            assert isinstance(hash_value, str)
            assert len(hash_value) == 32  # MD5 hash length

    @pytest.mark.asyncio
    @allure.title("TC-VT-008: VisualComparator - compare_hashes идентичные")
    async def test_visual_comparator_compare_hashes_identical(self, tmp_path):
        """Test hash comparison for identical images."""
        with allure.step("Create two identical images"):
            image1_path = tmp_path / "image1.png"
            image2_path = tmp_path / "image2.png"

            img = Image.new("RGB", (100, 100), color="red")
            img.save(image1_path)
            img.save(image2_path)

        with allure.step("Create VisualComparator and compare hashes"):
            comparator = VisualComparator()
            result = await comparator.compare_hashes(str(image1_path), str(image2_path))

        with allure.step("Verify True returned"):
            assert result is True

    @pytest.mark.asyncio
    @allure.title("TC-VT-009: VisualComparator - compare_hashes разные")
    async def test_visual_comparator_compare_hashes_different(self, tmp_path):
        """Test hash comparison for different images."""
        with allure.step("Create two different images"):
            image1_path = tmp_path / "image1.png"
            image2_path = tmp_path / "image2.png"

            img1 = Image.new("RGB", (100, 100), color="red")
            img2 = Image.new("RGB", (100, 100), color="blue")
            img1.save(image1_path)
            img2.save(image2_path)

        with allure.step("Create VisualComparator and compare hashes"):
            comparator = VisualComparator()
            result = await comparator.compare_hashes(str(image1_path), str(image2_path))

        with allure.step("Verify False returned"):
            assert result is False


@pytest.mark.unit
class TestTakeBaselineScreenshot:
    """Test take_baseline_screenshot function."""

    @pytest.mark.asyncio
    @allure.title("TC-VT-010: take_baseline_screenshot")
    async def test_take_baseline_screenshot(self):
        """Test baseline screenshot capture."""
        with allure.step("Create mocked UiClient"):
            ui_client = MagicMock()
            ui_client.take_screenshot = AsyncMock()

        with allure.step("Call take_baseline_screenshot"):
            result = await take_baseline_screenshot(ui_client, "baseline.png")

        with allure.step("Verify take_screenshot called"):
            ui_client.take_screenshot.assert_called_once_with("baseline.png")
            assert result == "baseline.png"

    @pytest.mark.asyncio
    @allure.title("TC-VT-011: take_baseline_screenshot с selector")
    async def test_take_baseline_screenshot_with_selector(self):
        """Test element screenshot."""
        with allure.step("Create mocked UiClient"):
            ui_client = MagicMock()
            ui_client.take_screenshot = AsyncMock()

        with allure.step("Call take_baseline_screenshot with selector"):
            result = await take_baseline_screenshot(ui_client, "baseline.png", selector="#element")

        with allure.step("Verify take_screenshot called"):
            ui_client.take_screenshot.assert_called_once_with("baseline.png")
            assert result == "baseline.png"
