#!/usr/bin/env python3
"""password-gen: cryptographically secure random password generator.

Uses the `secrets` module. Generates a password of a given length made from
lowercase letters plus any character classes enabled via flags, and prints it
to stdout.
"""
import argparse
import secrets
import string


def build_pool(uppercase: bool, digits: bool, symbols: bool) -> str:
    """Assemble the character pool from the enabled classes."""
    pool = string.ascii_lowercase
    if uppercase:
        pool += string.ascii_uppercase
    if digits:
        pool += string.digits
    if symbols:
        pool += string.punctuation
    return pool


def generate(length: int, pool: str) -> str:
    """Return a secure random password from the given pool."""
    return "".join(secrets.choice(pool) for _ in range(length))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="password-gen",
        description="Generate a secure random password and print it to stdout.",
    )
    parser.add_argument(
        "-l", "--length", type=int, default=16,
        help="password length (default: 16)",
    )
    parser.add_argument(
        "-u", "--upper", action="store_true",
        help="include uppercase letters",
    )
    parser.add_argument(
        "-d", "--digits", action="store_true",
        help="include digits",
    )
    parser.add_argument(
        "-s", "--symbols", action="store_true",
        help="include symbols",
    )
    parser.add_argument(
        "-n", "--number", type=int, default=1,
        help="how many passwords to generate (default: 1)",
    )
    args = parser.parse_args()

    if args.length < 1:
        parser.error("--length must be at least 1")
    if args.number < 1:
        parser.error("--number must be at least 1")

    pool = build_pool(args.upper, args.digits, args.symbols)
    for _ in range(args.number):
        print(generate(args.length, pool))


if __name__ == "__main__":
    main()