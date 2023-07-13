from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.foodtype import FoodType
from submissionhelper.info.playerpetinfo import PlayerPetInfo
from submissionhelper.info.shoppetinfo import ShopPetInfo
from submissionhelper.info.shopfoodinfo import ShopFoodInfo

import numpy as np

"""
# Improved buy/sell flow:
    # Find best pet and food, including their values
    # Find best sell, and determine if best pet is still best when selling
    # Proceed
"""

# A helper class for storing data of each pet type
class PetData:
    base_priority = 0
    food_priority = 0
    count = 0

    # Front is the pet in front of current pet, 
    # back is the pet behind the current pet.

    # Default is no bonus.
    default_placement_bonus = lambda back, front, pet_data: 0
    default_synergy_bonus = lambda battle_pets: 0

    def __init__(
            self, type : PetType, base_attack : int, base_health : int, placement_priorities: np.ndarray, placement_bonus: callable = None, synergy_bonus: callable = None
        ):
        self.type = type
        self.placement_priorities = placement_priorities
        self.base_attack = base_attack
        self.base_health = base_health

        # placement_bonus is the field that contains the function to calculate the bonus for the placement which can be used to add extra logic to 
        if placement_bonus == None:
            self.placement_bonus = PetData.default_placement_bonus
            print(f"Placement bonus for {type} set to default", flush=True)
        else:
            self.placement_bonus = placement_bonus
            print(f"Placement bonus for {type} set to custom", flush=True)

        if synergy_bonus == None:
            self.synergy_bonus = PetData.default_synergy_bonus
            print(f"Synergy bonus for {type} set to default", flush=True)
        else:
            self.synergy_bonus = synergy_bonus
            print(f"Synergy bonus for {type} set to custom", flush=True)

    # Returns the score of placing the unit a specific index
    @staticmethod
    def get_placement_score(
        pet, index : int, 
        back: PlayerPetInfo, front: PlayerPetInfo, pet_dict: dict[int : "PetData"]
    ) -> float:
        if pet:
            return pet.placement_priorities[index] + pet.placement_bonus(back, front, pet_dict)
        else:
            return 0

    # Sets the base priority    
    def set_priority(self, priority : float):
        self.base_priority = priority

    # Sets the food priority
    def set_food_priority(self, priority):
        self.food_priority = priority

class FoodData:
    base_priority = 0

    def __init__(self, type : FoodType, is_effect : bool, is_directed : bool):
        self.type = type
        self.is_effect = is_effect
        self.is_directed = is_directed

    # Sets the base priority    
    def set_priority(self, priority):
        self.base_priority = priority

def elephant_pb(back: PlayerPetInfo, front: PlayerPetInfo, pet_dict: dict[int : PetData]):
    bonus = 0
    if back == None:
        bonus += 0
    elif back.type == PetType.CAMEL:
        bonus += 30
    elif back.type == PetType.BLOWFISH:
        bonus += 20
    elif back.type == PetType.PEACOCK:
        bonus += 15
    else:
        bonus -= 10
    return bonus

def elephant_sb(battle_pets : list[PlayerPetInfo]):
    synergy = 0
    for pet in battle_pets:
        if not pet:
            continue
        if pet.type == PetType.PEACOCK:
            synergy = max(synergy, 2)
        elif pet.type == PetType.BLOWFISH:
            synergy = max(synergy, 4)
        elif pet.type == PetType.CAMEL:
            synergy = max(synergy, 6)
    return synergy

def camel_pb(back: PlayerPetInfo, front: PlayerPetInfo, pet_dict: dict[int : PetData]):
    bonus = 0
    if back == None:
        bonus -= 20
    else:
        bonus += 0.5 * (back.attack + back.health)
    if front == None:
        bonus += 0
    elif front.type == PetType.ELEPHANT:
        bonus += 30
    return bonus

def camel_sb(battle_pets : list[PlayerPetInfo]):
    for pet in battle_pets:
        if not pet:
            continue
        if pet.type == PetType.ELEPHANT:
            return 6
    return 0

def peacock_pb(back: PlayerPetInfo, front: PlayerPetInfo, pet_dict: dict[int : PetData]):
    bonus = 0
    if front == None:
        bonus += 0
    elif front.type == PetType.ELEPHANT:
        bonus += 20
    return bonus

