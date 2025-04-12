import argparse
import sys
from myder_core import list_providers, run_provider, build_docker

def main():
    parser = argparse.ArgumentParser(description="Myder Python CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("help", help="Show help")
    subparsers.add_parser("build", help="Build Docker image")
    parser_run = subparsers.add_parser("run", help="Run with provider")
    parser_run.add_argument("--model", type=str, help="Model name")
    parser_run.add_argument("--provider", type=str, help="Provider name")

    args = parser.parse_args()

    if args.command == "help" or args.command is None:
        parser.print_help()
        print("\nAvailable providers:", ", ".join(list_providers()))
    elif args.command == "build":
        build_docker()
    elif args.command == "run":
        if args.provider:
            run_provider(args.provider, model=args.model)
        else:
            print("No provider specified. Use --provider option.")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()