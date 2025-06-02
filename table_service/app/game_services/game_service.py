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
        if most_common == max_card:
            filtered_dict = {k: v for k, v in count_dict.items() if k != 'A'}
            max_card = max(filtered_dict, key=lambda x: Deck.values.index(x))
        sub_count = sub_order.get(max_card)
        power_combination = main_count + sub_count
        print("Kare " + most_common + "power combination: " + str(power_combination))
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
    print("full house power combination: " + str(power))
    return power

def flush(cards: List[Card]):
    # Подсчитываем количество карт каждой масти
    suits = [card.suit for card in cards]
    suit_counts = Counter(suits)

    # Ищем масть с 5+ картами
    flush_suit = None
    for suit, count in suit_counts.items():
        if count >= 5:
            flush_suit = suit
            break

    if not flush_suit:
        return False  # Флеша нет

    # Выбираем карты только этой масти
    suited_cards = [card for card in cards if card.suit == flush_suit]

    # Сортируем по старшинству
    suited_cards.sort(key=lambda c: Deck.values.index(c.value), reverse=True)

    # Берем топ-5
    top_five = suited_cards[:5]
    top_values = [c.value for c in top_five]

    # Оценка силы флеша по старшей карте
    main_order = {
        '2': 601, '3': 602, '4': 603, '5': 604, '6': 605, '7': 606, '8': 607,
        '9': 608, '10': 609, 'J': 610, 'Q': 611, 'K': 612, 'A': 613
    }
    power = main_order[top_values[0]]
    return power

def straight(cards: List[Card]):
    # Уникальные значения из карт
    values = list({card.value for card in cards})

    # Упорядочим значения по их позиции в Deck.values
    order = Deck.values
    indices = sorted([order.index(v) for v in values])

    # Обработка специального случая: A2345 (т.е. A считается как 1)
    if all(val in values for val in ['A', '2', '3', '4', '5']):
        indices.append(-1)  # Добавим фиктивный индекс ниже 0, чтобы цикл учёл его

    max_run = []
    current_run = []

    prev = None
    for idx in sorted(indices):
        if prev is None or idx == prev + 1:
            current_run.append(idx)
        elif idx != prev:  # Не подряд
            current_run = [idx]
        prev = idx

        if len(current_run) > len(max_run):
            max_run = current_run[:]

    if len(max_run) >= 5:
        high_card_idx = max_run[-1]
        # Обработка случая A2345
        if high_card_idx == -1:
            high_value = '5'
        else:
            high_value = order[high_card_idx]

        main_order = {
            '2': 501, '3': 502, '4': 503, '5': 504, '6': 505, '7': 506, '8': 507,
            '9': 508, '10': 509, 'J': 510, 'Q': 511, 'K': 512, 'A': 513
        }

        power = main_order[high_value]
        print(f"Стрит до {high_value} — сила {power}")
        return power
    else:
        return False

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

def three_of_a_kind(cards: List[Card]):
    values = [card.value for card in cards]
    count = Counter(values)

    # Найдём все значения, которые встречаются ровно 3 раза
    trips = [val for val, cnt in count.items() if cnt == 3]
    if not trips:
        return False

    # Выбираем старшую тройку
    trips.sort(key=lambda x: Deck.values.index(x), reverse=True)
    trip_value = trips[0]

    # Убираем тройку из руки и ищем кикеров
    remaining = [card.value for card in cards if card.value != trip_value]
    kicker_values = sorted(
        set(remaining), key=lambda x: Deck.values.index(x), reverse=True
    )[:2]  # Берём 2 старших кикера

    # Основной порядок (трёшка)
    main_order = {
        '2': 401, '3': 402, '4': 403, '5': 404, '6': 405, '7': 406, '8': 407,
        '9': 408, '10': 409, 'J': 410, 'Q': 411, 'K': 412, 'A': 413
    }
    # Дополнительный порядок (кикеры)
    kicker_order = {
        '2': 0.01, '3': 0.02, '4': 0.03, '5': 0.04, '6': 0.05, '7': 0.06,
        '8': 0.07, '9': 0.08, '10': 0.09, 'J': 0.10, 'Q': 0.11, 'K': 0.12, 'A': 0.13
    }

    # Считаем силу: основа + два кикера
    power = main_order[trip_value]
    if kicker_values:
        power += kicker_order[kicker_values[0]]
    if len(kicker_values) > 1:
        power += kicker_order[kicker_values[1]] / 10  # чуть меньший вклад

    print(f"Сет из {trip_value} с кикерами {kicker_values} — сила {power:.3f}")
    return power

