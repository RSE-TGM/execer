from Import_Py_Packages import *

# SAVING ##############################################################################################################
def save_results(m, t_passed):
    inj_v  = np.zeros((len(m.Nmax), len(m.Ntype), len(m.T)))
    abs_v  = np.zeros((len(m.Nmax), len(m.Ntype), len(m.T)))
    sha_v  = np.zeros(len(m.T))
    aut_v  = np.zeros((len(m.Nmax), len(m.Ntype), len(m.T)))
    flex_v = np.zeros((len(m.Nmax), len(m.Ntype), len(m.T)))
    for n in m.Nmax:
        for ntype in m.Ntype:
            for t in m.T:
                inj_v[n, ntype, t-t_passed]  = m.inj[n, ntype, t].value
                abs_v[n, ntype, t-t_passed]  = m.abs[n, ntype, t].value
                sha_v[t-t_passed]            = m.sha[t].value
                aut_v[n, ntype, t-t_passed]  = m.aut[n, ntype, t].value
                flex_v[n, ntype, t-t_passed] = m.flex[n, ntype, t].value
    return inj_v, abs_v, sha_v, aut_v, flex_v

# PROFILE MATRIX BUILD UP ##############################################################################################################
def matrix_build_up(ntype, max_len, res, off, sch, com, ind, pv_res, pv_off, pv_sch, pv_com, pv_ind, id_res, id_off, id_sch, id_com, id_ind):
    # cons matrix
    cons_matrix = np.zeros((ntype, max_len), dtype=int)
    cons_matrix[id_res, :len(res)] = res
    cons_matrix[id_off, :len(off)] = off
    cons_matrix[id_sch, :len(sch)] = sch
    cons_matrix[id_com, :len(com)] = com
    cons_matrix[id_ind, :len(ind)] = ind
    # pv_matrix
    pv_matrix = np.zeros((ntype, max_len), dtype=int)
    pv_matrix[id_res, :len(pv_res)] = pv_res
    pv_matrix[id_off, :len(pv_off)] = pv_off
    pv_matrix[id_sch, :len(pv_sch)] = pv_sch
    pv_matrix[id_com, :len(pv_com)] = pv_com
    pv_matrix[id_ind, :len(pv_ind)] = pv_ind
    return cons_matrix, pv_matrix

# FLEXIBILITY CAP MATRIX RESHAPE #####################################################################################################
def flex_cap_reshape(f_slot_check, F, flex_capF, ntype, max_len, flex_range):
    f_slot_check(np.array(F), np.array(flex_capF)) # ERROR CHECK
    flex_matrix_cap = np.zeros((ntype, 24))
    for f_slot, hours_range in enumerate(F):
        start_hour, end_hour = hours_range
        flex_matrix_cap[:, start_hour:end_hour+1] = np.array(flex_capF[f_slot]).reshape(ntype, 1)
    flex_matrix_cap = np.repeat(flex_matrix_cap, 4, axis=1)
    flex_matrix_cap = np.repeat(flex_matrix_cap[np.newaxis, :, :], max_len, axis=0)
    if flex_range == 0: #no flexibility condition
        flex_matrix_cap = flex_matrix_cap * 0
    flex_matrix_cap = np.tile(flex_matrix_cap, 2) # extending to 48h for simulation
    return flex_matrix_cap


# RANDOM PROFILES #####################################################################################################
def random_profiles(rand_var_CONS, rand_var_PROD, Frand_CONS, Frand_PROD, max_len, CONS, PROD, t_passed):
    CONS_var = np.zeros(CONS.shape)
    PROD_var = np.zeros(PROD.shape)
    rand_var_CONS = np.array(rand_var_CONS)
    rand_var_PROD = np.array(rand_var_PROD)
    # Consumption Var
    for f_slot, hours_range in enumerate(Frand_CONS):
        start_hour, end_hour = hours_range
        for n in range(max_len):
            var_cons = np.random.uniform(-rand_var_CONS[f_slot, :], rand_var_CONS[f_slot, :])
            CONS_var[n, :, start_hour*4:end_hour*4 + 4] = CONS[n, :, start_hour*4:end_hour*4 + 4] * (1 + var_cons[:, np.newaxis])
    # Production Var
    for f_slot, hours_range in enumerate(Frand_PROD):
        start_hour, end_hour = hours_range
        var_prod = np.random.uniform(-rand_var_PROD[f_slot], rand_var_PROD[f_slot])
        PROD_var[:, :, start_hour*4:end_hour*4 + 4] = PROD[:, :, start_hour*4:end_hour*4 + 4] * (1 + var_prod[np.newaxis, np.newaxis, :])
    # Substitution in CONS e PROD of only the first term
    CONS[:, :, t_passed] = CONS_var[:, :, t_passed]
    PROD[:, :, t_passed] = PROD_var[:, :, t_passed]
    return CONS, PROD


