import numpy as np
import sys
 
board_size=8
pop_size=100
cross_prob=0.5 
mut_prob=0.25
max_epochs= 100
min_fitness= 1

class Solver_8_queens:
    def __init__(self, pop_size=100, cross_prob=0.5, mut_prob=0.25): 
        self.pop_size= pop_size
        self.cross_prob= cross_prob
        self.mut_prob= mut_prob
        self.sequence= None
        self.fitnessFunction= None
        self.population= None
        
    def solve(self):
        global population
        population= generatePopulation(pop_size)
        best_fit= round(np.max([x.fitnessFunction for x in population]),1)
        epoch_num = 0
        visualization = None
        
        for each in population: 
            print ("iteration:", epoch_num, "\n"+"sequence: ", each.sequence, "fit_func: ", each.fitnessFunction)
        
        #if (min_fitness is not None) and (max_epochs is not None):        
        while ((best_fit < min_fitness) and (epoch_num != max_epochs)):
            population = geneticAlgorithm(epoch_num)
            best_fit= round(np.max([x.fitnessFunction for x in population]),1)
            for each in population: 
                 if each.fitnessFunction == best_fit:
                    print ("\n"+"best Solution:", each.sequence, "\n" + "Fitness:", "%.1f" % best_fit, "\n" + "Iterations:", epoch_num)            
            epoch_num +=1
        #else: print ("min_fitness and max_epochs is None") sys.exit(-1)
           
        for each in population:
            if each.fitnessFunction == best_fit:
                visualization= ("\n"+("\n".join("+"*i + "Q" + "+"*(board_size-i-1) for i in each.sequence)))
                #print ("\n"+"best Solution:" + "\n" + "Fitness:", "%.1f" % best_fit, "\n" + "Iterations:", epoch_num, visualization)            
        
        return best_fit, epoch_num, visualization
        

def generateChromosome():
    chromosome= np.random.permutation(board_size)
    return chromosome
    
    
def fitnessFunction(chromosome): 
    conflicts = 0 
    row_col_conflicts = abs(len(chromosome) - len(np.unique(chromosome))) 
    conflicts += row_col_conflicts 
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if ( i != j):
                dx = abs(i-j)
                dy = abs(chromosome[i] - chromosome[j])
                if(dx == dy):
                    conflicts += 1
    return (28 - conflicts)/28     
                          
    
def generatePopulation(pop_size):
    population = [Solver_8_queens() for i in range(pop_size)]
    for i in range(pop_size):
        population[i].sequence= generateChromosome()
        population[i].fitnessFunction= fitnessFunction(population[i].sequence)
    #for each in population: print ("sequence: ", each, each.sequence, "fit_func: ", each.fitnessFunction)
    return population


def getParent():
    parent1, parent2 = None, None
    while True:
        parent1tmp = [x for x in population if x.fitnessFunction >= cross_prob]
        try:
            parent1 = parent1tmp[0]
            #print ("parent1: ", parent1.sequence, parent1.fitnessFunction)
            break
        except:
            pass
    while True:
        parent2tmp = [x for x in population if x.fitnessFunction >= cross_prob]
        try:
            t = np.random.randint(len(parent2tmp))
            parent2 = parent2tmp[t]
            if parent2 != parent1:
                break
            else:
                continue
            #print ("parent2: ", parent2.sequence, parent2.fitnessFunction)
            break
        except:
            pass

    if parent1 is not None and parent2 is not None:
        return parent1, parent2
    else:
        sys.exit(-1)

                            
def getChild(parent1, parent2):
    n = len(parent1.sequence)
    c = np.random.randint(1,n)
    #print("cross c: ", c)
    child = Solver_8_queens()
    child.sequence = []
    child.sequence.extend(parent1.sequence[0:c])
    child.sequence.extend(parent2.sequence[c:])
    child.fitnessFunction= fitnessFunction(child.sequence)
    #print("child: ", child.sequence, child.fitnessFunction)
    return child
    
    
def mutateChild(child):
    if np.random.rand() > mut_prob:
        c = np.random.randint(board_size)
        #print("mutate c: ", c)
        child.sequence[c] = np.random.randint(board_size)
    return child
        

def geneticAlgorithm(epoch_num):
    newpopulation = []
    i=0
    while i != len(population):
        parent1, parent2 = getParent()
        #print ("Parents generated : ", parent1.sequence, parent1.fitnessFunction, parent2.sequence, parent1.fitnessFunction)
        child = getChild(parent1, parent2)
        #print ("Child : ", child.sequence, child.fitnessFunction)
        child = mutateChild(child)
        #print ("Mutate child : ", child.sequence)
        if (child.fitnessFunction>=parent1.fitnessFunction):
            newpopulation.append(child)
            print (i, "Child : ", child.sequence, child.fitnessFunction)
            i+= 1     
    return newpopulation 