def peacock_sb(battle_pets : list[PlayerPetInfo]):
    for pet in battle_pets:
        if not pet:
            continue
        if pet.type == PetType.ELEPHANT:
            return 2
    return 0

def blowfish_pb(back: PlayerPetInfo, front: PlayerPetInfo, pet_dict: dict[int : PetData]):
    bonus = 0
    if front == None:
        bonus += 0
    elif front.type == PetType.ELEPHANT:
        bonus += 15
    return bonus

def blowfish_sb(battle_pets : list[PlayerPetInfo]):
    for pet in battle_pets:
        if not pet:
            continue
        if pet.type == PetType.ELEPHANT:
            return 4
    return 0

def kangaroo_pb(back: PlayerPetInfo, front: PlayerPetInfo, pet_dict: dict[int : PetData]):
    bonus = 0
    if front == None:
        bonus -= 10
    else:
        if front.type == PetType.CRICKET or front.type == PetType.SPIDER or front.type == PetType.SHEEP:
            bonus += 10
        bonus += calculate_value(front, pet_dict)
    return bonus

def horse_dog_sb(battle_pets : list[PlayerPetInfo]):
    synergy = 0
    for pet in battle_pets:
        if not pet:
            continue
        if pet.type == PetType.SHEEP:
            synergy += 3
        elif pet.type == PetType.SPIDER:
            synergy += 2
        elif pet.type == PetType.CRICKET:
            synergy += 1
    return synergy

def sheep_spider_cricket_sb(battle_pets : list[PlayerPetInfo]):
    synergy = 0
    for pet in battle_pets:
        if not pet:
            continue
        if pet.type == PetType.HORSE:
            synergy += 1
        elif pet.type == PetType.DOG:
            synergy += 1
    return synergy

def bison_sb(battle_pets : list[PlayerPetInfo]):
    for pet in battle_pets:
        if not pet:
            continue
        if pet.level == 3:
            return 5
    return 0
      
# Each value corresponds to a pet below
base_pet_priorities = np.array([
    1, 0.5, 0, 1, 0.5, 0, -0.5,             # Tier 1 pets
    2, 0, 0, 2, 0, 1.5, 0,                  # Tier 2 pets
    0, 0, 0, 0, 3, 0, 0, 4, 3.5,            # Tier 3 pets
    2, 4, 1, 3, 1, 4.5                      # Tier 4 pets     
])

pet_food_priorities = np.array([
    -5, -5, -5, -10, -5, -5, -5,            # Tier 1 pets
    0, -5, -5, 5, -5, 6, -5,                # Tier 2 pets    
    3, -5, -5, -5, -5, -5, -5, 20, 5,       # Tier 3 pets
    2, 15, 1, 7, -5, -5                     # Tier 4 pets
])

