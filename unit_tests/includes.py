# add path ../engine ../admin ../apis ../web to sys.path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'apis')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'admin')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine', 'core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine', 'models')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine', 'utils')))