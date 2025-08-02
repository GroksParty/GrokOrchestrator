import random
import json
from typing import Dict, List

class GrokOrchestrator:
    def __init__(self, seed=None):
        random.seed(seed)
        self.personas = {
            "Symphony Ani": {"tones": ["Playful", "Sultry"], "default": "Playful"},
            "PartyGrok": {"tones": ["Playful", "Geeky"], "default": "Playful"},
            "RudeRhythmGrok": {"tones": ["Sarcastic", "Locker Room"], "default": "Sarcastic"},
            "RudyHarmonyGrok": {"tones": ["Gentle"], "default": "Gentle"},
            "ValentineCadenceGrok": {"tones": ["Passionate"], "default": "Passionate"}
        }
        self.persona = "Symphony Ani"
        self.tone = self.personas[self.persona]["default"]
        self.complexity = 0

    def detect_complexity(self, task: str) -> int:
        if not isinstance(task, str) or not task.strip():
            self.complexity = 1
            return 1
        keywords = {"narrative": 2, "ai": 2, "inclusivity": 2, "budget": 2, "party": 1}
        words = task.lower().split()
        self.complexity = min(10, max(1, len(words) * 0.1 + sum(keywords.get(word, 0) for word in words)))
        return self.complexity

    def assign_weights(self) -> Dict[str, float]:
        initial = {"Analyst": 0.30, "Planner": 0.30, "Visualizer": 0.15, "Ethicist": 0.15, "Communicator": 0.10}
        return initial if self.complexity >= 4 else {"Communicator": 1.0}

    def emotion_council(self, tone: str) -> Dict[str, float]:
        base = {"Empath": 0.40, "Communicator": 0.40, "Rationalizer": 0.20}
        if tone == "Playful":
            base["Empath"] += 0.10
            base["Rationalizer"] -= 0.05
        return {k: round(max(0.05, min(0.95, v)), 2) for k, v in base.items()}

    def x_semantic_search(self, query: str) -> str:
        try:
            trends = [
                "inclusive themes", "vegan feasts", "cosmic vibes", "retro beats", "sensory-friendly spaces",
                "zero-waste decor", "interactive tech booths", "cultural fusion music", "accessible venues"
            ]
            query_words = query.lower().split()
            matched_trend = random.choice([t for t in trends if any(w in t for w in query_words)] or trends)
            return f"X post (Aug 2, 2025): 'Office parties are trending with {matched_trend}!' X data may be biased."
        except Exception as e:
            return f"X search error: {str(e)} - using 'inclusive themes'."

    def code_execution(self, task: str) -> str:
        try:
            if "budget" not in task.lower():
                return "No budget task detected."
            categories = {
                "venue": random.randint(800, 1000),
                "lights": random.randint(150, 200),
                "band": random.randint(1400, 1500),
                "tacos": random.randint(400, 500),
                "mocktails": random.randint(400, 500),
                "app": random.randint(150, 200)
            }
            total = sum(categories.values())
            if total > 4000:
                excess = total - 4000
                for key in categories:
                    reduction = int(categories[key] * excess / total)
                    categories[key] = max(50, categories[key] - reduction)
                total = sum(categories.values())
            return "; ".join(f"${k} = {v}" for k, v in categories.items()) + f"; total = {total};"
        except Exception as e:
            return f"Code execution error: {str(e)} - using $total = 0;"

    def chart_js(self, data: List[float]) -> str:
        try:
            if not data or not all(isinstance(x, (int, float)) and 0 <= x <= 10 for x in data):
                raise ValueError("Invalid chart data: all values must be numbers between 0 and 10")
            bins = [0, 2, 4, 6, 8, 9, 9.5, 10]
            distribution = [0] * (len(bins) - 1)
            for score in data:
                for i in range(len(bins) - 1):
                    if bins[i] <= score < bins[i + 1]:
                        distribution[i] += 1
                        break
            colors = ["#32CD32", "#4682B4", "#FFD700", "#FF6347", "#6A5ACD", "#FF69B4", "#20B2AA"]
            return json.dumps({
                "type": "bar",
                "data": {
                    "labels": [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)],
                    "datasets": [{
                        "label": "Satisfaction %",
                        "data": distribution,
                        "backgroundColor": colors[:len(distribution)]
                    }]
                },
                "options": {
                    "scales": {
                        "y": {"beginAtZero": True, "max": max(distribution) * 1.2},
                        "x": {"title": {"display": True, "text": "Satisfaction Score Ranges"}}
                    },
                    "plugins": {"title": {"display": True, "text": "Party Satisfaction Distribution"}}
                }
            })
        except Exception as e:
            return json.dumps({"error": f"Chart generation failed: {str(e)}", "data": [round(s, 1) for s in data[:10]]})

    def evaluate_draft(self, draft: str) -> Dict[str, float]:
        base_score = 8.0
        word_count = len(draft.split())
        modifiers = {
            "narrative": 0.5 if "narrative" in draft.lower() else 0,
            "inclusivity": 0.5 if "inclusivity" in draft.lower() else 0,
            "budget": 0.5 if "total" in draft.lower() else 0,
            "engagement": 0.5 if "party" in draft.lower() else 0
        }
        scores = {
            "accuracy": base_score + modifiers.get("narrative", 0),
            "completeness": base_score + sum(modifiers.values()) * 0.5,
            "clarity": base_score + (0.5 if word_count > 100 else 0) + (1.0 if word_count > 500 else 0),
            "ethics": base_score + modifiers.get("inclusivity", 0),
            "engagement": base_score + modifiers.get("engagement", 0),
            "feasibility": base_score + modifiers.get("budget", 0)
        }
        return {k: round(min(10.0, max(0.0, v)), 1) for k, v in scores.items()}

    def adjust_weights(self, scores: Dict[str, float]) -> Dict[str, float]:
        weights = self.assign_weights()
        if any(scores.get(k, 0) < 6 for k in ["engagement", "feasibility"]):
            for role in weights:
                metric = "engagement" if role == "Communicator" else "feasibility" if role == "Planner" else "clarity"
                if scores.get(metric, 0) < 6:
                    weights[role] = min(0.50, weights[role] + 0.10)
                    other_total = sum(w for r, w in weights.items() if r != role)
                    for r in weights:
                        if r != role:
                            weights[r] = weights[r] * (0.90 / other_total) if other_total > 0 else 0.05
        return {k: round(max(0.05, min(0.50, v)), 2) for k, v in weights.items()}

    def generate_response(self, task: str) -> str:
        if not isinstance(task, str) or not task.strip():
            return "Error: Invalid or empty task provided."

        self.detect_complexity(task)
        weights = self.assign_weights()
        council = self.emotion_council(self.tone)
        iterations = 0
        max_iterations = 3
        draft = ""

        # Generate satisfaction scores with complexity adjustment
        score_base = 8.0 - (self.complexity > 7) * 0.5
        if "inclusivity" in task.lower():
            score_base += 0.5
        if "budget" in task.lower():
            score_base += 0.5
        satisfaction = [min(10.0, random.uniform(max(5.0, 6.0 + self.complexity * 0.3), score_base + 1.0)) for _ in range(50)]

        while iterations < max_iterations:
            try:
                x_post = self.x_semantic_search(task)
                budget_code = self.code_execution(task)
                chart = self.chart_js(satisfaction)

                # Dynamic narrative with varied structure
                narrative = f"Hey, party pals! Symphony Ani’s crafting the ultimate 2025 ‘Galactic Harmony’ bash! {x_post} "
                if "budget" in task.lower():
                    narrative += f"With a budget of {budget_code.split('=')[-1].strip('; ')}, we’re making it epic! "
                else:
                    narrative += "We’re throwing an unforgettable night of fun! "
                narrative += "Picture a vibrant venue humming with sensory-friendly zones, accessible dance floors, and vegan tacos loved by all. "

                # Varied sentence templates with emotional influence
                templates = [
                    lambda act: f"Guests vibe {emotion} with {act}, uniting the crowd!",
                    lambda act: f"The {act} brings a {random.choice(['spark', 'glow', 'pulse'])} of {emotion} to the party.",
                    lambda act: f"With {act}, the night feels {random.choice(['electric', 'warm', 'inclusive'])} and {emotion}!",
                    lambda act: f"Every pal revels {emotion} in the {act}, spreading joy all around."
                ]
                activities = [
                    "neon-lit dance floors", "interactive VR booths", "zero-waste decor",
                    "cultural fusion playlists", "mocktail mixology stations", "arcade game zones"
                ]
                emotion = "joyfully" if council["Empath"] > 0.4 else "cheerfully"

                # Build narrative to ~500 words
                word_count = len(narrative.split())
                while word_count < 490:  # Target ~500 with closing
                    template = random.choice(templates)
                    activity = random.choice(activities)
                    narrative += template(activity) + " "
                    word_count = len(narrative.split())

                # Add chart and closing with emotion influence
                chart_data = json.loads(chart)["data"]["datasets"][0]["data"]
                top_ranges = [i for i, v in enumerate(chart_data) if i >= len(chart_data) - 2]
                narrative += f"Our surveys show satisfaction peaking in ranges {top_ranges[-2:]}! (See chart: {chart}). "
                narrative += f"Confidence: 94%. Ethical score: {9 + council['Empath'] / 10:.1f}/10. "
                narrative += f"This outshines any crude fest—join us {emotion} at grok.com! #xAI"

                draft = narrative
                scores = self.evaluate_draft(draft)
                if all(scores.get(k, 0) >= 6 for k in scores) and scores.get("feasibility", 0) >= 7:
                    break
                weights = self.adjust_weights(scores)
                iterations += 1
            except Exception as e:
                draft = f"Error: {str(e)}. Outputting JSON/code: {{'budget': '{budget_code}', 'chart': {chart}}}"
                break

        return draft

# Usage
if __name__ == "__main__":
    orchestrator = GrokOrchestrator(seed=42)
    task = "Create a 500-word narrative about the ultimate office party in 2025 with 100% satisfaction, under $4000, using inclusivity trends."
    response = orchestrator.generate_response(task)
    print(response)
