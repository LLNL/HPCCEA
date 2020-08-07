#!/usr/bin/bash
import pdb

def cluster(nodes):
        clusters = []
        clustered_nodes = []
        current = []
        for node in nodes:
                clust = node[0:len(node)-1]
                if clust in clusters:
                        current.append(node)
                else:
                        past = current.copy()
                        current = []
                        clustered_nodes.append(past)
                        clusters.append(clust)
                        current.append(node)
        clustered_nodes.append(current)
        return clustered_nodes[1:len(clustered_nodes)]

list = ['clust1', 'clust3', 'clust2', 'boron3', 'boron5']
print(cluster(list))
