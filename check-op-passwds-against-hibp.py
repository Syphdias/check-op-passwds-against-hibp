#!/usr/bin/env python
from argparse import ArgumentParser
from subprocess import PIPE, Popen, check_output
from sys import stderr, stdout


def op_passwords(verbosity: int = 0) -> list[str]:
    """Gather lists in 1password via op CLI and return list of passwords"""

    if verbosity:
        print("Gathering all passwords...")

    op_items = Popen(
        ["op", "item", "list", "--categories", "Login", "--format=json"], stdout=PIPE
    )
    raw_passwords = check_output(
        ["op", "item", "get", "-", "--fields=password"], stdin=op_items.stdout
    )
    op_items.wait()

    return raw_passwords.decode().splitlines()


def main(args) -> None:
    passwords = op_passwords(args.verbosity)

    # insert faulty password to check if it is working
    if args.add_faulty:
        passwords.insert(0, "Test123")

    total_password_count = len(passwords)
    if args.verbosity:
        print(f"Number of passwords to test: {total_password_count}")

    passwords_tested = 0
    bad_passwords = []
    for password in passwords:
        # empty password is not interesting to test
        if not password:
            passwords_tested += 1
            continue

        # query Have I Been Pwned
        pwned = Popen([args.pwned_executable, "pw", password], stdout=PIPE, stderr=PIPE)
        out, err = pwned.communicate()

        if pwned.returncode != 0 or b"Oh no" in err:
            bad_passwords.append(
                (password, out.decode(), err.decode()),
            )
            if args.verbosity >= 3:
                print(out.decode(), file=stdout)
                print(err.decode(), file=stderr)

        passwords_tested += 1
        if args.verbosity and (
            passwords_tested % args.chunk_report_size == 0
            or passwords_tested == total_password_count
        ):
            print(f"{passwords_tested}/{total_password_count} passwords tested")

    if bad_passwords:
        print("Bad passwords:")
    for bad_password in bad_passwords:
        print(bad_password[0])
        if args.verbosity >= 2:
            print(bad_password[1])
            print(bad_password[2], file=stderr)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--pwned-executable",
        required=True,
        help="Path to pwned executable",
    )
    parser.add_argument(
        "--chunk-report-size",
        type=int,
        default=10,
        help="After which element count a status line is desplayed",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbosity",
        help="Increase verbosity",
    )
    parser.add_argument(
        "--add-faulty",
        action="store_true",
        default=False,
        help='Add Password "Test1234" which should always be a bad password',
    )

    args = parser.parse_args()
    main(args)
