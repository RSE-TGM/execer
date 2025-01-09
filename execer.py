from Profile_OPT import profile_opt
from Parameters import *
from Functions import *
from Members_Plants import CONS, PROD, max_len, ntype
import time

# Time range
start      = int(starting_hour*4)
duration   = int(duration_hour*4)

# Saving matrix
CONS_final = np.zeros((max_len, ntype, duration))
PROD_final = np.zeros((max_len, ntype, duration))
inj_final  = np.zeros((max_len, ntype, duration))
abs_final  = np.copy(inj_final)
sha_final  = np.zeros(duration)
aut_final  = np.copy(inj_final)
flex_final = np.copy(inj_final)
ctime      = np.zeros(duration)

####### SIMULATION #######
for t in range(0, duration):
    ### Computational time
    start_time = time.time()

    ### Time step
    print(f'\n\n ----- RESULTS (HOUR = {int((t+start)/4)} / QUARTER = {(t+start)-int((t+start)/4)*4}) -----')

    t_passed = t+start

    ### Random Oscillations Profiles
    # Variation should be applied only to single current time step - the rest is forecasted
    if random_set == 1:
        CONS, PROD = random_profiles(rand_var_CONS, rand_var_PROD, Frand_CONS, Frand_PROD, max_len, CONS, PROD, t_passed)
    CONS_final[:, :, t] = CONS[:, :, t_passed]
    PROD_final[:, :, t] = PROD[:, :, t_passed]

    ### OPTIMIZATION
    inj_v, abs_v, sha_v, aut_v, flex_v = profile_opt(t_passed, CONS, PROD)

    ### SAVING (at each iteration the current fluxes are saved as result of the optimization)
    inj_final[:, :, t]  = inj_v[:, :, 0]
    abs_final[:, :, t]  = abs_v[:, :, 0]
    sha_final[t]        = sha_v[0]
    aut_final[:, :, t]  = aut_v[:, :, 0]
    flex_final[:, :, t] = flex_v[:, :, 0]
    np.savez("z___figures\\result_opt.npz", inj_final=inj_final, abs_final=abs_final, sha_final=sha_final, aut_final=aut_final, flex_final=flex_final, CONS_final=CONS_final, PROD_final=PROD_final)

    ### Computational time
    end_time = time.time()
    ctime[t] = end_time - start_time #computational time
    # print(f'Iteration Computation Time {t}: {round(ctime[t], 2)} seconds')

print('\nSimulation Completed\n')
print(f'\nTotal Computation Time: {round(ctime.sum(), 2)} seconds\n')