#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


def observation(api, pair):
    pair = pair.replace("/", "_")

    libelles_coin = pair.split("_", 1)

    while True:
        market, error = api.get_market(pair)
        if error is not None:
            print("L'erreur suivante a été retournée : \n" + error)
        else:
            print('Dernier prix : {:.8f} {}'.format(market['LastPrice'], libelles_coin[1]))
            print("Prix d'achat : {:.8f} {}".format(market['BidPrice'], libelles_coin[1]))
            print('Prix de vente : {:.8f} {}'.format(market['AskPrice'], libelles_coin[1]))
            print('High : {:.8f} {}'.format(market['High'], libelles_coin[1]))
            print('Low : {:.8f} {}'.format(market['Low'], libelles_coin[1]))
            print('Change :', market['Change'], '%')

        time.sleep(5)


def buy_order(api, pair):
    pair = pair.replace("/", "_")

    libelles_coin = pair.split("_", 1)

    ordre_fini = False

    while ordre_fini is not True:

        balance_achat, error = api.get_balance(libelles_coin[1])
        if error is not None:
            print("L'erreur suivante a été retournée : \n" + error)
            disponibilite_achat = 0
        else:
            disponibilite_achat = balance_achat['Available']

        print('Vous avez', disponibilite_achat, libelles_coin[1], 'disponible(s).')

        if disponibilite_achat != 0:
            print('Vous ne pouvez pas effectuer de buy order')
            return
        else:
            correct = False
            while not correct:
                try:
                    balance_utilisee = float(
                        input("Combien de {} voulez-vous utiliser ? : ".format(libelles_coin[1])))
                    correct = True
                except ValueError:
                    print('Veuillez entrer un nombre !')

            while balance_utilisee > disponibilite_achat:
                print('Vous ne pouvez utiliser plus de {}'.format(disponibilite_achat))
                correct = False
                while not correct:
                    try:
                        balance_utilisee = float(
                            input("Combien de {} voulez-vous utiliser ? : ".format(libelles_coin[1])))
                        correct = True
                    except ValueError:
                        print('Veuillez entrer un nombre !')

            marche_paire, error = api.get_market(pair)
            if error is not None:
                print("L'erreur suivante a été retournée : \n" + error)
                return

            print("L'ordre de vente le moins cher est de {:.8f} \n".format(marche_paire['AskPrice']))

            correct = False
            while not correct:
                try:
                    bid_price = float(input("Quel est votre prix ? : "))
                    correct = True
                except ValueError:
                    print('Veuillez entrer un nombre !')

            # prise en compte des fees de Cryptopia pour calculé le nombre de coins achetable
            num_coins = (balance_utilisee * (balance_utilisee * 0.00201)) / bid_price
            prix_achat = bid_price * num_coins

            trade, error = api.submit_trade(pair.replace("_", "/"), 'Buy', bid_price, num_coins)
            if error is not None:
                print("L'erreur suivante a été retournée : \n" + error)
                return

            print(trade)

            print("\n[+] Ordre d'achat placé pour {:.8f} {} coins à {:.8f} {} \
                   chacun pour un total de {} {}".format(num_coins, libelles_coin[0], bid_price, libelles_coin[1],
                                                         prix_achat, libelles_coin[1]))

            time.sleep(5)

            open_orders, error = api.get_openorders(pair.replace("_", "/"))
            if error is not None:
                print("L'erreur suivante a été retournée : \n" + error)
                return

            if open_orders is not None:
                print("Votre ordre n'est pas passé entierement, il reste {:.8f} coins à acheter".format(open_orders[0]['Remaining']))

                correct = False

                while correct is not True:
                    reponse = input("Voulez-vous modifier votre ordre ? (y/n)")

                    if reponse == "y":
                        correct = True
                        data, error = api.cancel_trade('Buy', open_orders[0]['OrderId'], open_orders[0]['TradePairId'])

                        if error is not None:
                            print("L'erreur suivante a été retournée : \n" + error)
                            return
                    elif reponse == "n":
                        correct = True
                        ordre_fini = True
                        return
            else:
                balance, error = api.get_balance(libelles_coin[1])
                if error is not None:
                    print("L'erreur suivante a été retournée : \n" + error)
                    disponibilite = 0
                else:
                    disponibilite = balance['Available']

                print("Votre ordre est  passé entierement !")
                print('Vous avez', disponibilite, libelles_coin[1], 'disponible(s).')

                balance, error = api.get_balance(libelles_coin[1])
                if error is not None:
                    print("L'erreur suivante a été retournée : \n" + error)
                    disponibilite = 0
                else:
                    disponibilite = balance['Available']
                print('Vous avez', disponibilite, libelles_coin[0], 'disponible(s).')

                return


