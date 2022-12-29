import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.229.60' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180  #270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.16 # offset in meters
bin1_color = [0.6,0,0] # Red
bin2_offset = 0.16
bin2_color = [0,0.7,0] # Green
bin3_offset = 0.16
bin3_color = [0,0,0.4] # Blue
bin4_offset = 0.16
bin4_color = [0.1,0.1,0.1] # Gray

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------


##----------------
## ** Last Edit: 2022-02-13
##-------------------

import random, time



## Steven

## Dispensing container
# ======================
def dispense_container():

## Randomize dispensed container
    
    container_id = random.randint(1,6)

    
    
## Saving container properties to variables
    
    material, mass, bin_id = table.dispense_container(container_id, True)

## Container Dispensed
    
    dispensed = True
    
    
## Coverting bin IDs to numbers
## Pick th last digit of BinID --> Convert to integer
    
    bin_num = int(bin_id[-1])

    print("Table >>> Container with ID ",container_id, "has been dispensed  Bin", bin_num)


## Return --> bin number & container mass
    
    return dispensed, bin_num, mass

# =====================================================


## Steven

## Loading container
## =====================================================

def load_container(on_board,target_bin,to_bin,total_mass):

## Initializing coordinates
    
       
    container_pos = [0.644,0,0.273]              # Container Pickup Position (table) 
    arm_home = [0.406,0,0.483]                   # Q-arm Home Positon
    loading_pos =  [0.026-0.009,-0.432+0.2,0.538] # Loading (Hopper)Position




        
    ## Load container when
        # less than three containers are on QBot, and
        # destination bin matches, and
        # total mass doesn't exceed 90g
        
    if (on_board < 3) and (target_bin == to_bin[0]) and (total_mass <= 90):        
        
        ## Ensure q-arm is at home postion
        arm.home() 
        time.sleep(1)
        
        # Approach container on turntable
        arm.move_arm(container_pos[0], container_pos[1], container_pos[2]) 
        time.sleep(1)
        
        ## Close gripper
        arm.control_gripper(45) 
        time.sleep(1)
        
        ## Move to retrieved position
        arm.move_arm(arm_home[0]-0.1,arm_home[1], arm_home[2])
        time.sleep(1)
        
        ## Rotate Q-arm base to face the hopper
        arm.rotate_base(-90) 
        time.sleep(1)
        
        ## End effector pushes forward slightly
        arm.move_arm(loading_pos[0], loading_pos[1]-0.022-0.225, loading_pos[2]-0.05+0.01) 
        time.sleep(2)
        
        ## Open gripper
        arm.control_gripper(-45) 
        time.sleep(1.5)
        
        ## Move to retrieved position
        arm.move_arm(loading_pos[0], loading_pos[1], loading_pos[2]-0.05+0.01)
        time.sleep(0.5)
        
        ## Q-arm returns to home position
        arm.home()


        on_board += 1                ## Increment no. of container on board
        container_on_table = False   ## No longer has container_on table
        send_bot = False             ## Do NOT send QBot yet 


    ## When loading conditions aren't met
        
    else:
        print("Table >>> Current container on table desn't match condition. \n\n")
        print("Current Container: ")
        print("Bin: ", target_bin)
        print("Total mass: ", total_mass)
        print("\n\n\n")
        print("Table >>> Sending out Q-Bot ...")
        
        container_on_table = True   ## Container IS still on table
        send_bot = True             ## Send QBot to dispose container

        
         
    return on_board, container_on_table, send_bot

## ======================================================


    

## Udai & Steven

## Line follow
## ===================================================
def line_follow(speed):
          
## Accept argument of speed in m/s

    ## Initialize line following sensor
    left_IR, right_IR = bot.line_following_sensors()
    
    ## Cannot find line
    if left_IR == 0 and right_IR == 0:
        ## Move at a slower speed, slightly pivot to the left
        bot.set_wheel_speed([speed*0.45, speed*0.9])
        
    ## Forward
    ## When sensed line in both sides
    elif left_IR == 1 and right_IR == 1:
        bot.set_wheel_speed([speed,speed])

    ## Left
    ## When sensed line in the LEFT only
    elif left_IR == 1 and right_IR == 0:
        bot.set_wheel_speed([speed*0.45,speed*0.75])
       
    ## Right
    ## When sensed line in the RIGHT only
    elif left_IR == 0 and right_IR == 1:
        bot.set_wheel_speed([speed*0.75,speed*0.45])
        
## ============================================================  
    
        





## Udai & Steven
        
## Transferring container
## ======================================
def transfer_container(target_bin,speed):

    print("Will Transfer container to Bin ",target_bin)

    ## Speed-related variables
    approach_speed = speed/2.5
    approach_angle = [5,0,5,2.5]

    
    ## Colour-detection variables
    freq = 2          ## in seconds ## Freqency of checking the colour sensor
    sensed_color = 0    ## Count no. of times sensor detects specified bin color
    detect_times = [3,3,3,3]  ## QBot stops after no. of detected time has reached
    


    ## Assigning epxected RGB value based bin number
    bin_color = [bin1_color, bin2_color, bin3_color, bin4_color]
    target_color = bin_color[target_bin-1]
    
    ## Activating colour sensor
    bot.activate_color_sensor()  


    start_time = time.time()  ## Start timer


    


    while True:
        ## QBot - Follow yellow loop at inputed speed
        line_follow(speed)
        
        ## Check how many seconds has pass
        ## When time elasped has reached (roughly) the sensing frequency
        if time.time() >= start_time + freq:
            
            ## Sense colour
            bin_color = bot.read_color_sensor()[0]
            
            
            if (bin_color == target_color):
                
            ## QBot slows down when approaching bin
                speed = approach_speed
            ## Refresh old timestamp
                start_time = time.time()  
                sensed_color += 1
            else:
                ## Refresh old timestamp
                start_time = time.time()  

            ## QBot stops after detecting same colour for some # of times    
            if sensed_color == detect_times[target_bin-1]:
                bot.stop()
                ## QBot - Angle adjustment        
                bot.rotate(approach_angle[target_bin-1])
                break
            else:
                continue
            


    
    print("Q-bot >>> Arrived to Bin")

    ## Deactivating colour sensor
    bot.deactivate_color_sensor()

