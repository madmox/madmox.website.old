"""Defines core classes for navigation in the website
"""

class NavigationNode(object):
    def __init__(self, active, url, label):
        self.active = active
        self.url = url
        self.label = label
