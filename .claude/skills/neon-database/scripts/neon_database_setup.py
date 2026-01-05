#!/usr/bin/env python3
"""
Neon Database Setup Script

This script provides utilities for setting up and managing Neon PostgreSQL databases
with FastAPI applications. It includes functions for connection testing, 
table creation, and basic configuration.
"""

import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NeonDatabaseManager:
    def __init__(self, database_url=None):
        """
        Initialize the Neon Database Manager
        
        Args:
            database_url (str): PostgreSQL connection string for Neon
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL must be provided either as parameter or environment variable")
        
        # Create async engine
        self.engine = create_async_engine(
            self.database_url,
            echo=False,  # Set to True for debugging
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10
        )
    
    async def test_connection(self):
        """
        Test the database connection
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("✅ Successfully connected to Neon database")
            return True
        except SQLAlchemyError as e:
            print(f"❌ Database connection failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during connection: {e}")
            return False
    
    async def create_table_from_sql(self, sql_query):
        """
        Execute a SQL query to create a table
        
        Args:
            sql_query (str): SQL query to execute
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text(sql_query))
                await conn.commit()
            print("✅ Table created successfully")
            return True
        except SQLAlchemyError as e:
            print(f"❌ Error creating table: {e}")
            return False
    
    async def run_query(self, query, params=None):
        """
        Execute a SELECT query and return results
        
        Args:
            query (str): SQL query to execute
            params (dict): Optional parameters for the query
        
        Returns:
            list: Query results
        """
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text(query), params or {})
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]
        except SQLAlchemyError as e:
            print(f"❌ Error executing query: {e}")
            return []
    
    async def close(self):
        """Close the database engine"""
        await self.engine.dispose()


async def main():
    """
    Main function demonstrating Neon database operations
    """
    print("🚀 Neon Database Setup Utility")
    print("=" * 40)
    
    # Initialize the database manager
    try:
        db_manager = NeonDatabaseManager()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set DATABASE_URL environment variable or pass it as parameter")
        return
    
    # Test the connection
    print("\n1. Testing database connection...")
    connection_ok = await db_manager.test_connection()
    
    if not connection_ok:
        print("Cannot proceed without database connection.")
        return
    
    # Example: Create a simple users table
    print("\n2. Creating example 'users' table...")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    await db_manager.create_table_from_sql(create_table_sql)
    
    # Example: Insert a test user
    print("\n3. Inserting test data...")
    try:
        async with AsyncSession(db_manager.engine) as session:
            await session.execute(
                text("INSERT INTO users (name, email) VALUES (:name, :email) ON CONFLICT DO NOTHING"),
                {"name": "Test User", "email": "test@example.com"}
            )
            await session.commit()
            print("✅ Test user inserted (or already exists)")
    except SQLAlchemyError as e:
        print(f"❌ Error inserting test data: {e}")
    
    # Example: Query the data
    print("\n4. Querying test data...")
    results = await db_manager.run_query("SELECT * FROM users LIMIT 10")
    
    if results:
        print("📋 Retrieved data:")
        for row in results:
            print(f"   ID: {row['id']}, Name: {row['name']}, Email: {row['email']}, Created: {row['created_at']}")
    else:
        print("   No data found")
    
    # Close the connection
    await db_manager.close()
    print("\n✅ Database operations completed")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())