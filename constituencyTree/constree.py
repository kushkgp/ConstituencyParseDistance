#!/usr/bin/python
from stanfordcorenlp import StanfordCoreNLP as snlp
from nltk.tree import *
import numpy as np

class Constree:
	def __init__(self):
		self.nlp = snlp(r'../resources/stanford-corenlp-full-2018-01-31')
	def parseSentence(self,sentence):
		parsing = self.nlp.parse(sentence)
		self.ptree = ParentedTree.fromstring(parsing)
	def get_lca_length(self,location1, location2):
		i = 0
		while i < len(location1) and i < len(location2) and location1[i] == location2[i]:
			i+=1
		return i
	def get_labels_from_lca(self, lca_len, location):
		labels = []
		for i in range(lca_len, len(location)):
			labels.append(self.ptree[location[:i]].label())
		return labels
	def findPathLen(self, index1, index2):
		# leaf_values = self.ptree.leaves()
		# leaf_index1 = leaf_values.index(text1)
		# leaf_index2 = leaf_values.index(text2)
		leaf_index1 = index1
		leaf_index2 = index2

		location1 = self.ptree.leaf_treeposition(leaf_index1)
		location2 = self.ptree.leaf_treeposition(leaf_index2)

		#find length of least common ancestor (lca)
		lca_len = self.get_lca_length(location1, location2)

		#find path from the node1 to lca
		labels1 = self.get_labels_from_lca(lca_len, location1)
		#ignore the first element, because it will be counted in the second part of the path
		result = labels1[1:]
		#inverse, because we want to go from the node to least common ancestor
		result = result[::-1]

		#add path from lca to node2
		result = result + self.get_labels_from_lca(lca_len, location2)
		if len(result)==0:
			return 0
		return len(result) + 1
		# return result
	def adjMatrix(self,sentence,l=0.1):
		self.parseSentence(sentence)
		leaf_values = self.ptree.leaves()
		n = len(leaf_values)
		adj = np.zeros((n,n))
		for i in range(n):
			for j in range(n):
				adj[i][j] = self.findPathLen(i,j)
				adj[j][i] = adj[i][j]
		# adj = -adj*adj/(2*l*l)
		# adj = np.exp(adj)
		return adj


def main():
	c = Constree()
	sentence = 'i saw a dog today.'
	print(c.adjMatrix(sentence))

if __name__ == '__main__':
	main()