# Setting up lookup for pet id from the pet id (type.value)
pet_dict = {
    1 : PetData(PetType.FISH, 2, 3, np.array([-0.2, -0.1, 0, 0.1, 0.2])),
    2 : PetData(PetType.BEAVER, 3, 2, np.array([0.2, 0.1, 0, -0.1, -0.2])),
    3 : PetData(PetType.PIG, 4, 1, np.array([0.4, 0.2, 0, -0.2, -0.4])),
    4 : PetData(PetType.ANT, 2, 2, np.array([4, 2, 0, -2, -4])),
    5 : PetData(PetType.MOSQUITO, 2, 2, np.array([0, 0, 0, 0, 0])),
    6 : PetData(PetType.CRICKET, 1, 2, np.array([4, 2, 0, -2, -4])),
    7 : PetData(PetType.HORSE, 2, 1, np.array([-10, -5, -3, 8, 10])),

    8 : PetData(PetType.CRAB, 4, 1, np.array([0, 0, 0, 0, 0])),
    9 : PetData(PetType.SWAN, 1, 2, np.array([0.2, 0.1, 0, -0.1, -0.2])),
    10 : PetData(PetType.HEDGEHOG, 3, 2, np.array([-0.4, -0.2, 0, 0.2, 0.4])),
    11 : PetData(PetType.PEACOCK, 2, 5, np.array([-2, -1, 0, 1, 2]), peacock_pb),                 
    12 : PetData(PetType.FLAMINGO, 3, 2, np.array([6, 6, 6, -8, -10])),
    13 : PetData(PetType.KANGAROO, 2, 3, np.array([-10, 1, 4, 4, 1]), kangaroo_pb),               
    14 : PetData(PetType.SPIDER, 3, 3, np.array([4, 2, 0, -2, -4])),

    15 : PetData(PetType.DODO, 4, 2, np.array([-10, 3, 3, 2, 2])),                                
    16 : PetData(PetType.BADGER, 6, 3, np.array([-1, -0.5, -0.5, 0, 2])),
    17 : PetData(PetType.DOLPHIN, 4, 3, np.array([0.4, 0.2, 0, -0.2, -0.4])),
    18 : PetData(PetType.GIRAFFE, 1, 3, np.array([-8, -4, 0, 6, 6])),                            
    19 : PetData(PetType.BUNNY, 1, 2, np.array([0.2, 0.1, 0, -0.1, -0.2])),
    20 : PetData(PetType.DOG, 2, 3, np.array([-10, -8, 1, 7, 10])),
    21 : PetData(PetType.SHEEP, 2, 2, np.array([-10, 4, 4, 2, 0])),
    22 : PetData(PetType.ELEPHANT, 3, 7, np.array([0, -2, -3, -5, 10]), elephant_pb, elephant_sb),            
    23 : PetData(PetType.CAMEL, 2, 4, np.array([1, 3, 3, 3, -10]), camel_pb, camel_sb),                     

    24 : PetData(PetType.SKUNK, 3, 5, np.array([0.2, 0, 0, -0.1, -0.1])),
    25 : PetData(PetType.HIPPO, 4, 5, np.array([0, 0, 0, 0, 0])),
    26 : PetData(PetType.BISON, 5, 3, np.array([0, 0, 0, 0, 0]), None, bison_sb),
    27 : PetData(PetType.BLOWFISH, 3, 6, np.array([0, 0, 0, 0, 0]), blowfish_pb),                              
    28 : PetData(PetType.SQUIRREL, 2, 5, np.array([0.2, 0, 0, -0.1, -0.1])),
    29 : PetData(PetType.PENGUIN, 2, 4, np.array([0.2, 0, 0, -0.1, -0.1])),
}

base_food_priorities = np.array([
    0.75, -25,          # Tier 1 foods
    0, 0.5,             # Tier 2 foods
    1.5, 3,             # Tier 3 foods
    0, 2.5              # Tier 4 foods
])

food_dict = {
    1 : FoodData(FoodType.APPLE, False, True),
    2 : FoodData(FoodType.HONEY, True, True),
    3 : FoodData(FoodType.MEAT_BONE, True, True),
    4 : FoodData(FoodType.CUPCAKE, False, True),
    5 : FoodData(FoodType.SALAD_BOWL, False, False),
    6 : FoodData(FoodType.GARLIC, True, True),
    7 : FoodData(FoodType.CANNED_FOOD, False, False),
    8 : FoodData(FoodType.PEAR, False, True)
}

# Adding base priorities to pets
for pet_id in range(29):
    pet_dict[pet_id + 1].set_priority(base_pet_priorities[pet_id])
    pet_dict[pet_id + 1].set_food_priority(pet_food_priorities[pet_id])

# Adding base priorities to foods
for food_id in range(8):
    food_dict[food_id + 1].set_priority(base_food_priorities[food_id])

# Prints the shop's pets and food
def print_shop(shop_pets : list[ShopPetInfo], shop_foods : list[ShopFoodInfo]):
    print(f"The {len(shop_pets)} pets in the shop are:", flush=True)
    for pet in shop_pets:
        print(f"\t{pet.type}", flush=True)
    print(f"The {len(shop_foods)} food items in the shop are:", flush=True)
    for food in shop_foods:
        print(f"\t{food.type}", flush=True)

