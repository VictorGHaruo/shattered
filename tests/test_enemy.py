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
from src.ground import Ground

class Test_enemy(unittest.TestCase):

    def setUp(self):

        self.player = Yokai(0 ,0, 40, 70)
        self.dummy = Dummy(50, 0, 50, 80, self.player)
        self.mage = Mage(0, 0, 80, 150, self.player)
        self.flying = Flying(100, 0, 60, 60, self.player)

        path_game = os.path.dirname(os.path.abspath(sys.argv[0]))
        path_game = os.path.abspath(path_game)
        ground_path = os.path.join(path_game, os.pardir, "assets", "Ground")
        image_path = os.path.join(ground_path, "Ground_01.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.ground = Ground(0, 500, 500, 100, image_path)

    def test_fall(self):

        self.assertEqual(self.mage.rect.y, 0)
        self.assertEqual(self.flying.rect.y, 0)
        self.assertEqual(self.dummy.rect.y, 0)

        for _ in range(50):
            self.flying.on_collision(self.ground)
            self.mage.on_collision(self.ground)
            self.dummy.on_collision(self.ground)
            self.flying.update()
            self.dummy.update()
            self.mage.update()

        self.assertEqual(self.dummy.rect.y, 460)
        self.assertEqual(self.mage.rect.y, 390)
        self.assertEqual(self.flying.rect.y, 0)

    def test_dummy_movement_right(self):

        self.dummy.to_right = True

        for _ in range(50):

            self.dummy.on_collision(self.ground)
            self.dummy.update()

        self.assertFalse(self.dummy.to_right)

    def test_dummy_movement_left(self):

        self.dummy.to_left = True

        for _ in range(150):

            self.dummy.on_collision(self.ground)
            self.dummy.update()

        self.assertFalse(self.dummy.to_left)

    def test_mage_movement(self):

        self.mage.to_left = True

        self.player.rect.x = 50

        self.mage.on_collision(self.player)
        self.mage.update()
        self.assertFalse(self.mage.to_left)

        self.mage.rect.x = 100
        self.mage.on_collision(self.player)
        self.mage.update()
        self.assertTrue(self.mage.to_left)

    def test_projectile_damage(self):

            projectile1 = Projectile(0, 390, -20, 0, "Player", 20, 1000, 1000, self.image)
            projectile2 = Projectile(150, 390, -20, 0, "Monster", 20, 1000, 1000, self.image)
            self.player.projectiles.append(projectile1)
            self.mage.projectiles.append(projectile2)

            for _ in range(50):
                self.flying.on_collision(self.ground)
                self.mage.on_collision(self.ground)
                self.dummy.on_collision(self.ground)
                self.flying.on_collision(self.player)
                self.mage.on_collision(self.player)
                self.dummy.on_collision(self.player)
                self.player.on_collision(self.dummy)
                self.player.on_collision(self.mage)
                self.player.on_collision(self.flying)
                self.player.update()
                self.flying.update()
                self.dummy.update()
                self.mage.update()

            self.assertEqual(self.mage.life, 40)
            self.assertEqual(self.dummy.life, 5)
            self.assertEqual(self.flying.life, 5)

    def test_dead(self):

        self.dummy.life = -5
        self.mage.life = -5
        self.flying.life = -5

        self.assertFalse(self.mage.is_dead)
        self.assertFalse(self.dummy.is_dead)
        self.assertFalse(self.flying.is_dead)

        for _ in range(100):
            self.flying.update()
            self.mage.update()
            self.dummy.update()

        self.assertTrue(self.mage.is_dead)
        self.assertTrue(self.dummy.is_dead)
        self.assertTrue(self.flying.is_dead)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1000, 1000))  
    unittest.main()