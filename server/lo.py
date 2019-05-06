import pulp

from planes import *


def get_solution_lo(plan_list, limit_voice, limit_sms, limit_data):
    n = len(plan_list)
    opt_model = pulp.LpProblem('Model', pulp.LpMinimize)

    x = pulp.LpVariable.dicts('X', [i for i in range(n)], lowBound = 0, upBound = None, 
                                    cat = pulp.LpInteger)

    opt_model += sum([ plan_list[i].price * x[i] for i in range(n)])
    opt_model += sum([plan_list[i].voice * x[i] for i in range(n)]) >= limit_voice
    opt_model += sum([plan_list[i].sms * x[i] for i in range(n)]) >= limit_sms
    opt_model += sum([plan_list[i].data * x[i] for i in range(n)]) >= limit_data

    opt_model.solve()

    sol = []
    for i in range(len(plan_list)):
        sol.append(int(x[i].value()))
    return sol
