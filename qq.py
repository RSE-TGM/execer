from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, value

# Definizione del modello
model = ConcreteModel()

# Definizione delle variabili con bound opzionali (opzionale)
model.x = Var(initialize=0.0)
model.y = Var(initialize=0.0)

# Definizione della funzione obiettivo
def objective_rule(model):
    return (model.x - 1)**2 + (model.y - 2)**2

model.objective = Objective(rule=objective_rule, sense=1)  # sense=1 indica minimizzazione

# Definizione dei vincoli
def constraint1_rule(model):
    return model.x**2 + model.y >= 1

def constraint2_rule(model):
    return model.y >= model.x

model.constraint1 = Constraint(rule=constraint1_rule)
model.constraint2 = Constraint(rule=constraint2_rule)

# Creazione del solver
solver = SolverFactory('ipopt')

# Verifica se Ipopt è disponibile
if not solver.available():
    raise Exception("Ipopt solver is not available. Assicurati che Ipopt sia installato e nel PATH.")

# Risoluzione del modello
results = solver.solve(model, tee=True)

# Verifica lo stato della soluzione
if (results.solver.status == 'ok') and (results.solver.termination_condition == 'optimal'):
    print("\nSoluzione Ottimale Raggiunta:")
    print(f"x = {value(model.x):.4f}")
    print(f"y = {value(model.y):.4f}")
    print(f"f(x, y) = {value(model.objective):.4f}")
elif results.solver.termination_condition == 'infeasible':
    print("\nIl modello è infeasible.")
else:
    # Stampare ulteriori dettagli in caso di altri stati
    print("\nSolver Status:", results.solver.status)
    print("Termination Condition:", results.solver.termination_condition)

