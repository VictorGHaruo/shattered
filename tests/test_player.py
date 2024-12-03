import pygame
import unittest
import sys, os

sys.path.append(os.path.abspath('..'))

from src.player import Player
from src.player import Knight, Yokai, Ninja
from src.enemy import Mage, Flying, Dummy
from src.weapon import Projectile, Shield, Attack
from src.ground import Ground

def create_key_mock(pressed_keys):
    def mocked_get_pressed(): 
        tmp = [0] * 300
        for key in pressed_keys:
            tmp[key] = 1
        return tmp
    return mocked_get_pressed 

class TestPlayerFall(unittest.TestCase):
    def setUp(self): 
        self.player = Player(0, 0, 50, 50)  
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
        image_path = os.path.join(ground_path, "Ground_01.png")
        self.ground = Ground(0, 100, 1000, 20, image_path) 

    def test_player_ground_collision(self):

        self.assertFalse(self.player.on_ground)
     
        for _ in range(10):  
            mock_function = create_key_mock([pygame.K_d])
            pygame.key.get_pressed = mock_function
            self.player.update()  
            self.player.on_collision(self.ground)

        self.assertTrue(self.player.on_ground)

class TestPlayerMovement(unittest.TestCase):
    def setUp(self):
        self.players = [
            Knight(100, 0, 40, 70),
            Yokai(100, 0, 40, 70),
            Ninja(100, 0, 40, 70),
        ]
        self.actual_player = 0 
        self.player = self.players[self.actual_player]
        self.player.on_ground = True  
        self.player.action = None  

    def test_move_left(self):
 
        mock_function = create_key_mock([pygame.K_a])
        pygame.key.get_pressed = mock_function
        self.player.update()

        self.player.on_key_pressed(pygame.key.get_pressed(), None)
        self.assertEqual(self.player.speed_x, -5)  
        self.assertTrue(self.player.to_left) 
        self.assertEqual(self.player.action, "Walk")  

        self.player.on_key_pressed(pygame.key.get_pressed(), None)
        self.assertEqual(self.player.speed_x, -10)  
        self.assertTrue(self.player.to_left) 
        self.assertEqual(self.player.action, "Walk") 

        for _ in range(10):  
            self.player.on_key_pressed(pygame.key.get_pressed(), None)
            pygame.key.get_pressed = mock_function
            self.player.update()  
        self.assertEqual(self.player.rect.x, 0)

    def test_move_right(self):
        
        mock_function = create_key_mock([pygame.K_d])
        pygame.key.get_pressed = mock_function
        self.player.update()

        self.player.on_key_pressed(pygame.key.get_pressed(), None)

        self.assertEqual(self.player.speed_x, 5)  
        self.assertTrue(self.player.to_right) 
        self.assertEqual(self.player.action, "Walk")  

        self.player.on_key_pressed(pygame.key.get_pressed(), None)

        self.assertEqual(self.player.speed_x, 10)  
        self.assertTrue(self.player.to_right) 
        self.assertEqual(self.player.action, "Walk")

        for _ in range(10):  
            self.player.on_key_pressed(pygame.key.get_pressed(), None)
            pygame.key.get_pressed = mock_function
            self.player.update()  
        self.assertEqual(self.player.rect.x, 200)

    def test_stop_moving(self):
      
        mock_function = create_key_mock([])
        pygame.key.get_pressed = mock_function

       
        self.player.on_key_pressed(pygame.key.get_pressed(), None)

        self.assertEqual(self.player.rect.x, 100)
        self.assertEqual(self.player.speed_x, 0) 
        self.assertFalse(self.player.to_right)  
        self.assertFalse(self.player.to_left)  
        self.assertFalse(self.player.is_running)  
        self.assertIsNone(self.player.action) 

    def test_stop_moving_after_right_and_left(self):

        mock_function = create_key_mock([pygame.K_d, pygame.K_a])
        pygame.key.get_pressed = mock_function

        self.player.on_key_pressed(pygame.key.get_pressed(), None)

        self.assertEqual(self.player.rect.x, 100)
        self.assertEqual(self.player.speed_x, 0) 
        self.assertFalse(self.player.is_running)  
        self.assertIsNone(self.player.action) 

    def test_jump(self):
        self.player.jump()
        self.assertEqual(self.player.jump_count, 1)
        self.assertEqual(self.player.speed_y, -30)

    def test_jump_not(self):
        self.player.action = "Hurt"
        self.player.update()
        self.player.jump()
        self.assertEqual(self.player.jump_count,0)

        self.player.action = "Death"
        self.player.update()
        self.player.jump()
        self.assertEqual(self.player.jump_count,0)

        self.player.action = "Immune"
        self.player.update()
        self.player.jump()
        self.assertEqual(self.player.jump_count,0)

    def test_multijump_yokai(self):
        self.player = self.players[1]
        self.player.jump()
        self.player.jump()
        self.assertEqual(self.player.jump_count, 2)
        self.assertEqual(self.player.speed_y, -30)

    def test_multijump_ninja(self):
        self.player = self.players[2]
        self.player.jump()
        self.player.jump()
        self.player.jump()
        self.assertEqual(self.player.jump_count, 3)
        self.assertEqual(self.player.speed_y, -30)

