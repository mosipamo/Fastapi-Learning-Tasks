users: list[dict] = [
    {
    	"id": 1,
    	"name": "Sara",
    	"tier": "premium",
    	"age": 30,
    },
    {
    	"id": 2,
    	"name": "Kaveh",
    	"tier": "free",
    	"age": 17,
    },
    {
    	"id": 3,
    	"name": "Negar",
    	"tier": "free",
    	"age": 25,
    },
    {
    	"id": 4,
    	"name": "Arian",
    	"tier": "premium",
    	"age": 16,
    },
    {
    	"id": 5,
    	"name": "Bahar",
    	"tier": "free",
    	"age": 22,
    },
]

movies: list[dict] = [
	{
		"id": 10,
		"title": "Quera Origins",
		"required_tier": "free",
		"min_age": 0,
		"regions": ["IR", "EU"],
	},
	{
		"id": 11,
		"title": "Midnight in Tehran",
		"required_tier": "premium",
		"min_age": 0,
		"regions": ["IR"],
	},
	{
		"id": 12,
		"title": "The Last Algorithm",
		"required_tier": "premium",
		"min_age": 18,
		"regions": ["IR", "EU"],
	},
	{
		"id": 13,
		"title": "Sahar Sunrise",
		"required_tier": "free",
		"min_age": 13,
		"regions": ["IR"],
	},
]


def find_user(user_id: int) -> dict | None:
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def find_movie(movie_id: int) -> dict | None:
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None
