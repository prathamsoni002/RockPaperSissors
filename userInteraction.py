# This is to interract with the Users.
# This will contain the command prompt details. 

# Welcome Statement:

import json
import os
import handRecognition

userdb_file = "userdata.json"


class UserInterface:
    def __init__(self) -> None:
        self.users = self.loadData()

    def loadData(self):
        if os.path.exists(userdb_file):
            with open(userdb_file, 'r') as file:
                return json.load(file)
        print("\nERROR: No File Exist.\n")
    
    def saveData(self, data):
        with open(userdb_file, 'w') as file:
            json.dump(data, file, indent=4)

        
    def WelcomeStatement(self):
        print("Welcome to the Kingdom of Rock Paper and Sissors! \n It is a kingdom where your every actions are taken into our consideration and remembered for life!\n")
        print("\n\n")
        print("-R-P-S- "*25)
        print("1. If you are new then please register to this relm by type 'Rock'.\n")
        print("2. If you are already a member then type 'Paper'. \n")
        print("3. If you want to learn how to play then type 'Sissors'.\n")
        
        response = input()

        print("\n\n")
        print("-R-P-S- "*25)

        return response
    
    def Register(self):
        print("Welcome to the Registration:\n")
        print("\n")
        print("-R-P-S- "*25)
        while True:
            userName = input("Enter your User name: ").strip()
            if not userName:
                print("\n!!!Username could not be empty. Please try again: \n")
                continue
            if userName in self.users:
                print("Username already exist, please try another unique username. \n")
            else:
                break

        password = input("\n Enter a Password: ")

        self.users[userName] = {
            "password" : password,
            "predictionData" : {
                'loss':{
                    'rock': [[0, 0, 0], 0],
                    'paper': [[0, 0, 0], 0],
                    'sissors': [[0, 0, 0], 0]
                },
                'win':{
                    'rock': [[0, 0, 0], 0],
                    'paper': [[0, 0, 0], 0],
                    'sissors': [[0, 0, 0], 0]
                },
                'draw':{
                    'rock': [[0, 0, 0], 0],
                    'paper': [[0, 0, 0], 0],
                    'sissors': [[0, 0, 0], 0]
                }
            }
        }

        self.saveData(self.users)

    def play(self):
        print("\nPlease validate yourself: ")
        while True:
            userName = input("\nEnter your Username: ").strip()
            password = input("\n Enter your Password: ")
            if userName not in self.users or self.users[userName]["password"] != password:
                print("Username or password does not match. Try again.\n")
            else:
                break
        print("-R-P-S- "*25)
        return userName, self.users[userName]["predictionData"]
    
    def rules(self):
        print("\n Basic Rock-Paper-Sissors rules apply.")
        print("After the display of \nRock\nPaper\nSissors\nShoot:::\nYou have to give your response and at the same time the computer will give its response as well!")
        print("Your response will look like:\n"
              "J: Rock \nK: Paper \nL: Sissors \n"
              "X: To end the game")
        

def main():
    print("Running the Test")
    test = UserInterface()
    response = test.WelcomeStatement()
    if response == 'Rock':
        test.Register()
    elif response == 'Paper':
        print(test.play())
    elif response == 'Sissors':
        test.rules()
    

if __name__ == "__main__":
    main()

