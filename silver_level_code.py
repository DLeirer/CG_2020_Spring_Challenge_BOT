######################################################
################## load libraries ####################
######################################################
#load libraries
import sys
import math
#import random
import numpy as np

######################################################
################## Global Variables ##################
######################################################
#dictionary to keep track of pacs
pacs_dict = {}


######################################################
################## Define Classes ####################
######################################################


class Pac:

    def __init__(self, pac_id, mine, x,y,type_id,speed_turns_left, ability_cooldown):
        
        #initialising variables
        self.pac_id = pac_id ## between 0 and 4
        self.current_x = x ## x axis loc
        self.current_y = y ## y axis loc
        self.mine = mine ## true or false
        self.type_id = type_id ## Rock, Paper, or Scissor
        self.speed_turns_left = speed_turns_left ## number of turns at double speed left
        self.ability_cooldown = ability_cooldown ## turns until ability usable again. 
        
        #Command variables
        self.command_type = None
        self.move_x = None
        self.move_y = None
        self.type_id_switch = None
        
        
    # choose to MOVE, SWITCH, SPEED
    def pick_action():
        
        ###### 1. Check for danger: ######
        # If danger == True:
        ## If SWITCH possible:
        ### Action = SWITCH and ATTACK
        ## Else find new safe path:
        ### Action = Move
        
        ###### 2. Check current objective: ######
        # If need_new_command == "True":
        ## Find new path
        ### Action == Move
        #Check current objective.
        
        ###### 3. Check if SPEED should be activated: ######
        
        return None

######################################################
################## define functions ##################
######################################################   

def check_enemy_weakness(enemy_class):
    if enemy_class == "ROCK":
        return "PAPER"
    if enemy_class == "SCISSORS":
        return "ROCK"
    if enemy_class == "PAPER":
        return "SCISSORS"


def make_pacs_id(mine,pac_id):
    if mine == True:
        id_string = "m"
    elif mine == False:
        id_string = "e"
    return str(id_string)+str(pac_id)


def pac_create_updater(pacs_dict,pac_id, mine, x,y,type_id,speed_turns_left, ability_cooldown):
    if unique_pacs_id not in pacs_dict:
        #create pac
        pacs_dict[unique_pacs_id] = Pac(pac_id, mine, x,y,type_id,speed_turns_left, ability_cooldown)

    elif unique_pacs_id in pacs_dict:
        #update pac
        pacs_dict[unique_pacs_id].current_x = x
        pacs_dict[unique_pacs_id].current_y = y
        pacs_dict[unique_pacs_id].type_id = type_id
        pacs_dict[unique_pacs_id].speed_turns_left = speed_turns_left
        pacs_dict[unique_pacs_id].ability_cooldown = ability_cooldown

######## path finding functions ########
        
def find_best_path(input_location_x,input_location_y,game_map,speed_counter,blacklisted_locations):
    if speed_counter > 0:
        min_step_size = 2
    else:
        min_step_size = 1
    #copy game map
    c_game_map = game_map.copy()
    current_best_locations = np.array([[input_location_x,input_location_y,0]])
    #mark current location as visited on map
    c_game_map[input_location_x,input_location_y] = "v"
    #print(c_game_map)
    #set winner to false
    winner = False
    n_loops = 0
    while winner == False:
        n_loops += 1
        #print("current loop:", n_loops)
        potential_locations = []
        
        for current_loop_location in current_best_locations:
            
            #get_all_neighbours and values locations that are not walls. 
            neighbours=find_neighbour(current_loop_location[0],current_loop_location[1],c_game_map,blacklisted_locations)
            if len(neighbours) > 0:
                for n_neighbour in neighbours:
                    c_game_map[n_neighbour[0],n_neighbour[1]] = "v"
                    potential_locations.append(n_neighbour)

        #print(c_game_map)
        #print("potential locations pre array",potential_locations)
        potential_locations=np.array(potential_locations)
        #print("potential lcoations array from here",potential_locations)

        
        #find highest value in potential locations
        if len(potential_locations) > 0:
            highest_value = potential_locations[:,2].max()
        else:
            return current_best_locations
        #print("highest_value = ",highest_value)
        
        #subset array to highest value
        current_best_locations = potential_locations[potential_locations[:,2] == highest_value]
        #print("arrays_with_highest_value = ",current_best_locations)
        #check if there is a single best path
        
        if len(current_best_locations) == 1:
            winner = True
            return current_best_locations

        elif n_loops > 10:
            winner = True
            return current_best_locations
    
