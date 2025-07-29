#!/usr/bin/env python3
"""
Main entry point for running Convo programs
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from convo.__main__ import main

if __name__ == '__main__':
    main()
