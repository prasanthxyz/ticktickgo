# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:58:49 2018

@author: ticktickgo
"""

from rake_nltk import Rake
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gensim
from joblib import Parallel, delayed


RAKE = Rake()
PORTER_STEMMER = PorterStemmer()
global PRE_TRAINED_MODEL
PRE_TRAINED_MODEL = None


def load_pre_trained_model():
    """ Load pre-trained model """
    global PRE_TRAINED_MODEL
    PRE_TRAINED_MODEL = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)


def get_keywords(text):
    """
    Similarity score = avg no. of src keyword stems in target
    """
    tokens = word_tokenize(text)
    # stemming not required since word embeddings will take care of such nuances
    text_words = [word.lower() for word in tokens if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    return [word for word in text_words if word not in stop_words]


def get_sim_score_2(src_text, target_text):
    """ Uses word embeddings to get semantic similarity - Symmetric  """
    global PRE_TRAINED_MODEL
    if not PRE_TRAINED_MODEL:
        load_pre_trained_model()
    src_text_words = get_keywords(src_text)
    target_text_words = get_keywords(target_text)

    # Cosine similarity of the vectors
    try:
        distance = PRE_TRAINED_MODEL.n_similarity(src_text_words, target_text_words)
    except Exception:
        return get_sim_score(src_text, target_text)
    return distance


def get_max_sim_score_2(src_text, target_list):
    """ Return max sim score of src_stemmed_keywords against each text in target_list """
    scores = [get_sim_score_2(src_text, target_text) for target_text in target_list]
    try:
        return max(scores)
    except Exception:
        return 0


def get_sum_sim_scores_2(src_text, target_lists):
    """ Return sum of max sim scores of src_text against each list in target_lists """
    scores = Parallel(n_jobs=8)(delayed(get_max_sim_score_2)(src_text, target_list) for target_list in target_lists)
    try:
        return sum(scores)
    except Exception:
        return 0


def get_sim_score(src_text, target_text):
    """
    Unsymmetric Stem word based similarity measure
    """
    RAKE.extract_keywords_from_text(src_text)
    src_keywords = word_tokenize(" ".join(RAKE.get_ranked_phrases()))
    # print src_keywords
    src_stemmed_keywords = [PORTER_STEMMER.stem(word.lower()) for word in src_keywords if word.isalpha()]

    return get_sim_score_stemmed_keywords(src_stemmed_keywords, target_text)


def get_sim_score_stemmed_keywords(src_stemmed_keywords, target_text):
    """ Return sim score b/w src stemmed keywords and target text """
    RAKE.extract_keywords_from_text(target_text)
    target_keywords = word_tokenize(" ".join(RAKE.get_ranked_phrases()))
    # print target_keywords

    target_stemmed_keywords = [PORTER_STEMMER.stem(word.lower()) for word in target_keywords if word.isalpha()]
    # print target_stemmed_keywords

    count = len([keyword for keyword in src_stemmed_keywords if keyword in target_stemmed_keywords])
    match_score = float(count)/len(src_stemmed_keywords)
    return match_score


def get_max_sim_score(src_stemmed_keywords, target_list):
    """ Return max sim score of src_stemmed_keywords against each text in target_list """
    scores = [get_sim_score_stemmed_keywords(src_stemmed_keywords, target_text) for target_text in target_list]
    try:
        return max(scores)
    except Exception:
        return 0


def get_sum_sim_scores(src_text, target_lists):
    """ Return sum of max sim scores of src_text against each list in target_lists """
    RAKE.extract_keywords_from_text(src_text)
    src_keywords = word_tokenize(" ".join(RAKE.get_ranked_phrases()))
    src_stemmed_keywords = [PORTER_STEMMER.stem(word.lower()) for word in src_keywords if word.isalpha()]
    scores = Parallel(n_jobs=8)(delayed(get_max_sim_score)(src_stemmed_keywords, target_list) for target_list in target_lists)
    try:
        return sum(scores)
    except Exception:
        return 0

if __name__ == "__main__":
    get_sim_score("remember to pack medicine", "Make sure you pack Medicines")
    get_sim_score_2("remember to pack medicine", "Make sure you pack Medicines")

    get_sim_score("remember to pack medicine", "go to pharmacy")
    get_sim_score_2("remember to pack medicine", "go to pharmacy")
