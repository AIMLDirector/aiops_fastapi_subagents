# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # MUST be first

ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_INDEX = os.getenv("ELASTIC_INDEX")

if not ELASTIC_URL:
    raise RuntimeError("ELASTIC_URL is not set")

if not ELASTIC_INDEX:
    raise RuntimeError("ELASTIC_INDEX is not set")

# Normalize
ELASTIC_URL = ELASTIC_URL.rstrip("/")