"""
QueryBuilder usage example.

This example demonstrates how to use QueryBuilder for constructing
SQL queries with a fluent API.
"""

import asyncio

from py_web_automation import Config, DBClient
from py_web_automation.query_builder import QueryBuilder


async def main():
    """Main function demonstrating query builder usage."""

    config = Config(timeout=30, log_level="INFO")

    try:
        print("=== QueryBuilder Examples ===\n")

        # Example 1: Simple SELECT Query
        print("1. Simple SELECT query...")
        query, params = QueryBuilder().select("id", "name", "email").from_table("users").build()
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 2: SELECT with WHERE
        print("\n2. SELECT with WHERE clause...")
        query, params = (
            QueryBuilder().select("*").from_table("users").where("active", "=", True).where("age", ">", 18).build()
        )
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 3: SELECT with ORDER BY and LIMIT
        print("\n3. SELECT with ORDER BY and LIMIT...")
        query, params = (
            QueryBuilder()
            .select("id", "name", "created_at")
            .from_table("users")
            .order_by("created_at", "DESC")
            .limit(10)
            .build()
        )
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 4: INSERT Query
        print("\n4. INSERT query...")
        query, params = QueryBuilder().insert("users", name="John Doe", email="john@example.com", age=30).build()
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 5: UPDATE Query
        print("\n5. UPDATE query...")
        query, params = QueryBuilder().update("users", email="newemail@example.com", age=31).where("id", "=", 1).build()
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 6: DELETE Query
        print("\n6. DELETE query...")
        query, params = QueryBuilder().delete("users").where("id", "=", 1).build()
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 7: Complex SELECT with JOIN
        print("\n7. Complex SELECT with JOIN...")
        query, params = (
            QueryBuilder()
            .select("users.id", "users.name", "posts.title")
            .from_table("users")
            .join("INNER", "posts", "users.id", "=", "posts.user_id")
            .where("users.active", "=", True)
            .order_by("posts.created_at", "DESC")
            .limit(20)
            .build()
        )
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 8: SELECT with GROUP BY
        print("\n8. SELECT with GROUP BY...")
        query, params = (
            QueryBuilder()
            .select("category", "COUNT(*) as count")
            .from_table("products")
            .group_by("category")
            .having("COUNT(*)", ">", 5)
            .build()
        )
        print(f"   Query: {query}")
        print(f"   Params: {params}")

        # Example 9: Using QueryBuilder with DBClient
        print("\n9. Using QueryBuilder with DBClient...")
        db_client = DBClient.create(
            "sqlite",
            "sqlite:///:memory:",
            config,
            connection_string="sqlite:///:memory:",
        )

        await db_client.connect()

        # Create table
        await db_client.execute_command(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                active BOOLEAN DEFAULT 1
            )
            """
        )

        # Insert using QueryBuilder
        query, params = QueryBuilder().insert("users", name="Test User", email="test@example.com").build()
        await db_client.execute_command(query, params)
        print("   Inserted user using QueryBuilder")

        # Select using QueryBuilder
        query, params = QueryBuilder().select("*").from_table("users").where("active", "=", True).build()
        results = await db_client.execute_query(query, params)
        print(f"   Found {len(results)} active users")

        await db_client.disconnect()

        print("\n=== QueryBuilder Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