# Prints the board's pets
#   Needs to print pet level, sublevel, attack, health and effects        
def print_board(battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]):
    print(f"The board is:", flush=True)
    for pet in battle_pets:
        if pet == None:
            print("\tempty")
        else:
            print(f"\t{pet.type}: {pet.attack}/{pet.health} Level {pet.level}.{pet.sub_level} @ {pet.carried_food} - (Value: {calculate_value(pet, pet_dict)} + {pet_dict[pet.type.value].synergy_bonus(battle_pets)})")

# Returns the main information from game_info
def game_info_summary(game_info : GameInfo) -> tuple[int, int, list[PlayerPetInfo], list[ShopFoodInfo], list[ShopFoodInfo]]:
    return game_info.player_info.health, game_info.player_info.coins, game_info.player_info.pets, game_info.player_info.shop_pets, game_info.player_info.shop_foods

# Calculates the number of pets on the board
def count_battle_pets(battle_pets : list[PlayerPetInfo]) -> int:
    count = 0
    for pet in battle_pets:
        if pet != None:
            count += 1
    return count

# Calculates the number of pets with buffs on the board
def count_buffed_pets(battle_pets : list[PlayerPetInfo]) -> int:
    count = 0
    for pet in battle_pets:
        if pet != None:
            if pet.carried_food != None:
                count += 1
    return count

# Calculate total sublevels of a pet    
def get_total_sublevels(pet : PlayerPetInfo) -> int:
    total = pet.sub_level
    if pet.level == 2:
        total += 2
    elif pet.level == 3:
        total += 5
    return total

# Returns the best item to buy, and whether or not it's a pet
# Returns none as best item if it will not buy
    # Needs to be able to buy food
def find_best_pet(shop_pets : list[ShopPetInfo], battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]) -> tuple[int, float]:
    best_buy_id = None
    highest_priority = np.NINF

    # Finds the value of each pet
    for pet_id in range(1, 30):
        pet_shop_id = 0

        # If a pet is in the shop and has the currently highest value, it becomes the best item to buy
        for pet_shop_id in range(len(shop_pets)):
            shop_pet = shop_pets[pet_shop_id]
            if shop_pet.is_frozen:
                continue
            if pet_dict[pet_id].type == shop_pet.type:
                priority = pet_dict[pet_id].base_priority + pet_dict[pet_id].synergy_bonus(battle_pets)
                for battle_pet in battle_pets:
                    if battle_pet != None:
                        if battle_pet.type == shop_pet.type and battle_pet.level < 3:
                            priority += 10
                if priority > highest_priority:
                    highest_priority = priority
                    best_buy_id = pet_shop_id
                break

    return best_buy_id, highest_priority

def find_best_food(battle_pets : list[PlayerPetInfo], shop_foods : list[ShopFoodInfo], food_dict : dict[int : FoodData]) -> tuple[int, float]:
    
    buffed_pets_num = count_buffed_pets(battle_pets)
    highest_priority = np.NINF
    best_buy_id = None
    
    # Finds the value of each food
    for food_id in range(1, 9):

        # If a food is in the shop and has the currently highest value, it becomes the best item to buy
        for food_shop_id in range(len(shop_foods)):
            if buffed_pets_num == 5 and food_dict[food_id].is_effect:
                continue
            if food_dict[food_id].type == shop_foods[food_shop_id].type:
                priority = food_dict[food_id].base_priority
                if priority > highest_priority:
                    highest_priority = priority
                    best_buy_id = food_shop_id
                break

    return best_buy_id, highest_priority

# Returns the value of a pet to determine what is best to sell
    # Currently grossly simplified, should be unique lambda function for each pet?
def calculate_value(pet : PlayerPetInfo, pet_dict : dict[int : PetData]) -> float:
    pet_data = pet_dict[pet.type.value]
    return pet_data.base_priority + (pet.attack - pet_data.base_attack) / 4 + (pet.health - pet_data.base_health) / 4

# Returns the best player pet to sell, its index on the board, if an upgrade should be done and another index if upgrading from the board
# Returns none as best pet to sell if the board is not full or an evolution can take place
# Returns an index as other_space only if two pets are being evolved on the board
    # Needs to account for two of the same pets existing on the board, leveling into each other
