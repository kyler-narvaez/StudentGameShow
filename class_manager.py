import json
import os

def is_valid_path(path):
    try:
        with open(path, 'r') as f:
            return True
    except:
        return False

class class_manager:
    def __init__(self):
        self.parent_dir = 'classes'
        os.makedirs(self.parent_dir, exist_ok=True)

    def load_students(self, path):
        if not is_valid_path(path):
            print(f'{path} does not exist')
            return {}
        
        with open(path, 'r') as f:
            students = json.load(f)
        
        return students

    def add_students(self, class_path):
        students = self.load_students(class_path)
        # if students == {}:
        #     return -1

        done = False
        while not done:
            print(f'Current Class:\n{students}')
            student = input(f'Enter student {len(students)+1} (done = stop): ')
            if student == 'done':
                break
            if student in students:
                print(f'{student} is already in the class')
                continue
            students[student] = 0 #initial score
            
        with open(class_path, 'w') as write:
            json.dump(students, write, indent=4)

    def create_class(self):
        students = {}
        class_name = input('Enter the name of the class: ')
        path = f'{self.parent_dir}/{class_name}.json'
        if is_valid_path(path):
            print(f'{path} already exists')
        else:
            self.create_file(path)
        self.add_students(path)

    def create_file(self, path):
        with open(path, 'x') as f:
            json.dump({}, f)

    def save_scores(self, scores, path):
        if not is_valid_path(path):
            print(f'Save file was not valid. Creating path and adding that save to be added manually.')
            self.create_file(path)

        with open(path, 'w') as f:
            json.dump(scores, f, indent=4)

    def pick_class(self):
        while True:
            classes = self.get_classes()
            for i in range(len(classes)):
                print(f'\n{i+1}. {classes[i]}')
            choice = input('\nPick a class: ')
            try:
                if int(choice) < 1 or int(choice) > len(classes):
                    print('Invalid Choice')
                else:
                    break
            except:
                print('Error - Expected Number')
        
        class_path = classes[int(choice) - 1]
        return class_path
        #print(f'path within the classes: {self.class_path}')

    def get_classes(self):
        return os.listdir(self.parent_dir)
    
    
        