import random
import time
from smart_m3.m3_kp_api import *

minVal, maxVal = 0, 10

playerID = "player_1"
currentGame = ""

def askForGame(kp):
    kp.load_rdf_remove(Triple(URI(playerID), URI("ask_for_a_game"), URI("game_master")))
    kp.load_rdf_insert(Triple(URI(playerID), URI("ask_for_a_game"), URI("game_master")))

def guess(kp):
    number = input("Input: ")
    if number == "":
        number = random.randint(minVal, maxVal)
    print("suggestion is " + str(number))
    kp.load_rdf_remove(Triple(URI(playerID), URI("guess"), None))
    kp.load_rdf_insert(Triple(URI(playerID), URI("guess"), Literal(number)))

class GameStarter_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        for data in added:
            currentGame = str(data[2])
            print(playerID + " start to play the " + currentGame)
            guess(kp)

class Move_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        for data in added:
            result = str(data[2])
            print("result is " + result)
            if result != "equal":
                guess(kp)
            else:
                print("You win!")
                askForGame(kp)

if __name__ == '__main__':
    kp = m3_kp_api(PrintDebug=True)

    subscription_triple = Triple(URI(playerID), URI("play"), None)
    handler_gameStarter = GameStarter_Handler(kp)
    handler_subscription1 = kp.load_subscribe_RDF(subscription_triple, handler_gameStarter)

    subscription_triple = Triple(URI(playerID), URI("result_is"), None)
    handler_move = Move_Handler(kp)
    handler_subscription2 = kp.load_subscribe_RDF(subscription_triple, handler_move)

    time.sleep(3)
    askForGame(kp)
    time.sleep(600)

    kp.load_unsubscribe(handler_subscription1)
    kp.load_unsubscribe(handler_subscription2)

    kp.clean_sib()
    kp.leave()
