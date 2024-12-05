import pygame, os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(current_dir, '..')  
sys.path.append(src_path)

from src.ground import Ground, Block, Spike, Invisible, Obelisk
from src.enemy import Mage, Flying, Dummy

def maping(grounds : list, enemies : list, hero: object) -> None:
    """
    Generates the game map by parsing the grid layout and creating the
    corresponding game elements.
    This function iterates through a predefined grid and for each
    character in the grid, it creates a corresponding game element,
    such as a type of ground, enemy, or ground. The elements are
    added to the `grounds` and `enemies` lists for later use in the
    game.

    Parameters
    ----------
    grounds : list
        A list that stores all the ground elements (platforms, blocks,
        spikes, etc.) that are placed on the map.
    enemies : list
        A list that stores all the enemies that are placed on the map.
    hero : object
        The main player character (hero) used to initialize the enemies
        that interact with it (Dummy, Flying, Mage).

    Returns
    -------
    None
        The function doesn't return anything but updates the `grounds`
        and `enemies` lists with new objects based on the grid layout.
    """
    
    grid = [
        "                                                                                                     I                        I    CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "                                                                                                     I                        I    CC                          CC",
        "                       F                                               U           A             A O I                        I    CC                          CC",
        "                                                                     TMMMP         TMMMP         TMMMP                        I   CCC                          CC",
        "                                                                                                                              I   CCC                          CC",
        "                                                         TMMMP                                                                I  CCCC                          CC",
        "                                                                   F                                  F                       I  CCCC                          CC",
        "                                                                                                                              I CCCCC                          CC",
        "                                      U        A                                                                              ICCCCCC                          CC",
        "                              EXXXXXXXXXXXXXXXXXD                                                                             CCCCCCC                          CC",
        "                      U       LGGGGGGGGGGGGGGGGGR                                                                             CCCCCCC                          CC",
        "                    TMMMMP    LGGGGGGGGGGGGGGGGGR                                                                                  CC                          CC",
        "                              LGGGGGGGGGGGGGGGGGR   TMP       U         U               A                                                                      CC",
        "XXXXXXXXXXXXXXXD              LGGGGGGGGGGGGGGGGGR        EXXXXXXXXXXXXXXXXXXD           EXXXD        U        A                     B                          CC",
        "GGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGR   EXXD    LGGGR    EXXXXXXXD    EXD   EXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXX",
        "GGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGRSSSLGGRSSSSLGGGRSSSSLGGGGGGGRSSSSLGRSSSLGGGGGGGGGGGGGGGG  GGGGGGGGGGGGGGGGGGGGGGGGGG",
        "                                                                                                                                     GG                          ",
    ]
    
    path_game = os.path.dirname(os.path.abspath(sys.argv[0]))   
    Ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
    Ground_path = os.path.abspath(Ground_path)
    image_ground_X = os.path.join(Ground_path, "Ground_01.png")
    image_ground_E = os.path.join(Ground_path, "Ground_02.png")
    image_ground_G = os.path.join(Ground_path, "Ground_04.png")
    image_ground_D = os.path.join(Ground_path, "Ground_06.png")
    image_ground_L = os.path.join(Ground_path, "Ground_07.png")
    image_ground_T = os.path.join(Ground_path, "Ground_08.png")        
    image_ground_M = os.path.join(Ground_path, "Ground_09.png")
    image_ground_P = os.path.join(Ground_path, "Ground_10.png")
    image_ground_R = os.path.join(Ground_path, "Ground_11.png")
    image_ground_B = os.path.join(Ground_path, "Brick.png")
    image_spike_S = os.path.join(Ground_path, "Spikes.png")
    image_obelisk_O = os.path.join(Ground_path, "Obelisk.png")
    image_ground_C = os.path.join(Ground_path, "Brick.png")
    
    keys_ground = [
        ["X", image_ground_X], ["E", image_ground_E], ["G", image_ground_G],
        ["D", image_ground_D], ["L", image_ground_L], ["T", image_ground_T],
        ["M", image_ground_M], ["P", image_ground_P], ["R", image_ground_R],
        ["C", image_ground_C]
    ]
    
    
    i_range = len(grid)
    j_range = len(grid[0])
    for i in range(i_range):
        for j in range(j_range):
            
            if grid[i][j] == "O":
                grounds.append(
                    Obelisk(j*50, i*50 - 185, 150, 250, image_obelisk_O)
                )
            if grid[i][j] == "I":
                grounds.append(Invisible(j*50, i*50, 50, 50, image_ground_X))
            if grid[i][j] == "S":
                grounds.append(Spike(j*50, i*50, 50, 50, image_spike_S))
            if grid[i][j] == "B":
                grounds.append(
                    Block(j*50 - 11, i*50 - 50, 61, 102, image_ground_B)
                )                
            
            for key in keys_ground:
                if grid[i][j] == key[0]:
                    grounds.append(Ground(j*50, i*50, 50, 50, key[1]))
            
            #Enemies
            if grid[i][j] == "U":
                enemies.append(Dummy(j*50, i*50, 50, 80, hero))
            if grid[i][j] == "F":
                enemies.append(Flying(j*50, i*50, 60, 60, hero))
            if grid[i][j] == "A":
                enemies.append(Mage(j*50, i*50, 80, 150, hero))