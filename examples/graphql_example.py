"""
GraphQL API client usage example.

This example demonstrates how to use GraphQLClient for testing GraphQL APIs,
including queries, mutations, and subscriptions.
"""

import asyncio

from py_web_automation import Config, GraphQLClient


async def main():
    """Main function demonstrating GraphQL client usage."""

    config = Config(timeout=30, log_level="INFO")
    base_url = "https://api.example.com/graphql"

    try:
        print("=== GraphQL Client Examples ===\n")

        async with GraphQLClient(base_url, config) as gql:
            # Example 1: Simple Query
            print("1. Executing simple query...")
            query = """
            query {
                user(id: 1) {
                    id
                    name
                    email
                }
            }
            """
            result = await gql.query(query)
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")
            if result.success and result.json():
                data = result.json()
                print(f"   Data: {data.get('data', {})}")

            # Example 2: Query with Variables
            print("\n2. Executing query with variables...")
            query_with_vars = """
            query GetUser($userId: ID!) {
                user(id: $userId) {
                    id
                    name
                    email
                    posts {
                        id
                        title
                    }
                }
            }
            """
            variables = {"userId": "2"}
            result = await gql.query(query_with_vars, variables=variables)
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

            # Example 3: Mutation
            print("\n3. Executing mutation...")
            mutation = """
            mutation CreateUser($input: CreateUserInput!) {
                createUser(input: $input) {
                    id
                    name
                    email
                }
            }
            """
            mutation_variables = {
                "input": {
                    "name": "John Doe",
                    "email": "john@example.com",
                }
            }
            result = await gql.mutate(mutation, variables=mutation_variables)
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")

            # Example 4: Query with Authentication
            print("\n4. Executing authenticated query...")
            gql.set_auth_token("your-jwt-token-here", token_type="Bearer")
            result = await gql.query(
                """
                query {
                    me {
                        id
                        name
                        email
                    }
                }
                """
            )
            print(f"   Status: {result.status_code}")
            print(f"   Success: {result.success}")
            gql.clear_auth_token()

            # Example 5: Handling GraphQL Errors
            print("\n5. Handling GraphQL errors...")
            invalid_query = """
            query {
                nonExistentField {
                    id
                }
            }
            """
            result = await gql.query(invalid_query)
            if not result.success or (result.json() and result.json().get("errors")):
                errors = result.json().get("errors", []) if result.json() else []
                print(f"   GraphQL errors detected: {len(errors)}")
                for error in errors:
                    print(f"     - {error.get('message', 'Unknown error')}")

        print("\n=== GraphQL Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
