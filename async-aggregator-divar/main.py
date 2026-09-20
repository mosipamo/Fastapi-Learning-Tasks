import asyncio

from fastapi import FastAPI, HTTPException, Query

from sources import (
    fetch_chat_status,
    fetch_post,
    fetch_price_stats,
    fetch_reviews,
    fetch_seller,
    fetch_similar,
    fetch_view_count,
)


app = FastAPI()


VALID_SECTIONS = {
    "post",
    "seller",
    "similar",
    "price_stats",
    "chat",
}


async def aggregate_post(
    post_token: str,
    include_views: bool = False,
    include_reviews: bool = False,
    review_timeout_ms: int = 300,
):

    tasks = [
        fetch_post(post_token),
        fetch_seller(post_token),
        fetch_similar(post_token),
        fetch_price_stats(post_token),
        fetch_chat_status(post_token),
    ]

    if include_views:
        tasks.append(fetch_view_count(post_token))

    if include_reviews:
        review_timeout = review_timeout_ms / 1000

        tasks.append(
            asyncio.wait_for(
                fetch_reviews(post_token),
                timeout=review_timeout,
            )
        )

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True,
    )

    post = results[0]
    seller = results[1]
    similar = results[2]
    price_stats = results[3]
    chat = results[4]

    result = {
        "token": post_token,
        "found": post is not None,
        "post": post,
        "seller": seller,
        "similar": similar,
        "price_stats": price_stats,
        "chat": chat,
        "sources_count": 5,
    }

    index = 5

    if include_views:
        result["views"] = results[index]
        result["sources_count"] += 1
        index += 1

    if include_reviews:
        review_result = results[index]

        if isinstance(review_result, asyncio.TimeoutError):
            result["reviews"] = None
            result["degraded"] = ["reviews"]
        elif isinstance(review_result, Exception):
            result["reviews"] = None
            result["degraded"] = ["reviews"]
        else:
            result["reviews"] = review_result
            result["degraded"] = []

        result["sources_count"] += 1

    return result


@app.get("/")
async def health():
    return {
        "service": "divar-aggregator",
        "sources": 7,
    }


@app.get("/aggregate/{post_token}")
async def aggregate(
    post_token: str,
    sections: str | None = None,
    include_views: bool = False,
    include_reviews: bool = False,
    review_timeout_ms: int = 300,
):

    if review_timeout_ms <= 0:
        raise HTTPException(
            status_code=422,
            detail="review_timeout_ms must be positive",
        )

    selected_sections = None

    if sections is not None:
        selected_sections = [
            section.strip()
            for section in sections.split(",")
            if section.strip()
        ]

        if not selected_sections:
            raise HTTPException(
                status_code=422,
                detail="sections cannot be empty",
            )

        if any(section not in VALID_SECTIONS for section in selected_sections):
            raise HTTPException(
                status_code=422,
                detail="invalid section",
            )

    result = await aggregate_post(
        post_token=post_token,
        include_views=include_views,
        include_reviews=include_reviews,
        review_timeout_ms=review_timeout_ms,
    )

    if selected_sections is not None:
        filtered_result = {
            "token": result["token"],
            "found": result["found"],
            "sources_count": len(selected_sections),
        }

        for section in selected_sections:
            filtered_result[section] = result[section]

        if include_reviews:
            filtered_result["reviews"] = result["reviews"]
            filtered_result["degraded"] = result["degraded"]

        return filtered_result

    return result


@app.get("/batch")
async def batch(tokens: str = Query(min_length=1)):
    token_list = [
        token.strip()
        for token in tokens.split(",")
        if token.strip()
    ]

    if not token_list or len(token_list) > 5:
        raise HTTPException(
            status_code=422,
            detail="tokens must contain between 1 and 5 identifiers",
        )

    tasks = [
        aggregate_post(token)
        for token in token_list
    ]

    items = await asyncio.gather(*tasks)

    found_count = sum(
        1
        for item in items
        if item["found"]
    )

    return {
        "requested": len(token_list),
        "found_count": found_count,
        "items": items,
    }
