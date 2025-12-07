"""
QueryBuilder usage example.

This example demonstrates how to use QueryBuilder for constructing
SQL queries with a fluent API.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient


async def main():
    """Main function demonstrating query builder usage."""

    config = Config(timeout=30, log_level="INFO")

    try:
        print("=== QueryBuilder Examples ===\n")

        # Example 1: Simple SELECT Query
        print("1. Simple SELECT query...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = db.query().select("id", "name", "email").from_table("users")._build()
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 2: SELECT with WHERE
        print("\n2. SELECT with WHERE clause...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = (
                db.query()
                .select("*")
                .from_table("users")
                .where("active", "=", True)
                .where("age", ">", 18)
                ._build()
            )
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 3: SELECT with ORDER BY and LIMIT
        print("\n3. SELECT with ORDER BY and LIMIT...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = (
                db.query()
                .select("id", "name", "created_at")
                .from_table("users")
                .order_by("created_at", "DESC")
                .limit(10)
                ._build()
            )
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 4: INSERT Query
        print("\n4. INSERT query...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = db.query().insert("users", name="John Doe", email="john@example.com", age=30)._build()
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 5: UPDATE Query
        print("\n5. UPDATE query...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = (
                db.query()
                .update("users", email="newemail@example.com", age=31)
                .where("id", "=", 1)
                ._build()
            )
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 6: DELETE Query
        print("\n6. DELETE query...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = db.query().delete("users").where("id", "=", 1)._build()
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 7: Complex SELECT with JOIN
        print("\n7. Complex SELECT with JOIN...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = (
                db.query()
                .select("users.id", "users.name", "posts.title")
                .from_table("users")
                .join("INNER", "posts", "users.id", "=", "posts.user_id")
                .where("users.active", "=", True)
                .order_by("posts.created_at", "DESC")
                .limit(20)
                ._build()
            )
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 8: SELECT with GROUP BY
        print("\n8. SELECT with GROUP BY...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            query, params = (
                db.query()
                .select("category", "COUNT(*) as count")
                .from_table("products")
                .group_by("category")
                .having("COUNT(*)", ">", 5)
                ._build()
            )
            print(f"   Query: {query}")
            print(f"   Params: {params}")

        # Example 9: Using QueryBuilder with DBClient execution
        print("\n9. Using QueryBuilder with DBClient execution...")
        async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
            # Create table
            await db.execute_command(
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
            query, params = db.query().insert("users", name="Test User", email="test@example.com")._build()
            await db.execute_command(query, params)
            print("   Inserted user using QueryBuilder")

            # Select using QueryBuilder
            query, params = db.query().select("*").from_table("users").where("active", "=", True)._build()
            results = await db.execute_query(query, params)
            print(f"   Found {len(results)} active users")

        print("\n=== QueryBuilder Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