# SAVING PARAMETERS #####################################################################################################
def save_parameters_to_file(
    filename, solver_opt, random_set, flex_range, period, starting_hour, duration_hour,
    res, off, sch, com, ind, pv_res, pv_off, pv_sch, pv_com, pv_ind,
    TIP, cgrid, p_ref, net_tax, w_C, w_P, F, flex_capF, Frand_CONS, rand_var_CONS, Frand_PROD, rand_var_PROD
):
    with open(filename, 'w') as file:
        file.write(f"### Simulation Setting\n")
        file.write(f"solver_opt      = {solver_opt}\n")
        file.write(f"random_set      = {random_set}\n")
        file.write(f"flex_range      = {flex_range}\n")
        file.write(f"period          = {period}\n")
        file.write(f"starting_hour   = {starting_hour}\n")
        file.write(f"duration_hour   = {duration_hour}\n\n")

        file.write(f"### Members Consumption Peak Power\n")
        file.write(f"res = {res}\n")
        file.write(f"off = {off}\n")
        file.write(f"sch = {sch}\n")
        file.write(f"com = {com}\n")
        file.write(f"ind = {ind}\n\n")

        file.write(f"### Members PV nominal powers\n")
        file.write(f"pv_res = {pv_res}\n")
        file.write(f"pv_off = {pv_off}\n")
        file.write(f"pv_sch = {pv_sch}\n")
        file.write(f"pv_com = {pv_com}\n")
        file.write(f"pv_ind = {pv_ind}\n\n")

        file.write(f"### General Parameters\n")
        file.write(f"TIP            = {TIP}\n")
        file.write(f"cgrid          = {(cgrid.round(0)).tolist()}\n")
        file.write(f"p              = {(p_ref.round(0)).tolist()}\n")
        file.write(f"net_tax        = {net_tax}\n")
        file.write(f"w_C            = {w_C}\n")
        file.write(f"w_P            = {w_P}\n\n")

        file.write(f"### Flexibility Capability Margins per member type and time slot\n")
        file.write(f"F         = {F}\n")
        file.write(f"flex_capF = {flex_capF}\n\n")

        file.write(f"### Random oscillation profiles CONS\n")
        file.write(f"Frand_CONS     = {Frand_CONS}\n")
        file.write(f"rand_var_CONS  = {rand_var_CONS}\n\n")

        file.write(f"### Random oscillation profiles PROD\n")
        file.write(f"Frand_PROD     = {Frand_PROD}\n")
        file.write(f"rand_var_PROD  = {rand_var_PROD}\n")


# SAVING CHECK RESULTS #####################################################################################################
def save_check_results_to_file(
    filename, CONS_TOT, CONS_final_TOT, CONS_flex_TOT, cash_ref_TOT, cash_TOT,
    inc_ref_TOT, inc_TOT, aut_final, inj_final, p, cgrid, net_tax, duration
):
    with open(filename, 'w') as file:
        file.write('Check of Total Consumption conservation with oscillations:\n')
        file.write(f'    Consumption reference                   = {CONS_TOT.round(1)} kWh\n')
        file.write(f'    Consumption with oscillations           = {CONS_final_TOT.round(1)} kWh\n')
        file.write(f'    Difference                              = {((CONS_final_TOT - CONS_TOT) / CONS_TOT * 100).round(2)} %\n\n')

        file.write('Check of Total Consumption conservation with optimization:\n')
        file.write(f'    Consumption with oscillations (new ref) = {CONS_final_TOT.round(1)} kWh\n')
        file.write(f'    Consumption with optimization           = {CONS_flex_TOT.round(1)} kWh\n')
        file.write(f'    Difference                              = {((CONS_flex_TOT - CONS_final_TOT) / CONS_final_TOT * 100).round(2)} %\n\n')

        file.write('Comparison Total Cash Flow with optimization:\n')
        file.write(f'    Cash flow reference                     = {cash_ref_TOT.round(1)} €\n')
        file.write(f'    Cash flow with optimization             = {cash_TOT.round(1)} €\n')
        file.write(f'    Difference                              = {((cash_TOT - cash_ref_TOT) / cash_ref_TOT * 100).round(2)} %\n\n')

        file.write('Comparison Incentive Cash Flow with optimization:\n')
        file.write(f'    Inc flow reference                      = {inc_ref_TOT.round(1)} €\n')
        file.write(f'    Inc flow with optimization              = {inc_TOT.round(1)} €\n')
        file.write(f'    Difference                              = {((inc_TOT - inc_ref_TOT) / inc_ref_TOT * 100).round(2)} %\n\n')

        file.write('Total Cash Flow components with optimization:\n')
        file.write(f'    Self consumption savings                = {(aut_final * cgrid[:duration]).sum().round(1)} €\n')
        file.write(f'    Selling to grid                         = {(inj_final * p[:duration] * net_tax).sum().round(0)} €\n')
        file.write(f'    Incentive                               = {inc_TOT.round(1)} €\n')
