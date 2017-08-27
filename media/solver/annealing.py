import random
import math
import sys


def Eggholder(x):
    """
    domain: -512 <= x1, x2 <= 512
    optimum: x1 = 512, x2 =404.2319, f(x1, x2) = -959.6407
    """
    for t in x:
        if t <= -512 or t >= 512:
            return 10000000

    return -(x[1] + 47) * math.sin(math.sqrt(abs(x[1] + 0.5 * x[0] + 47))) - x[0] * math.sin(math.sqrt(abs(x[0] - (x[1] + 47))))


def annealing(f, T=1000, cool=0.999, step=1):
    x = [random.uniform(-512, 512) for j in range(2)]

    while T > 0.001:
        delta = (random.random() - 0.5) * step

        # ランダムな次元の要素だけ変化させる
        i = random.randint(0, len(x) - 1)
        new_x = x
        new_x[i] = x[i] + delta

        # 評価関数値の計算
        old_eval = f(x)
        new_eval = f(new_x)
        print("T:{}, eval:{}".format(T, old_eval))

        # 遷移確率の計算
        p = math.e ** (-abs(new_eval - old_eval) / T)

        if(new_eval < old_eval or random.random() < p):
            x = new_x

        T = T * cool
    return x


if __name__ == '__main__':
    args = sys.argv
    T = float(args[1])
    cool = float(args[2])
    step = int(args[3])

    x = annealing(Eggholder, T, cool, step)
    print("x={}".format(x))
    print("eval:\n{}".format(Eggholder(x)))
