import asyncio
from impo.db import Base,s_engine,a_engine
async def main():
    Base.metadata.create_all(s_engine)
    async with a_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
if __name__ == '__main__':
    asyncio.run(main())