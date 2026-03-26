# Model Card: Mood Machine

This model card describes both versions of the Mood Machine project:

1. A rule based classifier in `mood_analyzer.py`
2. A machine learning classifier in `ml_experiments.py`

## 1. Model Overview

**Model type:**  
I used both the rule based model and the ML model, and compared how they behaved on the same labeled dataset.

**Intended purpose:**  
The Mood Machine is meant to classify short text posts or messages as `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**  
The rule based model preprocesses text into tokens, looks for positive and negative signals, computes a score, and then maps that score to a label. The ML model turns the posts into bag-of-words features with `CountVectorizer` and trains a `LogisticRegression` classifier on the labels in `dataset.py`.

## 2. Data

**Dataset description:**  
The starter dataset had 6 labeled posts. I expanded it to 17 labeled posts in `SAMPLE_POSTS` and `TRUE_LABELS`. I added 11 new examples using slang, emojis, sarcasm, and mixed emotions, including:

- `Lowkey proud of myself today :)`
- `No cap, I'm tired but the concert was amazing`
- `I absolutely love getting stuck in traffic 💀`
- `That playlist is fire, no cap`
- `I'm exhausted but proud I finished the project`
- `Love that the wifi died right before my quiz`

**Labeling process:**  
I labeled posts based on the overall tone I thought a human reader would most likely infer.

- I used `mixed` when a post clearly contained both positive and negative feelings, such as `I'm exhausted but proud I finished the project`.
- I used `neutral` for flat or unclear posts like `This is fine` and `Meh, the movie was okay I guess`.
- Some labels were more arguable than others. The hardest examples were sarcasm or understatement, especially `I absolutely love getting stuck in traffic 💀`, `Love that the wifi died right before my quiz`, and `Meh, the movie was okay I guess`.

**Important characteristics of the dataset:**  

- It contains slang such as `lowkey`, `no cap`, and `fire`.
- It contains emojis and emoticons such as `:)`, `😂`, `🥲`, and `💀`.
- It includes mixed-emotion posts rather than only clear positive or negative statements.
- It includes sarcasm and ironic language.
- Most posts are very short, informal, and written in casual English.

**Possible issues with the dataset:**  

- The dataset is very small.
- Some labels are subjective.
- The classes are not based on a formal annotation process.
- The posts mainly reflect one style of internet English, so the coverage of other dialects, communities, or languages is weak.

## 3. How the Rule Based Model Works

**Your scoring rules:**  
The rule based model uses a small hand-written sentiment system.

- `preprocess()` lowercases text, trims whitespace, normalizes repeated characters like `soooo`, and tokenizes words plus a few emojis/emoticons.
- Positive words add `+1` to the score.
- Negative words subtract `-1` from the score.
- I expanded the word lists to include `fire` as positive and `exhausted` as negative.
- I also added extra positive signals such as `hopeful`, `proud`, `glad`, `:)`, and `😂`.
- I added extra negative signals such as `meh`, `ugh`, `annoying`, `drained`, `:(`, and `🥲`.
- I added simple negation handling. For example, `not happy` flips a positive word into a negative signal, and `not bad` flips a negative word into a positive signal.
- In `predict_label()`, if both positive and negative signals appear, the model usually returns `mixed`. Otherwise, a positive score becomes `positive`, a negative score becomes `negative`, and `0` becomes `neutral`.

**Strengths of this approach:**  

- It behaves predictably on clear keyword-driven examples.
- It is easy to debug because I can inspect tokens and matched signals.
- It handled simple mixed-emotion posts fairly well, such as `Feeling tired but kind of hopeful` and `I'm exhausted but proud I finished the project`.
- It handled simple negation correctly for `I am not happy about this` and `Not bad actually, I'm kind of excited for tomorrow`.

**Weaknesses of this approach:**  

- It does not understand sarcasm well.
- It ignores words that are not in the chosen word lists.
- It only handles a small set of emojis and internet phrases.
- It can overreact to one keyword, especially when there is no balancing signal.

## 4. How the ML Model Works

**Features used:**  
The ML model uses bag-of-words features from `CountVectorizer`.

**Training data:**  
It trains directly on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**  
The ML model was very sensitive to the labels and examples I created.

- Before I added more examples about `fire` and mixed feelings, the ML model predicted `That song is fire` as `neutral` and `I'm exhausted but proud of myself` as `positive`.
- After I added `That playlist is fire, no cap` and `I'm exhausted but proud I finished the project`, it changed and predicted those same breaker-style sentences as `positive` and `mixed`.

This shows that the learned model adapted to the new data much more than the rule based model did.

