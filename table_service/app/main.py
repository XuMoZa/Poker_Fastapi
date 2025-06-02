import uvicorn
from fastapi import FastAPI
from models.playable import Player, Card, Deck, Table
from game_services.game_service import add_hands, define_combinations

player1 = Player('Misha')
player2 = Player('Alex')
table = Table()
table.deck.shuffle()
add_hands(table, player1, player2)

table.add_cards(table.deck.draw(3))
table.add_cards(table.deck.draw(1))
table.add_cards(table.deck.draw(1))
print(table.cards)
print(player1.hand)
print(player2.hand)
data1 = define_combinations(table, player1)
data2 = define_combinations(table, player2)

if data1["power"] > data2["power"]:
    print("player1 win!")
elif data1["power"] < data2["power"]:
    print("player2 win!")
else:
    print("both players win!")
