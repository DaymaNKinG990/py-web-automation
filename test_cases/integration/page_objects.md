# Page Objects Integration Test Cases

## Overview
Integration tests for Page Object Model (POM) with UiClient and other components.
Tests verify page object workflows, component reuse, and integration with database and API.

## Test Categories

### 1. BasePage with UiClient

#### TC-INTEGRATION-PO-001: BasePage с UiClient - полный workflow
- **Purpose**: Verify BasePage integrates with UiClient for complete page workflows
- **Preconditions**:
  - UiClient instance
  - Web page available
  - Custom page class inheriting from BasePage
- **Test Steps**:
  1. Create UiClient with base URL
  2. Create custom page class inheriting from BasePage:
     ```python
     class LoginPage(BasePage):
         def __init__(self, ui_client: UiClient):
             super().__init__(ui_client, "https://example.com/login")
         
         async def is_loaded(self) -> bool:
             return await self.ui_client.is_visible("#login-form")
         
         async def login(self, username: str, password: str):
             await self.fill_input("#username", username)
             await self.fill_input("#password", password)
             await self.click_element("#submit")
     ```
  3. Create LoginPage instance with UiClient
  4. Navigate to page using `navigate()`
  5. Verify page loaded using `is_loaded()`
  6. Perform actions using page methods (login)
  7. Verify actions executed successfully
- **Expected Result**: BasePage integrates with UiClient, page workflows work correctly
- **Coverage**: `BasePage.navigate()`, `BasePage.is_loaded()`, page methods
- **Dependencies**: UiClient, BasePage, custom page class

#### TC-INTEGRATION-PO-002: Component с UiClient - reusable components
- **Purpose**: Verify Component class provides reusable UI components
- **Preconditions**:
  - UiClient instance
  - Web page with reusable components
  - Custom component class inheriting from Component
- **Test Steps**:
  1. Create UiClient with base URL
  2. Create custom component class inheriting from Component:
     ```python
     class ButtonComponent(Component):
         def __init__(self, ui_client: UiClient, selector: str):
             super().__init__(ui_client, selector)
         
         async def click(self):
             await self.ui_client.click_element(self.selector)
         
         async def is_enabled(self) -> bool:
             return await self.ui_client.is_enabled(self.selector)
     ```
  3. Create ButtonComponent instances
  4. Use components in page objects
  5. Verify components work correctly:
     - Components can be reused
     - Component methods work
     - Components integrate with UiClient
- **Expected Result**: Component class provides reusable UI components
- **Coverage**: Component class, reusable components
- **Dependencies**: UiClient, Component, custom component class

#### TC-INTEGRATION-PO-003: PageFactory с UiClient - управление страницами
- **Purpose**: Verify PageFactory manages page objects correctly
- **Preconditions**:
  - UiClient instance
  - Multiple page classes
  - PageFactory instance
- **Test Steps**:
  1. Create UiClient with base URL
  2. Create multiple page classes (LoginPage, HomePage, ProfilePage)
  3. Create PageFactory instance
  4. Register pages with PageFactory:
     ```python
     factory = PageFactory(ui_client)
     factory.register("login", LoginPage)
     factory.register("home", HomePage)
     factory.register("profile", ProfilePage)
     ```
  5. Get page instances from factory:
     ```python
     login_page = factory.get_page("login")
     home_page = factory.get_page("home")
     ```
  6. Verify pages created correctly:
     - Pages instantiated with UiClient
     - Pages can be navigated
     - Pages work correctly
- **Expected Result**: PageFactory manages page objects correctly
- **Coverage**: PageFactory.register(), PageFactory.get_page()
- **Dependencies**: UiClient, PageFactory, multiple page classes

### 2. Page Objects with DBClient

#### TC-INTEGRATION-PO-004: Page Objects с DBClient - проверка данных в БД
- **Purpose**: Verify Page Objects can verify data in database
- **Preconditions**:
  - UiClient instance
  - DBClient instance
  - Web page and database with related data
