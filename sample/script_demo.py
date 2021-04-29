# Import
from client.core import *
from client.utils import *

###############################
# Check DataGalaxy python SDK #
###############################
# put your datagalaxy token here
dgy_token = ""
dgy_sdk = DataGalaxyClient(dgy_token)
wkr = dgy_sdk.get_required_workspaces('my workspace name')

###############################
####### Check BulkTree ########
###############################
# Launch dataframe
# check bulktree for dataredkite
path = 'data_demo.csv'
df = pd.read_csv(path, sep=';')
dgy_drk_array = transform_dataframe(df)
dgy_sdk.post_bulk_tree('workspace DRK', 'drk_adls_sdk', 'NonRelational', dgy_drk_array)

#######################################
####### Check post new sources ########
#######################################
# Return error if source already exists
dgy_sdk.post_new_source('adls_gen1_azure', wkr)

######################################
####### Check get all sources ########
######################################
list_of_sources = dgy_sdk.get_all_sources(wkr)
print(len(list_of_sources))

#########################################
####### Check get all containers ########
#########################################
list_of_containers = dgy_sdk.get_all_containers(wkr, list_of_sources[0])
print(len(list_of_containers))

#######################################
####### Check post new element ########
#######################################
# Return error if container with same name already exists in the targeted space
dgy_sdk.post_new_element(wkr, list_of_containers[0], 'dataprovider_los_angeles')
