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


def genetic_algorithm(f, n_pop=40, pop_size=10, mut_prob=0.2, elite=0.2, max_iter=500):
    def mutate(x):
        i = random.randint(0, n_pop - 1)
        return x[0:i] + [random.randint(0, 9)] + x[i + 1:]

    def crossover(r1, r2):
        i = random.randint(1, pop_size - 2)
        return r1[0:i] + r2[i:]

    def conv_gene2v(x):
        v1 = sum([t * (10 ** (2 - j)) for j, t in enumerate(x[:len(x) // 2])])
        v2 = sum([t * (10 ** (2 - j)) for j, t in enumerate(x[len(x) // 2:])])
        return [v1, v2]

    pop = []
    for i in range(pop_size):
        x = [random.randint(0, 9) for v in range(0, n_pop)]
        pop.append(x)

    n_elite = int(elite * pop_size)

    evals = []
    for i in range(max_iter):
        for x in pop:
            v = conv_gene2v(x)
            evals.append([f(v), x])
        evals = sorted(evals)
        print("eval:{}".format(evals[0][0]))
        ranked = [x for (e, x) in evals]

        pop = ranked[0:n_elite]

        while(len(pop) < pop_size):
            if random.random() < mut_prob:
                c = random.randint(0, n_elite)
                pop.append(mutate(ranked[c]))
            else:
                c1 = random.randint(0, n_elite)
                c2 = random.randint(0, n_elite)
                pop.append(crossover(ranked[c1], ranked[c2]))
    return conv_gene2v(evals[0][1])


if __name__ == '__main__':
    args = sys.argv
    pop_size = int(args[1])
    mut_prob = float(args[2])
    elite = float(args[3])
    max_iter = int(args[4])

    x = genetic_algorithm(Eggholder, 40, pop_size, mut_prob, elite, max_iter)
    print("x={}".format(x))
    print("eval:\n{}".format(Eggholder(x)))
