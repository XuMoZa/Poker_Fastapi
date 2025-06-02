import uvicorn
from fastapi import FastAPI
from models.playable import Player, Card, Deck, Table
from game_services.game_service import add_hands, define_combinations

player1 = Player('Misha')
player2 = Player('Alex')
player3 = Player('Bob')
player3.hand = [Card(value='A', suit='Clubs'), Card(value='A', suit='Clubs')]
table = Table()
table.deck.shuffle()
table1 =Table()
table1.cards = [Card(value='A',suit='Clubs'),Card(value='K',suit='Clubs'),Card(value='4',suit='Clubs'),Card(value='K',suit='Clubs'),Card(value='K',suit='Clubs')]
add_hands(table, player1, player2)

table.add_cards(table.deck.draw(3))
table.add_cards(table.deck.draw(1))
table.add_cards(table.deck.draw(1))
print(table.cards)
print(player1.hand)
print(player2.hand)
define_combinations(table1, player3)