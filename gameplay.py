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
    
    rule = {
            'j': 'rock',
            'k': 'paper',
            'l': 'sissors',
            'J': 'rock',
            'K': 'paper',
            'L': 'sissors'
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
        if round != 1:
            if winner == 'computer':
                self.computer += 1
            elif winner == 'player': self.player += 1
            else: pass # Draw

    def printScore(self, computer, player):
        print("Score: \n computer = ", computer, " | Player = ", player)

    def computerPlay(self):
        maxVal = max(self.data.values())
        probab = [key for key, value in self.data.items() if value == maxVal]

        if len(probab) == 1:
            if Game.logic[probab[0]] == 'paper':
                return 'paper', rps.displayPaper()
            elif Game.logic[probab[0]] == 'rock':
                return 'rock', rps.displayRock()
            else:
                return 'sissors',rps.displaySissors()
        
        else:
            if self.lastResult != [None, None]:
                if self.lastResult[0] == 'rock':
                    if self.lastResult[1] == 'w':
                        return 'paper', rps.displayPaper()
                    else: 
                        return 'sissors', rps.displaySissors()
                elif self.lastResult[0] == 'paper':
                    if self.lastResult[1] == 'w':
                        return 'sissors', rps.displaySissors()
                    else: 
                        return 'rock', rps.displayRock()
                else:
                    if self.lastResult[1] == 'w':
                        return 'rock', rps.displayRock()
                    else: 
                        return 'paper', rps.displayPaper()

            else:
                return 'sissors', rps.displaySissors()
            
    def winnerIs(self, computer, player):
        self.data[Game.rule[player]] += 1  #The predictionData is also getting updated, Because the dictionaries are mutable. Only the reference is been passed to the new variable. 
        if computer == Game.rule[player]:
            self.lastResult = [player, 'd']
            return 'd'
        else:
            if Game.logic[Game.rule[player]] == computer:   
                self.lastResult = [Game.rule[player], 'l']            
                return 'c'
            else:
                self.lastResult = [Game.rule[player], 'w']
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
            time.sleep(0.8)
            cmp, computer = self.computerPlay()
            # player = msvcrt.getch().decode()
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
            print(f"\n You played: {Game.rule[player]}")

            

            
            
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