def find_best_pet_move(best_buy_id : int, shop_pets : list[ShopPetInfo], battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]) -> tuple[str, int, int, float]:
    
    for pet_id in range(5):
        # If battle pets are not full there is no need to sell
        pet = battle_pets[pet_id]
        if pet == None:
            return "Buy", pet_id, None, 0
    
    for pet_id in range(5):
        # If the pet can become an upgrade there is no need to sell
        pet = battle_pets[pet_id]
        if pet.type == shop_pets[best_buy_id].type and pet.level < 3:
            return "Shop Level", pet_id, None, 0
        
    for pet_id_a in range(1, 5):
        # If two existing pets can become upgrades of each other there is no need to sell
        pet_a = battle_pets[pet_id_a]
        for pet_id_b in range(pet_id_a):
            pet_b = battle_pets[pet_id_b]

            if pet_a.type == pet_b.type:
                if pet_a.level != 3 and pet_b.level != 3:
                    if get_total_sublevels(pet_a) > get_total_sublevels(pet_b):    
                        return "Board Level and Buy", pet_id_b, pet_id_a, 0
                    elif get_total_sublevels(pet_a) < get_total_sublevels(pet_b):
                        return "Board Level and Buy", pet_id_a, pet_id_b, 0
                    elif not pet_b.carried_food:
                        return "Board Level and Buy", pet_id_b, pet_id_a, 0
                    elif not pet_a.carried_food:
                        return "Board Level and Buy", pet_id_a, pet_id_b, 0
                    elif pet_a.carried_food.value > pet_b.carried_food.value:
                        return "Board Level and Buy", pet_id_b, pet_id_a, 0
                    else:
                        return "Board Level and Buy", pet_id_a, pet_id_b, 0
        
    # Otherwise, find lowest value pet
    worst_pet_id = None
    lowest_value = np.Inf
    for pet_id in range(5):
        pet = battle_pets[pet_id]
        value = calculate_value(pet, pet_dict) + pet_dict[pet.type.value].synergy_bonus(battle_pets) + 0.5 * get_total_sublevels(pet)
        if value < lowest_value:
            lowest_value = value
            worst_pet_id = pet_id

    return "Sell and Buy", worst_pet_id, None, -lowest_value

# Returns the best target for a food item
    # Currently using trivial calculations based on pet value
def find_best_food_move(battle_pets : list[PlayerPetInfo], food : ShopFoodInfo, pet_dict : dict[int : PetData], food_dict : dict[int : FoodData]) -> tuple[PlayerPetInfo, int]:
    food_data = food_dict[food.type.value]
    if not food_data.is_directed:
        return None, 0
    
    buffed_pets = count_buffed_pets(battle_pets)
    
    best_target = None
    best_value = np.NINF
    for pet_id in range(5):
        pet = battle_pets[pet_id]
        if pet != None:
            value = pet_dict[pet.type.value].food_priority
            if food_data.is_effect and pet.carried_food != None:
                if buffed_pets == 5:
                    value = np.NINF
                # Simplified calculation of value
                value -= 10 * food_dict[pet.carried_food.value].base_priority
            if value > best_value:
                best_target = pet
                best_value = value

    delta_food_value = count_battle_pets(battle_pets) - 5
    return best_target, delta_food_value

def buy_pet(bot_battle : BotBattle, best_buy : ShopPetInfo, target_id : int, pet_dict : dict[int : PetData]):
    print(f"Placing {best_buy.type} at position {target_id}", flush=True)
    pet_dict[best_buy.type.value].count += 1
    bot_battle.buy_pet(best_buy, target_id)

def sell_pet(bot_battle : BotBattle, best_sell : PlayerPetInfo, pet_dict : dict[int : PetData]):
    print(f"Selling {best_sell.type}", flush=True)
    pet_dict[best_sell.type.value].count -= 1
    bot_battle.sell_pet(best_sell)

def shop_level(bot_battle : BotBattle, best_buy : ShopPetInfo, target_id : int):
    print(f"Leveling up {best_buy.type} at position {target_id}", flush=True)
    bot_battle.level_pet_from_shop(best_buy, game_info.player_info.pets[target_id])

def board_level(bot_battle : BotBattle, battle_pets : list[PlayerPetInfo], target_id : int, other_id : int, pet_dict : dict[int : PetData]):
    print(f"Leveling up {battle_pets[other_id].type} at position {other_id} from position {target_id}", flush=True)
    bot_battle.level_pet_from_pets(battle_pets[target_id], battle_pets[other_id])
    pet_dict[battle_pets[target_id].type.value].count -= 1

