"""
Visual regression testing utilities for UI testing.

This module provides utilities for comparing screenshots and detecting
visual changes in web applications.
"""

# Python imports
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image, ImageChops

# Local imports
if TYPE_CHECKING:
    from .async_ui_client.ui_client import UiClient as AsyncUiClient
    from .sync_ui_client.ui_client import UiClient as SyncUiClient


@dataclass
class VisualDiff:
    """
    Result of visual comparison.

    Attributes:
        is_different: Whether images are different
        diff_percentage: Percentage of pixels that differ
        diff_image_path: Path to diff image (if generated)
        threshold: Threshold used for comparison
    """

    is_different: bool
    diff_percentage: float
    diff_image_path: str | None = None
    threshold: float = 0.0


class VisualComparator:
    """
    Comparator for visual regression testing.

    Compares screenshots to detect visual changes in web applications.
    Uses PIL/Pillow for image comparison.

    Example:
        >>> comparator = VisualComparator()
        >>> diff = await comparator.compare("baseline.png", "current.png")
        >>> if diff.is_different:
        ...     print(f"Visual difference: {diff.diff_percentage:.2f}%")
    """

    def __init__(self, threshold: float = 0.01) -> None:
        """
        Initialize visual comparator.

        Args:
            threshold: Percentage threshold for considering images different (default: 0.01 = 1%)

        Raises:
            ImportError: If PIL/Pillow is not installed
        """
        self.threshold = threshold

    async def compare(
        self,
        baseline_path: str,
        current_path: str,
        diff_path: str | None = None,
    ) -> VisualDiff:
        """
        Compare two images.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current image
            diff_path: Optional path to save diff image

        Returns:
            VisualDiff with comparison results

        Raises:
            FileNotFoundError: If image files don't exist
            ImportError: If PIL/Pillow is not installed
        """
        baseline, current = self._prepare_images(baseline_path, current_path)
        diff = ImageChops.difference(baseline, current)
        diff_percentage = self._calculate_diff_percentage(baseline, diff)
        is_different = diff_percentage > (self.threshold * 100.0)
        saved_diff_path = self._save_diff_image(diff, diff_path, is_different)
        return VisualDiff(
            is_different=is_different,
            diff_percentage=diff_percentage,
            diff_image_path=saved_diff_path,
            threshold=self.threshold * 100.0,
        )

    def _prepare_images(
        self, baseline_path: str, current_path: str
    ) -> tuple[Image.Image, Image.Image]:
        """
        Load and prepare images for comparison.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current image

        Returns:
            Tuple of (baseline_image, current_image)
        """
        baseline = Image.open(baseline_path)
        current = Image.open(current_path)
        if baseline.size != current.size:
            current = current.resize(baseline.size)
        return baseline, current

    def _calculate_diff_percentage(self, baseline: Image.Image, diff: Image.Image) -> float:
        """
        Calculate percentage of different pixels.

        Args:
            baseline: Baseline image
            diff: Difference image

        Returns:
            Percentage of different pixels
        """
        total_pixels = baseline.size[0] * baseline.size[1]
        pixel_data = diff.getdata()
        diff_pixels = sum(1 for pixel in pixel_data if sum(pixel) > 0)
        return (diff_pixels / total_pixels) * 100.0

    def _save_diff_image(
        self, diff: Image.Image, diff_path: str | None, is_different: bool
    ) -> str | None:
        """
        Save diff image if requested and images are different.

        Args:
            diff: Difference image
            diff_path: Optional path to save diff image
            is_different: Whether images are different

        Returns:
            Path to saved diff image, or None
        """
        if diff_path and is_different:
            diff.save(diff_path)
            return diff_path
        return None

    def calculate_hash(self, image_path: str | Path) -> str:
        """
        Calculate hash of image for quick comparison.

        Args:
            image_path: Path to image file (str or Path)

        Returns:
            MD5 hash of image

        Example:
            >>> hash1 = comparator.calculate_hash("screenshot1.png")
            >>> hash2 = comparator.calculate_hash(Path("screenshot2.png"))
            >>> if hash1 == hash2:
            ...     print("Images are identical")
        """
        path = Path(image_path)
        return hashlib.md5(path.read_bytes()).hexdigest()

    async def compare_hashes(self, baseline_path: str | Path, current_path: str | Path) -> bool:
        """
        Quick comparison using image hashes.

        Args:
            baseline_path: Path to baseline image (str or Path)
            current_path: Path to current image (str or Path)

        Returns:
            True if images are identical (same hash), False otherwise

        Example:
            >>> await comparator.compare_hashes("baseline.png", Path("current.png"))
        """
        hash1 = self.calculate_hash(baseline_path)
        hash2 = self.calculate_hash(current_path)
        return hash1 == hash2


async def take_baseline_screenshot(ui_client: AsyncUiClient | SyncUiClient, filename: str) -> str:
    """
    Take baseline screenshot for visual regression testing.

    Args:
        ui_client: UiClient instance
        filename: Filename to save screenshot
        selector: Optional CSS selector for element screenshot

    Returns:
        Path to saved screenshot

    Example:
        >>> await take_baseline_screenshot(ui_client, "homepage_baseline.png")
    """
    if isinstance(ui_client, AsyncUiClient):
        await ui_client.take_screenshot(filename)
    else:
        ui_client.take_screenshot(filename)
    return filename
