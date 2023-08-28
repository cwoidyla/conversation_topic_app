from flask import jsonify, request, render_template
from app import app
import gensim.downloader as api

model = api.load("word2vec-google-news-300")
words_list = list(model.key_to_index.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_intermediary_topics', methods=['POST'])
def get_intermediary_topics():
    start_topic = request.json.get('start_topic').lower()
    end_topic = request.json.get('end_topic').lower()

    symbolic_end_topic = end_topic

    # generalize comma-separated end topics
    gen_end_topic = end_topic.split(",")
    if len(gen_end_topic) > 1:
        symbolic_end_topic = model.most_similar(positive=gen_end_topic, topn=1)[0][0]
    
    num_intermediaries = int(request.json.get('num_intermediaries', 1))
    num_top_n = int(request.json.get('num_top_n', 10))

    topics = [start_topic]

    current_topic = start_topic.split(",")
    for _ in range(num_intermediaries):
        try:
            associated_topics = [k[0] for k in model.most_similar(positive=current_topic, topn=num_top_n)]
            accept_topic = False
            while not accept_topic:
                next_topic = model.most_similar_to_given(symbolic_end_topic, list(set(associated_topics)))
                associated_topics.remove(next_topic)
                check_topic = next_topic.lower()
                if check_topic not in topics and check_topic != symbolic_end_topic:
                    accept_topic = True
            topics.append(check_topic)
            current_topic = [next_topic]
        except Exception as e:
            print(e)
            break

    topics.append(end_topic)
    print(topics)

    return jsonify({"topics": topics})
