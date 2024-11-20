from userInteraction import UserInterface
import rps
import time

import msvcrt

import handRecognition

class Game:
    logic = {
            'rock': 'paper',
            'paper': 'sissors',
            'sissors': 'rock'
        }
    
    logicDisplay = {
            'rock': rps.displayRock(),
            'paper': rps.displayPaper(),
            'sissors': rps.displaySissors()
        }
    
    ruleNum = {
        'rock': 0,
        'paper': 1,
        'sissors': 2
    }
    
    def __init__(self, data) -> None:
        self.data = data
        self.round = 1
        self.computer = 0
        self.player = 0
        self.lastResult = [None, None]
        
    
    def shoot(self):
        print("Rock")
        time.sleep(0.4)
        print("Paper")
        time.sleep(0.4)
        print("Sissors")
        time.sleep(0.4)
        print("Shoot :::")

    def trackScore(self, round, winner):
        if winner == 'computer':
            self.computer += 1
        elif winner == 'player': self.player += 1
        else: pass # Draw

    def printScore(self, computer, player):
        print("Score: \n computer = ", computer, " | Player = ", player)

    def computerPlay(self):
        def maxIndxFun():
            # This if/else loop is due to we are storing the w/l/d in last result and full form in our json file.
            if self.lastResult[1] == 'd':
                winResultTemp = 'draw'
            elif self.lastResult[1] == 'w':
                winResultTemp = 'win'
            else:
                winResultTemp = 'loss'
            maxVal = max(self.data[winResultTemp][self.lastResult[0]][0])
            maxIndex = [index for index, value in enumerate(self.data[winResultTemp][self.lastResult[0]][0]) if value == maxVal]
            return maxIndex

        if self.lastResult != [None, None]:
            maxIndex = maxIndxFun()
            if len(maxIndex) == 1:
                if maxIndex[0] == 0:
                    return 'paper', rps.displayPaper()
                elif maxIndex[0] == 1:
                    return 'sissors', rps.displaySissors()
                else:
                    return 'rock', rps.displayRock()


            if self.lastResult[1] == 'w':
                if self.lastResult[0] == 'rock':
                    return 'paper', rps.displayPaper()
                elif self.lastResult[0] == 'paper':
                    return 'sissors', rps.displaySissors()
                else:
                    return 'rock', rps.displayRock()
            elif self.lastResult[1] == 'l':
                if self.lastResult[0] == 'rock':
                    return 'sissors', rps.displaySissors()
                elif self.lastResult[0] == 'paper':
                    return 'rock', rps.displayRock()
                else:
                    return 'paper', rps.displayPaper()
            else:
                if self.lastResult[0] == 'sissors':
                    return 'sissors', rps.displaySissors()
                elif self.lastResult[0] == 'rock':
                    return 'rock', rps.displayRock()
                else:
                    return 'paper', rps.displayPaper()
                
        else:
            rock_sum = (
                self.data["loss"]["rock"][1]
                + self.data["win"]["rock"][1]
                + self.data["draw"]["rock"][1]
            )
            paper_sum = (
                self.data["loss"]["paper"][1]
                + self.data["win"]["paper"][1]
                + self.data["draw"]["paper"][1]
            )
            sissors_sum = (
                self.data["loss"]["sissors"][1]
                + self.data["win"]["sissors"][1]
                + self.data["draw"]["sissors"][1]
            )

            # Store values in a dictionary for easy identification
            totals = {
                "rock": rock_sum,
                "paper": paper_sum,
                "sissors": sissors_sum,
            }

            # Find the maximum value
            max_value = max(totals.values())

            # Find all categories with the maximum value
            max_categories = [key for key, value in totals.items() if value == max_value]

            if len(max_categories) == 1:
                return Game.logic[max_categories[0]], Game.logicDisplay[Game.logic[max_categories[0]]]
            else:
                return 'sissors', rps.displaySissors()

    def updateUserData(self, player):
        if self.lastResult != [None, None]:    
            if self.lastResult[1] == 'w':
                self.data['win'][self.lastResult[0]][0][Game.ruleNum[player]] += 1
                self.data['win'][self.lastResult[0]][1] += 1
            elif self.lastResult[1] == 'l':
                self.data['loss'][self.lastResult[0]][0][Game.ruleNum[player]] += 1
                self.data['loss'][self.lastResult[0]][1] += 1
            elif self.lastResult[1] == 'd':
                self.data['draw'][self.lastResult[0]][0][Game.ruleNum[player]] += 1
                self.data['draw'][self.lastResult[0]][1] += 1
            
    def winnerIs(self, computer, player):
        #The predictionData is also getting updated, Because the dictionaries are mutable. Only the reference is been passed to the new variable. 
        self.updateUserData(player)
        
        if computer == player:
            self.lastResult = [player, 'd'] 
            return 'd'
        else:
            if Game.logic[player] == computer:   
                self.lastResult = [player, 'l']            
                return 'c'
            else:
                self.lastResult = [player, 'w']
                return 'p'   
            
    

    def game(self):  
        handRecognition.startWebcamThread()
        time.sleep(10)
        while True:
            print("\n\n\n The webcam is about to activate. Perform actions in front of the webcam. Keep a distance of about 50 centimeters.")
            print("MINIMIZE THE WINDOW.")
            
            print(f"Round Number: {self.round}")
            print("Press X to stop!")
            time.sleep(0.2)
            self.shoot()
            time.sleep(0.4)
            cmp, computer = self.computerPlay()

            # player = input("PLAY: ") #msvcrt.getch().decode()   # This is when the Hand tracking is not working and we need user input without letting them enter space on the terminal.
            print(f"Computer Played: \n{computer}")

            handRecognition.noteResults = 'now'
            time.sleep(0.4)
            handRecognition.noteResults = 'not now'

            player = max(handRecognition.result, key=handRecognition.result.get)
            if player == 'u' or player == None:
                print("Thanks for playing!")
                if self.round == 1:
                    pass
                else:
                    print(f"The final score is Computer: {self.computer} | Player: {self.player}")
                break
            print(f"\n You played: {player}")

            

            
            
            self.round += 1
            # print(f"Computer Played: \n{computer} \n\n You played: {player}")
            winner = self.winnerIs(cmp, player)
            if winner == 'd':
                print("Draw")
            elif winner == 'c':
                self.trackScore(self.round, 'computer')
                print(f"Computer Won! Computer: {self.computer} | Player: {self.player}")
            else:
                self.trackScore(self.round, 'player')
                print(f"Player Won! Computer: {self.computer} | Player: {self.player}")
            
            time.sleep(1.5)

        return (self.data)

        
def main():
    obj = UserInterface()
    response = obj.WelcomeStatement()
    if response == 'Rock':
        obj.Register()
    elif response == 'Paper':
        userName, predictionData = obj.play()
        game = Game(predictionData)
        changeData = game.game()
        obj.saveData(obj.users)


    elif response == 'Sissors':
        obj.rules()


if __name__ == '__main__':
    main()