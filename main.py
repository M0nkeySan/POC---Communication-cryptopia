#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import signal
import sys
from cryptopia_api import Api
import actions

# Get these from (link here)
def get_secret(secret_file):
    """Grabs API key and secret from file and returns them"""

    with open(secret_file) as secrets:
        secrets_json = json.load(secrets)
        secrets.close()

    return str(secrets_json['key']), str(secrets_json['secret'])


def sigint_handler():
    """Handler for ctrl+c"""
    print('\n[!] CTRL+C pressed. Exiting...')
    sys.exit(0)


EXIT_CYCLE = False
while not EXIT_CYCLE:

    # setup api
    KEY, SECRET = get_secret("secrets.json")
    API = Api(KEY, SECRET)

    COIN = input("Choisissez le coin à observer : \
           \nSoyez précis !\nEcrivez en majuscule (ex : WISH)\n")

    # do before entering coin to save the API call during the pump
    BALANCE, ERROR = API.get_balance(COIN)
    if ERROR is not None:
        print("L'erreur suivante a été retournée : \n" + ERROR)
        AVAILABLE = 0
    else:
        AVAILABLE = BALANCE['Available']

    signal.signal(signal.SIGINT, sigint_handler)

    ALLOW_ORDERS = True

    print('Vous avez', AVAILABLE, COIN, 'disponible(s).')

    PAIRS, ERROR = API.get_tradepairs()

    print('Choisissez votre paire :')
    index = 0
    LISTE_PAIRES = []

    for PAIR in PAIRS:
        if PAIR['Status'] == 'OK' and COIN + "/" in PAIR['Label']:
            LISTE_PAIRES.append(PAIR['Label'])
            print(index, ":", PAIR['Label'])
            index += 1

    if index == 0:
        print("Aucune paire tradable n'a été trouvé.")
        break

    while True:
        correct = False
        while not correct:
            try:
                INDEX_PAIRE = int(input("Votre choix : "))
                correct = True
            except ValueError:
                print('Veuillez entrer un chiffre en 0 et', index - 1, '!')

        if len(LISTE_PAIRES) > INDEX_PAIRE:
            PAIR = LISTE_PAIRES[INDEX_PAIRE]
            break

    liste_actions = {0: actions.observation,
                     1: actions.buy_order,
                     2: actions.sell_order}

    while True:
        correct = False
        while not correct:
            try:
                ACTION = int(input("Quelle action voulez-vous réaliser ? : \
                            \n0: Observation du cours. \
                            \n1: Faire un buy order. \
                            \n2: Faire un sell order. \
                            \nVotre choix : "))
                correct = True
            except ValueError:
                print('Veuillez entrer un chiffre en 0 et 2 !')

        if len(liste_actions) > ACTION:
            liste_actions[ACTION](API, PAIR)
            break

    if __name__ == "__main__":
        ANSWER = input("\nVoulez-vous relancer le bot ? (y/n) ")
        if ANSWER.lower().strip() in "n no".split():
            EXIT_CYCLE = True
