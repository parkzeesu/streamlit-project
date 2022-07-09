import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils import project_def as pfd

def app():
    pfd.app()
