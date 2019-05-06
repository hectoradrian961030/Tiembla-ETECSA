import dp
import random
from dp import *
import copy
from planes import *
from random import shuffle

MAX_POPULATION_SIZE = 50
MAX_ITER = 10000
MAX_POW_TWO = 7


def convert_to_01(plan_list):
    n = len(plan_list)
    my_plan_list = []
    for i in range(n):
        for j in range(MAX_POW_TWO):
            nvoice = plan_list[i].voice * (2 ** j)
            nsms = plan_list[i].sms * (2 ** j)
            ndata = plan_list[i].data * (2 ** j)
            nprice = plan_list[i].price * (2 ** j)
            my_plan_list.append(plan(nprice, nvoice, nsms, ndata))
    return my_plan_list

def convert_to_original(solution):
    n = len(solution)
    original_n = int(n / MAX_POW_TWO)
    result = [0 for i in range(original_n)]

    for i in range(n):
        p = int(i / MAX_POW_TWO)
        result[p] += solution[i] * (2 ** int(i % MAX_POW_TWO))
    return result

def generate_initial_population(plan_list, limit_voice, limit_sms, limit_data):
    n = len(plan_list)
    
    result = set({}) 
    it = 0
    while len(result) < MAX_POPULATION_SIZE and it < 200:
        aux = []
        for j in range(n):
            r = random.randint(0, 1)
            aux.append(r)
        result.add(List(repair(plan_list, limit_voice, limit_sms, limit_data, aux)))
        it += 1

    return result

def repair(plan_list, limit_voice, limit_sms, limit_data, solution):
    n = len(plan_list)

    voice, sms, data = 0, 0, 0

    order = [i for i in range(n)]
    random.shuffle(order)

    for i in range(n):
        voice += solution[i] * plan_list[i].voice
        sms += solution[i] * plan_list[i].sms
        data += solution[i] * plan_list[i].data

    #ADD
    for i in order:
        if solution[i] == 0 and (voice < limit_voice or sms < limit_sms or data < limit_data):
            solution[i] = 1
            voice += plan_list[i].voice
            sms += plan_list[i].sms
            data += plan_list[i].data
        
    #DROP
    for i in reversed(order):
        if solution[i] == 1 and (voice - plan_list[i].voice >= limit_voice and sms - plan_list[i].sms >= limit_sms and data - plan_list[i].data >= limit_data):
            solution[i] = 0
            voice -= plan_list[i].voice
            sms -= plan_list[i].sms
            data -= plan_list[i].data
    return solution 

def fitnes_function(plan_list, solution):
    price = 0

    for i in range(len(solution)):
        price += solution[i] * plan_list[i].price
    
    return price

#def random_crossover(a, b):
#    c = []
#    n = len(a)
#    p = random.randint(1, n)
#    for i in range(p):
#        c.append(a[i])
#    for i in range(p, n):
#        c.append(b[i])
#    return c

def uniform_crossover(a, b):
    c = []
    n = len(a)
    for i in range(n):
        r = random.randint(0, 1)
        if r == 0:
            c.append(a[i])
        else: 
            c.append(b[i])
    return c

def mutation(a):
    n = len(a)
    c = [a[i] for i in range(n)]
    p = random.randint(0, n - 1)
   
    c[p] = 1 - c[p]
    return c

class List(list):
    def __hash__(self):
        B = 123
        hash = 0
        for i in range(len(self)):
            hash = hash * B + i
        return hash

def get_solution_ga(original_plan_list, limit_voice, limit_sms, limit_data):
    plan_list = convert_to_01(original_plan_list)

    sol, best = [], INF

    population_set = generate_initial_population(plan_list, limit_voice, limit_sms, limit_data)
    
    for a in population_set:
        aux = fitnes_function(plan_list, a)
        if aux < best:
            sol, best = a, aux

    it = 0
    while it < MAX_ITER:
        #fixing the fathers
        candidate_fathers = random.sample(population_set, 4)
        
        p1, p2 = [], []

        if fitnes_function(plan_list, candidate_fathers[0]) < fitnes_function(plan_list, candidate_fathers[1]):
            p1 = candidate_fathers[0]
        else:
            p1 = candidate_fathers[1]
        if fitnes_function(plan_list, candidate_fathers[2]) < fitnes_function(plan_list, candidate_fathers[3]):
            p2 = candidate_fathers[2]
        else:
            p2 = candidate_fathers[3]

        #reprducing fathers
        c = uniform_crossover(p1, p2)
        c = mutation(c)

        c = repair(plan_list, limit_voice, limit_sms, limit_data, c)
        
        if List(c) in population_set:
           continue

        sol2, worst = [], -INF

        for a in population_set:
            aux2 = fitnes_function(plan_list, a)
            if aux2 > worst:
                sol2, worst = a, aux2
        
        fc = fitnes_function(plan_list, c)
        if fc < worst:
            population_set.discard(sol2)
            population_set.add(List(c))
        if fc < best:
            sol, best = c, fc
        it += 1
    
    return convert_to_original(sol)

        
            
