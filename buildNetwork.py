from itertools import izip
import csv, json
import numpy as np 
import pandas as pd
import networkx as nx  
import matplotlib.pyplot as plt 
from collections import defaultdict
pd.set_option('display.width', 200)

def visualize(G):
	'''
	Build and visualize network 
	'''
	for e in common:
		G.add_edge(e[0],e[1],weight=len(common[e]))

	plt.figure()
	nx.draw(G, pos=nodePos, node_color='blue', node_size=15, style='dotted', edge_color='orange')
	plt.savefig('output/network.png', bbox_inches='tight')

def topdict(d,tn):
	'''
	Returns top tn centrality scores, given the dictionary d
	'''
	ind=sorted(d, key=d.get, reverse=True)
	for i in range(0,tn):
		print('{0}|{1}:{2}'.format(i+1,ind[i],d[ind[i]]))

def bottomdict(d,tn):
	'''
	Returns bottom tn centrality scores, given the dictionary d
	'''
	ind=sorted(d, key=d.get, reverse=False)
	for i in range(0,tn):
		print('{0}|{1}:{2},{3}'.format(i+1,ind[i],d[ind[i]],fac[ind[i]]))

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

# Build network and visualize
visualize(G)

c1= nx.degree(G)
# Output top tn centrality scores, given the dictionary d
#topdict(c1,10)

# Output bottom tn centrality scores, given the dictionary d
#bottomdict(c1,20)