from typing import List
import random
class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0


    def create_a_population(self, string_length, size):
        result: List[str] = list()
        for i in range(size):
            string_of_action = ''
            for j in range(string_length):
                act = random.randint(0, 3)
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
        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            if (current_step == '_'):
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
        if actions[self.current_level_len - 1] == 1:
            ability += 1

        return end_of_game, ability

g = Game(["____G__LM_", "___G_M___L_"])
g.load_next_level()

# This outputs (False, 4)
print(g.get_score("0010002001", 1))
