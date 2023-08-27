from flask import jsonify, request, render_template
from app import app
from gensim.downloader import api

#model = api.load("word2vec-google-news-300")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_intermediary_topics', methods=['POST'])
def get_intermediary_topics():
    start_topic = request.json.get('start_topic')
    end_topic = request.json.get('end_topic')
    num_intermediaries = int(request.json.get('num_intermediaries', 1))

    topics = [start_topic]

    current_topic = start_topic
    for _ in range(num_intermediaries):
        try:
            next_topic = current_topic #model.most_similar_to_given(end_topic, current_topic)#list(set(topics)))
            topics.append(next_topic)
            current_topic = next_topic
        except:
            break

    topics.append(end_topic)

    return jsonify({"topics": topics})
