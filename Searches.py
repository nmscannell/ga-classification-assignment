import csv
from utils import *


class Searches:

    @staticmethod
    def greedy_search(file, budget):
        q = PriorityQueue()
        remaining = budget
        reach = 0
        result = list()
        with open(file) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            i = 0
            for row in readcsv:
                q.push(Node((i, row[0], row[1], row[2]), row[2]))
                result.append(0)
                i = i+1
        for j in range(q.size()):
            option = q.pop()
            if int(option.data[2]) <= remaining:
                remaining = remaining - int(option.data[2])
                result[option.data[0]] = 1
                reach += int(option.data[3])
        result_str = ""
        for i in result:
            result_str += str(i)
        result_str = result_str + " cost: " + str(budget - remaining) + " reach: " + str(reach)
        return result_str

    @staticmethod
    def genetic_search(file, budget, num_options, ngen=100, pmut=0.1):
        info = []
        with open(file) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            i = 0
            for row in readcsv:
                info.append((i, row[0], row[1], row[2]))
                i = i + 1

        states = [[0 for i in range(num_options+1)] for j in range(2**num_options+1)]
        n = 1
        for i in range(1, 2**num_options):
            left = n
            if n % 2 == 1:
                states[i][num_options] = 1
                left -= 1
            j = 1
            while left > 0:
                k = left/(2**(num_options-j))
                if k >= 1:
                    states[i][j] = 1
                    left -= 2**(num_options-j)
                j += 1
            n += 1
            Searches.fitness(info, states[i], budget)
        random.shuffle(states)
        return Searches.genetic_algorithm(states[:100], budget, info, [0,1], ngen, pmut)

    @staticmethod
    def genetic_algorithm(population, budget, info, gene_pool=[0, 1], ngen=100, pmut=0.3):
        best_so_far = population[0]
        for i in range(100):
            for i in range(len(population)):
                x, y = Searches.select(2, population, info, budget)
                if Searches.fitness(info, x, budget) > Searches.fitness(info, best_so_far, budget):
                    best_so_far = x
                if Searches.fitness(info, y, budget) > Searches.fitness(info, best_so_far, budget):
                    best_so_far = y
                x, y = Searches.recombine(x, y)
                x = Searches.mutate(x, gene_pool, pmut, info, budget)
                y = Searches.mutate(y, gene_pool, pmut, info, budget)
                population.append(x)
                population.append(y)
                if Searches.fitness(info, x, budget) > Searches.fitness(info, best_so_far, budget):
                    best_so_far = x
                if Searches.fitness(info, y, budget) > Searches.fitness(info, best_so_far, budget):
                    best_so_far = y
                if len(population) > 100:
                    k = len(population)
                    l = 0
                    ll = 0
                    j = 0
                    while k > 100 > j:
                        if population[j][0] == 0:
                            del population[j]
                            k -= 1
                        if population[j][0] < population[l][0]:
                            ll = l
                            l = j
                        j += 1
                    del population[l]
                    del population[ll]

        q = PriorityQueue()
        for i in range(len(population)):
            q.push(Node(population[i][1:], population[i][0]))
        best = q.pop()
        if Searches.fitness(info, best_so_far, budget) < Searches.fitness(info, best.data, budget):
            best_so_far = best.data
        result = ""
        for i in range(1, len(best_so_far)):
            result += str(best_so_far[i])
        result += "  cost: "
        cost = 0
        for i in range(1, len(best_so_far)):
            if best_so_far[i] == 1:
                cost += int(info[i-1][2])
        result = result + str(cost) + " reach: " + str(best_so_far[0])
        return result

    @staticmethod
    def fitness(info, state, threshold):
        cost = 0
        fit_lev = 0
        for i in range(1, len(state)):
            if state[i] == 1:
                cost += int(info[i-1][2])
                if cost > threshold:
                    state[0] = 0
                    return 0
                fit_lev += int(info[i-1][3])
        state[0] = fit_lev
        return fit_lev

    @staticmethod
    def mutate(x, gene_pool, pmut, info, budget):
        if random.uniform(0, 1) >= pmut:
            return x

        n = len(x)
        g = len(gene_pool)
        c = random.randrange(0,n)
        r = random.randrange(0,g)

        new_gene = gene_pool[r]
        new = x[:c] + [new_gene] + x[c+1:]
        new[0] = Searches.fitness(info, new, budget)
        return new

    @staticmethod
    def recombine(x, y):
        n = len(x)
        c = random.randrange(0, n)
        return x[:c] + y[c:], y[:c] + x[c:]

    @staticmethod
    def select(r, population, info, budget):
        fitnesses = []
        for i in range(len(population)):
            fitnesses.append(Searches.fitness(info, population[i], budget))
        sampler = weighted_sampler(population, fitnesses)
        return[sampler() for i in range(r)]


class Node:

    def __init__(self, data, priority):
        self.data = data
        self.priority = priority


class PriorityQueue:

    def __init__(self):
        self.queue = list()

    def push(self, node):
        if self.size() == 0:
            self.queue.append(node)
        else:
            for i in range(self.size()):
                if int(node.priority) < int(self.queue[i].priority):
                    if i == self.size()-1:
                        self.queue.insert(i+1, node)
                        break
                    else:
                        continue
                elif int(node.priority) == int(self.queue[i].priority):
                    if node.data[2] < self.queue[i].data[2]:
                        self.queue.insert(i, node)
                    else:
                        self.queue.insert(i+1, node)
                    break
                else:
                    self.queue.insert(i, node)
                    break

    def pop(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)
