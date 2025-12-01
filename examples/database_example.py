"""
Database client usage example.

This example demonstrates how to use DBClient for testing database operations,
including queries, transactions, and multiple database backends.
"""

import asyncio

from py_web_automation import Config, DBClient


async def main():
    """Main function demonstrating database client usage."""

    config = Config(timeout=30, log_level="INFO")

    try:
        print("=== Database Client Examples ===\n")

        # Example 1: SQLite Database
        print("1. SQLite database operations...")
        sqlite_client = DBClient.create(
            "sqlite",
            "sqlite:///:memory:",
            config,
            connection_string="sqlite:///:memory:",
        )

        await sqlite_client.connect()
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

        await sqlite_client.disconnect()
        print("   Disconnected from SQLite\n")

        # Example 2: Transactions
        print("2. Database transactions...")
        sqlite_client = DBClient.create(
            "sqlite",
            "sqlite:///:memory:",
            config,
            connection_string="sqlite:///:memory:",
        )
        await sqlite_client.connect()

        await sqlite_client.execute_command(
            "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance REAL)"
        )

        try:
            await sqlite_client.begin_transaction()
            print("   Transaction started")

            await sqlite_client.execute_command(
                "INSERT INTO accounts (balance) VALUES (:balance)",
                params={"balance": 1000.0},
            )
            await sqlite_client.execute_command(
                "INSERT INTO accounts (balance) VALUES (:balance)",
                params={"balance": 500.0},
            )

            await sqlite_client.commit_transaction()
            print("   Transaction committed")

        except Exception as e:
            await sqlite_client.rollback_transaction()
            print(f"   Transaction rolled back: {e}")

        await sqlite_client.disconnect()

        # Example 3: PostgreSQL (conceptual - requires actual database)
        print("\n3. PostgreSQL database operations (conceptual)...")
        # postgres_client = DBClient.create(
        #     "postgresql",
        #     "postgresql://user:password@localhost:5432/dbname",
        #     config,
        #     connection_string="postgresql://user:password@localhost:5432/dbname",
        # )
        # await postgres_client.connect()
        # results = await postgres_client.execute_query("SELECT * FROM users")
        # await postgres_client.disconnect()
        print("   PostgreSQL operations (requires actual database connection)")

        # Example 4: MySQL (conceptual - requires actual database)
        print("\n4. MySQL database operations (conceptual)...")
        # mysql_client = DBClient.create(
        #     "mysql",
        #     "mysql://user:password@localhost:3306/dbname",
        #     config,
        #     connection_string="mysql://user:password@localhost:3306/dbname",
        # )
        # await mysql_client.connect()
        # results = await mysql_client.execute_query("SELECT * FROM users")
        # await mysql_client.disconnect()
        print("   MySQL operations (requires actual database connection)")

        print("\n=== Database Examples Completed ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
