import json
import random
import re

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stemmer = PorterStemmer()

# Load chatbot questions and answers
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

patterns = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])


# NLP text processing
def tokenize(sentence):
    words = re.findall(r"[a-zA-Z]+", sentence.lower())
    return [stemmer.stem(word) for word in words]


vectorizer = TfidfVectorizer(
    tokenizer=tokenize,
    token_pattern=None
)

training_vectors = vectorizer.fit_transform(patterns)


# Generate chatbot response
def get_response(user_message):

    user_vector = vectorizer.transform([user_message])

    similarities = cosine_similarity(
        user_vector,
        training_vectors
    )[0]

    best_match = similarities.argmax()
    confidence = similarities[best_match]

    if confidence < 0.25:
        return "Sorry, I don't understand. Please ask another question."

    matched_tag = tags[best_match]

    for intent in data["intents"]:
        if intent["tag"] == matched_tag:
            return random.choice(intent["responses"])

    return "Sorry, I could not find an answer."