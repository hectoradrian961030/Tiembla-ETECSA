from dp import *
from ga import *
from planes import *
from lo import *


def get_solution(plan_list, limit_voice, limit_sms, limit_data):
    #nplan_list, nlimit_voice, nlimit_sms, nlimit_data = gcd_reduction(plan_list, limit_voice, limit_sms, limit_data)
    #result = get_solution_ga(nplan_list, nlimit_voice, nlimit_sms, nlimit_data)
    result = get_solution_ga(plan_list, limit_voice, limit_sms, limit_data)
    return result, fitnes_function(plan_list, result)


#debug----------------------------------
def get_solution2(plan_list, limit_voice, limit_sms, limit_data):
    result = get_solution_lo(plan_list, limit_voice, limit_sms, limit_data)
    return result, fitnes_function(plan_list, result)

ga, fga = get_solution(planes, 1560, 2120, 4500)
for i in range(len(ga)):
    print(ga[i])
print (str(fga) + "  fitnes ga")

print("\n\n")

lo, flo = get_solution2(planes, 1560, 2120, 4500)
for i in range(len(lo)):
    print(lo[i])
print (str(flo) + "  fitnes lo")