from itertools import izip
import csv, json
import numpy as np 
import pandas as pd
import networkx as nx  
import matplotlib.pyplot as plt 
import warnings
import seaborn as sns 
from collections import defaultdict
pd.set_option('display.width', 200)
warnings.simplefilter(action = "ignore", category = (FutureWarning, UserWarning))

def visualize(G):
	'''
	Build and visualize network 
	'''
	for e in common:
		G.add_edge(e[0],e[1],weight=len(common[e]))

	plt.figure()
	nx.draw(G, pos=nodePos, node_color='blue', node_size=15, style='dotted', edge_color='orange')
	plt.savefig('output/network.png', bbox_inches='tight')

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

# Dictionary of {facility: [chemicals]} resulting in 377 facilities
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

G = nx.Graph()

# BUILD network and visualize
visualize(G)

# DESCRIBE network and visualize

# Degrees
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
clust_coefficients = nx.clustering(G)
clust_coefficients_df = pd.DataFrame(clust_coefficients.items(), columns=['Facility', 'Clustering Coefficient'])
clust_coefficients_df = clust_coefficients_df.sort('Clustering Coefficient', ascending=False)
#print clust_coefficients_df

# Node centrality measures
FCG=list(nx.connected_component_subgraphs(G, copy=True))[0]
# Betweenness centrality
betweeness = nx.current_flow_betweenness_centrality(FCG)
betweeness_df = pd.DataFrame(betweeness.items(), columns=['Facility', 'Betweeness'])
betweeness_df = betweeness_df.sort('Betweeness', ascending=False)
# Closeness centrality
closeness = nx.closeness_centrality(FCG)
closeness_df = pd.DataFrame(closeness.items(), columns=['Facility', 'Closeness'])
closeness_df = closeness_df.sort('Closeness', ascending=False)
# Eigenvector centrality
eigenvector = nx.eigenvector_centrality(FCG)
eigenvector_df = pd.DataFrame(eigenvector.items(), columns=['Facility', 'Eigenvector'])
eigenvector_df = eigenvector_df.sort('Eigenvector', ascending=False)

# Merge everything
#describeNetwork = pd.merge(degrees_df, clust_coefficients_df, on='Facility')
describeNetwork = degrees_df.merge(clust_coefficients_df,on='Facility').merge(betweeness_df,on='Facility').merge(closeness_df, on='Facility').merge(eigenvector_df, on='Facility')
print describeNetwork



