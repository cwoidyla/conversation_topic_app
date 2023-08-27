from flask import request, jsonify
from app import app
from gensim.models import KeyedVectors

# Load the word2vec model
model = KeyedVectors.load("static/data/word2vec-google-news-300")

@app.route('/get_associated_topics', methods=['POST'])
def get_associated_topics():
    topic = request.json.get('topic')
    if topic:
        related = model.most_similar(positive=[topic], topn=3)
        related_topics = [word[0] for word in related]
        return jsonify({"topics": related_topics})
    return jsonify({"error": "Topic not provided"}), 400

