"""
Extract the checklist from SERP urls
"""

from serp_utils import get_serp_links
from html_to_keywords import html2keywords
from reference_list import get_reference_checklist
from similarity_checker import get_sum_sim_scores
from joblib import Parallel, delayed


def get_serp_checklists(keyword):
    """ Get list of checklists from SERP """
    serp_urls = get_serp_links('checklist for travel ' + keyword)
    return Parallel(n_jobs=8)(delayed(html2keywords)(url) for url in serp_urls)


def get_similarity_scores(serp_checklists):
    """ Get similarity scores of each reference checklist item """
    reference_checklist = get_reference_checklist()
    similarity_scores = {}

    # import time
    # start = time.clock()
    for reference_item in reference_checklist:
        print "checking item", reference_item
        similarity_scores[reference_item] = get_sum_sim_scores(reference_item, serp_checklists)
    # print time.clock() - start
    return similarity_scores

def get_checklist(keyword):
    """ Get the checklist for the destination """
    serp_checklists = get_serp_checklists(keyword)
    similarity_scores = get_similarity_scores(serp_checklists)
    sorted_items = sorted(similarity_scores, key=lambda k: similarity_scores[k])
    return [(item, similarity_scores[item]) for item in sorted_items]


if __name__ == "__main__":
    # print get_serp_checklists('goa')
    # print get_reference_checklist()
    # get_serp_checklists('goa')
    SCORES = get_checklist('goa')
    SORTED_LIST = sorted(SCORES, key=lambda k: SCORES[k])
    for item in SORTED_LIST:
        print item, SCORES[item]
