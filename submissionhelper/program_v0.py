from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.foodtype import FoodType
from submissionhelper.info.playerpetinfo import PlayerPetInfo
from submissionhelper.info.shoppetinfo import ShopPetInfo
from submissionhelper.info.shopfoodinfo import ShopFoodInfo

import numpy as np

# A helper class for storing data of each pet type
class PetData:
    base_priority = 0
    count = 0

    def __init__(self, type : PetType, placement_priorities: np.ndarray):
        self.type = type
        self.placement_priorities = placement_priorities

    # Returns the score of placing the unit a specific index
    @staticmethod
    def get_placement_score(pet, index : int) -> float:
        if pet:
            return pet.placement_priorities[index]
        else:
            return 0

    # Sets the base priority    
    def set_priority(self, priority):
        self.base_priority = priority

class FoodData:
    base_priority = 0

    def __init__(self, type : FoodType, is_effect : bool, is_directed : bool):
        self.type = type
        self.is_effect = is_effect
        self.is_directed = is_directed

    # Sets the base priority    
    def set_priority(self, priority):
        self.base_priority = priority
        
# Each value corresponds to a pet below
base_pet_priorities = np.array([
    1, 0.5, 0, 1, 0.5, 0, 0,            # Tier 1 pets
    2, 1, 0.5, 2, 1.5, 1, 1.5,          # Tier 2 pets
    1, 2, 2.5, 3, 2, 2, 0.5, 1.5, 3,    # Tier 3 pets
    3.5, 3, 4, 4, 2, 1                  # Tier 4 pets     
])

# Setting up lookup for pet id from the pet id (type.value)
pet_dict = {
    1 : PetData(PetType.FISH, np.array([-0.2, -0.1, 0, 0.1, 0.2])),
    2 : PetData(PetType.BEAVER, np.array([0.2, 0.1, 0, -0.1, -0.2])),
    3 : PetData(PetType.PIG, np.array([0.4, 0.2, 0, -0.2, -0.4])),
    4 : PetData(PetType.ANT, np.array([4, 2, 0, -2, -4])),
    5 : PetData(PetType.MOSQUITO, np.array([0, 0, 0, 0, 0])),
    6 : PetData(PetType.CRICKET, np.array([4, 2, 0, -2, -4])),
    7 : PetData(PetType.HORSE, np.array([-10, -5, -3, 8, 10])),

    8 : PetData(PetType.CRAB, np.array([0, 0, 0, 0, 0])),
    9 : PetData(PetType.FLAMINGO, np.array([6, 6, 6, -8, -10])),
    10 : PetData(PetType.HEDGEHOG, np.array([-0.4, -0.2, 0, 0.2, 0.4])),
    11 : PetData(PetType.KANGAROO, np.array([-10, 1, 4, 4, 1])),                # Override when tank / summoner present
    12 : PetData(PetType.PEACOCK, np.array([-2, -1, 0, 1, 2])),                 # Override when elephant present
    13 : PetData(PetType.SPIDER, np.array([4, 2, 0, -2, -4])),
    14 : PetData(PetType.SWAN, np.array([0.2, 0.1, 0, -0.1, -0.2])),

    15 : PetData(PetType.BADGER, np.array([-1, -0.5, -0.5, 0, 2])),
    16 : PetData(PetType.CAMEL, np.array([1, 3, 3, 3, -10])),                   # Override when elephant present
    17 : PetData(PetType.DODO, np.array([-10, 3, 3, 2, 2])),                    # Override when tank present?
    18 : PetData(PetType.DOG, np.array([-10, -8, 1, 7, 10])),
    19 : PetData(PetType.DOLPHIN, np.array([0.4, 0.2, 0, -0.2, -0.4])),
    20 : PetData(PetType.ELEPHANT, np.array([-4, -3, -2, -1, 10])),             # Override when peacock / camel / blowfish present
    21 : PetData(PetType.GIRAFFE, np.array([-8, -4, 0, 6, 6])),                 # Override based on level?
    22 : PetData(PetType.BUNNY, np.array([0.2, 0.1, 0, -0.1, -0.2])),
    23 : PetData(PetType.SHEEP, np.array([-10, 4, 4, 2, 0])),

    24 : PetData(PetType.BISON, np.array([0, 0, 0, 0, 0])),
    25 : PetData(PetType.BLOWFISH, np.array([0, 0, 0, 0, 0])),                  # Override when elephant present
    26 : PetData(PetType.HIPPO, np.array([-5, 3, 5, 2, -5])),
    27 : PetData(PetType.PENGUIN, np.array([0.2, 0, 0, -0.1, -0.1])),
    28 : PetData(PetType.SKUNK, np.array([0.2, 0, 0, -0.1, -0.1])),
    29 : PetData(PetType.SQUIRREL, np.array([0.2, 0, 0, -0.1, -0.1])),
}

