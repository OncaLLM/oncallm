import sys
import os

# Add the project root directory to Python path so that oncallm module can be imported.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