class TestPlayerActions(unittest.TestCase):
    def setUp(self):
        self.players = [
            Knight(100, 0, 40, 70),
            Yokai(100, 0, 40, 70),
            Ninja(100, 0, 40, 70),
        ]

        self.actual_player = 0 
        self.player = self.players[self.actual_player]
        self.player.on_ground = True  
        self.player.action = None

        self.enemy1 = Mage(300, 0, 80, 150, self.player)
        self.enemy1.to_left = True
        self.enemy2 = Dummy(120, 0, 50, 80, self.player)

        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
        image_path = os.path.join(ground_path, "Ground_01.png")
        self.image = pygame.image.load(image_path).convert_alpha()

    def test_protect(self):
        
        mock_function = create_key_mock([pygame.K_v])
        pygame.key.get_pressed = mock_function

        self.player.actions(pygame.key.get_pressed())

        self.assertEqual(self.player.action, "Immune")

    def test_reflect(self):

        mock_function = create_key_mock([pygame.K_v])
        pygame.key.get_pressed = mock_function

        projectile = Projectile(150, 35, - 20, 0, "Monster", 20, 50, 30, self.image)
        self.enemy1.projectiles.append(projectile)
        self.player.action = "Immune"

        for _ in range(10):
            self.player.actions(pygame.key.get_pressed())
            self.player.on_collision(self.enemy1)
            self.enemy1.on_collision(self.player)
            self.player.update()
            self.enemy1.update()
            
        self.assertEqual( projectile.speed_x, 20)

    def test_projectile(self):
        mock_function = create_key_mock([pygame.K_v])
        pygame.key.get_pressed = mock_function

        self.player = self.players[1]

        for _ in range(100):
            self.player.actions(pygame.key.get_pressed())
            self.player.on_collision(self.enemy2)
            self.enemy2.on_collision(self.player)
            self.player.update()
            self.enemy2.update()

        self.assertTrue(self.enemy2.is_dead)

    def test_attack(self):
        mock_function = create_key_mock([pygame.K_v])
        pygame.key.get_pressed = mock_function

        self.player = self.players[2]

        for _ in range(100):
            self.player.actions(pygame.key.get_pressed())
            self.player.on_collision(self.enemy2)
            self.enemy2.on_collision(self.player)
            self.player.update()
            self.enemy2.update()

        self.assertTrue(self.enemy2.is_dead)

class TestDead(unittest.TestCase):

    def setUp(self):
        self.players = [
            Knight(100, 0, 40, 70),
            Yokai(100, 0, 40, 70),
            Ninja(100, 0, 40, 70),
        ]
        self.actual_player = 0 
        self.player = self.players[self.actual_player]
        self.player.life = 50
        self.player.on_ground = True  
        self.player.action = None

        self.enemy = Dummy(120, 0, 50, 80, self.player)

    def test_Death(self):

        for _ in range(100):
            self.player.on_collision(self.enemy)
            self.enemy.on_collision(self.player)
            self.player.update()
            self.enemy.update()

        self.assertEqual(self.player.action, "Death")

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1000, 1000))  
    unittest.main()