def buy_food(bot_battle : BotBattle, best_food : ShopFoodInfo, target : PlayerPetInfo):
    if target == None:
        print(f"Giving {best_food.type} to all pets")
        bot_battle.buy_food(best_food)
    else:
        print(f"Giving {best_food.type} to {target.type}")
        bot_battle.buy_food(best_food, target)
        
        
# Generates all permutations of a list "positions"
def recursive_placement(positions : list[int], depth : int, placement : list[int]) -> list[int]:
    #print(f"placement: {placement}, depth: {depth}, positions: {positions}, flush=True")
    if depth == 1:
        placement[0] = positions[0]
        yield placement
    else:
        for i in range(depth):
            pet_id = positions.pop(i)
            placement[depth - 1] = pet_id
            yield from recursive_placement(positions, depth - 1, placement)
            positions.insert(i, pet_id)

# Returns the best placement of pets as a list of indices
def calculate_placement(battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]) -> list[int]:
    best_placement = None
    best_score = np.NINF
    positions = [0, 1, 2, 3, 4]
    current_placement = [-1, -1, -1, -1, -1]

    # Generates every placement and calculates its score
    for placement in recursive_placement(positions, 5, current_placement):
        score = 0
        for pet_id in range(5):

            # Get information about the pet behind and in front.

            # Need confirmation on whether my interpretation of the code is 
            # correct.
            front_pet = None
            back_pet = None

            if (pet_id > 0):
                front_pet = battle_pets[placement[pet_id - 1]]

            if (pet_id < 4):
                back_pet = battle_pets[placement[pet_id + 1]]

            if battle_pets[placement[pet_id]] != None:
                score += PetData.get_placement_score(
                    pet_dict[battle_pets[placement[pet_id]].type.value],
                    pet_id,
                    back_pet, front_pet, pet_dict
                )
        
        # Updates when a new best score is found
        if score > best_score:
            #print(f"Best score updated to {score} with placement {placement}")
            best_score = score
            best_placement = placement.copy()

    print(f"Chose {best_placement} as best placement, with score {best_score}", flush=True)

    return best_placement

# Performs a placement of pets with 4 swaps
def perform_placement(bot_battle : BotBattle, placement : list[int]):
    # Pets are permuted to get the desired pets in the desired indices
    for i in range(4):
        if i != placement[i]:
            bot_battle.swap_pets(i, placement[i])

            # The placement is updated whenever a swap occurs
            # The placement list should end up as [0, 1, 2, 3, 4]
            swap_index = placement.index(i)
            placement[i], placement[swap_index] = placement[swap_index], placement[i]

            bot_battle.get_game_info()

def end_turn(bot_battle : BotBattle, battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]):
    placement = calculate_placement(battle_pets, pet_dict)
    perform_placement(bot_battle, placement)
    print("Phase completed", flush=True)

# Makes a move that may comprise of:
    # A buy action
        # A level up action
    # A sell action
    # A reroll
    # Ending the turn
