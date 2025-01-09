from Parameters import *
from Import_Py_Packages import *
from Members_Plants import CONS, PROD, gamma_u, max_len, ntype
from Parameters import duration_hour
from Functions import save_check_results_to_file
from Excel_Profiles_Data import profiles, cluster_dict, id_profiles

# Time range graphs
duration = int(duration_hour*4)

# Unpacking results
data       = np.load("z___figures\\result_opt.npz")
abs_final  = data['abs_final']
inj_final  = data['inj_final']
flex_final = data['flex_final']
aut_final  = data['aut_final']
CONS_final = data['CONS_final']
PROD_final = data['PROD_final']
sha_final  = data['sha_final']

# Reference Profiles without optimization
abs_ref = np.maximum(CONS_final-PROD_final, 0)
inj_ref = np.maximum(PROD_final-CONS_final, 0)

# Member profiles (select one member to analyze)
member_number = 0 # [0 - len_max]
member_type   = 4 # [0 - 4]

abs_final_member  = abs_final[member_number, member_type, :duration]
abs_ref_member    = abs_ref[member_number, member_type, :duration]
inj_final_member  = inj_final[member_number, member_type, :duration]
inj_ref_member    = inj_ref[member_number, member_type, :duration]
CONS_final_member = CONS_final[member_number, member_type, :duration]
CONS_flex_member  = (CONS_final * (1+flex_final))[member_number, member_type, :duration]

# Total Energy profiles (sum over members)
CONS_tot       = CONS.sum(0).sum(0)[:duration]
CONS_final_tot = CONS_final.sum(0).sum(0)[:duration]
CONS_flex_tot  = (CONS_final*(1+flex_final)).sum(0).sum(0)[:duration]
PROD_tot       = PROD.sum(0).sum(0)[:duration]
PROD_final_tot = PROD_final.sum(0).sum(0)[:duration]
abs_final_tot  = abs_final.sum(0).sum(0)[:duration]
abs_ref_tot    = abs_ref.sum(0).sum(0)[:duration]
inj_final_tot  = inj_final.sum(0).sum(0)[:duration]
inj_ref_tot    = inj_ref.sum(0).sum(0)[:duration]
sha_ref_tot    = np.minimum(abs_ref_tot, inj_ref_tot)
sha_final_tot  = sha_final[:duration]
aut_ref        = (PROD_final - inj_ref)[:, :, :duration]

# Calculating Cash flows
cash           = (aut_final * cgrid[:duration] + inj_final * p[:duration] * net_tax + sha_final * gamma_u[:, :, np.newaxis] * TIP)
cash_ref       = (aut_ref * cgrid[:duration] + inj_ref[:, :, :duration] * p[:duration] * net_tax + sha_ref_tot * gamma_u[:, :, np.newaxis] * TIP)
cash_tot       = cash.sum(0).sum(0)
cash_ref_tot   = cash_ref.sum(0).sum(0)
cash_diff_tot  = cash_tot - cash_ref_tot

# Calculating Incentives
inc           = sha_final * gamma_u[:, :, np.newaxis] * TIP
inc_ref       = sha_ref_tot * gamma_u[:, :, np.newaxis] * TIP
inc_tot       = inc.sum(0).sum(0)
inc_ref_tot   = inc_ref.sum(0).sum(0)
inc_diff_tot  = inc_tot - inc_ref_tot

# Total values over time period
CONS_TOT       = CONS_tot.sum()
CONS_final_TOT = CONS_final_tot.sum()
CONS_flex_TOT  = CONS_flex_tot.sum()
cash_TOT       = cash_tot.sum()
cash_ref_TOT   = cash_ref_tot.sum()
cash_diff_TOT  = (cash_tot - cash_ref_tot).sum()
inc_TOT        = inc_tot.sum()
inc_ref_TOT    = inc_ref_tot.sum()
inc_diff_TOT   = (inc_tot - inc_ref_tot).sum()

