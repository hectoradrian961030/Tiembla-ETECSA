import copy

INF = 1000*1000*1000
MAX_COMPLEXITY = 1000*1000*10

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def gcd_reduction(plan_list, limit_voice, limit_sms, limit_data):
    n = len(plan_list)

    gcd_voice, gcd_sms, gcd_data = 0, 0, 0

    for i in range(n):
        gcd_voice = gcd(gcd_voice, plan_list[i].voice)
        gcd_sms = gcd(gcd_sms, plan_list[i].sms)
        gcd_data = gcd(gcd_data, plan_list[i].data)

    my_plan_list = copy.deepcopy(plan_list)
    #gcd reduction
    for i in range(n):
        my_plan_list[i].voice = int(my_plan_list[i].voice / gcd_voice)
        my_plan_list[i].sms = int(my_plan_list[i].sms / gcd_sms)
        my_plan_list[i].data = int(my_plan_list[i].data / gcd_data)

    limit_voice = int((limit_voice + gcd_voice - 1) / gcd_voice)
    limit_sms = int((limit_sms + gcd_sms - 1) / gcd_sms)
    limit_data = int((limit_data + gcd_data - 1) / gcd_data)

    return (my_plan_list, limit_voice, limit_sms, limit_data)


def get_solution_dp(plan_list, limit_voice, limit_sms, limit_data):
    n = len(plan_list)

    max_voice, max_sms, max_data = -1, -1, -1

    for i in range(n):
        max_voice = max(max_voice, plan_list[i].voice)
        max_sms = max(max_sms, plan_list[i].sms)
        max_data = max(max_data, plan_list[i].data)
  

    voice, sms, data = limit_voice + max_voice, limit_sms + max_sms, limit_data + max_data

    print(str(n) + "  " + str(voice) + "  " + str(sms) + "  " + str(data))

    #computing dp
    dp = [[[INF for i in range(data + 1)] for j in range(sms + 1)] for k in range(voice + 1)]
    prev = [[[0 for i in range(data + 1)] for j in range(sms + 1)] for k in range(voice + 1)]

    dp[0][0][0] = 0

    for h in range(n):
        current_voice, current_sms = plan_list[h].voice, plan_list[h].sms
        current_data, current_price = plan_list[h].data, plan_list[h].price
        for i in range(current_voice, voice + 1):
            for j in range(current_sms, sms + 1):
                for k in range(current_data, data + 1):
                    if dp[i - current_voice][j - current_sms][k - current_data] + current_price < dp[i][j][k]:
                        dp[i][j][k] = dp[i - current_voice][j - current_sms][k - current_data] + current_price
                        prev[i][j][k] = h

    #reconstructing solution
    current_i, current_j, current_k, best = 0, 0, 0, INF

    for i in range(limit_voice, voice + 1):
        for j in range(limit_sms, sms + 1):
            for k in range(limit_data, data + 1):
                if dp[i][j][k] < best:
                    best = dp[i][j][k]
                    current_i, current_j, current_k = i, j, k
    
    result = [0 for i in range(n)]

    while(current_i != 0 or current_j != 0 or current_k != 0):
        p = prev[current_i][current_j][current_k]
        result[p] += 1
        current_i -= plan_list[p].voice
        current_j -= plan_list[p].sms
        current_k -= plan_list[p].data
    
    return result