## ================================================







## Steven
    
## Disposing container
## ====================================
def dispose_container():

## Initial angle that hopper rotates (in degs)
    hopper_angle = 1
    
    ## Activating actuator
    bot.activate_linear_actuator()
    time.sleep(0.1)



    ## Increasing hopper angle (exponentially)
    ## Pupose: Counter-act QLab's physics bug
    
    while hopper_angle <= 60:
        bot.rotate_hopper(hopper_angle)
        time.sleep(0.5)
        hopper_angle += hopper_angle/3



    ## "Rapidly" rotate hopper back to 90 deg
    bot.rotate_hopper(90)
    time.sleep(0.2)

    print("Hopper is emptied")

    ## "Rapidly" rotate hopper back to 0 deg
    bot.rotate_hopper(0)
    time.sleep(2)

    # Deactivating actuators
    bot.deactivate_linear_actuator()
    
## ============================================  


    




## Udai & Steven
    
## Return Home
## =========================================
def return_home(home_pos,speed):

    print("Q-bot returning home")
    
    ## Initialize an OLD timestamp
    start_time = time.time()
    
    ## Freq that system checks QBot postion (in seconds)
    freq = 2
    

    while True:
        line_follow(speed)

        ## When if it is the time to check QBot pos
        if time.time() >= start_time + freq:

            ## QBot x-pos and y-pos
            bot_xpos = bot.position()[0]
            bot_ypos = bot.position()[1]
            
           ## Checks Q-bot's x and y position is within the range of home pos
            x_check = (abs(bot_xpos - home_pos[0])*1000 <= 40) # Q-bot x postion check
            y_check = (abs(bot_ypos - home_pos[1])*1000 <= 30) # Q-bot y position check
            

            ## When both x and y coditions are met
            if x_check and y_check:
                bot.stop()
                break
            else:
                continue

        
            
        
#===========
## DELAY START
#==============

'''
This function has a purpose of intializing the system timer when pi first starts,
and to provide time for Q-Lab system to load
'''
## Steven


def delay_start(waiting_time):
## waiting time before starting the program - in seconds
    
    print("Starting program. It will take", waiting_time, "seconds ...")

## Start the timer
    start_time = time.time()

    while time.time() <= (start_time + waiting_time):
        print("Time is ", time.time())

## Print after waiting time (after exceuting)
    print("Initialization Completed\n\n\n\n\n")

        
##-----------------------------------
## MAIN
##------------------------------------

## Udai and Steven    

def main():
    container_on_table = False  ## Showing if container is on table
    send_bot = False            ## Determine whether to send Q-Bot
    target_bin = 0              ## The bin which the container on table needs to go
    to_bin = []                 ## The bin Q-bot is currently/will be going to
    on_board = 0                ## Number of container(s) on Q-Bot
    total_mass = 0              ## Masses of containers (current and next)


    while True:

        print("Bin Seqence: ",to_bin)

        ## Dispense Container when no container on table
        if (not container_on_table):
            
            container_on_table, target_bin, mass = dispense_container() ## Save container properties
            to_bin.append(target_bin)   ## Add target bin to bin list
            total_mass += mass          ## Increment total mass
            

        ## Load container when currently has container on table and send_bot trigger is False
        elif (container_on_table) and (not send_bot):

            on_board, container_on_table, send_bot = load_container(on_board,target_bin,to_bin,total_mass)
            


        
        ## Else - Send Q-bot and start 'transfer container' cycle
        else:

            print("Q-bot>>> Departs")

            

            ## Sending container to bin
            transfer_container(to_bin[0],speed)
            time.sleep(0.5)


            ## Dumping container
            dispose_container()
            to_bin.clear()  ## Clear to_bin list
            to_bin.append(target_bin) ## Save the target bin for the container currently on table



            ## Reset counters and triggers
            on_board = 0
            total_mass = 0
            send_bot = False

            
            time.sleep(0.5)
            

            ## QBot return home
            return_home(home_pos,speed)
            
            
            print("Q-bot is at HOME")
            print("<><><><>Cycle Completed<><><><>\n\n")

            
            time.sleep(0.5)
            



        
        ### Infinite loop until interrupted ###
   
    
    
        
## =========================================================
## End of all functions
## ==========================================================

## Wait for 2 seconds before starting
delay_start(2)     

speed = 0.15                        ## Normal speed of q-bot
home_pos = bot.position()           ## Record home position of Q-bot upon initialzation
print("Q-bot Home Position >>>", home_pos)
arm.home()                          ## Q-arm at home position



print("<><><><><> Program Starts<><><><><><>\n")

main()

print("<><><><><> Program Ends <><><><><><>")
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
