Script to test all 1Password passwords against Have I Been Pwned.

It uses the official [op] command from 1Password (required to be set up
beforehand) to look up passwords and the unofficial tool [pwned] to check
against Have I Been Pwned database.

## Example
```sh
❯ ./check-op-passwds-against-hibp.py --pwned-executable ~/.npm/_npx/6adee5baa5ad468a/node_modules/.bin/pwned --add-faulty
Bad passwords:
Test123
```

[op]: https://1password.com/de/downloads/command-line/
[pwned]: https://github.com/wKovacs64/pwned
