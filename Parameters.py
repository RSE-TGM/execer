from Import_Py_Packages import *
from Functions import save_parameters_to_file

### Simulation Setting
solver_opt      = 'ipopt'
random_set      = 1  # 1=random oscillation profile / 0=average profile
flex_range      = 1  # 1=consumers profiles can vary in defined range / 0=no flexibility (ref case)
dynamic_cgrid   = 1  # 1=grid price for buying is correlated to grid price for selling / 0=grid price for buying is fixed
period          = 4  # forecasted period in hours
starting_hour   = 0  # hours
duration_hour   = 24 # hours

######### REC COMPOSITION: MEMBERS & PV PLANTS ##########
### Members Consumption Peak Power
#(add as many members per typology as desired with their Consumption Peak Power)
res = []
off = [10]
sch = [6]
com = []
ind = [] #--> let zero in this model version

### Members PV nominal powers
#(match the same number of elements in vectors for Consumption Peak Power)
#(if there is the corresponding consumer but it has no PV power installed then put a zero ni the corresponding slot)
pv_res = []
pv_off = [15]
pv_sch = [10]
pv_com = []
pv_ind = [] #--> let zero in this model version

### General Parameters
TIP            = 0.147                          # €/kWh Premium Incentive Tariff (130 + 10,57)
p_ref          = np.array([68, 60, 57, 58, 62, 71, 88, 95, 105, 92, 82, 69, 52, 51, 59, 69, 78, 84, 93, 88, 87, 82, 73, 70]) #€/MWh GME date 03.04.2024
p              = np.tile(np.repeat(p_ref, 4), 365)/1e3 # €/kWh
net_tax        = 0.72                           # after tax income
w_C            = 0.40                           # weight "consumers" in incentive redistribution scheme (it is a fixed scheme without individual performance)
w_P            = 0.60                           # weight "producers" in incentive redistribution scheme (it is a fixed scheme without individual performance)

### Grid buy price
cgrid_fix    = 0.250                            # €/kWh
price_spread = cgrid_fix / np.mean(p)
if dynamic_cgrid == 1:
    cgrid_ref = p_ref * price_spread
    cgrid     = p * price_spread
else:
    cgrid_ref = p_ref / p_ref * cgrid_fix
    cgrid     = p / p * cgrid_fix

### Flexibility Capability Margins per member type and time slot
F              = [[0,7], [8,12], [13,17], [18,23]] #time slots
                   #RES  #OFF  #SCH  #COM  #IND
flex_capF      = [[0.05, 0.05, 0.00, 0.10, 0.30],  #0-07 NIGHT
                  [0.15, 0.20, 0.20, 0.30, 0.30],  #08-12 MORNING
                  [0.15, 0.20, 0.10, 0.30, 0.30],  #13-17 AFTERNOON
                  [0.30, 0.05, 0.00, 0.20, 0.30]]  #18-23 EVENING

### Random oscillation profiles CONS
Frand_CONS     = [[0,7], [8,12], [13,17], [18,23]] #time slots
                   #RES  #OFF  #SCH  #COM  #IND
rand_var_CONS  = [[0.00, 0.05, 0.00, 0.05, 0.10],  #0-07 NIGHT
                  [0.10, 0.20, 0.10, 0.20, 0.20],  #08-12 MORNING
                  [0.10, 0.20, 0.10, 0.20, 0.20],  #13-17 AFTERNOON
                  [0.20, 0.05, 0.00, 0.05, 0.20]]  #18-23 EVENING

### Random oscillation profiles PROD
Frand_PROD     = [[0,5], [6,18], [19,23]] #time slots
rand_var_PROD  = [[0.00],  #0-07 NIGHT
                  [0.10],  #08-17 MORNING / AFTERNOON
                  [0.00]]  #18-23 EVENING


### Save parameters to text file
filename = 'z___figures\\parameters.txt'
save_parameters_to_file(
    filename, solver_opt, random_set, flex_range, period, starting_hour, duration_hour,
    res, off, sch, com, ind, pv_res, pv_off, pv_sch, pv_com, pv_ind,
    TIP, cgrid_ref, p_ref, net_tax, w_C, w_P, F, flex_capF, Frand_CONS, rand_var_CONS, Frand_PROD, rand_var_PROD)
