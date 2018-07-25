"""
Get reference checklist
"""

def get_reference_checklist():
    """ Returns reference checklist """
    try:
        return [line.strip() for line in open('reference_list.txt').readlines()]
    except Exception:
        return []
