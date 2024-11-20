import json
import os

SCORES_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as file:
            return json.load(file)
    return []

def save_score(score):
    scores = load_scores()
    scores.append(score)
    scores.sort(reverse=True)
    with open(SCORES_FILE, "w") as file:
        json.dump(scores, file)

def get_top_scores(limit=5):
    scores = load_scores()
    return scores[:limit]
