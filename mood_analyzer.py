# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)
        self.extra_positive_words = {
            "hopeful",
            "proud",
            "glad",
            ":)",
            "😂",
        }
        self.extra_negative_words = {
            "meh",
            "ugh",
            "annoying",
            "drained",
            ":(",
            "🥲",
        }
        self.negation_words = {"not", "never", "no"}
        self.positive_signals = self.positive_words | self.extra_positive_words
        self.negative_signals = self.negative_words | self.extra_negative_words

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Current preprocessing:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Normalizes repeated characters ("soooo" -> "soo")
          - Tokenizes words plus a few emojis/emoticons
        """
        cleaned = text.strip().lower()
        # Shrink exaggerated spellings like "soooo" to something closer to the base word.
        cleaned = re.sub(r"(.)\1{2,}", r"\1\1", cleaned)
        tokens = re.findall(r"[:;]-?[)(]|[a-z']+|[😂🥲💀]", cleaned)

        return tokens

    def _analyze_tokens(self, tokens: List[str]) -> Tuple[int, List[str], List[str]]:
        """
        Return a score plus the positive and negative signals that were matched.
        """
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        i = 0

        while i < len(tokens):
            token = tokens[i]
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None

            # Treat simple negation as flipping the next sentiment word.
            if token in self.negation_words and next_token is not None:
                if next_token in self.positive_signals:
                    score -= 1
                    negative_hits.append(f"{token} {next_token}")
                    i += 2
                    continue

                if next_token in self.negative_signals:
                    score += 1
                    positive_hits.append(f"{token} {next_token}")
                    i += 2
                    continue

            if token in self.positive_signals:
                score += 1
                positive_hits.append(token)
            elif token in self.negative_signals:
                score -= 1
                negative_hits.append(token)

            i += 1

        return score, positive_hits, negative_hits

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Current improvements include:
          - Simple negation handling such as "not happy" or "not bad"
          - Extra slang / emoji / emoticon signals
          - Counting repeated matched signals across the text
        """
        tokens = self.preprocess(text)
        score, _, _ = self._analyze_tokens(tokens)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Current mapping:
          - If both positive and negative signals are present, return "mixed"
            unless the score is strongly positive or strongly negative.
          - Otherwise, score > 0 -> "positive"
          - score < 0 -> "negative"
          - score == 0 -> "neutral"
        """
        tokens = self.preprocess(text)
        score, positive_hits, negative_hits = self._analyze_tokens(tokens)

        if positive_hits and negative_hits:
            if score > 1:
                return "positive"
            if score < -1:
                return "negative"
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        The explanation includes the tokens, final score, predicted label,
        and the positive/negative signals that were matched.
        """
        tokens = self.preprocess(text)
        score, positive_hits, negative_hits = self._analyze_tokens(tokens)
        label = self.predict_label(text)

        return (
            f"tokens={tokens}; "
            f"score={score}; "
            f"label={label}; "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
