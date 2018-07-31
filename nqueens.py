import numpy as np
import sys
 
board_size=8
pop_size=100
cross_prob=0.8 
mut_prob=0.6
max_epochs= 100
min_fitness= 1

class Solver_8_queens:
    def __init__(self, pop_size=100, cross_prob=0.8, mut_prob=0.6): 
        self.pop_size= pop_size
        self.cross_prob= cross_prob
        self.mut_prob= mut_prob
        self.sequence= None
        self.fitnessFunction= None
        self.population= None

        
    def solve(self, min_fitness= 1, max_epochs= 100):
        epoch_num = 0
        condition= True
        visualization = None      
        
        global population
        population= generatePopulation(pop_size)
        
        if ((min_fitness is None) and (max_epochs is None)):
            sys.exit("min_fitness and max_epochs are None")
               
        while condition:
            population = geneticAlgorithm(epoch_num)
            best_fit= np.max([x.fitnessFunction for x in population])
            for each in population:
                if each.fitnessFunction == best_fit:
                    visualization= ("\n".join("+"*i + "Q" + "+"*(board_size-i-1) for i in each.sequence))
            epoch_num +=1
            condition= ((best_fit < min_fitness) and (epoch_num != max_epochs)) if ((min_fitness is not None) and (max_epochs is not None)) else (epoch_num != max_epochs) if (max_epochs is not None) else (best_fit < min_fitness)                        

        #print ("\n"+"best Solution:" + "\n" + "Fitness:", "%.1f" % best_fit, "\n" + "Iterations:", epoch_num, visualization)                
        return round(best_fit,1), epoch_num, visualization
        

def generateChromosome():
    chromosome= np.random.permutation(board_size)
    return chromosome
    
    
def fitnessFunction(chromosome): 
    conflicts = 0 
    max_unique= (board_size*(board_size-1))/2
    row_col_conflicts = abs(len(chromosome) - len(np.unique(chromosome))) 
    conflicts += row_col_conflicts 
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if ( i != j):
                dx = abs(i-j)
                dy = abs(chromosome[i] - chromosome[j])
                if(dx == dy):
                    conflicts += 1
    return (max_unique - conflicts)/max_unique     
                          
    
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
        parent1tmp = [x for x in population if x.fitnessFunction <= cross_prob]
        try:
            parent1 = parent1tmp[0]
            #print ("parent1: ", parent1.sequence, parent1.fitnessFunction)
            break
        except:
            pass
    while True:
        parent2tmp = [x for x in population if x.fitnessFunction <= cross_prob]
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
    c = np.random.randint(board_size)
    #print("mutate c: ", c)
    child.sequence[c] = np.random.randint(board_size)
    return child
        

def geneticAlgorithm(epoch_num):
    newpopulation = []
    for i in range(len(population)):
        parent1, parent2 = getParent()
        #print ("Parents generated : ", parent1.sequence, parent1.fitnessFunction, parent2.sequence, parent1.fitnessFunction)
        child = getChild(parent1, parent2)
        #print ("Child : ", child.sequence, child.fitnessFunction)
        if mut_prob>= np.random.rand():
            child = mutateChild(child)
            #print ("Mutate child : ", child.sequence)
        newpopulation.append(child)
        #print (i, "Child : ", child.sequence, child.fitnessFunction)
    return newpopulation 