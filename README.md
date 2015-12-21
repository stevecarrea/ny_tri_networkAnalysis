# Network Analysis and Community Detection of Industrial Facilities in New York State
###### Steve Carrea, Andrew Fair

Industrial facilities can emit a variety of toxic chemicals into the air. Depending on a variety of factors, such as the processes being employed, each facility will emit a distinct type, amount, and group of chemicals. Certain chemical emissions are known to co-occur since they are typically present in specific processes. For example, benzene, toluene, ethylbenzene, and xylene are collectively referred to as BTEX compounds. These compounds are often found together in petroleum related industries since they are naturally found in crude oil. Formaldehyde and dioxins are other common toxins since they are released as byproducts of incomplete combustion and through a broad area of activities. This project performs network analysis and community detection on industrial facilities, which are linked based upon commonalities in their chemical emissions. 

## Toxic Release Inventory
The U.S. Environmental Protection Agency’s Toxic Release Inventory (TRI) specifies the amount of toxic air releases for each industrial facility that reports to the database. Those facilities that are within specified industries and meet minimum thresholds report to this database on an annual basis. The reporting thresholds are 25,000 pounds of chemicals manufactured or processed, or 10,000 pounds otherwise used. Certain persistent and bioaccumulative chemicals have lower reporting thresholds. Dioxins and dioxin-like compounds have the lowest reporting threshold in the inventory at 0.1 grams over a calendar year.

## Network 
We construct a non-directed network with industrial facilities as nodes and chemicals shared as edges. The buildNetwork.py file sets up the data as needed by the networkx library for Python and stores the necessary information into the graph. The edges are weighted based on the number of chemicals in common between two nodes.

## Community Detection
We use the Louvain Modularity method to perform community detection. Modularity optimization and community aggregation are performed automatically according to this method. The communities are derived by maximizing intra-community edges while minimizing inter-community edges.

## Output
The resulting graph of 369 nodes contains 11,277 edges with an average degree of 61 and a modularity coefficient of 0.47.

The buildNetwork.py file outputs a describeNetwork.csv which contains all the nodes in the network as separate records. This file becomes a basis for analysis within the communityAnalysis.ipynb Jupyter notebook. The attributes of each record include the number of degrees, clustering coefficient, industry classification code, and list of chemicals pertaining to the node.

## Results
A subset of facilities share the same number of degrees at 68 and 70. Many of these facilities are either within the same industry, the same type of facility, or owned by the same parent entity. Part of this is because only a subset of industries are required to report to the TRI database. The facilities with the highest degree centrality are large facilities that use a wide variety of chemicals. 

Given a positive modularity, we are sure that the communities detected have not risen by chance. The Louvain Modularity community detection algorithm identifies six distinct communities, and the identified communities have industrial classification profiles that appear to reflect broad recognizable industrial categories. See each community output csv file for the industries found within each community.

