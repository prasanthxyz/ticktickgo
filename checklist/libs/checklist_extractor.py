"""
Extract the checklist from SERP urls
"""

from serp_utils import get_serp_links
from html_to_keywords import html2keywords
from reference_list import get_reference_checklist
from similarity_checker import get_sim_score

def get_serp_checklists(keyword):
    """ Get list of checklists from SERP """
    serp_urls = get_serp_links('checklist for travel ' + keyword)

    serp_data = []
    for url in serp_urls:
        print url
        serp_data.append(html2keywords(url))
    return serp_data


def get_similarity_scores(serp_checklists):
    """ Get similarity scores of each reference checklist item """
    reference_checklist = get_reference_checklist()
    similarity_scores = {}

    for reference_item in reference_checklist:
        similarity_scores[reference_item] = 0

    for reference_item in reference_checklist:
        print "checking item", reference_item
        for serp_checklist in serp_checklists:
            similarity_score = 0
            for list_item in serp_checklist:
                similarity_score = max(similarity_score, get_sim_score(reference_item, list_item))
            similarity_scores[reference_item] += similarity_score

    return similarity_scores

def get_checklist(keyword):
    """ Get the checklist for the destination """
    serp_checklists = get_serp_checklists(keyword)
    return get_similarity_scores(serp_checklists)

if __name__ == "__main__":
    # print get_serp_checklists('goa')
    # print get_reference_checklist()
    print get_checklist('goa')
