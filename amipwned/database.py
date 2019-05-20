import asyncio
import mmap
import hashlib
import sys

import asyncpg

# mmap may be a better choice
def get_num_lines(file_path):
    with open(file_path, "r") as f:
        return len(f.readlines())


async def load(filename: str) -> None:
    """ Load passwords from file to database """

    pool = await asyncpg.create_pool("postgresql://postgres@localhost/amipwned", command_timeout=60)
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS dump(
                hash varchar PRIMARY KEY,
                plaintext varchar NOT NULL,
                created timestamp DEFAULT current_timestamp
            );
            CREATE TABLE IF NOT EXISTS used(
                fk_hash varchar,
                total INTEGER DEFAULT 0,
                FOREIGN KEY (fk_hash) REFERENCES dump (hash)
            );
            ''')

        # Sort and remove duplicates here
        # Use multiple asyncio tasks to load data into DB
        amount = get_num_lines(filename)
        with open(filename, "r", errors="ignore") as f:
            for count, pw in enumerate(f.readlines()):
                print(f"[+] Loading {count}/{amount-1}", end="\r", flush=True)
                sha256 = hashlib.sha224(pw.encode()).hexdigest()
                row = await conn.fetchrow('SELECT hash FROM dump WHERE hash = $1', sha256)
                if not row:
                    await conn.execute("INSERT INTO dump(hash, plaintext) VALUES($1, $2)", sha256, pw)
            print("\n[+] Done!")


