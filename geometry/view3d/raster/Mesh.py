'''
Created on Apr 22, 2015

@author: soultaker
'''

class Mesh(object):
    def __init__(self, meshSubsets):
        self.__meshSubsets = meshSubsets
    
    def getSubsets(self):
        return self.__meshSubsets
    