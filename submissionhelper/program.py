from submissionhelper.botbattle import BotBattle
from submissionhelper.info.gameinfo import GameInfo
from submissionhelper.info.pettype import PetType
from submissionhelper.info.playerpetinfo import PlayerPetInfo
from submissionhelper.info.shoppetinfo import ShopPetInfo
from submissionhelper.info.shopfoodinfo import ShopFoodInfo

import numpy as np

class PetData:
    base_priority = 0

    def __init__(self, type : PetType, placement_priorities: np.ndarray):
        self.type = type
        self.placement_priorities = placement_priorities

    @staticmethod
    def get_placement_score(pet, index):
        if pet:
            return pet.placement_priorities[index]
        else:
            return 0
        
    def set_priority(self, priority):
        self.base_priority = priority
        
# SETUP
base_priorities = np.array([
    1, 0.5, 0, 1, 0.5, 0, 0,            # Tier 1 pets
    2, 1, 0.5, 2, 1.5, 1, 1.5,          # Tier 2 pets
    1, 2, 2.5, 3, 2, 2, 0.5, 1.5, 3,    # Tier 3 pets
    3.5, 3, 4, 4, 2, 1                         
])

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

for id in range(29):
    pet_dict[id + 1].set_priority(base_priorities[id])

def count_battle_pets(battle_pets : list[PlayerPetInfo]) -> int:
    count = 0
    for pet in battle_pets:
        if pet != None:
            count += 1
    return count

def find_best_buy(battle_pets : list[PlayerPetInfo], shop_pets : list[ShopPetInfo], shop_foods : list[ShopFoodInfo], pet_dict : dict[int : PetData]) -> tuple[ShopPetInfo, int, bool]:
    best_buy = None
    highest_priority = -np.infty

    for pet_id in range(1, 30):
        # Currently simplified for only purchasing pets
        for shop_id in range(len(shop_pets)):
            if pet_dict[pet_id] == shop_pets[shop_id]:
                priority = pet_dict[pet_id].base_priority
                if priority > highest_priority:
                    highest_priority = priority
                    best_buy = shop_pets[shop_id]
                break

    return best_buy, shop_id, True

def calculate_value(pet : PlayerPetInfo, pet_dict : dict[int : PetData]) -> float:
    # Currently simplified calculation
    return pet_dict[pet.type].base_priority + pet.health / 10 + pet.attack / 10

def find_best_sell(best_buy, is_pet, battle_pets, pet_dict) -> tuple[PlayerPetInfo, int, bool]:
    # No need to sell if food is bought
    if not is_pet:
        return None, None, False
    
        
    for pet_id in range(5):
        # If battle pets are not full there is no need to sell
        pet = battle_pets[pet_id]
        if pet == None:
            return None, pet_id, False
    
    for pet_id in range(5):
        # If the pet can become an upgrade there is no need to sell
        pet = battle_pets[pet_id]
        if pet.type == best_buy.type and pet.level < 3:
            return None, pet_id, True
        
    # Otherwise, find lowest value pet
    worst_pet = None
    worst_pet_id = None
    lowest_value = np.infty
    for pet_id in range(5):
        pet = battle_pets[pet_id]
        value = calculate_value(pet, pet_dict)
        if value < lowest_value:
            lowest_value = value
            worst_pet = pet
            worst_pet_id = pet_id

    return worst_pet, worst_pet_id, False

def perform_actions(bot_battle : BotBattle, battle_pets : list[PlayerPetInfo], best_buy : PlayerPetInfo, is_pet : bool, target_space : int, best_sell : ShopPetInfo, is_level_up : bool):
    if best_sell != None:
        bot_battle.sell_pet(best_sell)

    # Case where a new pet is bought
    if is_pet:
        # Case where a pet is bought for level up
        if is_level_up:
            bot_battle.level_pet_from_shop(best_buy, battle_pets[target_space])

        else:
            bot_battle.buy_pet(best_buy, target_space)

    # Case where food is bought
    else:
        return
        
    

def recursive_placement(positions : list[int], depth : int, placement : list[int]) -> list[int]:
    if depth == 1:
        placement[0] = positions[0]
        yield placement
    else:
        for i in range(depth):
            pet = positions.pop(i)
            placement[depth - 1] = pet
            recursive_placement(positions, depth - 1, placement)
            positions.insert(i, pet)

def calculate_placement(battle_pets : list[PlayerPetInfo], pet_dict : dict[int : PetData]) -> list[int]:
    best_placement = None
    best_score = -np.infty
    positions = [0, 1, 2, 3, 4]
    current_placement = []

    for placement in recursive_placement(positions, 5, current_placement):
        score = sum(PetData.get_placement_score(pet_dict[battle_pets[placement[i]]], i) for i in range(5))
        if score > best_score:
            best_score = score
            best_placement = placement

    return best_placement

def perform_placement(bot_battle : BotBattle, battle_pets : list[PlayerPetInfo], placement : list[int]):
    for i in range(4):
        if placement[i] != i:
            bot_battle.swap_pets(i, placement[i])
            swap_index = placement.index[i]
            placement[i], placement[swap_index] = placement[swap_index], placement[i]



def make_move(bot_battle : BotBattle, game_info : GameInfo, pet_dict : dict[int : PetData]) -> bool:
    health = game_info.player_info.health           # int
    coins = game_info.player_info.coins             # int
    battle_pets = game_info.player_info.pets        # List[PlayerPetInfo]
    shop_pets = game_info.player_info.shop_pets     # List[ShopPetInfo]
    shop_foods = game_info.player_info.shop_foods   # List[ShopFoodInfo]

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
    # Need to implement buying and using food
    # Need to add level up from player pets

    # Buying and selling process. Upgrading can only occur from the shop currently
    best_buy, shop_id, is_pet = find_best_buy(battle_pets, shop_pets, shop_foods)
    best_sell, free_space, is_level_up = find_best_sell(best_buy, is_pet, battle_pets, pet_dict)
    perform_actions(bot_battle, battle_pets, best_buy, is_pet, free_space, best_sell, is_level_up)

    # Insert level up process here (if leveling up from board)

    # Finding and performing the ideal placement
    #   No dynamic calculation currently:
    #       Not considering attack / health
    #       Not considering synergy between units
    placement = calculate_placement(battle_pets, pet_dict)
    perform_placement(bot_battle, battle_pets, placement)

    # End turn if no enough coins to buy a new pet
    return False


bot_battle = BotBattle()

round_number = True
object_ids = []
while True:
    game_info = bot_battle.get_game_info()

    # Check if a new round has started
    if prev_round_num != game_info.round_num:
        prev_round_num = game_info.round_num
        print(f"Round {prev_round_num}\n\n")

    if make_move(bot_battle, game_info, pet_dict):
        bot_battle.end_turn()