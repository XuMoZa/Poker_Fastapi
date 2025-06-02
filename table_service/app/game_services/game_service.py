from copy import deepcopy

from models.playable import Table, Player, Card, Deck, Combination
from typing import List
from collections import Counter


def street_power(value:str):
    order = {'2' : 501, '3' : 502, '4' : 503, '5' : 504, '6' : 505, '7' : 506, '8' : 507, '9' : 508, '10' : 509,
             'J' : 510, 'Q' : 511, 'K' : 512, 'A' : 513}
    return order.get(value)

def add_hands(table : Table, *args):
    for player in args:
        player.receive(table.deck.draw(2))



def street_flash(cards : List[Card]):
    suits = []
    for card in cards:
        suits.append(card.suit)
    max_suit, max_suit_value = suit_count(suits)
    potential_street_flash = []
    print(max_suit)
    if max_suit >= 4:
        for card in cards:
            if card.suit == max_suit_value:
                potential_street_flash.append(card)
        max_card = street(potential_street_flash)
        if max_card:
            power_combination = street_power(max_card)+400
            return power_combination
        else:
            return False
    else:
        return False


def kare(cards: List[Card]):
    value = []
    for card in cards:
        value.append(card.value)
    count_dict = Counter(value)
    most_common = max(count_dict, key=count_dict.get)
    if count_dict.get(most_common) == 4:
        main_order = {'2': 801, '3': 802, '4': 803, '5': 804, '6': 805, '7': 806, '8': 807, '9': 808, '10': 809,
                 'J': 810, 'Q': 811, 'K': 812, 'A': 813}
        sub_order = {'2': 0.01, '3': 0.02, '4': 0.03, '5': 0.04, '6': 0.05, '7': 0.06, '8': 0.07, '9': 0.08, '10': 0.09,
                 'J': 0.10, 'Q': 0.11, 'K': 0.12, 'A': 0.13}
        main_count = main_order.get(most_common)
        max_card = max(count_dict, key=lambda x: Deck.values.index(x))
        print(count_dict)
        if most_common == max_card:
            filtered_dict = {k: v for k, v in count_dict.items() if k != 'A'}
            max_card = max(filtered_dict, key=lambda x: Deck.values.index(x))
        sub_count = sub_order.get(max_card)
        power_combination = main_count + sub_count
        print(power_combination)
        return power_combination
    else:
        return False

def full_house(cards: List[Card]):
    value_list = [card.value for card in cards]
    count_dict = Counter(value_list)

    triplets = [val for val, count in count_dict.items() if count >= 3]
    if not triplets:
        return False
    triplets.sort(key=lambda x: Deck.values.index(x), reverse=True)
    set_com = triplets[0]

    remaining_cards = [card for card in cards if card.value != set_com]
    remaining_values = [card.value for card in remaining_cards]
    pair_dict = Counter(remaining_values)

    pairs = [val for val, count in pair_dict.items() if count >= 2]
    if not pairs:
        return False
    pairs.sort(key=lambda x: Deck.values.index(x), reverse=True)
    pair_com = pairs[0]

    main_order = {'2': 701, '3': 702, '4': 703, '5': 704, '6': 705, '7': 706, '8': 707, '9': 708, '10': 709,
                  'J': 710, 'Q': 711, 'K': 712, 'A': 713}
    sub_order = {'2': 0.01, '3': 0.02, '4': 0.03, '5': 0.04, '6': 0.05, '7': 0.06, '8': 0.07, '9': 0.08, '10': 0.09,
                 'J': 0.10, 'Q': 0.11, 'K': 0.12, 'A': 0.13}

    power = main_order[set_com] + sub_order[pair_com]
    return power


def street(cards : List[Card]):
    values = []
    order = Deck.values
    for card in cards:
        values.append(card.value)
    card_set = set(values)
    max_run = []
    alt_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    def find_max_run(order_list):
        best = []
        for i in range(len(order_list)):
            current = []
            for j in range(i, len(order_list)):
                if order_list[j] in card_set:
                    current.append(order_list[j])
                else:
                    break
            if len(current) > len(best):
                best = current
        return best

    run1 = find_max_run(order)
    run2 = find_max_run(alt_order)

    # Выбор между обычным порядком и альтернативным (где A = 1)
    if len(run2) >= 5 and len(run2) > len(run1):
        max_run = run2
    else:
        max_run = run1

    if len(max_run) >= 5:
        print(f"Найден отрезок по порядку: {max_run}")
        return max_run[-1] if max_run != ['A', '2', '3', '4', '5'] else '5'
    else:
        print(f"Максимальный отрезок по порядку: {max_run}")
        return False

def set_ckeck(cards : List[Card]):
    value = []
    for card in cards:
        value.append(card.value)
    count_dict = Counter(value)
    most_common = max(count_dict, key=lambda x: Deck.values.index(x))
    if count_dict.get(most_common) == 3:
        return most_common
    else:
        return False

def pair_check (cards : List[Card]):
    value = []
    for card in cards:
        value.append(card.value)
    count_dict = Counter(value)
    most_common = max(count_dict, key=lambda x: Deck.values.index(x))
    if count_dict.get(most_common) >= 2:
        return most_common
    else:
        return False

def suit_count(suits : List[str]):
    hearts = 0
    diamonds = 0
    clubs = 0
    spades = 0
    counter = 0
    for suit in suits:
        if suit == 'Hearts':
            hearts += 1
        elif suit == 'Diamonds':
            diamonds += 1
        elif suit == 'Clubs':
            clubs += 1
        elif suit == 'Spades':
            spades += 1
    dictionary = {'Heart': hearts, 'Clubs' : clubs, 'Spades' : spades, 'Diamonds' : diamonds}
    max_suit = max(dictionary, key=dictionary.get)
    max_value = dictionary[max_suit]
    return max_value, max_suit

def define_combinations(table : Table, player : Player):

    total_cards = table.cards + player.hand
    print(total_cards)
    if street_flash(total_cards):
        return {'name' : 'Street Flash', 'power' : street_flash(total_cards)}
    elif kare(total_cards):
        return {'name' : 'Kare', 'power' : kare(total_cards)}
    elif full_house(total_cards):
        return {'name' : 'Full House', 'power' : full_house(total_cards)}
    else:
        return ...

