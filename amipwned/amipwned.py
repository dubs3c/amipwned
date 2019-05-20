import asyncio
import argparse
import os
import sys

from amipwned.config import Config
from amipwned.daemon import Daemon
from amipwned import database
from amipwned.web_service import get_app, web


def banner():
    return """
 ▄▄▄       ██▀███  ▓█████    ▓██   ██▓ ▒█████   █    ██     ██▓███   █     █░███▄    █ ▓█████ ▓█████▄ 
▒████▄    ▓██ ▒ ██▒▓█   ▀     ▒██  ██▒▒██▒  ██▒ ██  ▓██▒   ▓██░  ██▒▓█░ █ ░█░██ ▀█   █ ▓█   ▀ ▒██▀ ██▌
▒██  ▀█▄  ▓██ ░▄█ ▒▒███        ▒██ ██░▒██░  ██▒▓██  ▒██░   ▓██░ ██▓▒▒█░ █ ░█▓██  ▀█ ██▒▒███   ░██   █▌
░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄      ░ ▐██▓░▒██   ██░▓▓█  ░██░   ▒██▄█▓▒ ▒░█░ █ ░█▓██▒  ▐▌██▒▒▓█  ▄ ░▓█▄   ▌
 ▓█   ▓██▒░██▓ ▒██▒░▒████▒     ░ ██▒▓░░ ████▓▒░▒▒█████▓    ▒██▒ ░  ░░░██▒██▓▒██░   ▓██░░▒████▒░▒████▓ 
 ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░      ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒    ▒▓▒░ ░  ░░ ▓░▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒▒▓  ▒ 
  ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░    ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░    ░▒ ░       ▒ ░ ░ ░ ░░   ░ ▒░ ░ ░  ░ ░ ▒  ▒ 
  ░   ▒     ░░   ░    ░       ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░    ░░         ░   ░    ░   ░ ░    ░    ░ ░  ░ 
      ░  ░   ░        ░  ░    ░ ░         ░ ░     ░                     ░            ░    ░  ░   ░    
                              ░ ░                                                              ░      
"""


class Balthazar(Daemon):
    def __init__(self, *args, **kwargs):
        super(Balthazar, self).__init__(*args, **kwargs)
        self.port = 8000

    def run(self):
        loop = asyncio.get_event_loop()
        app = loop.run_until_complete(get_app())
        web.run_app(app, port=8000)


def main():
    print(f"\n{banner()}")
    parser = argparse.ArgumentParser(
        prog="amipwned",
        description=f"Self-hosted service for checking if a given password \
            has been recorded in public password dumps. Created by @dubsec",
    )
    parser.add_argument(
        "--web",
        choices=["start", "stop", "restart"],
        help="Control the amipwned web service",
    )
    parser.add_argument(
        "--load", action="store", dest="filename", help="Stop the amipwned web service"
    )
    parser.add_argument(
        "--port",
        action="store",
        dest="port",
        type=int,
        help="Listening port for the web service",
    )
    parser.add_argument(
        "--config",
        action="store",
        dest="config",
        type=int,
        help="Configuration file location",
    )
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        quit()

    if args.web:
        
        config = Config()
        if not config.location():
            print(f"[-] Could not read configuration file at {config.filename}, does it exist?")
            sys.exit(1)

        d = Balthazar(f"/var/run/user/{os.getuid()}/amipwned.pid")
        if args.port:
            d.port = args.port

        if args.web == "start":
            d.start()
        elif args.web == "stop":
            d.stop()
        elif args.web == "restart":
            d.restart()

    if args.filename:
        print(f"[+] Loading {args.filename} into database...")
        asyncio.run(database.load(args.filename))
