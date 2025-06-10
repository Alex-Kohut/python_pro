import requests
import json
from collections import Counter, defaultdict

BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

    def to_dict(self):
        return vars(self)

class CommentModerator:
    def __init__(self):
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []

    def fetch_comments(self):
        try:
            resp = requests.get(f"{BASE_URL}/comments")
            resp.raise_for_status()
            for c in resp.json():
                if all(k in c for k in ("id","postId","name","email","body")):
                    self.comments.append(Comment(c["id"], c["postId"], c["name"], c["email"], c["body"]))
        except Exception as e:
            print("Error fetching comments:", e)

    def flag_suspicious_comments(self):
        keywords = {"buy", "free", "offer"}
        for c in self.comments:
            body_low = c.body.lower()
            if any(word in body_low for word in keywords) or "!!!" in c.body:
                self.flagged_comments.append(c)

    def group_by_post(self) -> dict[int, list[Comment]]:
        grouped = defaultdict(list)
        for c in self.flagged_comments:
            grouped[c.post_id].append(c)
        return grouped

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        emails = [c.email for c in self.flagged_comments]
        return [email for email, _ in Counter(emails).most_common(n)]

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.flagged_comments], f, indent=2)

if __name__ == "__main__":
    cm = CommentModerator()
    cm.fetch_comments()
    cm.flag_suspicious_comments()
    by_post = cm.group_by_post()
    print("Flagged per post:", {pid: len(lst) for pid, lst in by_post.items()})
    print("Top spammy emails:", cm.top_spammy_emails())
    cm.export_flagged_to_json()
    print("Flagged comments saved to flagged_comments.json")