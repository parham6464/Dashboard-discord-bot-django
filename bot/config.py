from __future__ import annotations
from dotenv import load_dotenv
import os
from typing import Final


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


