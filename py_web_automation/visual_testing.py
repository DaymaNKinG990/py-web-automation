"""
Visual regression testing utilities for UI testing.

This module provides utilities for comparing screenshots and detecting
visual changes in web applications.
"""

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

try:
    from PIL import Image, ImageChops

    HAS_PIL = True
except ImportError:
    HAS_PIL = False

if TYPE_CHECKING:
    from .clients.ui_client import UiClient


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
        if not HAS_PIL:
            raise ImportError("PIL/Pillow is required for visual testing. Install with: pip install Pillow")
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
        baseline = Image.open(baseline_path)
        current = Image.open(current_path)

        # Ensure same size
        if baseline.size != current.size:
            # Resize current to match baseline
            current = current.resize(baseline.size)  # type: ignore[assignment]

        # Calculate difference
        diff = ImageChops.difference(baseline, current)

        # Calculate percentage of different pixels
        total_pixels = baseline.size[0] * baseline.size[1]
        pixel_data = diff.getdata()
        diff_pixels = sum(1 for pixel in pixel_data if sum(pixel) > 0)  # type: ignore[misc, attr-defined]
        diff_percentage = (diff_pixels / total_pixels) * 100.0

        is_different = diff_percentage > (self.threshold * 100.0)

        # Save diff image if requested
        saved_diff_path = None
        if diff_path and is_different:
            diff.save(diff_path)
            saved_diff_path = diff_path

        return VisualDiff(
            is_different=is_different,
            diff_percentage=diff_percentage,
            diff_image_path=saved_diff_path,
            threshold=self.threshold * 100.0,
        )

    def calculate_hash(self, image_path: str) -> str:
        """
        Calculate hash of image for quick comparison.

        Args:
            image_path: Path to image file

        Returns:
            MD5 hash of image

        Example:
            >>> hash1 = comparator.calculate_hash("screenshot1.png")
            >>> hash2 = comparator.calculate_hash("screenshot2.png")
            >>> if hash1 == hash2:
            ...     print("Images are identical")
        """
        with open(image_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    async def compare_hashes(self, baseline_path: str, current_path: str) -> bool:
        """
        Quick comparison using image hashes.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current image

        Returns:
            True if images are identical (same hash), False otherwise
        """
        hash1 = self.calculate_hash(baseline_path)
        hash2 = self.calculate_hash(current_path)
        return hash1 == hash2


async def take_baseline_screenshot(
    ui_client: "UiClient",
    filename: str,
    selector: str | None = None,
) -> str:
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
    if selector:
        # Element screenshot (would need to be implemented in UiClient)
        await ui_client.take_screenshot(filename)
    else:
        await ui_client.take_screenshot(filename)
    return filename
