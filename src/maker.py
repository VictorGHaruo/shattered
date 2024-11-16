import pygame, os, sys
from ground import Ground, Block, Spike, Invsible, Obelisk
from enemy import Mage, Flying, Dummy

def maping(grounds : list, enemies : list, hero):
    
    grid = [
        "                                                                                                     I                              CCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "                                                                                                     I                              C                          CC",
        "                       F                                               U           A             A O I                              C                          CC",
        "                                                                      TMMP         TMMMP         TMMMP                              C                          CC",
        "                                                                                                                                    C                          CC",
        "                                                         TMMMP                                                                      C                          CC",
        "                                                                                                                                    C                          CC",
        "                                                                   F                                  F                             C                          CC",
        "                                      U        A                                                                                    C                          CC",
        "                              EXXXXXXXXXXXXXXXXXD                                                                                   C                          CC",
        "                      U       LGGGGGGGGGGGGGGGGGR                                                                                   C                          CC",
        "                    TMMMMP    LGGGGGGGGGGGGGGGGGR                                                                                                              CC",
        "                              LGGGGGGGGGGGGGGGGGR   TMP       U         U               A                                                                      CC",
        "XXXXXXXXXXXXXXXD              LGGGGGGGGGGGGGGGGGR        EXXXXXXXXXXXXXXXXXXD           EXXXD        U        A                     B                          CC",
        "GGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGR   EXXD    LGGGR    EXXXXXXXD    EXD   EXXXXXXXXXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "GGGGGGGGGGGGGGGR              LGGGGGGGGGGGGGGGGGR        LGGGGGGGGGGGGGGGGGGRSSSLGGRSSSSLGGGRSSSSLGGGGGGGRSSSSLGRSSSLGGGGGGGGGGGGGGGG GGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "                                                                                                                                                                 ",
        "                                                                                                                                     G                           ",
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
    image_ground_B = os.path.join(Ground_path, "Box.png")
    image_spike_S = os.path.join(Ground_path, "Spikes.png")
    image_obelisk_O = os.path.join(Ground_path, "Obelisk.png")
    image_ground_C = os.path.join(Ground_path, "Brick.png")
    
    keys_ground = [
        ["X", image_ground_X], ["E", image_ground_E], ["G", image_ground_G], ["D", image_ground_D],
        ["L", image_ground_L], ["T", image_ground_T], ["M", image_ground_M], ["P", image_ground_P],
        ["R", image_ground_R], ["C", image_ground_C]
    ]
    
    
    i_range = len(grid)
    j_range = len(grid[0])
    for i in range(i_range):
        for j in range(j_range):
            if grid[i][j] == "O":
                grounds.append(Obelisk(j*50, i*50 - 185, 150, 250, image_obelisk_O))
            if grid[i][j] == "I":
                grounds.append(Invsible(j*50, i*50, 50, 50, image_ground_X))
            if grid[i][j] == "S":
                grounds.append(Spike(j*50, i*50, 50, 50, image_spike_S))    
            if grid[i][j] == "B":
                grounds.append(Block(j*50, i*50 - 100, 40, 152, image_ground_B))                
            for key in keys_ground:
                if grid[i][j] == key[0]:
                    grounds.append(Ground(j*50, i*50, 50, 50, key[1]))
            if grid[i][j] == "U":
                enemies.append(Dummy(j*50, i*50, 90, 140, hero))
            if grid[i][j] == "F":
                enemies.append(Flying(j*50, i*50, 70, 70, hero))
            if grid[i][j] == "A":
                enemies.append(Mage(j*50, i*50, 100, 150, hero))