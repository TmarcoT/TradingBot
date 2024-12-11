import ccxt
import ephem
from datetime import datetime

# Configuration des clés API
api_key = "API-Key"
api_secret = "API-Secret"

# Connexion à Binance spot
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'options': {'defaultType': 'spot'}  # Utiliser le marché Spot
})
def view_balance():
    """
    Affiche les soldes disponibles pour BTC et USDT.
    """
    try:
        balance = exchange.fetch_balance()
        btc_balance = balance['free']['BTC']
        usdt_balance = balance['free']['USDT']
        print("\n=== Soldes disponibles ===")
        print(f"BTC : {btc_balance:.6f}")
        print(f"USDT : {usdt_balance:.2f}")
        return btc_balance, usdt_balance
    except Exception as e:
        print(f"Erreur lors de la récupération des soldes : {e}")
        return 0, 0


def buy_market(symbol, usdt_amount):
    """
    Passe un ordre d'achat au marché.
    """
    try:
        price = exchange.fetch_ticker(symbol)['last']
        quantity = round(usdt_amount / price, 6)

        print(f"Prix actuel du BTC : {price:.2f} USDT")
        print(f"Achat de {quantity} BTC pour un total de {usdt_amount} USDT")

        order = exchange.create_order(
            symbol=symbol,
            type='market',
            side='buy',
            amount=quantity
        )
        print("\n=== Détails de l'ordre d'achat ===")
        print(f"ID de l'ordre : {order['id']}")
        print(f"Quantité achetée : {order['filled']} BTC")
        print(f"Montant total dépensé : {order['cost']:.2f} USDT")
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'ordre d'achat : {e}")


def sell_market(symbol, btc_amount):
    """
    Passe un ordre de vente au marché.
    """
    try:
        price = exchange.fetch_ticker(symbol)['last']
        print(f"Prix actuel du BTC : {price:.2f} USDT")
        print(f"Vente de {btc_amount} BTC")

        order = exchange.create_order(
            symbol=symbol,
            type='market',
            side='sell',
            amount=btc_amount
        )
        print("\n=== Détails de l'ordre de vente ===")
        print(f"ID de l'ordre : {order['id']}")
        print(f"Quantité totale vendue : {order['filled']} BTC")
        print(f"Montant total reçu : {order['cost']:.2f} USDT")
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'ordre de vente : {e}")


# Menu interactif
while True:
    print("\n=== Menu ===")
    print("1. Consulter mes soldes")
    print("2. Acheter BTC")
    print("3. Vendre BTC")
    print("4. Quitter")

    choice = input("Choisissez une option : ")

    if choice == '1':
        # Consulter les soldes
        view_balance()

    elif choice == '2':
        # Achat
        try:
            btc_balance, usdt_balance = view_balance()
            print("\nVoulez-vous utiliser :")
            print("1. Un montant spécifique en USDT")
            print("2. Tout votre solde USDT disponible")

            buy_choice = input("Choisissez une option : ")
            if buy_choice == '1':
                usdt_amount = float(input("Entrez le montant en USDT pour l'achat : "))
                if usdt_amount > 0:
                    buy_market(symbol="BTC/USDT", usdt_amount=usdt_amount)
                else:
                    print("Le montant doit être supérieur à 0.")
            elif buy_choice == '2':
                if usdt_balance > 0:
                    buy_market(symbol="BTC/USDT", usdt_amount=usdt_balance)
                else:
                    print("Vous n'avez pas assez de USDT.")
            else:
                print("Option invalide.")
        except ValueError:
            print("Veuillez entrer un montant valide.")

    elif choice == '3':
        # Vente
        try:
            btc_balance, usdt_balance = view_balance()
            print("\nVoulez-vous utiliser :")
            print("1. Une quantité spécifique de BTC")
            print("2. Tout votre solde BTC disponible")

            sell_choice = input("Choisissez une option : ")
            if sell_choice == '1':
                btc_amount = float(input("Entrez la quantité de BTC à vendre : "))
                if btc_amount > 0:
                    sell_market(symbol="BTC/USDT", btc_amount=btc_amount)
                else:
                    print("La quantité doit être supérieure à 0.")
            elif sell_choice == '2':
                if btc_balance > 0:
                    sell_market(symbol="BTC/USDT", btc_amount=btc_balance)
                else:
                    print("Vous n'avez pas assez de BTC.")
            else:
                print("Option invalide.")
        except ValueError:
            print("Veuillez entrer une quantité valide.")

    elif choice == '4':
        print("Quitter le programme...")
        break

    else:
        print("Option invalide. Veuillez réessayer.")