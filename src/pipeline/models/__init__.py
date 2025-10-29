import os
import importlib

# Get the directory of the current file
models_dir = os.path.dirname(__file__)
__all__ = []

# Iterate over all files in the models directory
for filename in os.listdir(models_dir):
    # Check if the file is a Python file and not __init__.py
    if filename.endswith('.py') and filename != '__init__.py':
        # Get the module name by removing the .py extension
        module_name = filename[:-3]

        # Dynamically import the module
        module = importlib.import_module(f'.{module_name}', package=__name__)

        # Add all public attributes from the module to __all__
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                globals()[attr_name] = getattr(module, attr_name)
                if attr_name not in __all__:
                    __all__.append(attr_name)
