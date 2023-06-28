from typing import List, Tuple
import random
from matplotlib import pyplot as plt
best_chromosome__ : Tuple[str, int] = ('', 0)
best_chromosomes: List[int] = list()
avg_chromosomes: List[float] = list()
worse_chromosomes: List[int] = list()
class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0


    def initial_a_population(self, string_length, size):
        result: List[str] = list()
        for i in range(size):
            string_of_action = ''
            for j in range(string_length):
                act = random.randint(0, 10)
                if act<= 5:
                    act =0
                elif act > 5 and act<8:
                    act = 1
                elif act >=8 and act <=10:
                    act = 2
                string_of_action += str(act)
            result.append(string_of_action)
        return result


    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])
    
    def get_score(self, actions, permission):
        # Get an action sequence and determine the steps taken/score
        # Return a tuple, the first one indicates if these actions result in victory
        # and the second one shows the steps taken

        current_level = self.levels[self.current_level_index]
        steps = 0
        max_scores: List[int] = list()
        number_of_mashroom = 0
        number_of_dead_Gomba = 0
        end_of_game = False
        negative_action = 0
        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            if (current_step == '_'):
                if actions[i-1] == 1 or actions[i-1] ==2:
                    negative_action += 1
                steps += 1
            elif (current_step == 'G'):
                if actions[i-1] == '1':
                    steps += 1
                elif actions[i-2] == '1':
                    steps += 1
                    number_of_dead_Gomba += 1

            elif (current_step == 'L' and actions[i - 1] == '2'):
                steps += 1
            elif (current_step == 'M'):
                steps += 1
                if actions[i-1] == '_':
                    number_of_mashroom += 1

            else:
                max_scores.append(steps)
                steps = 0
                continue
        max_scores.append(steps)
        ability = max(max_scores)
        # TODO don't add anything upper this text
        if permission and ability == self.current_level_len - 1:
            end_of_game = True
            ability += 5
        ability += number_of_mashroom * 2
        ability += number_of_dead_Gomba * 2
        ability -= negative_action * 0.5
        if actions[self.current_level_len - 1] == 1:
            ability += 1

        return end_of_game, ability

    def my_func(self, val):
        (a,b) = val
        return b

    def find_result(self, probability, chromosomes:List[Tuple[str,int]]):
        for (string, scor) in chromosomes:
            if scor >= probability:
                return (string, scor)


    def select(self, type_selection,chromosomes  :List[Tuple[str, int]], number_of_selection):
        if type_selection == 0:
            # if type selection equal zero that's mean, we only have a selection of the best
            chromosomes.sort(key=self.my_func, reverse=True)
            return chromosomes[:number_of_selection]
        else:
            possibility_of_selection: List[Tuple[str, int]] = list()
            total_value = 0
            for value in chromosomes:
                string_, score = value
                total_value += score

            last_value = 0
            # maximum of each interval
            for val in chromosomes:
                string_2, score_2 = val
                score_2 = score_2/total_value
                score_2 += last_value
                last_value = score_2

            random_selection_by_probability = 0
            for i in range(number_of_selection):
                random_selection_by_probability = random.randint(0, 100)
                random_selection_by_probability = random_selection_by_probability/100
                possibility_of_selection.append(self.find_result(random_selection_by_probability, chromosomes))
            return possibility_of_selection


    def cross_over(self, parentA:str, parentB:str, type_of_crros_over:int):
        parentA = list(parentA)
        parentB = list(parentB)
        if type_of_crros_over == 0:
            # single point cross over
            mid_point = int(abs(len(parentA) / 2))
            child_1 = parentA[: mid_point] + parentB[mid_point:]
            child_2 = parentB[:mid_point] + parentA[mid_point:]
        else:
            one_third = int(abs(len(parentA)/3))
            two_third = int(abs((len(parentA) * 2)/3))
            child_1 = parentA[:one_third]+parentB[one_third:two_third]+parentA[two_third:]
            child_2 = parentB[:one_third]+parentA[one_third:two_third]+parentB[two_third:]
        return child_1, child_2

    def mutate_bits(self, string:str, mutation_prob:int):
        new_string = list(string)
        for i in range(len(new_string)):
            create_random_number = random.randint(0, 100)
            create_random_number = create_random_number/100
            if create_random_number < mutation_prob:
                create_new_act = random.randint(0, 2)
                new_string[i] = str(create_new_act)
        return "".join(new_string)


