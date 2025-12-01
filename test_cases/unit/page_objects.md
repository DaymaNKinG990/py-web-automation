# Page Objects Module - Unit Test Cases

## Overview
Tests for `py_web_automation.page_objects` module - Page Object Model support for UI testing.

## Test Categories

### 1. BasePage Tests

#### TC-PO-001: BasePage - инициализация
- **Purpose**: Verify BasePage initialization
- **Preconditions**: UiClient instance, optional URL
- **Test Steps**:
  1. Create BasePage with UiClient and URL
  2. Verify ui_client and url set correctly
- **Expected Result**: BasePage initialized correctly
- **Coverage**: `BasePage.__init__` method

#### TC-PO-002: BasePage - navigate
- **Purpose**: Verify navigation to page URL
- **Preconditions**: BasePage with URL, mocked UiClient
- **Test Steps**:
  1. Create BasePage with URL
  2. Call navigate()
  3. Verify setup_browser and page.goto called
- **Expected Result**: Navigation performed correctly
- **Coverage**: `BasePage.navigate` method

#### TC-PO-003: BasePage - navigate без URL
- **Purpose**: Verify ValueError when no URL provided
- **Preconditions**: BasePage without URL
- **Test Steps**:
  1. Create BasePage without URL
  2. Call navigate() without URL
  3. Verify ValueError raised
- **Expected Result**: ValueError: "URL must be provided or set in page object"
- **Coverage**: `BasePage.navigate` method - validation

#### TC-PO-004: BasePage - wait_for_page_load
- **Purpose**: Verify waiting for page load
- **Preconditions**: BasePage with UiClient
- **Test Steps**:
  1. Create BasePage
  2. Call wait_for_page_load(timeout=5000)
  3. Verify wait_for_navigation called with timeout
- **Expected Result**: wait_for_navigation called correctly
- **Coverage**: `BasePage.wait_for_page_load` method

#### TC-PO-005: BasePage - делегирование методов
- **Purpose**: Verify methods delegate to ui_client
- **Preconditions**: BasePage with mocked UiClient
- **Test Steps**:
  1. Create BasePage
  2. Call click_element, fill_input, get_element_text
  3. Verify ui_client methods called
- **Expected Result**: Methods delegate correctly
- **Coverage**: `BasePage` delegation methods

#### TC-PO-006: BasePage - is_element_visible
- **Purpose**: Verify element visibility check
- **Preconditions**: BasePage with mocked UiClient
- **Test Steps**:
  1. Create BasePage
  2. Mock wait_for_element to succeed
  3. Call is_element_visible("#element")
  4. Verify True returned
- **Expected Result**: True returned when element visible
- **Coverage**: `BasePage.is_element_visible` method

#### TC-PO-007: BasePage - is_element_visible невидимый элемент
- **Purpose**: Verify False returned for invisible element
- **Preconditions**: BasePage with mocked UiClient
- **Test Steps**:
  1. Create BasePage
  2. Mock wait_for_element to raise NotFoundError
  3. Call is_element_visible("#element")
  4. Verify False returned
- **Expected Result**: False returned when element not found
- **Coverage**: `BasePage.is_element_visible` method - not found

### 2. Component Tests

#### TC-PO-008: Component - инициализация
- **Purpose**: Verify Component initialization
- **Preconditions**: UiClient instance, base_selector
- **Test Steps**:
  1. Create Component with UiClient and base_selector
  2. Verify ui_client and base_selector set correctly
- **Expected Result**: Component initialized correctly
- **Coverage**: `Component.__init__` method

#### TC-PO-009: Component - _selector
- **Purpose**: Verify selector building
- **Preconditions**: Component with base_selector
- **Test Steps**:
  1. Create Component with base_selector="nav.main"
  2. Call _selector("a.home")
  3. Verify "nav.main a.home" returned
- **Expected Result**: Full selector built correctly
- **Coverage**: `Component._selector` method

#### TC-PO-010: Component - _selector с полным селектором
- **Purpose**: Verify full selector not modified
- **Preconditions**: Component with base_selector
- **Test Steps**:
  1. Create Component with base_selector="nav.main"
  2. Call _selector("nav.main a.home")
  3. Verify "nav.main a.home" returned (not duplicated)
- **Expected Result**: Full selector returned as-is
- **Coverage**: `Component._selector` method - full selector

#### TC-PO-011: Component - делегирование методов
- **Purpose**: Verify methods use _selector
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Call click_element("a.home")
  3. Verify ui_client.click_element called with "nav a.home"
- **Expected Result**: Methods use _selector correctly
- **Coverage**: `Component` delegation methods

#### TC-PO-012: Component - is_visible
- **Purpose**: Verify component visibility check
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component
  2. Mock wait_for_element to succeed
  3. Call is_visible()
  4. Verify True returned
- **Expected Result**: True returned when component visible
- **Coverage**: `Component.is_visible` method