def two_pair(cards: List[Card]):
    # Собираем значения карт
    values = [card.value for card in cards]
    count = Counter(values)

    # Находим все значения, которые встречаются 2+ раза
    pairs = [value for value, cnt in count.items() if cnt >= 2]

    # Нужно минимум 2 разные пары
    if len(pairs) < 2:
        return False

    # Сортируем пары по старшинству, берём две старшие
    sorted_pairs = sorted(pairs, key=lambda x: Deck.values.index(x), reverse=True)
    top_pair, second_pair = sorted_pairs[:2]

    # Определим силу комбинации
    main_order = {
        '2': 301, '3': 302, '4': 303, '5': 304, '6': 305, '7': 306, '8': 307,
        '9': 308, '10': 309, 'J': 310, 'Q': 311, 'K': 312, 'A': 313
    }
    sub_order = {
        '2': 0.01, '3': 0.02, '4': 0.03, '5': 0.04, '6': 0.05, '7': 0.06, '8': 0.07,
        '9': 0.08, '10': 0.09, 'J': 0.10, 'Q': 0.11, 'K': 0.12, 'A': 0.13
    }

    power = main_order[top_pair] + sub_order[second_pair]

    print(f"Две пары: {top_pair} и {second_pair} — сила {power}")
    return power

def one_pair(cards: List[Card]):
    values = [card.value for card in cards]
    count = Counter(values)

    # Ищем все значения, встречающиеся 2 раза (пары)
    pairs = [val for val, cnt in count.items() if cnt == 2]
    if not pairs:
        return False

    # Выбираем старшую пару
    pairs.sort(key=lambda x: Deck.values.index(x), reverse=True)
    pair_value = pairs[0]

    # Удаляем пару и берём 3 старших кикера
    remaining = [card.value for card in cards if card.value != pair_value]
    kicker_values = sorted(
        set(remaining), key=lambda x: Deck.values.index(x), reverse=True
    )[:3]

    # Основной порядок (для пары)
    main_order = {
        '2': 201, '3': 202, '4': 203, '5': 204, '6': 205, '7': 206, '8': 207,
        '9': 208, '10': 209, 'J': 210, 'Q': 211, 'K': 212, 'A': 213
    }

    # Кикерный порядок
    kicker_order = {
        '2': 0.01, '3': 0.02, '4': 0.03, '5': 0.04, '6': 0.05, '7': 0.06,
        '8': 0.07, '9': 0.08, '10': 0.09, 'J': 0.10, 'Q': 0.11, 'K': 0.12, 'A': 0.13
    }

    # Общая сила = пара + 3 кикера с убывающим весом
    power = main_order[pair_value]
    if kicker_values:
        power += kicker_order[kicker_values[0]]
    if len(kicker_values) > 1:
        power += kicker_order[kicker_values[1]] / 10
    if len(kicker_values) > 2:
        power += kicker_order[kicker_values[2]] / 100

    print(f"Пара из {pair_value} с кикерами {kicker_values} — сила {power:.3f}")
    return power

def high_card(cards: List[Card]):
    values = [card.value for card in cards]
    # Убираем дубликаты и сортируем по старшинству
    unique_values = sorted(
        set(values), key=lambda x: Deck.values.index(x), reverse=True
    )[:5]  # Берем 5 старших

    # Порядок значимости карт
    kicker_order = {
        '2': 0.01, '3': 0.02, '4': 0.03, '5': 0.04, '6': 0.05, '7': 0.06,
        '8': 0.07, '9': 0.08, '10': 0.09, 'J': 0.10, 'Q': 0.11, 'K': 0.12, 'A': 0.13
    }

    # Высчитываем силу на основе кикеров
    power = 100  # Базовый вес для high card (меньше пары, сета и т.п.)
    weights = [1, 0.1, 0.01, 0.001, 0.0001]  # Вклад каждой карты
    for i in range(len(unique_values)):
        power += kicker_order[unique_values[i]] * weights[i]

    print(f"High card: {unique_values} — сила {power:.5f}")
    return power

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
    elif flush(total_cards):
        return {'name' : 'Flush', 'power' : flush(total_cards)}
    elif straight(total_cards):
        return {'name' : 'Straight', 'power' : straight(total_cards)}
    elif three_of_a_kind(total_cards):
        return {'name' : 'Three of a kind', 'power' : three_of_a_kind(total_cards)}
    elif two_pair(total_cards):
        return {'name' : 'Two pair', 'power' : two_pair(total_cards)}
    elif one_pair(total_cards):
        return {'name' : 'One pair', 'power' : one_pair(total_cards)}
    else:
        return {'name' : 'Kicker', 'power' : high_card(total_cards)}

