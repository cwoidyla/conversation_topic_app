from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import gensim.downloader as api

# Load the model
model = api.load("word2vec-google-news-300")

app = Flask(__name__)
api_app = Api(app)


class MostSimilar(Resource):
    def get(self):
        # Get words lists from query parameters
        positive = request.args.get('positive', '')
        negative = request.args.get('negative', '')
        topn = int(request.args.get('topn', ''))

        # check input strings
        if positive != '':
            positive = positive.split(',')
        else:
            positive = []
        
        if negative != '':
            negative = negative.split(',')
        else:
            negative = []
        
        # Check if words lists are not empty
        if type(positive) != list or type(negative) != list or type(topn) != int:
            return jsonify({"error": "Provide positive or negative as comma-separated lists. topn as an int"})

        try:
            most_similar_words = model.most_similar(positive=positive, negative=negative, topn=topn)
            return jsonify({"most_similar": most_similar_words})
        except Exception as e:
            return jsonify({"error": str(e)})


class NSimilarity(Resource):
    def get(self):
        # Get words lists from query parameters
        words1 = request.args.get('words1', '').split(',')
        words2 = request.args.get('words2', '').split(',')
        
        # Check if words lists are not empty
        if not words1 or not words2:
            return jsonify({"error": "Provide words1 and words2 as comma-separated lists."})

        try:
            similarity = model.n_similarity(words1, words2)
            return jsonify({"similarity": float(similarity)})
        except Exception as e:
            return jsonify({"error": str(e)})
        

class MostSimilarToGiven(Resource):
    def get(self):
        # Get words lists from query parameters
        word = request.args.get('word', '').split(',')
        list_of_words = request.args.get('list_of_words', '').split(',')
        
        # Check if words lists are not empty
        if not word or not list_of_words:
            return jsonify({"error": "Provide word as str and list_of_words as comma-separated list."})

        try:
            most_similar = model.most_similar_to_given(word, list_of_words)
            return jsonify({"most_similar": most_similar})
        except Exception as e:
            return jsonify({"error": str(e)})

# Add routes
api_app.add_resource(NSimilarity, '/n_similarity')
api_app.add_resource(MostSimilar, '/most_similar')
api_app.add_resource(MostSimilarToGiven, '/most_similar_to_given')

if __name__ == '__main__':
    app.run(debug=False, port=8080)
