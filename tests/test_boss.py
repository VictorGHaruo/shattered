import pygame
import unittest
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(current_dir, '..')  
sys.path.append(src_path)

from src.player import Player
from src.player import Knight, Yokai, Ninja
from src.enemy import Mage, Flying, Dummy
from src.weapon import Projectile, Shield, Attack
from src.boss import Balrog, Ganon, Demagorgon
from src.ground import Ground

#auxiliary function used to simulate that certain keys have been pressed

def create_key_mock(pressed_keys):
    def mocked_get_pressed(): 
        tmp = [0] * 300
        for key in pressed_keys:
            tmp[key] = 1
        return tmp
    return mocked_get_pressed 

class Test_Balrog(unittest.TestCase):

    def setUp(self):

        self.player = Yokai(500 ,500, 40, 70)
        self.Boss = Balrog(500, 100, 140, 180, self.player)
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
        image_path = os.path.join(ground_path, "Ground_01.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.grounds = [
        Ground(0, 1000, 1000, 10, image_path),
        Ground(0, 0, 10, 1000, image_path),
        Ground(1000, 0, 10, 1000, image_path),
        Ground(0, 0, 1000, 10, image_path)
        ]

#This function tests whether bosses have y speed and collide with the ground

    def test_fall(self):

        self.assertEqual(self.Boss.rect.y, 100)

        for _ in range(10):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertEqual(self.Boss.rect.y, 100)

#the function tests the behavior of the boss's movement

    def test_movement(self):

        self.assertEqual(self.Boss.rect.y, 100)
        for _ in range(100):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

            self.assertGreater(self.Boss.rect.x, 0)
            self.assertLess(self.Boss.rect.x, 1000)

#the function tests the behavior of the boss's atks

    def test_attack(self):

        self.Boss.attack()
        self.assertEqual(len(self.Boss.attacks), 0)

        for _ in range(120):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertEqual(len(self.Boss.attacks), 2)
        self.assertGreater(self.Boss.atk_cooldown, 0)

class Test_Ganon(unittest.TestCase):

    def setUp(self):

        self.player = Yokai(500 ,1400, 40, 70)
        self.player.on_ground = True
        self.Boss = Ganon(300, 1200, 150, 220, self.player)
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
        image_path = os.path.join(ground_path, "Ground_01.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.grounds = [
        Ground(0, 1500, 1500, 10, image_path),
        Ground(0, 0, 10, 1500, image_path),
        Ground(1500, 0, 10, 1500, image_path),
        Ground(0, 0, 1500, 10, image_path)
        ]

    def test_fall(self):

        self.assertEqual(self.Boss.rect.y, 1200)

        for _ in range(100):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertEqual(self.Boss.rect.y, 1320)

    def test_movement(self):

        self.assertEqual(self.Boss.rect.x, 300)


        #we simulate that the player is walking

        mock_function = create_key_mock([pygame.K_a])
        pygame.key.get_pressed = mock_function
        self.player.update()

        for _ in range(50):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
                self.player.on_collision(ground)
            self.player.on_key_pressed(pygame.key.get_pressed(), None)
            pygame.key.get_pressed = mock_function
            self.player.update()
            self.Boss.on_collision(self.player)
            self.Boss.move()
            self.Boss.update()

        self.assertEqual(self.Boss.rect.x, 900)

        self.player.rect.x = 850
        self.player.rect.y = 1280

        for _ in range(50):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
                self.player.on_collision(ground)
            self.player.on_key_pressed(pygame.key.get_pressed(), None)
            pygame.key.get_pressed = mock_function
            self.player.update()
            self.Boss.on_collision(self.player)
            self.Boss.move()
            self.Boss.update()

        self.assertEqual(self.Boss.rect.x, 100)

    def test_attack(self):

        self.player.rect.x = 850
        self.player.rect.y = 1280

        for _ in range(100):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.on_collision(self.player)
            self.Boss.update()

        self.assertEqual(len(self.Boss.projectiles), 7)

class Test_Demargogon(unittest.TestCase):

    def setUp(self):

        self.player = Yokai(500 ,1400, 40, 70)
        self.player.on_ground = True
        self.Boss = Demagorgon(1000, 400, 100, 300, self.player)
        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
        image_path = os.path.join(ground_path, "Ground_01.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.grounds = [
        Ground(0, 1500, 1500, 10, image_path),
        Ground(0, 0, 10, 1500, image_path),
        Ground(1500, 0, 10, 1500, image_path),
        Ground(0, 0, 1500, 10, image_path)
        ]

    def test_fall(self):

        self.assertEqual(self.Boss.rect.y, 400)

        for _ in range(100):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertEqual(self.Boss.rect.y, 1240)

    def test_movement(self):

        for _ in range(100):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

            self.assertGreater(self.Boss.rect.x, 0)
            self.assertLess(self.Boss.rect.x, 1500)

    #tests whether the boss follows the player depending on their position

    def test_follow_player(self):

        self.player.rect.x = 700
        self.player.rect.y = 400

        for _ in range(200):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertEqual(self.Boss.rect.x, 700)

        self.player.rect. x = 1000

        for _ in range(150):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()
        self.assertEqual(self.Boss.rect.x, 1000)

    def test_attack(self):

        self.player.rect.x = 700
        self.player.rect.y = 1240

        for _ in range(99):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertEqual(self.Boss.atk_timer, 1)

        for _ in range(50):
            for ground in self.grounds:
                self.Boss.on_collision(ground)
            self.Boss.update()

        self.assertGreater(self.Boss.atk_timer, 100)

class Test_Dead(unittest.TestCase):

#tests whether bosses gain dead stats only after their death animation ends

    def setUp(self):

        self.player = Yokai(500 ,1400, 40, 70)
        self.Demagorgon = Demagorgon(1000, 400, 100, 300, self.player)
        self.Ganon = Ganon(1000, 400, 100, 300, self.player)
        self.Balrog = Balrog(1000, 400, 100, 300, self.player)
    def test_death(self):

            self.Demagorgon.life = -10
            self.Balrog.life = -10
            self.Ganon.life = -10
            self.assertFalse(self.Demagorgon.is_dead)
            self.assertFalse(self.Ganon.is_dead)
            self.assertFalse(self.Balrog.is_dead)
            
            for _ in range(100):
                self.Demagorgon.update()
                self.Balrog.update()
                self.Ganon.update()

            self.assertTrue(self.Demagorgon.is_dead)
            self.assertTrue(self.Ganon.is_dead)
            self.assertTrue(self.Balrog.is_dead)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1000, 1000))  
    unittest.main()