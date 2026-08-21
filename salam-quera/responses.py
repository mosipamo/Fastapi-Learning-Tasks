from data import SERVICES, TEAM_NAME, TEAM_MEMBERS


def welcome_payload() -> dict:
    return {"app": "quera-hello", "message": "به سامانهٔ خوش‌آمدگویی کوئرا خوش آمدید!"}


def health_payload() -> dict:
    return {"status": "ok"}


def info_payload() -> dict:
    return {"service": "quera-hello", "version": "1.0.0", "language": "fa"}


def ping_payload() -> dict:
	return {"ping": "pong"}


def team_payload() -> dict:
    return {"team": TEAM_NAME, "members": [member["name"] for member in TEAM_MEMBERS]}


def services_payload() -> list:
    return SERVICES


def stats_payload() -> dict:
    return {"members": len(TEAM_MEMBERS), "services": len(SERVICES), "healthy_services": len([s for s in SERVICES if s["healthy"]]), "all_healthy": all(s["healthy"] for s in SERVICES)}
