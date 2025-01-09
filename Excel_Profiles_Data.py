#Imports
from Import_Py_Packages import *
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import squareform

# GUAG:
PROFPATH_DATISTAT='./dati_statistici_profili/linear_15m_profiles.xlsx'
PROFPATH_DATITEST='./dati_reali_CER/Dati_test.xlsx'

# STATISTICAL DATA #####################################################################################################
#Load profiles from excel file

#pu_profiles = pd.read_excel(r'C:\Users\neri\OneDrive - RSE S.p.A\Documenti\a___CER\a___RDS\a___CER profiles opt tool\linear_15m_profiles.xlsx', sheet_name='linear_15m_profiles')
pu_profiles = pd.read_excel(r'./dati_statistici_profili/linear_15m_profiles.xlsx', sheet_name='linear_15m_profiles')
pu_profiles = np.array(pu_profiles)[:, 4:10]
T           = pu_profiles.shape[0] # number of steps of considered period

# Basic Consumption and Production profiles
CONS_pu = pu_profiles[:, 0:-1]
PROD_pu = pu_profiles[:, -1]

# IDs profiles consumers
id_res = 0
id_off = 1
id_sch = 2
id_com = 3
id_ind = 4

# REAL RESIDENTIAL DATA #####################################################################################################

#Load profiles from excel file

#data = pd.read_excel(r'C:\Users\neri\OneDrive - RSE S.p.A\Documenti\a___CER\a___RDS\b___report 2024\dati reali CER\Dati test.xlsx', sheet_name='selected profiles groups')
data = pd.read_excel(r'./dati_reali_CER/Dati_test.xlsx', sheet_name='selected profiles groups')
#data= pd.read_excel(r"{PROFPATH}, sheet_name='selected profiles groups'")
id_profiles = np.array(data)[0, 1:21]
correlation = np.array(data)[1:21, 1:21]

# From correlation matrix to condensed distance matrix
correlation = pd.to_numeric(correlation.flatten(), errors='coerce').reshape(correlation.shape)
correlation = np.nan_to_num(correlation)
distance_matrix = np.clip(1 - correlation, 0, 1)
np.fill_diagonal(distance_matrix, 0)
condensed_distance_matrix = squareform(distance_matrix)

# Agglomerative Clustering
linked = linkage(condensed_distance_matrix, method='ward')

# Clusters cutting
max_d = 0.35  # this defines the level where to form the clusters: the higher it is the less the clustering  is precise and viceversa
clusters = fcluster(linked, max_d, criterion='distance')

# Clustering levels graphs
plt.figure(figsize=(10, 7))
dendrogram(linked, labels=[f'{int(x)}' for x in id_profiles])
plt.axhline(y=max_d, color='r', linestyle='--')  # Aggiungi una linea orizzontale
plt.title('Dendrogram Clustering Levels')
plt.xlabel('Profiles')
plt.ylabel('Distance')
plt.show()

# Clusters
cluster_dict = {i: [] for i in np.unique(clusters)}
for profile, cluster in zip(id_profiles, clusters):
    cluster_dict[cluster].append(profile)
print("\nClusters:")
for cluster, profiles in cluster_dict.items():
    profiles_int = [int(profile) for profile in profiles]
    print(f"Cluster {cluster}: {profiles_int}")

# Load real data profiles
#profiles_data = pd.read_excel(r'C:\Users\neri\OneDrive - RSE S.p.A\Documenti\a___CER\a___RDS\b___report 2024\dati reali CER\Dati test.xlsx', sheet_name='python profiles')
profiles_data = pd.read_excel(r'./dati_reali_CER/Dati_test.xlsx', sheet_name='python profiles')
pv_profile = np.array(profiles_data)[0:96*2+2, 23] * 2  # Profilo di produzione PV connesso alla rete
profiles = np.array(profiles_data)[0:96*2, 3:23]  # Profili di consumo dei singoli consumatori

# Cluster matrix creation
profile_index = {name: i for i, name in enumerate(id_profiles)}
cluster_sums = {}
consumer_cluster_matrix = []
for cluster, profile_names in cluster_dict.items():
    indices = [profile_index[name] for name in profile_names]  # Ottieni gli indici dei profili nel cluster
    cluster_sum = np.sum(profiles[:, indices], axis=1)  # Somma dei profili nel cluster
    cluster_sums[f"Cluster {cluster}"] = cluster_sum
    consumer_cluster_matrix.append(cluster_sum)  # Aggiungi il profilo aggregato alla matrice
consumer_cluster_matrix = np.array(consumer_cluster_matrix).T

print('\nProfile Data Imported from Excel\n')
