import asyncio
import hashlib
import sys

import psycopg2
from psycopg2 import OperationalError
import asyncpg
from asyncpg.pool import Pool


class Database():

    def __init__(self, db: dict):
        self.user = db.get("username")
        self.password = db.get("password")
        self.host = db.get("host")
        self.port = db.get("port")
        self.database = db.get("name")


    @staticmethod
    def get_num_lines(file_path: str) -> int:
        """ Return the amount of lines within a given file """
        # mmap may be a better choice
        try:
            with open(file_path, "r") as f:
                return len(f.readlines())
        except OSError as e:
            print(f"[-] Error opening file: {e}")
            sys.exit(1)


    async def get_pool(self) -> Pool:
        """ Acquire pool object for interacting with DB """
        pool = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            command_timeout=60,
        )

        return pool


    def init_db(self) -> None:
        """ Sync. method for initializing DB """
        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database)
        except OperationalError as e:
            print(f"[-] Error connecting to DB: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute('''
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
        conn.commit()
        conn.close()

    async def init_db_async(self) -> None:
        """ Async. method for initializing DB """
        pool = await self.get_pool()
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

    async def load(self, filename: str) -> None:
        """ Async Load passwords from file to database """
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            # Sort and remove duplicates here?
            # Use multiple asyncio tasks to load data into DB?
            amount = self.get_num_lines(filename)
            with open(filename, "r", errors="ignore") as f:
                for count, pw in enumerate(f.readlines()):
                    print(f"[+] Loading {count}/{amount-1}", end="\r", flush=True)
                    sha256 = hashlib.sha224(pw.encode()).hexdigest()
                    row = await conn.fetchrow('SELECT hash FROM dump WHERE hash = $1', sha256)
                    if not row:
                        await conn.execute("INSERT INTO dump(hash, plaintext) VALUES($1, $2)", sha256, pw)
                print("\n[+] Done!")


