# -*- coding: utf-8 -*-
from itertools import izip
import csv, json
import numpy as np 
import pandas as pd
import networkx as nx  
import community
import matplotlib.pyplot as plt 
import warnings
import seaborn as sns 
from collections import defaultdict
pd.set_option('display.width', 200)
warnings.simplefilter(action = "ignore", category = (FutureWarning, UserWarning))

def build(G):
	'''
	Build and visualize network 
	'''
	
	# Read data
	ny_tri = pd.read_csv('data/toxic-release-inventory.ny.2013.geoid.csv')
	ny_tri_trim = ny_tri[['tri_facility_id','facility_name','county','n_5_2_stack_air', 'chemical', 'latitude', 'longitude']]
	ny_tri_trim = ny_tri_trim[ny_tri_trim['facility_name']!='NATIONAL GRID WADING RIVER IC FACILITY']  # Null value for location
	ny_tri_trim = ny_tri_trim[ny_tri_trim['facility_name']!='EMAGIN CORP']  # Null value for location
	ny_group = ny_tri_trim.groupby(['facility_name', 'chemical'], as_index=False).aggregate(np.sum)

	# Create chemical table, single record per facility.
	chemicals_pivot = ny_group.pivot(index='facility_name', columns='chemical', values='n_5_2_stack_air')

	# Create location dictionary
	latLon = ny_tri_trim[['facility_name', 'longitude', 'latitude']].set_index('facility_name').drop_duplicates()
	nodePos = latLon.T.to_dict('list')

	# Dictionary of {facility: [chemicals]} resulting in 377 facilities and chemicals reported 
	fac = defaultdict(list)
	for i in chemicals_pivot.index:
	    for j in chemicals_pivot:
	        if chemicals_pivot[j][i] > 0:
	            fac[i].append(j)

	# Dictionary of {(facility1, facility2): [chemicals in common]} resulting in 11283 pairs of facilities
	common = defaultdict(list)
	for i in fac:
	    for j in fac:
	        if i < j:
	            for x in fac[i]:
	                for y in fac[j]:
	                    if x == y:
	                    	common[(i,j)].append(x)
	for e in common:
		G.add_edge(e[0],e[1],weight=len(common[e]))

	plt.figure()
	nx.draw(G, pos=nodePos, node_color='blue', node_size=15, style='dotted', edge_color='orange')
	plt.savefig('output/network.png', bbox_inches='tight')
	plt.close()

	plt.figure()
	nx.draw(G, node_color='blue', node_size=15, style='dotted', edge_color='orange')
	plt.savefig('output/network_noPosition.png', bbox_inches='tight')
	plt.close()

def describe(G):
	'''
	Describe the network: degrees, clustering, and centrality measures
	'''	
	# Degree
	# The number of connections a node has to other nodes.
	degrees= nx.degree(G)
	degrees_df = pd.DataFrame(degrees.items(), columns=['Facility', 'Degrees'])
	values = sorted(set(degrees.values())) 
	hist = [degrees.values().count(x) for x in values]
	plt.figure()
	plt.plot(values, hist,'ro-') # degree
	plt.xlabel('Degree')
	plt.ylabel('Number of nodes')
	plt.title('Degree Distribution')
	plt.savefig('output/degree_distribution.png')

	# Clustering coefficients
	# The bipartie clustering coefficient is a measure of local density of connections.
	clust_coefficients = nx.clustering(G)
	clust_coefficients_df = pd.DataFrame(clust_coefficients.items(), columns=['Facility', 'Clustering Coefficient'])
	clust_coefficients_df = clust_coefficients_df.sort('Clustering Coefficient', ascending=False)
	#print clust_coefficients_df

	# Node centrality measures
	FCG=list(nx.connected_component_subgraphs(G, copy=True))[0]
	# Current flow betweenness centrality
	# Current-flow betweenness centrality uses an electrical current model for information spreading 
	# in contrast to betweenness centrality which uses shortest paths.
	betweeness = nx.current_flow_betweenness_centrality(FCG)
	betweeness_df = pd.DataFrame(betweeness.items(), columns=['Facility', 'Betweeness'])
	betweeness_df = betweeness_df.sort('Betweeness', ascending=False)
	# Closeness centrality
	# The closeness of a node is the distance to all other nodes in the graph 
	# or in the case that the graph is not connected to all other nodes in the connected component containing that node.
	closeness = nx.closeness_centrality(FCG)
	closeness_df = pd.DataFrame(closeness.items(), columns=['Facility', 'Closeness'])
	closeness_df = closeness_df.sort('Closeness', ascending=False)
	# Eigenvector centrality
	# Eigenvector centrality computes the centrality for a node based on the centrality of its neighbors.
	# In other words, how connected a node is to other highly connected nodes.
	eigenvector = nx.eigenvector_centrality(FCG)
	eigenvector_df = pd.DataFrame(eigenvector.items(), columns=['Facility', 'Eigenvector'])
	eigenvector_df = eigenvector_df.sort('Eigenvector', ascending=False)

	# Merge everything
	describeNetwork = degrees_df.merge(clust_coefficients_df,on='Facility').merge(betweeness_df,on='Facility').merge(closeness_df, on='Facility').merge(eigenvector_df, on='Facility')
	describeNetwork = describeNetwork.sort('Degrees', ascending=False)
	describeNetwork.to_csv('output/describeNetwork.csv')

def community_detection(G):
	'''
	Perform community detection by maximizing intra-community edges while minimizing inter-community edges​
	The value of the modularity lies in the range (-0.5, 1)
	It is positive if the number of edges within groups exceeds the number expected on the basis of chance.
	'''

	part = community.best_partition(G)
	mod = community.modularity(part,G)
	print("modularity:", mod)
	# Plot, color nodes using community structure
	values = [part.get(node) for node in G.nodes()]
	plt.figure()
	nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
	plt.savefig('output/network_communities.png', bbox_inches='tight')
	plt.close()

########################## Functions Above ########################## 

G = nx.Graph()

# BUILD network and visualize
build(G)

# DESCRIBE network 
print nx.info(G)  # General  
describe(G) 

# COMMUNITY DETECTION
community_detection(G)





