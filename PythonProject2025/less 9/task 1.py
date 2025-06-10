import requests
from statistics import mean

BASE_URL = "https://jsonplaceholder.typicode.com"

class Post:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body

class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def average_title_length(self) -> float:
        return mean(len(p.title) for p in self.posts) if self.posts else 0.0

    def average_body_length(self) -> float:
        return mean(len(p.body) for p in self.posts) if self.posts else 0.0

class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []

    def fetch_data(self):
        try:
            users_resp = requests.get(f"{BASE_URL}/users")
            users_resp.raise_for_status()
            users_data = users_resp.json()
        except Exception as e:
            print("Error fetching users:", e)
            return

        for u in users_data:
            user = User(u["id"], u["name"])
            try:
                posts_resp = requests.get(f"{BASE_URL}/posts", params={"userId": user.id})
                posts_resp.raise_for_status()
                for p in posts_resp.json():
                    user.add_post(Post(p["id"], p["title"], p["body"]))
            except Exception as e:
                print(f"Error fetching posts for user {user.id}:", e)
            self.users.append(user)

    def user_with_longest_average_body(self) -> User:
        return max(self.users, key=lambda u: u.average_body_length(), default=None)

    def users_with_many_long_titles(self) -> list[User]:
        return [
            u for u in self.users
            if sum(1 for p in u.posts if len(p.title) > 40) > 5
        ]

if __name__ == "__main__":
    ba = BlogAnalytics()
    ba.fetch_data()
    top = ba.user_with_longest_average_body()
    print(f"User with longest avg post body: {top.name} ({top.average_body_length():.1f} chars)")
    many = ba.users_with_many_long_titles()
    print("Users with >5 long titles:", [u.name for u in many])