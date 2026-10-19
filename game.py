import class_manager
import bets as bts
import spin_wheel
import random
import score_graph
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class game:
    def __init__(self):
        self.class_path = ''
        self.scores = {}
        self.class_manager = class_manager.class_manager()
    
    def start_game(self):
        #what class is playing
        self.class_path = self.class_manager.pick_class()
        self.scores = self.get_contestants()
        contestants = list(self.scores)
        print(contestants)

        #placing bets
        bets = bts.place_bets(contestants)
        print(bets)

        clear_screen()

        #pick the problem
        # max_problem = int(input('Enter the max problem number: '))
        # rand_problem = random.randint(1, max_problem)
        # print(f'The problem is {rand_problem}! (Can be changed)')
        input(f'Ready to continue: ') #wait to look at the problem

        clear_screen()

        #Double Downs
        double_downs = bts.place_bets(contestants)

        #Spin the online wheel
        chosen = spin_wheel.spin_wheel(contestants)

        if chosen == None:
            print('There seems to be some error in picking through spin. Randomly choosing contestant')
            chosen = random.choice(contestants)
        
        print(f'Congrats {chosen}! You have been chosen to answer the question\n')
        
        correct = input('\nDid they get it correct? ')

        clear_screen()

        if correct == 'yes':
            correct = True
            print(f'Congrats {chosen}! You did it!')
        else:
            correct = False
            print(f'Nice try {chosen}! Better luck next time!')

        #apply bets to scores
        self.apply_kyler_points(correct, chosen, bets, double_downs)

    def get_contestants(self):
        return self.class_manager.load_students(f'classes/{self.class_path}')
    
    def apply_kyler_points(self, correct, chosen, bets, double_downs):
        scores_before_game = self.scores.copy()
        double_down_points = 10
        bet_points = 10 #FIXME - Allow for input
        correct_points = 10

        for student in self.scores:
            if bets[student] == correct:
                print(f'\n{student} gets {bet_points} points for guessing right!')
                self.scores[student] += bet_points

                if double_downs[student] == True:
                    print(f'{student} also gets an additional {double_down_points} for doing a double down!')
                    self.scores[student] += double_down_points
                    
            
            elif double_downs[student] == True:
                print(f'{student} got it incorrect while they had a double down, they lose {double_down_points}')
                self.scores[student] -= double_down_points
        
        if correct:
            print(f'{chosen} got it correct, they get {correct_points} points!\n')
            self.scores[chosen] += correct_points

            if double_downs[chosen] == True:
                print(f'{chosen} double downed and they got it right! They get an additional {double_down_points * 2}')
                self.scores[chosen] += double_down_points * 2
        elif double_downs[chosen] == True:
            print(f'{chosen} double downed! They lose {double_down_points * 2}')
            self.scores[chosen] -= double_down_points * 2

        self.class_manager.save_scores(self.scores, f'classes/{self.class_path}')
        self.show_scores(scores_before_game)
        
    
    def show_scores(self, scores_before_game):
        print(f'Scores before game: {scores_before_game}\n')
        print(f'Scores after game: {self.scores}\n')
        score_graph.show_scores(scores_before_game, self.scores)
        