def get_square_value(current_x,current_y,c_game_map):
    temp_c_square = c_game_map[current_x,current_y]
    #print("the value on current square is",temp_c_square)
    #check if square is 
    #possible values "#"," "."1","10","0"
    if temp_c_square == "1":
        c_value_out = 5
    elif temp_c_square == "10":
        c_value_out = 50
    elif temp_c_square == "0":
        c_value_out = 0
    elif temp_c_square == " ":
        c_value_out = 1
    else:
        c_value_out = -10
    return c_value_out

def find_neighbour(starting_loc_x,starting_loc_y,c_game_map,blacklisted_locations):
    #find all valid_neighbours
    #select highest value as output. 
    #output location to go to. [x,y]
    neighbour_locs = []
    max_x_map_loc = c_game_map.shape[0]-1
    xy_axes = ["x_axis","y_axis"]
    pos_negs = ["positive","negative"]
    for axis in xy_axes:
        for pos_neg in pos_negs:
            current_x = starting_loc_x
            current_y = starting_loc_y
            if pos_neg == "positive":
                if axis == "x_axis":
                    #check if at map edge
                    if current_x == max_x_map_loc:
                        current_x = 0
                    else:
                        current_x +=1
                elif axis == "y_axis":
                    current_y +=1
                    
            elif pos_neg == "negative":
                if axis == "x_axis":
                    if current_x == 0:
                        current_x = max_x_map_loc
                    else:
                        current_x -=1
                elif axis == "y_axis":
                    current_y -=1
            #check if location has been visited before                        
            if c_game_map[current_x,current_y] == "#":
                reached_wall = True
            elif c_game_map[current_x,current_y] == "v":
                reached_wall = True
            elif  [current_x,current_y] in blacklisted_locations:
                reached_wall = True
            else:
                s_value = get_square_value(current_x,current_y,c_game_map)
                current_location = [current_x,current_y,int(s_value)]
                neighbour_locs.append(current_location)
    return neighbour_locs

########  map functions ########

def update_map_visible_pellets(map_full,x,y,value):
    # update map using visible pellets:
    map_full[x,y] = value
    return map_full


def find_visible_squares(starting_x_loc,starting_y_loc, game_map):
    '''
    takes location and map to find all visible squares from that point. 
    visible squares are only visible in straight line from starting position.
    return list of visible squares. 
    '''
    
    max_x_map_loc = game_map.shape[0]-1
    current_visible_locations = []
    xy_axes = ["x_axis","y_axis"]
    pos_negs = ["positive","negative"]
    
    for axis in xy_axes:
        for pos_neg in pos_negs:
            reached_wall = False
            current_x = starting_x_loc
            current_y = starting_y_loc
            while reached_wall == False:
                
                if pos_neg == "positive":
                    if axis == "x_axis":
                        #check if at map edge
                        if current_x == max_x_map_loc:
                            current_x = 0
                        else:
                            current_x +=1
                    elif axis == "y_axis":
                        current_y +=1
                        
                elif pos_neg == "negative":
                    if axis == "x_axis":
                        if current_x == 0:
                            current_x = max_x_map_loc
                        else:
                            current_x -=1
                    elif axis == "y_axis":
                        current_y -=1
                        
                # check if current xy is wall. 
                if game_map[current_x,current_y] == "#":
                    reached_wall = True
                else:
                    current_location = [current_x,current_y]
                    current_visible_locations.append(current_location)

    return current_visible_locations

# update list of squares and their scores
def update_square_score_list(arr_square_scores,l_visible_squares):
    square_score_list=arr_square_scores[:,[0,1]].tolist()
    for l_vsquare in l_visible_squares:
        if l_vsquare not in square_score_list:
            add_val=[l_vsquare[0],l_vsquare[1],0]
            arr_square_scores = np.append(arr_square_scores, [add_val],axis = 0)
            #print("added",add_val )
    return arr_square_scores

def update_map_values(game_map,square_score_list):
    '''
    takes map of game and numpy array of 3 * N dimensions, where each row is [x,y,value]
    updates each x y coordinate with value
    '''
    for square in square_score_list:
        game_map[square[0],square[1]] = square[2]
    
    return game_map



######################################################
################## Get Map          ##################
######################################################  

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]

#make array for map
map_full = np.empty([width, height], dtype='<U31')

for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall
    r_list=list(row)

    for row_coord in range(len(r_list)):
        map_full[row_coord,i] = r_list[row_coord]  



######################################################
################## Start Game Loop  ##################
######################################################  

