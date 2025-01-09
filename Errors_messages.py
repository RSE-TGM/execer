
#####################################################################################################################
def check_lenght_members(res, off, sch, com, ind, pv_res, pv_off, pv_sch, pv_com, pv_ind):
    if len(res) != len(pv_res):
        raise ValueError(
            f"Errore: La lunghezza di res ({len(res)}) non corrisponde alla lunghezza di pv_res ({len(pv_res)})")
    if len(off) != len(pv_off):
        raise ValueError(
            f"Errore: La lunghezza di off ({len(off)}) non corrisponde alla lunghezza di pv_off ({len(pv_off)})")
    if len(sch) != len(pv_sch):
        raise ValueError(
            f"Errore: La lunghezza di sch ({len(sch)}) non corrisponde alla lunghezza di pv_sch ({len(pv_sch)})")
    if len(com) != len(pv_com):
        raise ValueError(
            f"Errore: La lunghezza di com ({len(com)}) non corrisponde alla lunghezza di pv_com ({len(pv_com)})")
    if len(ind) != len(pv_ind):
        raise ValueError(
            f"Errore: La lunghezza di ind ({len(ind)}) non corrisponde alla lunghezza di pv_ind ({len(pv_ind)})")

#####################################################################################################################
def solver_error(e):
    if 'Cannot load a SolverResults object with bad status: error' in str(e):
        print("Errore: Cannot load a SolverResults object with bad status: error. Riprova nuova esecuzione...")
    else:
        print("Errore:", e)

#####################################################################################################################
def redistribution_weights_error(w_C, w_P):
    if w_C+w_P != 1:
        print('The shares weights (w_C & w_p) for componentes do not sum up to 100%')

#####################################################################################################################
def f_slot_check(F, flex_capF):
    if F.shape[0] != flex_capF.shape[0]:
        print('The number of rows in flex_capF is not consistent with the number of F slots')
