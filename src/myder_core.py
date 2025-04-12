import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import importlib
import os

PROVIDER_DIR = os.path.join(os.path.dirname(__file__), "provider")

def list_providers():
    providers = []
    for fname in os.listdir(PROVIDER_DIR):
        if fname.endswith(".py") and fname != "__init__.py":
            providers.append(fname[:-3])
    return providers

def load_provider(name):
    module = importlib.import_module(f"provider.{name}")
    return module.Provider()

def run_provider(provider_name, model=None):
    provider = load_provider(provider_name)
    return provider.run(model)

def build_docker():
    import os
    return os.system("docker build -t myder .")