# Check conservation of total Consumption with oscillations
print('\nCheck of Total Consumption conservation with oscillations:\n')
print(f'    Consumption reference                   = {CONS_TOT.round(1)} kWh\n'
      f'    Consumption with oscillations           = {CONS_final_TOT.round(1)} kWh\n'
      f'    Difference                              = {((CONS_final_TOT - CONS_TOT) / CONS_TOT * 100).round(2)} %\n')

# Check conservation of total Consumption with oscillations
print('\nCheck of Total Consumption conservation with optimization:\n')
print(f'    Consumption with oscillations (new ref) = {CONS_final_TOT.round(1)} kWh\n'
      f'    Consumption with optimization           = {CONS_flex_TOT.round(1)} kWh\n'
      f'    Difference                              = {((CONS_flex_TOT - CONS_final_TOT) / CONS_final_TOT * 100).round(2)} %\n')

# Comparison cash flow with flexibility
print('\nComparison Total Cash Flow with optimization:\n')
print(f'    Cash flow reference                     = {cash_ref_TOT.round(1)} €\n'
      f'    Cash flow with optimization             = {cash_TOT.round(1)} €\n'
      f'    Difference                              = {((cash_TOT - cash_ref_TOT) / cash_ref_TOT * 100).round(2)} %\n')

# Comparison inc flow with flexibility
print('\nComparison Incentive Cash Flow with optimization:\n')
print(f'    Inc flow reference                      = {inc_ref_TOT.round(1)} €\n'
      f'    Inc flow with optimization              = {inc_TOT.round(1)} €\n'
      f'    Difference                              = {((inc_TOT - inc_ref_TOT) / inc_ref_TOT * 100).round(2)} %\n')

# Total Cash Flow components
print('\nTotal Cash Flow components with optimization:\n')
print(f'    Self consumption savings                = {(aut_final*cgrid[:duration]).sum().round(1)} €\n'
      f'    Selling to grid                         = {(inj_final * p[:duration] * net_tax).sum().round(1)} €\n'
      f'    Incentive                               = {inc_TOT.round(1)} €\n')

