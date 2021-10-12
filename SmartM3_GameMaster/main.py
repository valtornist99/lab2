import random
import time
from smart_m3.m3_kp_api import *

minVal, maxVal = 0, 10

gameCounter = 0

def startGame(playerID, kp):
    global gameCounter
    gameCounter += 1
    game = "game_" + str(gameCounter)
    number = random.randint(minVal, maxVal)
    kp.load_rdf_remove(Triple(URI(playerID), URI("play"), None))
    kp.load_rdf_insert(Triple(URI(playerID), URI("play"), URI(game)))
    kp.load_rdf_remove(Triple(URI(game), URI("number_is"), None))
    kp.load_rdf_insert(Triple(URI(game), URI("number_is"), Literal(number)))

def evaluateMove(playerID, number, kp):
    kp.load_query_rdf(Triple(URI(playerID), URI("play"), None))
    res = kp.result_rdf_query
    game = str(res[0][2])
    kp.load_query_rdf(Triple(URI(game), URI("number_is"), None))
    res = kp.result_rdf_query
    realNumber = int(str(res[0][2]))
    if number > realNumber:
        kp.load_rdf_remove(Triple(URI(playerID), URI("result_is"), URI("more")))
        kp.load_rdf_insert(Triple(URI(playerID), URI("result_is"), URI("more")))
    elif number < realNumber:
        kp.load_rdf_remove(Triple(URI(playerID), URI("result_is"), URI("less")))
        kp.load_rdf_insert(Triple(URI(playerID), URI("result_is"), URI("less")))
    else:
        kp.load_rdf_remove(Triple(URI(playerID), URI("result_is"), URI("equal")))
        kp.load_rdf_insert(Triple(URI(playerID), URI("result_is"), URI("equal")))


class GameStarter_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        time.sleep(3)
        for data in added:
            playerID = str(data[0])
            print("Start a new game for the " + playerID)
            startGame(playerID, kp)


class Move_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        time.sleep(3)
        for data in added:
            playerID = str(data[0])
            number = int(str(data[2]))
            print(playerID + " have guessed " + str(number))
            evaluateMove(playerID, number, kp)


if __name__ == '__main__':
    kp = m3_kp_api(PrintDebug=True)

    subscription_triple = Triple(None, URI("ask_for_a_game"), URI("game_master"))
    handler_gameStarter = GameStarter_Handler(kp)
    handler_subscription1 = kp.load_subscribe_RDF(subscription_triple, handler_gameStarter)

    subscription_triple = Triple(None, URI("guess"), None)
    handler_move = Move_Handler(kp)
    handler_subscription2 = kp.load_subscribe_RDF(subscription_triple, handler_move)

    input("...")

    kp.load_unsubscribe(handler_subscription1)
    kp.load_unsubscribe(handler_subscription2)

    kp.clean_sib()
    kp.leave()
