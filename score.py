import json
import os

SCORES_FILE = "scores.json"

class Score:
    def __init__(self):
        self.current_score = 0
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as file:
                return json.load(file)
        return []

    def save_score(self):
        self.scores.append(self.current_score)
        self.scores.sort(reverse=True)
        with open(SCORES_FILE, "w") as file:
            json.dump(self.scores, file)

    def get_top_scores(self, limit=5):
        return self.scores[:limit]

    def increment_score(self, value):
        self.current_score += value

    def reset_score(self):
        self.current_score = 0
