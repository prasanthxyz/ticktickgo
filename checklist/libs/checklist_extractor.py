"""
Extract the checklist from SERP urls
"""

from serp_utils import get_serp_links
from html_to_keywords import html2keywords
from similarity_checker import get_sum_sim_scores
from joblib import Parallel, delayed

REFERENCE_LIST = []
METADATA_LIST = []
METADATA_REFERENCE_MAP = {}


def load_reference_list_and_metadata():
    """ Load reference list and metadata """
    global REFERENCE_LIST
    global METADATA_LIST
    global METADATA_REFERENCE_MAP
    print "Loading reference list..."
    try:
        REFERENCE_LIST = [line.strip() for line in open('reference_list.txt').readlines()]
        print "Reference list loaded."
        print "Loading metadata list..."
        METADATA_LIST = [line.strip() for line in open('metadata_list.txt').readlines()]
        print "Metadata list loaded."
        print "Generating metadata-reference dictionary..."
        for i in range(min(len(METADATA_LIST), len(REFERENCE_LIST))):
            METADATA_REFERENCE_MAP[METADATA_LIST[i]] = REFERENCE_LIST[i]
        print "metadata-reference dictionary generated."
    except Exception, error:
        print "ERROR: Could not load reference list."
        print error


def get_serp_checklists(keyword):
    """ Get list of checklists from SERP """
    serp_urls = get_serp_links('checklist for travel to ' + keyword, 5)
    return Parallel(n_jobs=8)(delayed(html2keywords)(url) for url in serp_urls)


def get_similarity_scores(serp_checklists):
    """ Get similarity scores of each reference checklist item """
    global METADATA_LIST
    similarity_scores = {}

    import time
    start = time.clock()
    for reference_item in METADATA_LIST:
        print "checking item", reference_item
        similarity_scores[reference_item] = get_sum_sim_scores(reference_item, serp_checklists)
    print time.clock() - start
    return similarity_scores


def get_checklist(keyword, num_items=20):
    """ Get the checklist for the destination """
    serp_checklists = get_serp_checklists(keyword)
    similarity_scores = get_similarity_scores(serp_checklists)
    sorted_items = sorted(similarity_scores, key=lambda k: similarity_scores[k], reverse=True)[:num_items]
    return [METADATA_REFERENCE_MAP[checklist_item] for checklist_item in sorted_items]


if __name__ == "__main__":
    # print get_serp_checklists('goa')
    # get_serp_checklists('goa')
    SCORES = get_checklist('andaman')
    SORTED_LIST = sorted(SCORES, key=lambda k: SCORES[k], reverse=True)
    for item in SORTED_LIST:
        print item, SCORES[item]