def sell_order(api, pair):
    pair = pair.replace("/", "_")

    libelles_coin = pair.split("_", 1)

    ordre_fini = False

    while ordre_fini is not True:
        balance_vente, error = api.get_balance(libelles_coin[0])
        if error is not None:
            print("L'erreur suivante a été retournée : \n" + error)
            disponibilite_vente = 0
        else:
            disponibilite_vente = balance_vente['Available']

        print('Vous avez', disponibilite_vente, libelles_coin[0], 'disponible(s).')

        if disponibilite_vente == 0:
            print('Vous ne pouvez pas effectuer de sell order')
            return
        else:
            while not correct:
                try:
                    balance_utilisee = float(
                        input("Combien de {} voulez-vous utiliser ? : ".format(libelles_coin[0])))
                    correct = True
                except ValueError:
                    print('Veuillez entrer un nombre !')

            while balance_utilisee > disponibilite_vente:
                print('Vous ne pouvez utiliser plus de {}'.format(disponibilite_vente))
                correct = False
                while not correct:
                    try:
                        balance_utilisee = float(
                            input("Combien de {} voulez-vous utiliser ? : ".format(libelles_coin[0])))
                        correct = True
                    except ValueError:
                        print('Veuillez entrer un nombre !')

            marche_paire, error = api.get_market(pair)
            if error is not None:
                print("L'erreur suivante a été retournée : \n" + error)
                return

            print("L'ordre d'achat le plus cher est de {:.8f} \n".format(marche_paire['BidPrice']))

            correct = False
            while not correct:
                try:
                    ask_price = float(input("Quel est votre prix ? : "))
                    correct = True
                except ValueError:
                    print('Veuillez entrer un nombre !')

            # prise en compte des fees de Cryptopia pour calculé le nombre de coins vendable
            num_coins = (balance_utilisee * (balance_utilisee * 0.00201)) / ask_price
            prix_vente = ask_price * num_coins

            trade, error = api.submit_trade(pair.replace("_", "/"), 'Sell', ask_price, num_coins)
            if error is not None:
                print("L'erreur suivante a été retournée : \n" + error)
                return

            print(trade)

            print("\n[+] Ordre de vente placé pour {:.8f} {} coins à {:.8f} {} \
                   chacun pour un total de {} {}".format(num_coins, libelles_coin[0], ask_price, libelles_coin[1],
                                                         prix_vente, libelles_coin[1]))
            time.sleep(5)

            open_orders, error = api.get_openorders(pair.replace("_", "/"))
            if error is not None:
                print("L'erreur suivante a été retournée : \n" + error)
                return

            if open_orders is not None:
                print("Votre ordre n'est pas passé entierement, il reste {:.8f} coins à vendre".format(
                    open_orders[0]['Remaining']))

                correct = False

                while correct is not True:
                    reponse = input("Voulez-vous modifier votre ordre ? (y/n)")

                    if reponse == "y":
                        correct = True
                        data, error = api.cancel_trade('Sell', open_orders[0]['OrderId'], open_orders[0]['TradePairId'])

                        if error is not None:
                            print("L'erreur suivante a été retournée : \n" + error)
                            return
                    elif reponse == "n":
                        correct = True
                        ordre_fini = True
                        return
            else:
                balance, error = api.get_balance(libelles_coin[1])
                if error is not None:
                    print("L'erreur suivante a été retournée : \n" + error)
                    disponibilite = 0
                else:
                    disponibilite = balance['Available']

                print("Votre ordre est  passé entierement !")
                print('Vous avez', disponibilite, libelles_coin[1], 'disponible(s).')

                balance, error = api.get_balance(libelles_coin[1])
                if error is not None:
                    print("L'erreur suivante a été retournée : \n" + error)
                    disponibilite = 0
                else:
                    disponibilite = balance['Available']
                print('Vous avez', disponibilite, libelles_coin[0], 'disponible(s).')

                return