def calculate_score_for_initialize_population(initialize_population, permission):
    for ini_pop in initialize_population:
        end_of_game, ability = my_game.get_score(ini_pop, permission)
        chromosomes.append((ini_pop, ability))

def cross_over_of_parent(parent:List[Tuple[str, int]], type_of_cross_over):
    cross_over_parents :List[str] = list()
    for i in range(0,len(parent),2):
        parentA , score = parent[i]
        parentB, score =parent[i+1]
        child_1, child_2 = my_game.cross_over(parentA, parentB, type_of_cross_over)
        cross_over_parents.append("".join(child_1))
        cross_over_parents.append("".join(child_2))
    return cross_over_parents

def mutate_chromosomes(children, mutation_probability):
    new_children :List[str] =list()
    for child in children:
        new_child = my_game.mutate_bits(child, mutation_probability)
        new_children.append(new_child)
    return new_children
def calculate_score_of_children(new_children,permission):
    for child in new_children:
        end_of_game, ability = my_game.get_score(child, permission)
        chromosomes.append((child, ability))

def find_best_avg_worst_chromosomes():
    total_chromosome = 0
    val , min_score = chromosomes[0]
    val , max_score = chromosomes[0]
    best_chromosome_until_see = (val, max_score)
    for string , scor in chromosomes:
        total_chromosome += scor
        if max_score < scor:
            max_score = scor
            best_chromosome_until_see = (string, scor)
        if min_score > scor:
            min_score = scor
    avg_chromosome = total_chromosome/len(chromosomes)
    avg_chromosomes.append(avg_chromosome)
    best_chromosomes.append(max_score)
    worse_chromosomes.append(min_score)

    final_value , final_score = best_chromosome__
    now_value, now_score = best_chromosome_until_see
    if final_score > now_score:
        return best_chromosome__
    else:
        return best_chromosome_until_see



chromosomes :List[Tuple[str, int]] = list()
my_game = Game(["____G_G_MMM___L__L_G_____G___M_L__G__L_GM____L____"])
my_game.load_next_level()
size_of_population = int(input("Enter the number of the initial population you want: "))
initialize_population = my_game.initial_a_population(my_game.current_level_len, int(size_of_population))
permission = int(input("Allow calculation of fitness evaluation with winning points(0 or 1): "))
calculate_score_for_initialize_population(initialize_population, permission)
type_of_selections= int(input("Enter your approach for selection(0-best chromosomes , 1-weighted selection based on fitness evaluation): "))
type_of_cross_over = int(input("Enter type of cross over (0-single point 1-double points): "))
mutation_probability = float(input("Mutation probability: (like 0.20): "))
generation = 100
while True:
    select_parent = my_game.select(type_of_selections, chromosomes, size_of_population)
    children = cross_over_of_parent(select_parent, type_of_cross_over)
    new_children = mutate_chromosomes(children, mutation_probability)
    calculate_score_of_children(new_children, permission)
    next_generation = my_game.select(type_of_selections, chromosomes, size_of_population)
    best_chromosome__ = find_best_avg_worst_chromosomes()
    chromosomes.clear()
    chromosomes = next_generation
    generation -= 1
    if generation < 0:
        break


print(best_chromosome__)
print(best_chromosomes)
print(avg_chromosomes)
print(worse_chromosomes)
plt.plot(best_chromosomes)
plt.plot(avg_chromosomes)
plt.plot(worse_chromosomes)
plt.show()
