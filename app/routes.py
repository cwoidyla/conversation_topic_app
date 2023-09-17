from flask import jsonify, request, render_template
from app import app
from app.services import query_most_similar_to_given, query_most_similar, query_n_similarity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_intermediary_topics', methods=['POST'])
def get_intermediary_topics():
    start_topic = request.json.get('start_topic').lower()
    end_topic = request.json.get('end_topic').lower()
    speaker_role = request.json.get('speaker_role').lower()
    num_intermediaries = int(request.json.get('num_intermediaries', 1))
    num_top_n = int(request.json.get('num_top_n', 10))

    symbolic_end_topic = end_topic

    # generalize comma-separated end topics
    gen_end_topic = end_topic.split(",")
    if len(gen_end_topic) > 1:
        symbolic_end_topic = query_most_similar(positive=gen_end_topic, topn=1)[0][0]

    # returned as json object
    topics = [start_topic]

    # prevents revisiting same topic
    prev_topics = [start_topic]

    current_topic = start_topic.split(",")
    for _ in range(num_intermediaries):
        try:
            # Find associations w.r.t. the speaker's role
            if speaker_role:
                current_topic += speaker_role.split(",")
            
            # Nearest neighbor search in semantic space
            associated_topics = [k[0] for k in query_most_similar(positive=current_topic, topn=num_top_n)]
            
            # Find associated topic most similar to end topic
            accept_topic = False
            while not accept_topic:
                next_topic = query_most_similar_to_given(symbolic_end_topic, list(set(associated_topics)))
                associated_topics.remove(next_topic)
                check_topic = next_topic.lower()
                if check_topic not in prev_topics and check_topic != symbolic_end_topic:
                    accept_topic = True
            
            # To avoid revisiting same topic, track accepted topics
            prev_topics.append(check_topic)
            
            # Return accepted topics and their similarity scores w.r.t. starting topic(S) and ending topic(E)
            sim_score_start = query_n_similarity(start_topic.split(","), next_topic.split(","))
            sim_score_end = query_n_similarity(symbolic_end_topic.split(","), next_topic.split(","))
            topics.append(f"{next_topic} S:{sim_score_start:.2f} E:{sim_score_end:.2f}")
            
            # Set new current topic
            current_topic = [next_topic]
        except Exception as e:
            print(e)
            break

    topics.append(end_topic)
    print(topics)

    return jsonify({"topics": topics})
