from pyomo.environ import *
from Parameters import *
from Members_Plants import max_len, ntype, gamma_u, flex_matrix_cap
from Errors_messages import solver_error
from Functions import *
import inspect

def profile_opt(t_passed, CONS, PROD):
    ### MODEL
    m = ConcreteModel()

    # NUMBER OF DISPATCHABLE RESOURCES
    m.Nmax  = RangeSet(0, max_len-1) # members number of longest member vector (max_len)
    m.Ntype = RangeSet(0, ntype-1)       # members consumers type number

    # TIME PERIOD
    T    = period * 4 #timestep are quarters
    m.T  = RangeSet(t_passed, T+t_passed-1)

    #INDEXES
    m_indexes = [m.Nmax, m.Ntype, m.T]

    # DECISION VARIABLES
    m.sha   = Var(m.T,                  within=NonNegativeReals)
    m.abs   = Var(m.Nmax, m.Ntype, m.T, within=NonNegativeReals)
    m.inj   = Var(m.Nmax, m.Ntype, m.T, within=NonNegativeReals)
    m.flex  = Var(m.Nmax, m.Ntype, m.T, within=Reals)
    m.delta = Var(m.Nmax, m.Ntype, m.T, within=Binary)
    m.aut   = Var(m.Nmax, m.Ntype, m.T, within=NonNegativeReals)

    # OBJECTIVE FUNCTION
    m.obj = Objective(expr =
    sum(  m.aut[n, y, t] * cgrid[t]        # Physical Autoconsumptio Savings
        + m.inj[n, y, t] * p[t] * net_tax  # Grid Injection Selling
        + m.sha[t] * gamma_u[n, y] * TIP   # Tariff Incentive Premium

        for n     in m.Nmax
        for y     in m.Ntype
        for t     in m.T
    )
    , sense=maximize)

    # CONSTRAINTS
    # Absorption
    m.con1  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.abs[n, y, t]  == (CONS[n, y, t]*(1+m.flex[n, y, t]) - PROD[n, y, t]) * (1-m.delta[n, y, t]))
    m.con2  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.abs[n, y, t]  >= 0)
    # Injection
    m.con3  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.inj[n, y, t]  == (PROD[n, y, t] - CONS[n, y, t]*(1+m.flex[n, y, t])) * (m.delta[n, y, t]))
    m.con4  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.inj[n, y, t]  >= 0)
    # Autoconsumption
    m.con5  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.aut[n, y, t]  == PROD[n, y, t] - m.inj[n, y, t])
    # Total Energy Autoconsumption Conservation
    m.con7  = Constraint(m.Nmax, m.Ntype, rule=lambda m, n, y: sum(CONS[n, y, t]*(1+m.flex[n, y, t]) for t in m.T) == sum(CONS[n, y, t] for t in m.T))
    # Energy flexibility limit
    m.con10  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.flex[n, y, t] <= +flex_matrix_cap[n, y, t])
    m.con11  = Constraint(*m_indexes, rule=lambda m, n, y, t: m.flex[n, y, t] >= -flex_matrix_cap[n, y, t])
    # REC sharing
    m.con20 = Constraint(m.T, rule=lambda m, t: m.sha[t] <= sum(m.abs[n, y, t] for n in m.Nmax for y in m.Ntype))
    m.con21 = Constraint(m.T, rule=lambda m, t: m.sha[t] <= sum(m.inj[n, y, t] for n in m.Nmax for y in m.Ntype))

    # SOLVER
    solver = SolverFactory(solver_opt)
    while True:
        try:
            solver.solve(m)
            break
        except ValueError as e:
            solver_error(e)
    print(f"Optimal Value: {m.obj():.2f}")

    # SAVING
    inj_v, abs_v, sha_v, aut_v, flex_v = save_results(m, t_passed)

    return inj_v, abs_v, sha_v, aut_v, flex_v


### Saving optimization as txt
def save_function_to_file(func, filename):
    with open(filename, 'w') as file:
        file.write(inspect.getsource(func))

# Utilizzo della funzione per salvare il codice della funzione profile_opt
save_function_to_file(profile_opt, 'z___figures\\profile_opt.txt')