base_food_priorities = np.array([
    0.5, 0.75,          # Tier 1 foods
    1, 0.25,            # Tier 2 foods
    1.5, 2,             # Tier 3 foods
    1.25, 1.75          # Tier 4 foods
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
            print(f"\t{pet.type}: {pet.attack}/{pet.health} Level {pet.level}.{pet.sub_level} @ {pet.carried_food} - (Value: {calculate_value(pet, pet_dict)})")

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
def find_best_buy(battle_pets : list[PlayerPetInfo], shop_pets : list[ShopPetInfo], shop_foods : list[ShopFoodInfo], pet_dict : dict[int : PetData], food_dict : dict[int : FoodData]) -> tuple[int, bool]:
    best_buy_id = None
    highest_priority = np.NINF
    is_pet = True

    
    buffed_pets_num = count_buffed_pets(battle_pets)
    battle_pets_num = count_battle_pets(battle_pets)

    """
    pet_priority_offset = 0
    if battle_pets_num == 5:
        pet_priority_offset = -3
    """

    # Finds the value of each pet
    for pet_id in range(1, 30):
        pet_shop_id = 0

        # If a pet is in the shop and has the currently highest value, it becomes the best item to buy
        for pet_shop_id in range(len(shop_pets)):
            if pet_dict[pet_id].type == shop_pets[pet_shop_id].type:
                priority = pet_dict[pet_id].base_priority
                if priority > highest_priority:
                    highest_priority = priority
                    best_buy_id = pet_shop_id
                break


    # Finds the value of each food
    for food_id in range(1, 9):
        food_shop_id = 0

        # If a food is in the shop and has the currently highest value, it becomes the best item to buy
        for food_shop_id in range(len(shop_foods)):
            if buffed_pets_num == 5 and food_dict[food_id].is_effect:
                continue
            if food_dict[food_id].type == shop_foods[food_shop_id].type:
                priority = food_dict[food_id].base_priority
                priority += 4 * (battle_pets_num - 4)
                if priority > highest_priority:
                    highest_priority = priority
                    best_buy_id = food_shop_id
                    is_pet = False
                break

    return best_buy_id, is_pet

# Returns the value of a pet to determine what is best to sell
    # Currently grossly simplified, should be unique lambda function for each pet?
def calculate_value(pet : PlayerPetInfo, pet_dict : dict[int : PetData]) -> float:
    return pet_dict[pet.type.value].base_priority + pet.health / 4 + pet.attack / 4

# Returns the best player pet to sell, its index on the board, if an upgrade should be done and another index if upgrading from the board
# Returns none as best pet to sell if the board is not full or an evolution can take place
# Returns an index as other_space only if two pets are being evolved on the board
    # Needs to account for two of the same pets existing on the board, leveling into each other
def find_best_sell(best_buy_id : int, is_pet : bool, shop_pets : list[ShopPetInfo], battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]) -> tuple[PlayerPetInfo, int, bool, int]:
    # No need to sell if food is bought
    if not is_pet:
        return None, None, False, None
        
    for pet_id in range(5):
        # If battle pets are not full there is no need to sell
        pet = battle_pets[pet_id]
        if pet == None:
            return None, pet_id, False, None
    
    for pet_id in range(5):
        # If the pet can become an upgrade there is no need to sell
        pet = battle_pets[pet_id]
        if pet.type == shop_pets[best_buy_id].type and pet.level < 3:
            return None, pet_id, True, None
        
    for pet_id_a in range(1, 5):
        # If two existing pets can become upgrades of each other there is no need to sell
        pet_a = battle_pets[pet_id_a]
        for pet_id_b in range(pet_id_a):
            pet_b = battle_pets[pet_id_b]

            if pet_a.type == pet_b.type:
                if pet_a.level != 3 and pet_b.level != 3:
                    if get_total_sublevels(pet_a) > get_total_sublevels(pet_b):    
                        return None, pet_id_b, True, pet_id_a
                    else:
                        return None, pet_id_a, True, pet_id_b   
        
    # Otherwise, find lowest value pet
    worst_pet = None
    worst_pet_id = None
    lowest_value = np.Inf
    for pet_id in range(5):
        pet = battle_pets[pet_id]
        value = calculate_value(pet, pet_dict)
        if value < lowest_value:
            lowest_value = value
            worst_pet = pet
            worst_pet_id = pet_id

    return worst_pet, worst_pet_id, False, None

# Returns the best target for a food item
    # Currently using trivial calculations based on pet value
def choose_best_food_target(battle_pets : list[PlayerPetInfo], food_data : FoodData, pet_dict : dict[int : PetData], food_dict : dict[int : FoodData]) -> PlayerPetInfo:
    best_target = None
    best_value = np.NINF
    for pet_id in range(5):
        pet = battle_pets[pet_id]
        if pet != None:
            value = calculate_value(pet, pet_dict)
            if food_data.is_effect and pet.carried_food != None:
                value -= 5 * food_dict[pet.carried_food.value].base_priority
            if value > best_value:
                best_target = pet
                best_value = value
    return best_target

# Performs the buy and sell operations
    # Needs to incorporate food
def perform_actions(bot_battle : BotBattle, game_info : GameInfo, best_buy_id : int, is_pet : bool, target_space : int, other_space : int, best_sell : ShopPetInfo, is_level_up : bool, pet_dict : dict[int : PetData], food_dict : dict[int : FoodData]):
    # If there is something to sell, it sells it and refreshes game_info
    if best_sell != None:
        print(f"Selling {best_sell.type} at position {target_space}", flush=True)
        pet_dict[best_sell.type.value].count -= 1
        bot_battle.sell_pet(best_sell)
        game_info = bot_battle.get_game_info()
    
    
    battle_pets = game_info.player_info.pets

    # Case where a new pet is bought
    if is_pet:
        best_buy = game_info.player_info.shop_pets[best_buy_id]

        # Case where a level up will occur
        if is_level_up:

            # Case where shop pet is used as a level up
            if other_space == None:
                print(f"Leveling up {best_buy.type} at position {target_space}", flush=True)
                bot_battle.level_pet_from_shop(best_buy, game_info.player_info.pets[target_space])

            # Case where existing pets are combined
            else:
                print(f"Leveling up {battle_pets[other_space]} at position {other_space} from position {target_space}", flush=True)
                bot_battle.level_pet_from_pets(battle_pets[target_space], battle_pets[other_space])
                pet_dict[battle_pets[target_space].type.value].count -= 1
                game_info = bot_battle.get_game_info()
                best_buy = game_info.player_info.shop_pets[best_buy_id]

        # Case where the pet is placed on the board normally (including after level up from board)
        if not is_level_up or other_space != None:
            print(f"Placing {best_buy.type} at position {target_space}", flush=True)
            pet_dict[best_buy.type.value].count += 1
            bot_battle.buy_pet(best_buy, target_space)

    # Case where food is bought
    else:
        best_buy = game_info.player_info.shop_foods[best_buy_id]
        food_data = food_dict[best_buy.type.value]
        if food_data.is_directed:
            target = choose_best_food_target(battle_pets, food_data, pet_dict, food_dict)
            print(f"Giving {food_data.type} to {target.type}")
            bot_battle.buy_food(best_buy, target)
        else:
            print(f"Giving {food_data.type} to all pets")
            bot_battle.buy_food(best_buy)
        
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
            if battle_pets[placement[pet_id]] != None:
                score += PetData.get_placement_score(pet_dict[battle_pets[placement[pet_id]].type.value], pet_id)
        
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
        bot_battle.swap_pets(i, placement[i])

        # The placement is updated whenever a swap occurs
        # The placement list should end up as [0, 1, 2, 3, 4]
        swap_index = placement.index(i)
        placement[i], placement[swap_index] = placement[swap_index], placement[i]

        # Should not get_game_info after the last permutation, since no more actions happen in the loop
        if i != 3:
            bot_battle.get_game_info()

# Makes a move that may comprise of:
    # A buy action
        # A level up action
    # A sell action
    # A reroll
    # Ending the turn
def make_move(bot_battle : BotBattle, game_info : GameInfo, pet_dict : dict[int : PetData], food_dict : dict[int : FoodData]) -> bool:
    health, coins, battle_pets, shop_pets, shop_foods = game_info_summary(game_info)

    print_shop(shop_pets, shop_foods)
    print_board(battle_pets, pet_dict)

    # Turn ends if there is not enough coins
    if coins < 3:
        return True

    """
    Choices of action are:
        buy_pet                                     
        buy_food
        level_pet_from_shop
        level_pet_from_pets
        sell_pet
        reroll_shop
        freeze_pet
        freeze_food
        unfreeze_pet
        unfreeze_food
        swap_pets
        end_turn

    Move flow:
        1. Check the highest "priority" item in both shops
            a. If it can be bought, mark it for purchase
            b. If it can not be bought, freeze the "n" highest priority items
            c. If a pet was bought but there was no space, sell lowest "value" pet
            d. If all non-frozen priorities are below reroll, perform reroll (reroll priority is lowest when coins is a multiple of 3)

        2. When placing a new pet:
            Calculate total value of all 120 assortments
            Pick highest value assortment and swap pairs
                    
        3. If coins is zero and all "n" high priority items are frozen, end turn
    """

    # Need to support freezing
    # Need to add reroll
    # Need to account for money aside from end turn 

    best_buy_id, is_pet = find_best_buy(battle_pets, shop_pets, shop_foods, pet_dict, food_dict)
    if best_buy_id == None:
        if coins > 0:
            print("Rerolling", flush=True)
            bot_battle.reroll_shop()
            return False

    best_sell, free_space, is_level_up, other_space = find_best_sell(best_buy_id, is_pet, shop_pets, battle_pets, pet_dict)
    perform_actions(bot_battle, game_info, best_buy_id, is_pet, free_space, other_space, best_sell, is_level_up, pet_dict, food_dict)

    # Must refresh game_info after buying
    game_info = bot_battle.get_game_info()
    battle_pets = game_info.player_info.pets

    # Finding and performing the ideal placement
    #   No dynamic calculation currently:
    #       Not considering attack / health
    #       Not considering synergy between units
    placement = calculate_placement(battle_pets, pet_dict)
    perform_placement(bot_battle, placement)
    print("Phase completed", flush=True)

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
    print(f"Coins: {game_info.player_info.coins}", flush=True)

    # Ends turn only if all actions are complete
    if make_move(bot_battle, game_info, pet_dict, food_dict):
        print("Ending turn", flush=True)
        bot_battle.end_turn()

    phase_num += 1