"""
Response validation usage example.

This example demonstrates how to use validators for validating
API responses against schemas.
"""

import asyncio

import msgspec

from py_web_automation import ApiClient, Config
from py_web_automation.exceptions import ValidationError
from py_web_automation.validators import (
    create_schema_from_dict,
    validate_api_result,
    validate_json_response,
    validate_response,
)


async def main():
    """Main function demonstrating validators usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com"

    try:
        print("=== Validators Examples ===\n")

        # Example 1: Validate with msgspec Struct
        print("1. Validate with msgspec Struct...")

        class UserResponse(msgspec.Struct):
            id: int
            name: str
            email: str
            active: bool = True

        data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "active": True,
        }

        try:
            user = validate_response(data, UserResponse)
            print(f"   Validated user: {user.name} ({user.email})")
        except ValidationError as e:
            print(f"   Validation failed: {e}")

        # Example 2: Validate JSON String
        print("\n2. Validate JSON string...")
        json_data = '{"id": 2, "name": "Jane Smith", "email": "jane@example.com"}'

        try:
            user = validate_json_response(json_data, UserResponse)
            print(f"   Validated user: {user.name} ({user.email})")
        except ValidationError as e:
            print(f"   Validation failed: {e}")

        # Example 3: Validate API Result
        print("\n3. Validate API result...")
        async with ApiClient(base_url, config) as api:
            result = await api.make_request("/api/user/1", method="GET")

            try:
                validated = validate_api_result(result, UserResponse)
                print(f"   Validated result: {validated.name}")
            except ValidationError as e:
                print(f"   Validation failed: {e}")

        # Example 4: Validate List Response
        print("\n4. Validate list response...")

        class UserListResponse(msgspec.Struct):
            users: list[UserResponse]
            total: int

        list_data = {
            "users": [
                {"id": 1, "name": "User 1", "email": "user1@example.com"},
                {"id": 2, "name": "User 2", "email": "user2@example.com"},
            ],
            "total": 2,
        }

        try:
            response = validate_response(list_data, UserListResponse)
            print(f"   Validated {len(response.users)} users")
            print(f"   Total: {response.total}")
        except ValidationError as e:
            print(f"   Validation failed: {e}")

        # Example 5: Validate with Dict Schema
        print("\n5. Validate with dict schema...")
        data = {"id": 1, "name": "Test", "email": "test@example.com"}

        try:
            validated = validate_response(data, dict)
            print(f"   Validated dict: {validated}")
        except ValidationError as e:
            print(f"   Validation failed: {e}")

        # Example 6: Validate with List Schema
        print("\n6. Validate with list schema...")
        list_data = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

        try:
            validated = validate_response(list_data, list)
            print(f"   Validated list: {len(validated)} items")
        except ValidationError as e:
            print(f"   Validation failed: {e}")

        # Example 7: Create Schema from Dict
        print("\n7. Create schema from dict...")
        schema_dict = {
            "id": int,
            "name": str,
            "email": str,
            "optional_field": str | None,
        }

        schema = create_schema_from_dict("UserSchema", schema_dict)
        data = {"id": 1, "name": "Test", "email": "test@example.com"}

        try:
            validated = validate_response(data, schema)
            print(f"   Validated with dynamic schema: {validated}")
        except ValidationError as e:
            print(f"   Validation failed: {e}")

        # Example 8: Handle Validation Errors
        print("\n8. Handle validation errors...")
        invalid_data = {
            "id": "not-a-number",  # Should be int
            "name": "Test",
            # Missing required field: email
        }

        try:
            user = validate_response(invalid_data, UserResponse)
            print(f"   Validated: {user}")
        except ValidationError as e:
            print(f"   Validation error caught: {e.message}")
            print(f"   Details: {e.details}")

        print("\n=== Validators Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