# game loop
while True:
    ## get variables for game loop
    arr_square_update=[]

    my_score, opponent_score = [int(i) for i in input().split()]
    
    
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    
    ################ MAKE PACCS ######################
    visible_enemies = []
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
        
        


        # add pacs too. 
        if mine == True:
            arr_square_update.append([x,y,-1]) 
        else: 
            enemy_id = make_pacs_id(mine,pac_id)
            visible_enemies.append(enemy_id)
            arr_square_update.append([x,y,-2])

        #get unique pacs id
        unique_pacs_id= make_pacs_id(mine,pac_id)

        # create or update pacs
        pac_create_updater(pacs_dict,pac_id, mine, x,y,type_id,speed_turns_left, ability_cooldown)



    ################ Get Pellets ######################
    visible_pellet_count = int(input())  # all pellets in sight
    
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        #append location of pellets
        arr_square_update.append([x, y, value])
    arr_square_update=np.array(arr_square_update)


    ################ UPDATE MAP ######################
    #for all my pacs
    for pac in pacs_dict:
        print(["Pac",pac], file=sys.stderr)
        if pacs_dict[pac].mine == True:
            ## find visible squares for current pac
            visible_squares = find_visible_squares(pacs_dict[pac].current_x,pacs_dict[pac].current_y, map_full)

            ## update array of squares that need updating. Only do this if there are vissible pellets
            if visible_pellet_count > 0:
                arr_square_update = update_square_score_list(arr_square_update,visible_squares)
        
        ## update map with new values. 
        map_full = update_map_values(map_full,arr_square_update)

    print(["Map updated",map_full], file=sys.stderr)
    ################ FIND ACTIONS ######################
    pac_destinations = []
    for pac in pacs_dict:
        if pacs_dict[pac].mine == True:
            command_found = False
            #check if enemy in view
            if len(visible_enemies) > 0:
                #check closest enemy
                for enemy in visible_enemies: 
                    x_dist = pacs_dict[pac].current_x - pacs_dict[enemy].current_x
                    y_dist = pacs_dict[pac].current_y - pacs_dict[enemy].current_y
                    ## if enemy within 2 dist on either axis.
                    if (x_dist == 0 and abs(y_dist) < 2) or (y_dist == 0 and abs(x_dist) < 2):
                        #check if we can eat them
                        enemy_weakness=check_enemy_weakness(pacs_dict[enemy].type_id)
                        if pacs_dict[pac].type_id == enemy_weakness:
                            pacs_dict[pac].x_move = int(pacs_dict[enemy].current_x)
                            pacs_dict[pac].y_move = int(pacs_dict[enemy].current_y)
                            pacs_dict[pac].command_type = "MOVE"
                            command_found = True
                        elif pacs_dict[pac].ability_cooldown == 0:
                            pacs_dict[pac].command_type = "SWITCH"
                            pacs_dict[pac].type_id_switch = enemy_weakness
                            command_found = True

            if command_found == False:
                best_path = find_best_path(pacs_dict[pac].current_x,pacs_dict[pac].current_y,map_full,pacs_dict[pac].speed_turns_left,pac_destinations)
                pacs_dict[pac].x_move = int(best_path[0][0])
                pacs_dict[pac].y_move = int(best_path[0][1])
                pacs_dict[pac].command_type = "MOVE" 
                pac_destinations.append([pacs_dict[pac].x_move,pacs_dict[pac].y_move])
                command_found = True
    print(["Debug messages...pac_destinations",pac_destinations], file=sys.stderr)
    ################ GIVE COMMANDS ######################
    command_list = []
    ## give commands
    for pac in pacs_dict:
        if pacs_dict[pac].mine == True:
            if pacs_dict[pac].command_type == "SWITCH":
                output = "SWITCH"+ " " + str(pacs_dict[pac].pac_id) + " " + str(pacs_dict[pac].type_id_switch)
                command_list.append(output)
            if pacs_dict[pac].command_type == "MOVE":
                x_dist = pacs_dict[pac].x_move - pacs_dict[pac].current_x
                y_dist = pacs_dict[pac].y_move - pacs_dict[pac].current_y
                if (abs(x_dist)+abs(y_dist) > 4)  and (pacs_dict[pac].ability_cooldown == 0):
                    pacs_dict[pac].command_type = "SPEED"
                    output = "SPEED"+ " " + str(pacs_dict[pac].pac_id)
                    command_list.append(output)
                else:
                    output = "MOVE"+ " " + str(pacs_dict[pac].pac_id) + " " +str(pacs_dict[pac].x_move)+ " " + str(pacs_dict[pac].y_move)
                    command_list.append(output)
#            if pacs_dict[pac].command_type == "SPEED":
#                output = "SPEED"+ " " + str(pacs_dict[pac].pac_id)
#                command_list.append(output)

    #Final Output
    print('|'.join(command_list))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # MOVE <pacId> <x> <y>
   