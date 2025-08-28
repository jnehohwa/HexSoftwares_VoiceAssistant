#!/usr/bin/env python3
"""
HexSoftwares Voice Assistant GUI Launcher
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from voice_assistant.gui import main
    main()
except ImportError as e:
    print(f"Error: {e}")
    print("Make sure you have installed the requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error launching GUI: {e}")
    sys.exit(1)
