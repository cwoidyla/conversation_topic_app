import requests

def query_most_similar(positive=[], negative=[], topn=1):
    """
    Queries gensim_service.py flask API service.
    Utilizes model.most_similar(positive=, negative=, topn=)
    """
    base_url = "http://127.0.0.1:8080/most_similar"
    params = {
        'positive': ",".join(positive),
        'negative': ",".join(negative),
        'topn': topn
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        most_similar_words = response.json()['most_similar']
        return most_similar_words
    else:
        return {"error": f"Received {response.status_code} status code from server"}

def query_n_similarity(words1:list, words2:list):
    """
    Queries gensim_service.py flask API service.
    Utilizes model.n_similarity(words1, words2)
    """
    base_url = "http://127.0.0.1:8080/n_similarity"
    params = {
        'words1': ",".join(words1),
        'words2': ",".join(words2)
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        sim_score = response.json()['similarity']
        return float(sim_score)
    else:
        return {"error": f"Received {response.status_code} status code from server"}

def query_most_similar_to_given(word:str, list_of_words:list):
    """
    Queries gensim_service.py flask API service.
    Utilizes model.most_similar_to_given(word, list_of_words)
    """
    base_url = "http://127.0.0.1:8080/most_similar_to_given"
    params = {
        'word': word,
        'list_of_words': ",".join(list_of_words)
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            most_similar_word = response.json()['most_similar']
            return most_similar_word
        except Exception as e:
            return response.json()['error']
        
    else:
        return {"error": f"Received {response.status_code} status code from server"}