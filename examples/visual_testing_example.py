"""
Visual regression testing usage example.

This example demonstrates how to use VisualComparator for
visual regression testing of web applications.
"""

import asyncio

from py_web_automation import Config, UiClient
from py_web_automation.visual_testing import (
    VisualComparator,
    take_baseline_screenshot,
)


async def main():
    """Main function demonstrating visual testing usage."""

    config = Config(timeout=30, browser_headless=True, log_level="INFO")
    web_url = "https://example.com"

    try:
        print("=== Visual Testing Examples ===\n")

        # Example 1: Take Baseline Screenshot
        print("1. Taking baseline screenshot...")
        async with UiClient(web_url, config) as ui:
            await ui.setup_browser()
            await ui.page.goto(web_url, wait_until="networkidle")

            baseline_path = "baseline_homepage.png"
            await take_baseline_screenshot(ui, baseline_path)
            print(f"   Baseline saved: {baseline_path}")

        # Example 2: Compare Screenshots
        print("\n2. Comparing screenshots...")
        comparator = VisualComparator(threshold=0.01)  # 1% threshold

        # Take current screenshot
        async with UiClient(web_url, config) as ui:
            await ui.setup_browser()
            await ui.page.goto(web_url, wait_until="networkidle")
            current_path = "current_homepage.png"
            await ui.take_screenshot(current_path)

        # Compare
        diff = await comparator.compare(baseline_path, current_path)
        print(f"   Images different: {diff.is_different}")
        print(f"   Difference: {diff.diff_percentage:.2f}%")
        if diff.diff_image_path:
            print(f"   Diff image: {diff.diff_image_path}")

        # Example 3: Visual Testing with Threshold
        print("\n3. Visual testing with custom threshold...")
        comparator = VisualComparator(threshold=0.05)  # 5% threshold

        diff = await comparator.compare(baseline_path, current_path)
        print(f"   Threshold: {comparator.threshold}")
        print(f"   Is different: {diff.is_different}")
        print(f"   Difference: {diff.diff_percentage:.2f}%")

        # Example 4: Generate Diff Image
        print("\n4. Generating diff image...")
        diff_path = "diff_homepage.png"
        diff = await comparator.compare(baseline_path, current_path, diff_path=diff_path)
        print(f"   Diff image saved: {diff_path}")
        print(f"   Difference: {diff.diff_percentage:.2f}%")

        # Example 5: Visual Testing Workflow
        print("\n5. Visual testing workflow...")
        async with UiClient(web_url, config) as ui:
            await ui.setup_browser()
            await ui.page.goto(web_url, wait_until="networkidle")

            # Take baseline
            baseline = "workflow_baseline.png"
            await take_baseline_screenshot(ui, baseline)
            print(f"   Baseline: {baseline}")

            # Make some changes (simulated)
            # In real scenario, you would modify the page or wait for changes

            # Take current
            current = "workflow_current.png"
            await ui.take_screenshot(current)
            print(f"   Current: {current}")

            # Compare
            diff = await comparator.compare(baseline, current)
            if diff.is_different:
                print(f"   ⚠️ Visual changes detected: {diff.diff_percentage:.2f}%")
            else:
                print("   ✅ No visual changes detected")

        # Example 6: Multiple Page Visual Testing
        print("\n6. Testing multiple pages...")
        pages = ["/", "/about", "/contact"]
        comparator = VisualComparator(threshold=0.01)

        async with UiClient(web_url, config) as ui:
            await ui.setup_browser()

            for page_path in pages:
                await ui.page.goto(f"{web_url}{page_path}", wait_until="networkidle")

                baseline = f"baseline_{page_path.replace('/', '_')}.png"
                current = f"current_{page_path.replace('/', '_')}.png"

                await take_baseline_screenshot(ui, baseline)
                await ui.take_screenshot(current)

                diff = await comparator.compare(baseline, current)
                print(f"   {page_path}: {'Different' if diff.is_different else 'Match'} ({diff.diff_percentage:.2f}%)")

        print("\n=== Visual Testing Examples Completed ===")

    except ImportError:
        print("Error: PIL/Pillow is required for visual testing")
        print("Install with: pip install Pillow")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
