"""
Database client usage example.

This example demonstrates how to use DBClient for testing database operations,
including queries, transactions, and multiple database backends.
"""

import asyncio

from py_web_automation import Config
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient


async def main():
    """Main function demonstrating database client usage."""

    config = Config(timeout=30, log_level="INFO")

    try:
        print("=== Database Client Examples ===\n")

        # Example 1: SQLite Database
        print("1. SQLite database operations...")
        sqlite_client = SQLiteClient(connection_string="sqlite:///:memory:")

        async with sqlite_client:
            print("   Connected to SQLite database")

            # Create table
            await sqlite_client.execute_command(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            print("   Table created")

            # Insert data
            await sqlite_client.execute_command(
                "INSERT INTO users (name, email) VALUES (:name, :email)",
                params={"name": "John Doe", "email": "john@example.com"},
            )
            await sqlite_client.execute_command(
                "INSERT INTO users (name, email) VALUES (:name, :email)",
                params={"name": "Jane Smith", "email": "jane@example.com"},
            )
            print("   Data inserted")

            # Query data
            results = await sqlite_client.execute_query("SELECT * FROM users")
            print(f"   Found {len(results)} users:")
            for row in results:
                print(f"     - {row}")

            # Update data
            await sqlite_client.execute_command(
                "UPDATE users SET email = :email WHERE name = :name",
                params={"name": "John Doe", "email": "john.doe@example.com"},
            )
            print("   Data updated")

            # Query with parameters
            results = await sqlite_client.execute_query(
                "SELECT * FROM users WHERE name = :name",
                params={"name": "John Doe"},
            )
            print(f"   Found {len(results)} matching users")

        print("   Disconnected from SQLite\n")

        # Example 2: Transactions
        print("2. Database transactions...")
        sqlite_client = SQLiteClient(connection_string="sqlite:///:memory:")

        async with sqlite_client:
            await sqlite_client.execute_command(
                "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance REAL)"
            )

            try:
                async with sqlite_client.transaction():
                    print("   Transaction started")

                    await sqlite_client.execute_command(
                        "INSERT INTO accounts (balance) VALUES (:balance)",
                        params={"balance": 1000.0},
                    )
                    await sqlite_client.execute_command(
                        "INSERT INTO accounts (balance) VALUES (:balance)",
                        params={"balance": 500.0},
                    )

                    print("   Transaction committed")

            except Exception as e:
                print(f"   Transaction rolled back: {e}")

        # Example 3: PostgreSQL (conceptual - requires actual database)
        print("\n3. PostgreSQL database operations (conceptual)...")
        # from py_web_automation.clients.db_clients.postgresql_client import PostgreSQLClient
        # postgres_client = PostgreSQLClient(
        #     connection_string="postgresql://user:password@localhost:5432/dbname"
        # )
        # async with postgres_client:
        #     results = await postgres_client.execute_query("SELECT * FROM users")
        print("   PostgreSQL operations (requires actual database connection)")

        # Example 4: MySQL (conceptual - requires actual database)
        print("\n4. MySQL database operations (conceptual)...")
        # from py_web_automation.clients.db_clients.mysql_client import MySQLClient
        # mysql_client = MySQLClient(
        #     connection_string="mysql://user:password@localhost:3306/dbname"
        # )
        # async with mysql_client:
        #     results = await mysql_client.execute_query("SELECT * FROM users")
        print("   MySQL operations (requires actual database connection)")

        print("\n=== Database Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
