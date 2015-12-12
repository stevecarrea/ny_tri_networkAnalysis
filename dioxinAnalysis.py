import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action = "ignore")

def chemPickCommunity(comm, chem):
    # Checks if chemical is emitted by node. If true assign node to withChem dataframe
    withChem = allFacilities[allFacilities['Chemicals'].str.contains(chem)]
    # If false, assign node to withoutChem
    withoutChem = allFacilities[~allFacilities['Chemicals'].str.contains(chem)]
    # Subset dataframe based on community
    withChemComm = withChem[withChem['Community'] == comm]
    withoutChemComm = withoutChem[withoutChem['Community'] == comm]
    # Get NAICS for all reporting facilities
    chemNaics = pd.unique(withChemComm['primary_naics'].values.ravel())
    # Check if a non-reporter has a counterpart that is reporting based on NAICS, community, and chemical
    nonReporters = withoutChemComm[withoutChemComm['primary_naics'].isin(chemNaics)]
    nonReporters['nonReportChem'] = chem
    nonReporters['num_reporting'] = len(withChemComm)
    nonReporters_df = nonReporters[cols]
    return nonReporters_df

allFacilities = pd.read_csv("output/describeNetwork.csv", dtype={'primary_naics': object})
naics = pd.read_csv("data/naics.csv", dtype={'2012 NAICS US Code': object})
tri2013 = pd.read_csv('data/toxic-release-inventory.ny.2013.geoid.csv')

allChems = sorted(pd.unique(tri2013['chemical'].values.ravel()))
print 'Number of chemicals:', len(allChems)
allComms = sorted(pd.unique(allFacilities['Community'].values.ravel()))
print 'Communities:', len(allComms)

# chem = 'DIOXIN AND DIOXIN-LIKE COMPOUNDS'
naics = naics.drop(naics.columns[[0,3,4]], axis=1)
naics.columns = ["naics", "industry"]
allFacilities = allFacilities.merge(naics, left_on=["primary_naics"], right_on="naics", how="left")
allFacilities = allFacilities.drop(['Unnamed: 0', 'naics', 'Betweeness','Closeness','Eigenvector'], axis=1)

cols = ['nonReportChem', 'Community', 'Facility', 'parent_company_name', 'industry', 'primary_naics', 'num_reporting']

allNonRepList = []

for i in allComms:
    for j in allChems:
        allNonRepList.append(chemPickCommunity(i,j))

final = pd.concat(i for i in allNonRepList)
final.to_csv('output/nonReporters.csv')
print 'Number of non-reporters:', len(final['Facility'].unique())


