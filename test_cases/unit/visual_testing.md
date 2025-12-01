# Visual Testing Module - Unit Test Cases

## Overview
Tests for `py_web_automation.visual_testing` module - visual regression testing utilities.

## Test Categories

### 1. VisualComparator Tests

#### TC-VT-001: VisualComparator - инициализация
- **Purpose**: Verify VisualComparator initialization
- **Preconditions**: Optional threshold
- **Test Steps**:
  1. Create VisualComparator(threshold=0.01)
  2. Verify threshold set correctly
- **Expected Result**: VisualComparator initialized correctly
- **Coverage**: `VisualComparator.__init__` method

#### TC-VT-002: VisualComparator - инициализация без PIL
- **Purpose**: Verify ImportError when PIL not available
- **Preconditions**: PIL not installed (mocked)
- **Test Steps**:
  1. Mock HAS_PIL = False
  2. Create VisualComparator
  3. Verify ImportError raised
- **Expected Result**: ImportError raised
- **Coverage**: `VisualComparator.__init__` method - PIL check

#### TC-VT-003: VisualComparator - compare идентичные изображения
- **Purpose**: Verify comparison of identical images
- **Preconditions**: Two identical image files
- **Test Steps**:
  1. Create VisualComparator
  2. Call compare("baseline.png", "identical.png")
  3. Verify is_different = False
- **Expected Result**: is_different = False
- **Coverage**: `VisualComparator.compare` method - identical

#### TC-VT-004: VisualComparator - compare разные изображения
- **Purpose**: Verify comparison of different images
- **Preconditions**: Two different image files
- **Test Steps**:
  1. Create VisualComparator
  2. Call compare("baseline.png", "different.png")
  3. Verify is_different = True, diff_percentage > 0
- **Expected Result**: is_different = True
- **Coverage**: `VisualComparator.compare` method - different

#### TC-VT-005: VisualComparator - compare с diff_path
- **Purpose**: Verify diff image generation
- **Preconditions**: Two different images
- **Test Steps**:
  1. Create VisualComparator
  2. Call compare("baseline.png", "different.png", diff_path="diff.png")
  3. Verify diff_image_path set, file created
- **Expected Result**: Diff image saved
- **Coverage**: `VisualComparator.compare` method - diff image

#### TC-VT-006: VisualComparator - compare разные размеры
- **Purpose**: Verify handling of different image sizes
- **Preconditions**: Images with different dimensions
- **Test Steps**:
  1. Create VisualComparator
  2. Call compare("baseline.png", "resized.png")
  3. Verify current image resized to match baseline
- **Expected Result**: Images resized for comparison
- **Coverage**: `VisualComparator.compare` method - size mismatch

#### TC-VT-007: VisualComparator - calculate_hash
- **Purpose**: Verify hash calculation
- **Preconditions**: Image file
- **Test Steps**:
  1. Create VisualComparator
  2. Call calculate_hash("image.png")
  3. Verify MD5 hash returned
- **Expected Result**: MD5 hash returned
- **Coverage**: `VisualComparator.calculate_hash` method

#### TC-VT-008: VisualComparator - compare_hashes идентичные
- **Purpose**: Verify hash comparison for identical images
- **Preconditions**: Two identical images
- **Test Steps**:
  1. Create VisualComparator
  2. Call compare_hashes("image1.png", "image1.png")
  3. Verify True returned
- **Expected Result**: True returned
- **Coverage**: `VisualComparator.compare_hashes` method

#### TC-VT-009: VisualComparator - compare_hashes разные
- **Purpose**: Verify hash comparison for different images
- **Preconditions**: Two different images
- **Test Steps**:
  1. Create VisualComparator
  2. Call compare_hashes("image1.png", "image2.png")
  3. Verify False returned
- **Expected Result**: False returned
- **Coverage**: `VisualComparator.compare_hashes` method - different

### 2. take_baseline_screenshot Tests

#### TC-VT-010: take_baseline_screenshot
- **Purpose**: Verify baseline screenshot capture
- **Preconditions**: UiClient instance
- **Test Steps**:
  1. Create mocked UiClient
  2. Call take_baseline_screenshot(ui_client, "baseline.png")
  3. Verify take_screenshot called
- **Expected Result**: Screenshot taken
- **Coverage**: `take_baseline_screenshot` function

#### TC-VT-011: take_baseline_screenshot с selector
- **Purpose**: Verify element screenshot
- **Preconditions**: UiClient instance, selector
- **Test Steps**:
  1. Create mocked UiClient
  2. Call take_baseline_screenshot(ui_client, "baseline.png", selector="#element")
  3. Verify take_screenshot called
- **Expected Result**: Element screenshot taken
- **Coverage**: `take_baseline_screenshot` function - with selector

