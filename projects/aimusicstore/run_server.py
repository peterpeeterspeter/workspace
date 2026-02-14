#!/usr/bin/env python3
"""
Startup script for aimusicstore API.
Run this from the project root directory.
"""

import sys
import os
from pathlib import Path

# Add api directory to Python path
api_dir = Path(__file__).parent / 'api'
sys.path.insert(0, str(api_dir))

# Set environment
os.chdir(Path(__file__).parent)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"Starting aimusicstore API on {host}:{port}")
    print(f"API docs: http://{host}:{port}/docs")
    
    uvicorn.run("main:app", host=host, port=port)
