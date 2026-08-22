accounts: dict[str, dict] = {}


def has_user(username: str) -> bool:
    return username in accounts


def add_account(account: dict) -> None:
    accounts[account["username"]] = account


def get_account(username: str) -> dict | None:
    return accounts.get(username)


def count_accounts() -> int:
    return len(accounts)


def find_usernames(prefix: str | None = None) -> list[str]:
    if prefix is None:
        return list(accounts.keys())
    return [username for username in accounts if username.startswith(prefix)]
