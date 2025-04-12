import argparse
import importlib
import os
import sys

PROVIDER_DIR = os.path.join(os.path.dirname(__file__), "provider")

def list_providers():
    providers = []
    for fname in os.listdir(PROVIDER_DIR):
        if fname.endswith(".py") and fname != "__init__.py":
            providers.append(fname[:-3])
    return providers

def load_provider(name):
    try:
        module = importlib.import_module(f"provider.{name}")
        return module.Provider()
    except Exception as e:
        print(f"Provider load error: {e}")
        sys.exit(1)

def build():
    os.system("docker build -t myder .")

def run(model=None, provider_name=None):
    if provider_name:
        provider = load_provider(provider_name)
        provider.run(model)
    else:
        print("No provider specified. Use --provider option.")

def main():
    parser = argparse.ArgumentParser(description="Myder Python CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_help = subparsers.add_parser("help", help="Show help")
    parser_build = subparsers.add_parser("build", help="Build Docker image")
    parser_run = subparsers.add_parser("run", help="Run with provider")
    parser_run.add_argument("--model", type=str, help="Model name")
    parser_run.add_argument("--provider", type=str, help="Provider name")

    args = parser.parse_args()

    if args.command == "help" or args.command is None:
        parser.print_help()
        print("\nAvailable providers:", ", ".join(list_providers()))
    elif args.command == "build":
        build()
    elif args.command == "run":
        run(model=args.model, provider_name=args.provider)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()