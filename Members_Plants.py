from Excel_Profiles_Data import consumer_cluster_matrix, pv_profile, id_res, id_off, id_sch, id_com, id_ind, CONS_pu, PROD_pu
from Errors_messages import *
from Parameters import *
from Functions import *

################### MATRIX ENERGY PROFILES ##########################
n_res = len(res) + len(consumer_cluster_matrix[0,:])
n_off = len(off)
n_sch = len(sch)
n_com = len(com)
n_ind = len(ind)

max_len = max(n_res, n_off, n_sch, n_com, n_ind)
ntype   = 5
check_lenght_members(res, off, sch, com, ind, pv_res, pv_off, pv_sch, pv_com, pv_ind) # ERROR CHECK

# cons_matrix
cons_matrix, pv_matrix =  matrix_build_up(ntype, max_len, res, off, sch, com, ind, pv_res, pv_off, pv_sch, pv_com, pv_ind, id_res, id_off, id_sch, id_com, id_ind)

### Statistical profiles
CONS = (CONS_pu[:, :, np.newaxis] * cons_matrix[np.newaxis, :, :]).T
PROD = (PROD_pu[:, np.newaxis, np.newaxis] * pv_matrix[np.newaxis, :, :]).T

### Real Profiles
CONS_res_real = consumer_cluster_matrix.T
PROD_grid_real = pv_profile.T

### Complete Profiles
CONS[len(res):,0,:] = CONS_res_real   #real residentials data are inserted after other possible residential profiles
PROD[0,-1,:] = PROD_grid_real         #real pv data only-grid-connected is attributed to the identification "pv_ind" (if you put in "Parameters"-->"ind" a value this will autoconsume form the real pv data)

################## INCENTIVE DIVISION SCHEME ########################
PREL = np.maximum(CONS-PROD, 0).sum(2)
INJ  = np.maximum(PROD-CONS, 0).sum(2)
gamma_u = ((PREL * w_C + INJ * w_P) / np.sum(PREL * w_C + INJ * w_P)) #single member incentive percentual share (in this model it considers the energy absorption and injection amounts)
redistribution_weights_error(w_C, w_P) # ERROR CHECK

################## FLEXIBILITY RESHAPING ############################
flex_matrix_cap = flex_cap_reshape(f_slot_check, F, flex_capF, ntype, max_len, flex_range)