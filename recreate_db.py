import asyncio
from main import engine, Base

async def recreate_tables():
    """Drop all tables and recreate them with new schema"""
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        print("✓ Dropped all tables")

        # Create all tables with new schema
        await conn.run_sync(Base.metadata.create_all)
        print("✓ Created all tables with new schema")

if __name__ == "__main__":
    asyncio.run(recreate_tables())
    print("\n✓ Database recreated successfully!")