**Strengths and weaknesses:**  

- Strength: it can pick up patterns from labeled examples without me manually writing every rule.
- Strength: it correctly classified some sarcastic or subtle examples in the training set, such as `I absolutely love getting stuck in traffic 💀` and `Love that the wifi died right before my quiz`.
- Weakness: the reported accuracy is training accuracy on the same dataset, so it likely overfits.
- Weakness: it can still generalize poorly on unseen sentences because the dataset is tiny.
- Weakness: it may learn accidental word associations from a handful of posts.

## 5. Evaluation

**How I evaluated the model:**  
I ran both models on the labeled posts in `dataset.py`.

- Rule based accuracy on `SAMPLE_POSTS`: `0.82`
- ML accuracy on the same `SAMPLE_POSTS`: `1.00`

The ML score is less impressive than it looks because it is measured on the same data the model trained on.

**Examples of correct predictions:**  

- `Today was a terrible day` was correctly labeled `negative` by both models because `terrible` is a strong negative signal.
- `I am not happy about this` was correctly labeled `negative` by the rule based model because the negation rule flipped `not happy`.
- `I'm exhausted but proud I finished the project` was correctly labeled `mixed` by both models after I expanded the data and vocabulary.

**Examples of incorrect predictions:**  

- Rule based: `I absolutely love getting stuck in traffic 💀` was predicted `positive` even though the true label is `negative`. The model counted `love`, but ignored `stuck`, `traffic`, and the sarcastic meaning of the sentence.
- Rule based: `Love that the wifi died right before my quiz` was predicted `positive` even though the true label is `negative`. Again, the positive word `love` dominated the decision.
- Rule based: `Meh, the movie was okay I guess` was predicted `negative` even though the true label is `neutral`, because `meh` is treated as a negative signal even though the full sentence is more flat than clearly negative.
- ML on breaker sentences: `I'm fine 🙂` was predicted `positive` and `This soup made me sick` was predicted `positive`, even though those are not clearly positive. This suggests the ML model learned unstable associations from a very small dataset.

## 6. Limitations

The most important limitations are:

- **Small dataset:** 17 posts is not enough to cover the variety of real language people use.
- **Sarcasm failure in the rule based model:** `I love getting stuck in traffic` and `Love that the wifi died right before my quiz` are misread because the model sees `love` and does not understand irony.
- **Ambiguity and understatement:** `Meh, the movie was okay I guess` is hard because the sentence is somewhere between neutral and mildly negative.
- **Limited emoji coverage:** the rule based model does not currently treat `🙂` as a signal, so `I'm fine 🙂` becomes `neutral`.
- **Polysemy / multiple meanings:** the word `sick` can mean illness or praise. The rule based model ignores it, and the ML model currently predicts `This soup made me sick` as `positive`, which is clearly wrong.
- **Overfitting in the ML model:** the ML model gets perfect accuracy on the training posts, but that does not mean it truly understands mood. It is likely memorizing patterns from a tiny dataset.

## 7. Ethical Considerations

This project is a classroom-scale experiment, not a safe system for real emotional analysis.

- If used on real messages, it could misclassify distress or frustration.
- It may misinterpret people who use different slang, dialects, or cultural references than the ones in this dataset.
- It is optimized for short informal English posts and a narrow set of internet expressions. It is not optimized for longer writing, code-switching, sarcasm-heavy communities, or non-English text.
- Mood detection also raises privacy concerns if applied to personal chats, journals, or sensitive communication without consent.

## 8. Bias and Scope

The data I added reflects my own assumptions about tone and labeling. That means the model is shaped by my vocabulary choices and my interpretation of what counts as positive, negative, neutral, or mixed.

- It is most optimized for casual English social-media style posts.
- It may work better for people who use slang like `lowkey`, `no cap`, `fire`, and `chill`.
- It may misread users from other communities whose emotional tone is expressed through different phrases, humor styles, or emojis.
- Because the labels are subjective, another annotator might disagree with some of my choices, especially on sarcastic or understated posts.

## 9. Ideas for Improvement

- Add a larger and more balanced labeled dataset.
- Use multiple annotators instead of only one person labeling posts.
- Expand preprocessing to support more emojis and internet slang.
- Add more context-aware rule logic for sarcasm, contrast words like `but`, and stronger negative events like `died`, `failed`, or `stuck`.
- Replace bag-of-words with TF-IDF or another representation that generalizes a little better.
- Evaluate the ML model on a held-out test set instead of only training accuracy.
- Keep the rule based model simple, but rewrite `score_text()` more explicitly if the goal is beginner readability.
