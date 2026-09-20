import asyncio
from unicodedata import category

SOURCE_DELAY = 0.2
SLOW_SOURCE_DELAY = 0.5

POSTS = {
    "QP-1001": {
        "token": "QP-1001",
        "title": "Pride 1396 White",
        "city": "Tehran",
        "price": 4250000000,
        "category": "vehicles",
    },
    "QP-1002": {
        "token": "QP-1002",
        "title": "MacBook Air M2 2023",
        "city": "Shiraz",
        "price": 980000000,
        "category": "electronics",
    },
    "QP-1003": {
        "token": "QP-1003",
        "title": "Two Bedroom Apartment 95m",
        "city": "Mashhad",
        "price": 18500000000,
        "category": "real-estate",
    },
}

SELLERS = {
    "QP-1001": {
        "name": "Kaveh",
        "member_since": 2019,
        "active_posts": 3,
        "is_verified": True,
    },
    "QP-1002": {
        "name": "Yasaman",
        "member_since": 2021,
        "active_posts": 1,
        "is_verified": False,
    },
    "QP-1003": {
        "name": "Mehrshad",
        "member_since": 2017,
        "active_posts": 7,
        "is_verified": True,
    },
}

SIMILAR = {
    "QP-1001": ["QP-1101", "QP-1102", "QP-1103"],
    "QP-1002": ["QP-1201", "QP-1202"],
    "QP-1003": ["QP-1301", "QP-1302", "QP-1303", "QP-1304"],
}

PRICE_STATS = {
    "vehicles": {
        "min": 3800000000,
        "avg": 4600000000,
        "max": 6100000000,
    },
    "electronics": {
        "min": 720000000,
        "avg": 1050000000,
        "max": 1600000000,
    },
    "real-estate": {
        "min": 12000000000,
        "avg": 19500000000,
        "max": 31000000000,
    },
}

VIEW_COUNTS = {
    "QP-1001": 1840,
    "QP-1002": 970,
    "QP-1003": 3120,
}

REVIEWS = {
    "QP-1001": {
        "count": 42,
        "average": 4.3,
    },
    "QP-1002": {
        "count": 11,
        "average": 4.8,
    },
    "QP-1003": {
        "count": 67,
        "average": 3.9,
    },
}


async def fetch_post(post_token: str) -> dict | None:
    await asyncio.sleep(SOURCE_DELAY)

    return POSTS.get(post_token)


async def fetch_seller(post_token: str) -> dict | None:
    await asyncio.sleep(SOURCE_DELAY)

    return SELLERS.get(post_token)


async def fetch_similar(post_token: str) -> list[str]:
    await asyncio.sleep(SOURCE_DELAY)

    similar = SIMILAR.get(post_token, [])

    return similar


async def fetch_price_stats(post_token: str) -> dict | None:
    await asyncio.sleep(SOURCE_DELAY)

    post = POSTS.get(post_token)

    if post is None:
        return None

    category = post["category"]
    return PRICE_STATS.get(category)


async def fetch_chat_status(post_token: str) -> dict:
    await asyncio.sleep(SOURCE_DELAY)

    return {
        "chat_enabled": post_token in POSTS,
        "unread": 0,
    }


async def fetch_view_count(post_token: str) -> int:
    await asyncio.sleep(SOURCE_DELAY)

    return VIEW_COUNTS.get(post_token, 0)


async def fetch_reviews(post_token: str) -> dict | None:
    await asyncio.sleep(SLOW_SOURCE_DELAY)

    return REVIEWS.get(post_token)