def make_move(bot_battle : BotBattle, game_info : GameInfo, pet_dict : dict[int : PetData], food_dict : dict[int : FoodData]) -> bool:
    health, coins, battle_pets, shop_pets, shop_foods = game_info_summary(game_info)

    print(f"Coins: {coins}", flush=True)
    print(f"Health: {health}", flush=True)
    print_shop(shop_pets, shop_foods)
    print_board(battle_pets, pet_dict)

    """
    Move flow:
        1. Check the highest "priority" item in both shops
            a. If it can be bought, mark it for purchase
            b. If it can not be bought, freeze the highest priority item
            c. If a pet was bought but there was no space, sell lowest value pet
            d. If all non-frozen priorities are below reroll, perform reroll (reroll priority is lowest when coins is a multiple of 3)

        2. When placing a new pet:
            Calculate total value of all 120 assortments
            Pick highest value assortment and swap pairs
    """

    best_pet_id, pet_value = find_best_pet(shop_pets, battle_pets, pet_dict)
    best_food_id, food_value = find_best_food(battle_pets, shop_foods, food_dict)
    if best_pet_id == None and best_food_id == None:
        if coins > 0:
            print("Rerolling", flush=True)
            bot_battle.reroll_shop()
            return False

    delta_pet_value = np.NINF
    delta_food_value = np.NINF
    if best_pet_id != None:
        pet_move, target_id, other_id, delta_pet_value = find_best_pet_move(best_pet_id, shop_pets, battle_pets, pet_dict)
    if best_food_id != None:
        best_food_target, delta_food_value = find_best_food_move(battle_pets, shop_foods[best_food_id], pet_dict, food_dict)

    # Custom reroll priority based on current coin count
    reroll_priority = (coins % 3) / 2

    # Case where nothing should be bought
    if food_value + delta_food_value < reroll_priority and pet_value + delta_pet_value < reroll_priority:
        # Rerolls if coins are available
        if coins > 0:
            print("Rerolling", flush=True)
            bot_battle.reroll_shop()
        # Otherwise ends turn
        else:
            end_turn(bot_battle, battle_pets, pet_dict)
            return True

    # Case where buying the food is the best option
    elif food_value + delta_food_value > pet_value + delta_pet_value:
        # Freezes the food and ends turn if it can't be bought
        if coins < 3:
            print(f"Freezing {shop_foods[best_food_id].type}", flush=True)
            bot_battle.freeze_food(shop_foods[best_food_id])
            game_info = bot_battle.get_game_info()
            end_turn(bot_battle, battle_pets, pet_dict)
            return True
        # Otherwise buys the food
        buy_food(bot_battle, shop_foods[best_food_id], best_food_target)

    # Case where buying the pet is the best option
    else:
        # Freezes the pet and ends turn if it can't be bought
        if coins < 3 and pet_move != "Sell and Buy" or coins < 2 and pet_move == "Sell and Buy":
            print(f"Freezing {shop_pets[best_pet_id].type}", flush=True)
            bot_battle.freeze_pet(shop_pets[best_pet_id])
            return False
        # Otherwise buys the pet and takes any other required actions
        if pet_move == "Buy":
            buy_pet(bot_battle, shop_pets[best_pet_id], target_id, pet_dict)
        elif pet_move == "Shop Level":
            shop_level(bot_battle, shop_pets[best_pet_id], target_id)
        elif pet_move == "Sell and Buy":
            sell_pet(bot_battle, battle_pets[target_id], pet_dict)
            game_info = bot_battle.get_game_info()
            buy_pet(bot_battle, game_info.player_info.shop_pets[best_pet_id], target_id, pet_dict)
        elif pet_move == "Board Level and Buy":
            board_level(bot_battle, battle_pets, target_id, other_id, pet_dict)
            game_info = bot_battle.get_game_info()
            buy_pet(bot_battle, game_info.player_info.shop_pets[best_pet_id], target_id, pet_dict)

    # Turn continues
    return False


bot_battle = BotBattle()

prev_round_num = 0
phase_num = 1

print("--- Starting battle ---", flush=True)

while True:
    print("Getting new game info", flush=True)
    game_info = bot_battle.get_game_info()

    # Check if a new round has started
    if prev_round_num != game_info.round_num:
        prev_round_num = game_info.round_num
        phase_num = 1
    
    print(f"\n\nRound {prev_round_num} Phase {phase_num}\n", flush=True)

    # Unfreeze anything frozen from previous round
    if phase_num == 1:
        for shop_pet_id in range(len(game_info.player_info.shop_pets)):
            shop_pet = game_info.player_info.shop_pets[shop_pet_id]
            if shop_pet:
                if shop_pet.is_frozen:
                    bot_battle.unfreeze_pet(shop_pet)
                    game_info = bot_battle.get_game_info()
        for shop_food in game_info.player_info.shop_foods:
            if shop_food:
                if shop_food.is_frozen:
                    bot_battle.unfreeze_food(shop_food)
                    game_info = bot_battle.get_game_info()

    # Ends turn only if all actions are complete
    if make_move(bot_battle, game_info, pet_dict, food_dict):
        print("Ending turn", flush=True)
        bot_battle.end_turn()

    phase_num += 1