#### TC-PO-COMP-001: Component - get_element_attribute_value
- **Purpose**: Verify getting element attribute value
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Mock ui_client.get_element_attribute_value to return "value"
  3. Call get_element_attribute_value("a.link", "href")
  4. Verify ui_client.get_element_attribute_value called with "nav a.link", "href"
  5. Verify "value" returned
- **Expected Result**: Attribute value retrieved correctly
- **Coverage**: `Component.get_element_attribute_value` method

#### TC-PO-COMP-002: Component - wait_for_element
- **Purpose**: Verify waiting for element within component
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Mock ui_client.wait_for_element
  3. Call wait_for_element("a.link")
  4. Verify ui_client.wait_for_element called with "nav a.link", timeout=None
- **Expected Result**: wait_for_element called with correct selector
- **Coverage**: `Component.wait_for_element` method

#### TC-PO-COMP-003: Component - get_element_attribute_value
- **Purpose**: Verify getting element attribute value within component
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Mock ui_client.get_element_attribute_value to return "value"
  3. Call get_element_attribute_value("a.link", "href")
  4. Verify ui_client.get_element_attribute_value called with "nav a.link", "href"
  5. Verify "value" returned
- **Expected Result**: Attribute value retrieved correctly
- **Coverage**: `Component.get_element_attribute_value` method (через BasePage, но используется в Component контексте)

#### TC-PO-COMP-004: Component - fill_input
- **Purpose**: Verify filling input within component
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="form"
  2. Mock ui_client.fill_input
  3. Call fill_input("input.name", "John")
  4. Verify ui_client.fill_input called with "form input.name", "John"
- **Expected Result**: Input filled correctly
- **Coverage**: `Component.fill_input` method

#### TC-PO-COMP-005: Component - get_element_text
- **Purpose**: Verify getting element text within component
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="div"
  2. Mock ui_client.get_element_text to return "Text"
  3. Call get_element_text("span")
  4. Verify ui_client.get_element_text called with "div span"
  5. Verify "Text" returned
- **Expected Result**: Element text retrieved correctly
- **Coverage**: `Component.get_element_text` method

#### TC-PO-COMP-006: Component - wait_for_element с timeout
- **Purpose**: Verify waiting for element with custom timeout
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Mock ui_client.wait_for_element
  3. Call wait_for_element("a.link", timeout=5000)
  4. Verify ui_client.wait_for_element called with "nav a.link", timeout=5000
- **Expected Result**: wait_for_element called with correct timeout
- **Coverage**: `Component.wait_for_element` method with timeout

#### TC-PO-COMP-007: Component - is_visible с NotFoundError
- **Purpose**: Verify False returned when component not found
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Mock ui_client.wait_for_element to raise NotFoundError
  3. Call is_visible()
  4. Verify False returned
- **Expected Result**: False returned when component not found
- **Coverage**: `Component.is_visible` method - NotFoundError handling

#### TC-PO-COMP-008: Component - is_visible с TimeoutError
- **Purpose**: Verify False returned when component timeout
- **Preconditions**: Component with mocked UiClient
- **Test Steps**:
  1. Create Component with base_selector="nav"
  2. Mock ui_client.wait_for_element to raise TimeoutError
  3. Call is_visible()
  4. Verify False returned
- **Expected Result**: False returned when component timeout
- **Coverage**: `Component.is_visible` method - TimeoutError handling

### 3. PageFactory Tests

#### TC-PO-013: PageFactory - инициализация
- **Purpose**: Verify PageFactory initialization
- **Preconditions**: UiClient instance
- **Test Steps**:
  1. Create PageFactory with UiClient
  2. Verify ui_client and _pages initialized
- **Expected Result**: PageFactory initialized correctly
- **Coverage**: `PageFactory.__init__` method

#### TC-PO-014: PageFactory - create_page
- **Purpose**: Verify page object creation
- **Preconditions**: PageFactory, page class
- **Test Steps**:
  1. Create PageFactory
  2. Create page class
  3. Call create_page(page_class, url="https://example.com")
  4. Verify page instance created and stored
- **Expected Result**: Page object created and stored
- **Coverage**: `PageFactory.create_page` method

#### TC-PO-015: PageFactory - get_page
- **Purpose**: Verify getting page by URL
- **Preconditions**: PageFactory with created page
- **Test Steps**:
  1. Create PageFactory
  2. Create page with URL
  3. Call get_page(url)
  4. Verify page returned
- **Expected Result**: Page returned by URL
- **Coverage**: `PageFactory.get_page` method

#### TC-PO-016: PageFactory - get_page не найден
- **Purpose**: Verify None returned when page not found
- **Preconditions**: PageFactory without page
- **Test Steps**:
  1. Create PageFactory
  2. Call get_page("https://nonexistent.com")
  3. Verify None returned
- **Expected Result**: None returned
- **Coverage**: `PageFactory.get_page` method - not found