- **Test Steps**:
  1. Create UiClient and DBClient instances
  2. Create page class that interacts with UI
  3. Perform UI action (e.g., create user via form)
  4. Verify data in database using DBClient:
     ```python
     # After UI action
     query = "SELECT * FROM users WHERE email = :email"
     result = await db_client.execute_query(query, {"email": "test@example.com"})
     assert len(result) > 0
     ```
  5. Verify UI displays data from database:
     ```python
     # Navigate to page showing user data
     await page.navigate()
     displayed_email = await ui_client.get_text("#user-email")
     assert displayed_email == db_result[0]["email"]
     ```
- **Expected Result**: Page Objects can verify data in database and UI
- **Coverage**: Page Objects with DBClient integration
- **Dependencies**: UiClient, DBClient, Page Objects

### 3. Page Objects with ApiClient

#### TC-INTEGRATION-PO-005: Page Objects с ApiClient - API + UI workflow
- **Purpose**: Verify Page Objects work with ApiClient for API + UI workflows
- **Preconditions**:
  - UiClient instance
  - ApiClient instance
  - Web page and API endpoints
- **Test Steps**:
  1. Create UiClient and ApiClient instances
  2. Create page class for UI interactions
  3. Create data via API using ApiClient:
     ```python
     result = await api_client.make_request("/users", method="POST", data={"name": "John"})
     user_id = result.json()["id"]
     ```
  4. Navigate to page showing created data
  5. Verify UI displays data from API:
     ```python
     await page.navigate()
     displayed_name = await ui_client.get_text(f"#user-{user_id}-name")
     assert displayed_name == "John"
     ```
  6. Perform UI action (e.g., update via form)
  7. Verify update via API:
     ```python
     result = await api_client.make_request(f"/users/{user_id}", method="GET")
     assert result.json()["name"] == "Updated Name"
     ```
- **Expected Result**: Page Objects work with ApiClient for API + UI workflows
- **Coverage**: Page Objects with ApiClient integration
- **Dependencies**: UiClient, ApiClient, Page Objects

### 4. Page Objects Navigation

#### TC-INTEGRATION-PO-006: Page Objects navigation workflow
- **Purpose**: Verify Page Objects navigation between pages works correctly
- **Preconditions**:
  - UiClient instance
  - Multiple page classes
  - Web application with multiple pages
- **Test Steps**:
  1. Create UiClient instance
  2. Create multiple page classes (LoginPage, HomePage, ProfilePage)
  3. Navigate through pages:
     ```python
     login_page = LoginPage(ui_client)
     await login_page.navigate()
     await login_page.login("user", "pass")
     
     home_page = HomePage(ui_client)
     await home_page.navigate()
     assert await home_page.is_loaded()
     
     profile_page = ProfilePage(ui_client)
     await profile_page.navigate()
     assert await profile_page.is_loaded()
     ```
  4. Verify navigation works:
     - Pages navigate correctly
     - Pages detect when loaded
     - Page state maintained
- **Expected Result**: Page Objects navigation between pages works correctly
- **Coverage**: Page Objects navigation, page state management
- **Dependencies**: UiClient, multiple page classes

### 5. Page Objects with Visual Testing

#### TC-INTEGRATION-PO-007: Page Objects с visual testing
- **Purpose**: Verify Page Objects work with visual regression testing
- **Preconditions**:
  - UiClient instance
  - VisualComparator instance
  - Page class
  - Baseline screenshots
- **Test Steps**:
  1. Create UiClient and VisualComparator instances
  2. Create page class
  3. Navigate to page
  4. Take screenshot using UiClient:
     ```python
     await page.navigate()
     screenshot_path = await ui_client.take_screenshot("current.png")
     ```
  5. Compare with baseline using VisualComparator:
     ```python
     diff = await comparator.compare("baseline.png", "current.png")
     assert not diff.is_different
     ```
  6. Verify visual comparison works:
     - Screenshots captured correctly
     - Visual comparison detects differences
     - Page objects integrate with visual testing
- **Expected Result**: Page Objects work with visual regression testing
- **Coverage**: Page Objects with VisualComparator
- **Dependencies**: UiClient, VisualComparator, Page Objects

