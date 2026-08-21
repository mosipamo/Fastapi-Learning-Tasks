TEAM_NAME = "infrastructure"

TEAM_MEMBERS: list = [
    {"name": "nazanin", "role": "backend"},
    {"name": "kaveh", "role": "devops"},
    {"name": "yasaman", "role": "sre"}
]

SERVICES: list = [
    {"name": "status-board", "healthy": True},
    {"name": "metrics", "healthy": True},
    {"name": "notifier", "healthy": False}
]
