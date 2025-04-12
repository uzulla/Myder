import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import importlib

PROVIDER_DIR = os.path.join(os.path.dirname(__file__), "provider")

def list_providers():
    providers = []
    for fname in os.listdir(PROVIDER_DIR):
        if fname.endswith(".py") and fname != "__init__.py":
            providers.append(fname[:-3])
    return providers

import inspect

def load_provider(name, api_key):
    module = importlib.import_module(f"provider.{name.lower()}")
    provider_class = None
    for _, cls in inspect.getmembers(module, inspect.isclass):
        if cls.__module__ == module.__name__:
            provider_class = cls
            break
    if provider_class is None:
        raise ImportError(f"No valid provider class found in module 'provider.{name.lower()}'")
    return provider_class(api_key)

def run_provider(provider_name, api_key, model=None):
    provider = load_provider(provider_name, api_key)
    return provider.run(model)

def build_docker():
    import os
    return os.system("docker build -t myder .")