import random
import math
import numpy as np
import sys
import copy


def Eggholder(x):
    """
    domain: -512 <= x1, x2 <= 512
    optimum: x1 = 512, x2 =404.2319, f(x1, x2) = -959.6407
    """
    for t in x:
        if t <= -512 or t >= 512:
            return 10000000

    return -(x[1] + 47) * math.sin(math.sqrt(abs(x[1] + 0.5 * x[0] + 47))) - x[0] * math.sin(math.sqrt(abs(x[0] - (x[1] + 47))))


def pso(f, N=500, max_iter=1000, w=0.5, rho_max=0.14):
    x_min, x_max = -512, 512
    ps = [{"x": [random.uniform(x_min, x_max) for i in range(2)]} for j in range(N)]
    vs = [{"x": [0.0 for i in range(2)]} for j in range(N)]
    pbest = [f(p["x"]) for p in ps]
    pbest_x = copy.deepcopy(ps)
    gbest = np.argmin(pbest)
    gbest_x = copy.deepcopy(pbest_x[gbest])

    for t in range(max_iter):
        for i in range(N):
            x = ps[i]["x"]
            v = vs[i]["x"]

            # xの更新
            new_x = [x[i] + v[i] for i in range(2)]
            ps[i] = {"x": new_x}

            # vの更新
            rho1 = random.uniform(0, rho_max)
            rho2 = random.uniform(0, rho_max)
            new_v = [w * v[j] + rho1 * (pbest_x[i]["x"][j] - x[j]) + rho2 * (gbest_x["x"][j] - x[j]) for j in range(2)]
            vs[i] = {"x": new_v}

            # 評価値の計算
            eval_v = f(new_x)
            if eval_v < pbest[i]:
                pbest[i] = eval_v
                pbest_x[i] = {"x": new_x}
        gbest = np.argmin(pbest)
        gbest_x = copy.deepcopy(pbest_x[gbest])
        print("eval:{}".format(min(pbest)))
    return gbest_x["x"]


if __name__ == '__main__':
    args = sys.argv
    N = int(args[1])
    max_iter = int(args[2])
    w = float(args[3])
    rho_max = float(args[4])

    x = pso(Eggholder, N, max_iter, w, rho_max)
    print("x={}".format(x))
    print("eval:\n{}".format(Eggholder(x)))
