"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fire",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "exhausted",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey proud of myself today :)",
    "No cap, I'm tired but the concert was amazing",
    "lol that quiz was bad but I'm weirdly chill now 😂",
    "I absolutely love getting stuck in traffic 💀",
    "Not bad actually, I'm kind of excited for tomorrow",
    "Happy for you and kinda sad for me at the same time 🥲",
    "Meh, the movie was okay I guess",
    "I was stressed all morning, then good music helped",
    "That playlist is fire, no cap",
    "I'm exhausted but proud I finished the project",
    "Love that the wifi died right before my quiz",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # "Lowkey proud of myself today :)"
    "mixed",     # "No cap, I'm tired but the concert was amazing"
    "mixed",     # "lol that quiz was bad but I'm weirdly chill now 😂"
    "negative",  # "I absolutely love getting stuck in traffic 💀"
    "positive",  # "Not bad actually, I'm kind of excited for tomorrow"
    "mixed",     # "Happy for you and kinda sad for me at the same time 🥲"
    "neutral",   # "Meh, the movie was okay I guess"
    "mixed",     # "I was stressed all morning, then good music helped"
    "positive",  # "That playlist is fire, no cap"
    "mixed",     # "I'm exhausted but proud I finished the project"
    "negative",  # "Love that the wifi died right before my quiz"
]

# Notes for future expansion:
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
