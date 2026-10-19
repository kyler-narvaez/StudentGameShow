import os
import class_manager
import game
import bets

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    cm = class_manager.class_manager()
    g = game.game()
    loop = True
    while loop:
        while True:
            todo = input('What would you like to do?\n\n1. Play\n2. Create New Class\n3. Add Students to Class\nOption: ')
            if todo == 'q':
                loop = False
                break
            try:
                if int(todo) < 1 or int(todo) > 4:
                    print('Invalid Input -- Try again')
                else:
                    break
            except:
                print('Error - Must enter number')

        match todo:
            case '1':
                g.start_game()
            case '2':
                cm.create_class()
            case '3':
                class_to_add = f'classes/{cm.pick_class()}'
                cm.add_students(class_to_add)

        #clear_screen()



if __name__ == '__main__':
    main()