####    GRAPHS    ######################################################################################################
fs = 14 #fontsize text, legends, ticks
# Graph clusters profiles
for cluster, profile_names in cluster_dict.items():
    indices = [np.where(id_profiles == profile)[0][0] for profile in profile_names]  # Trova gli indici dei profili nel cluster
    plt.figure(figsize=(14, 7))
    for idx in indices:
        profile_sum = np.sum(profiles[:96 + 1, idx])  # Somma dei consumi del profilo corrente
        if profile_sum != 0:  # Evita divisioni per zero
            plt.plot(profiles[:96 + 1, idx] / profile_sum, label=f'P. {int(id_profiles[idx])}')
    plt.title(f'Cluster {cluster} Profiles Consumption p.u.', fontsize=14)
    plt.xlabel('Quarters', fontsize=14)
    plt.ylabel('Consumption p.u.', fontsize=14)
    plt.legend(fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.show()

plt.figure(figsize=(14, 7))
plt.title('Comparison consumption/production profile with random oscillation', fontsize=fs)
plt.plot(CONS_tot, label='cons_final', color='red', linestyle='-', marker='o')
plt.plot(CONS_final_tot, label='cons_ref', color='red', linestyle='--', marker='x')
plt.plot(PROD_tot, label='prod_final', color='blue', linestyle='-', marker='o')
plt.plot(PROD_final_tot, label='prod_ref', color='blue', linestyle='--', marker='x')
plt.xlabel('Quarters', fontsize=fs)
plt.ylabel('kWh', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.legend(fontsize=fs)
plt.grid(True)
plt.savefig('z___figures\\Comparison consumption and production profile with random oscillation')
plt.show()

plt.figure(figsize=(14, 7))
plt.title('Comparison consumption profile REC with flexibility', fontsize=fs)
plt.plot(CONS_final_tot, label='cons_final', color='red', linestyle='-', marker='o')
plt.plot(CONS_tot, label='cons_ref', color='red', linestyle='--', marker='x')
plt.plot(CONS_flex_tot, label='cons_flex', color='k', linestyle='-.', marker='d')
plt.xlabel('Quarters', fontsize=fs)
plt.ylabel('kWh', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.legend(fontsize=fs)
plt.grid(True)
plt.savefig('z___figures\\Comparison consumption profile REC with flexibility')
plt.show()

### Graph for single member analysis
# plt.figure(figsize=(14, 7))
# plt.title(f'Comparison abs/inj profile with flexibility (member {member_number} - {member_type})', fontsize=fs)
# plt.plot(abs_final_member, label='abs_final', color='red', linestyle='-', marker='o')
# plt.plot(abs_ref_member, label='abs_ref', color='red', linestyle='--', marker='x')
# plt.plot(inj_final_member, label='inj_final', color='blue', linestyle='-', marker='o')
# plt.plot(inj_ref_member, label='inj_ref', color='blue', linestyle='--', marker='x')
# plt.xlabel('Quarters', fontsize=fs)
# plt.ylabel('kWh', fontsize=fs)
# plt.xticks(fontsize=fs)
# plt.yticks(fontsize=fs)
# plt.legend(fontsize=fs)
# plt.grid(True)
# plt.savefig(f'z___figures\\Comparison absorption and injection profile with flexibility (member {member_number} - {member_type})')
# plt.show()
#
# plt.figure(figsize=(14, 7))
# plt.title(f'Comparison consumption profile with flexibility (member {member_number} - {member_type})', fontsize=fs)
# plt.plot(CONS_flex_member, label='cons_flex', color='red', linestyle='-', marker='o')
# plt.plot(CONS_final_member, label='cons_final', color='red', linestyle='--', marker='x')
# plt.xlabel('Quarters', fontsize=fs)
# plt.ylabel('kWh', fontsize=fs)
# plt.xticks(fontsize=fs)
# plt.yticks(fontsize=fs)
# plt.legend(fontsize=fs)
# plt.grid(True)
# plt.savefig(f'z___figures\\Comparison consumption profile with flexibility (member {member_number} - {member_type})')
# plt.show()

plt.figure(figsize=(14, 7))
plt.title('Comparison REC with flexibility', fontsize=fs)
plt.plot(abs_final_tot, label='abs_final', color='red', linestyle='-', marker='o')
plt.plot(abs_ref_tot, label='abs_ref', color='red', linestyle='--', marker='x')
plt.plot(inj_final_tot, label='inj_final', color='blue', linestyle='-', marker='o')
plt.plot(inj_ref_tot, label='inj_ref', color='blue', linestyle='--', marker='x')
plt.plot(sha_final_tot, label='sha_final', color='green', linestyle='-', marker='o')
plt.plot(sha_ref_tot, label='sha_ref', color='green', linestyle='--', marker='x')
plt.xlabel('Quarters', fontsize=fs)
plt.ylabel('kWh', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.legend(fontsize=fs)
plt.grid(True)
plt.savefig('z___figures\\Comparison REC with flexibility')
plt.show()

plt.figure(figsize=(14, 7))
plt.title('Average Flexibility Optimzation', fontsize=fs)
plt.plot(flex_final.mean(0).mean(0), label='flex', color='k', linestyle='-', marker='o')
plt.xlabel('Quarters', fontsize=fs)
plt.ylabel('kWh', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.legend(fontsize=fs)
plt.grid(True)
plt.savefig('z___figures\\Average Flexibility Optimzation')
plt.show()

plt.figure(figsize=(14, 7))
plt.title('Comparison Cash Flow result', fontsize=fs)
plt.plot(cash_tot, label='cash', color='g', linestyle='-', marker='o')
plt.plot(cash_ref_tot, label='cash_ref', color='r', linestyle='-', marker='x')
plt.plot(cash_diff_tot, label='cash_diff', color='b', linestyle='--', marker='s')
plt.text(0.02, 0.95, f'CF ref: {cash_ref_TOT.round(0)} €', fontsize=16, ha='left', va='top', color='k', transform=plt.gca().transAxes)
plt.text(0.02, 0.90, f'CF opt: {cash_TOT.round(0)} €', fontsize=16, ha='left', va='top', color='k', transform=plt.gca().transAxes)
plt.text(0.02, 0.85, f'CF diff: {(cash_diff_TOT/cash_ref_TOT*100).round(2)} %', fontsize=16, ha='left', va='top', color='k', transform=plt.gca().transAxes)
plt.xlabel('Quarters', fontsize=fs)
plt.ylabel('€', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.legend(fontsize=fs)
plt.grid(True)
plt.savefig('z___figures\\Comparison Cash Flow result')
plt.show()

### Member identification
id_members = np.empty((ntype, max_len), dtype=object)
types      = ['res cluster', 'off', 'sch', 'com', 'pv_onlygrid']
tol        = 1e-6
for j in range(ntype):
      for i in range(max_len):
            if inc.sum(2)[i,j].T>tol:
                  id_members[j, i] = f"{types[j]} {i+1}"
id_members = id_members[id_members != None]
id_members = id_members[id_members != '']

fig, ax1 = plt.subplots(figsize=(16, 12))
plt.title('Comparison Members Cash Flow result', fontsize=fs)
tol = 1e-6
cash_member_period     = (cash.sum(2)).T[cash.sum(2).T>tol].reshape(-1)           # filtering fictious zero elements + reshaping
cash_member_period_ref = (cash_ref.sum(2)).T[cash_ref.sum(2).T>tol].reshape(-1)   # filtering fictious zero elements + reshaping
variation_percentage   = ((cash_member_period - cash_member_period_ref) / cash_member_period_ref) * 100
bar_width = 0.35
n_member = len(cash_member_period)
index = np.arange(n_member)
ax1.bar(index - bar_width/2, cash_member_period, bar_width, label='Cash Member', color='b')
ax1.bar(index + bar_width/2, cash_member_period_ref, bar_width, label='Cash Member (Ref)', color='g')
ax1.set_xlabel('Members', fontsize=fs)
ax1.set_ylabel('€', fontsize=fs)
ax1.set_xticks(index)
ax1.set_xticklabels(id_members)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax1.grid(True)
ax1.legend(loc='upper left', bbox_to_anchor=(0.65, -0.033), fontsize=fs, frameon=False)
ax2 = ax1.twinx()
ax2.scatter(index, variation_percentage, color='r', marker='s', label='Variation %', s=40)
ax2.set_ylabel('Variation (%)')
ax2.legend(loc='upper left', bbox_to_anchor=(0.90, -0.033), fontsize=fs, frameon=False)
plt.savefig('z___figures\\Comparison Members Cash Flow result')
plt.show()

##### INCENTIVE GAIN REALLOCATION CONSIDERING MEMBER'S PARTICIPATION
# Incentive comparison per members/clusters
flex_tot         = abs(abs_final[:, :, :duration] - abs_ref[:, :, :duration]).sum()
flex_members_p   = np.zeros((max_len, ntype, duration))
inc_gain_realloc = np.zeros((max_len, ntype, duration))
inc_realloc      = np.zeros((max_len, ntype, duration))
for n in range(max_len):
      for t in range(ntype):
            flex_members_p[n, t, :duration]   = abs(abs_final[n, t, :duration] - abs_ref[n, t, :duration]) / flex_tot
            inc_gain_realloc[n, t, :duration] =  flex_members_p[n, t, :duration] * inc_diff_TOT
            inc_realloc[n, t, :duration]      = inc_ref[n, t, :duration] + inc_gain_realloc[n, t, :duration]
fig, ax1 = plt.subplots(figsize=(16, 12))
plt.title('Comparison Members Incentive result', fontsize=fs)
inc_member_period         = (inc.sum(2)).T[inc.sum(2).T>tol].reshape(-1)                 # filtering fictious zero elements + reshaping
inc_member_period_realloc = (inc_realloc.sum(2)).T[inc_realloc.sum(2).T>tol].reshape(-1) # filtering fictious zero elements + reshaping
inc_member_period_ref     = (inc_ref.sum(2)).T[inc_ref.sum(2).T>tol].reshape(-1)         # filtering fictious zero elements + reshaping
bar_width = 0.35
n_member = len(inc_member_period)
index = np.arange(n_member)
ax1.bar(index - bar_width/2, inc_member_period_realloc, bar_width, label='Inc Member (reallocated)', color='purple')
ax1.bar(index, inc_member_period, bar_width, label='Inc Member', color='b')
ax1.bar(index + bar_width/2, inc_member_period_ref, bar_width, label='Inc Member (Ref)', color='g')
plt.text(0.02, 0.95, f'INC ref: {inc_ref_TOT.round(1)} €', fontsize=16, ha='left', va='top', color='k', transform=plt.gca().transAxes)
plt.text(0.02, 0.90, f'INC opt: {inc_TOT.round(1)} €', fontsize=16, ha='left', va='top', color='k', transform=plt.gca().transAxes)
plt.text(0.02, 0.85, f'INC diff: {(inc_diff_TOT/inc_ref_TOT*100).round(2)} %', fontsize=16, ha='left', va='top', color='k', transform=plt.gca().transAxes)
ax1.set_xlabel('Members', fontsize=fs)
ax1.set_ylabel('€', fontsize=fs)
ax1.set_xticks(index)
ax1.set_xticklabels(id_members)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax1.grid(True)
ax1.legend(loc='upper left', bbox_to_anchor=(0.65, -0.033), fontsize=fs, frameon=False)
plt.savefig('z___figures\\Comparison Members Incentive result')
plt.show()

#graph that normalizes the obtained incentive with the tot energy flux to/from the grid per member
fig, ax1 = plt.subplots(figsize=(16, 12))
plt.title('Comparison Members Specific Incentive result', fontsize=fs)
tol = 1e-6
exchange_grid                      = inj_final + abs_final # tot energy flux to/from the grid per member
exchange_grid_period               = (exchange_grid.sum(2)).T[exchange_grid.sum(2).T>tol].reshape(-1)                    # filtering fictious zero elements + reshaping
inc_member_period_specific         = (inc.sum(2)).T[inc.sum(2).T>tol].reshape(-1) / exchange_grid_period                 # filtering fictious zero elements + reshaping
inc_member_period_realloc_specific = (inc_realloc.sum(2)).T[inc_realloc.sum(2).T>tol].reshape(-1) / exchange_grid_period # filtering fictious zero elements + reshaping
inc_member_period_ref_specific     = (inc_ref.sum(2)).T[inc_ref.sum(2).T>tol].reshape(-1) / exchange_grid_period         # filtering fictious zero elements + reshaping
bar_width = 0.35
n_member = len(inc_member_period)
index = np.arange(n_member)
ax1.bar(index - bar_width/2, inc_member_period_realloc_specific, bar_width, label='Inc Member (reallocated) spec.', color='purple')
ax1.bar(index, inc_member_period_specific, bar_width, label='Inc Member spec.', color='b')
ax1.bar(index + bar_width/2, inc_member_period_ref_specific, bar_width, label='Inc Member (Ref) spec.', color='g')
ax1.set_xlabel('Members', fontsize=fs)
ax1.set_ylabel('€/kWh_grid_exchange', fontsize=fs)
ax1.set_xticks(index)
ax1.set_xticklabels(id_members)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
ax1.grid(True)
ax1.legend(loc='upper left', bbox_to_anchor=(0.65, -0.033), fontsize=fs, frameon=False)
plt.savefig('z___figures\\Comparison Members Specific Incentive result')
plt.show()


### Saving check results to file
filename = 'z___figures\\results_check.txt'
save_check_results_to_file(
    filename, CONS_TOT, CONS_final_TOT, CONS_flex_TOT, cash_ref_TOT, cash_TOT,
    inc_ref_TOT, inc_TOT, aut_final, inj_final, p, cgrid, net_tax, duration)
