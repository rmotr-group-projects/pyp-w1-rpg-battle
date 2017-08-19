import unittest

from rpg_battle import monsters
from rpg_battle.exceptions import *

class TargetDummy(object):
    def __init__(self):
        self.maxhp = 200
        self.hp = self.maxhp

    def take_damage(self, damage):
        self.hp -= damage

    def heal_damage(self, healing):
        self.hp += healing
        if self.hp > self.maxhp:
            self.hp = self.maxhp


class BaseMonsterTestCase(unittest.TestCase):
    def setUp(self):
        self.monster = monsters.Monster()
        self.dummy = TargetDummy()

    def test_create_monster(self):
        expected_stats = {'str': 8,
                          'con': 8,
                          'int': 8,
                          'spd': 12,

                          'maxhp': 10}
        actual_stats = {'str': self.monster.strength,
                        'con': self.monster.constitution,
                        'int': self.monster.intelligence,
                        'spd': self.monster.speed,
                        'maxhp': self.monster.maxhp}
        self.assertEqual(self.monster.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.monster.hp, self.monster.maxhp)
        self.assertFalse(self.monster.is_dead())

    def test_create_levelled_monster(self):
        self.monster = monsters.Monster(level=5)
        expected_stats = {'str': 12,
                          'con': 12,
                          'int': 12,
                          'spd': 16,

                          'maxhp': 34}
        actual_stats = {'str': self.monster.strength,
                        'con': self.monster.constitution,
                        'int': self.monster.intelligence,
                        'spd': self.monster.speed,
                        'maxhp': self.monster.maxhp}
        self.assertEqual(self.monster.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.monster.hp, self.monster.maxhp)

    def test_fight(self):
        self.monster.fight(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 8)

    def test_take_damage(self):
        self.monster.take_damage(5)
        self.assertEqual(self.monster.hp, self.monster.maxhp - 5)

    def test_dead_monster(self):
        self.monster.take_damage(100)
        self.assertTrue(self.monster.is_dead())

    def test_heal_damage(self):
        self.monster.take_damage(5)
        self.assertNotEqual(self.monster.hp, self.monster.maxhp)
        self.monster.heal_damage(5)
        self.assertEqual(self.monster.hp, self.monster.maxhp)

    def test_heal_damage_overheal(self):
        self.monster.take_damage(5)
        self.assertNotEqual(self.monster.hp, self.monster.maxhp)
        self.monster.heal_damage(10)
        self.assertEqual(self.monster.hp, self.monster.maxhp)


class DragonTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy = TargetDummy()

    def test_create_red_dragon(self):
        dragon = monsters.RedDragon()
        expected_stats = {'str': 16,
                          'con': 16,
                          'int': 12,
                          'spd': 12,

                          'maxhp': 100}
        actual_stats = {'str': dragon.strength,
                        'con': dragon.constitution,
                        'int': dragon.intelligence,
                        'spd': dragon.speed,
                        'maxhp': dragon.maxhp}
        self.assertEqual(dragon.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(dragon.hp, dragon.maxhp)

    def test_create_levelled_red_dragon(self):
        dragon = monsters.RedDragon(level=5)
        expected_stats = {'str': 24,
                          'con': 24,
                          'int': 18,
                          'spd': 16,

                          'maxhp': 148}
        actual_stats = {'str': dragon.strength,
                        'con': dragon.constitution,
                        'int': dragon.intelligence,
                        'spd': dragon.speed,
                        'maxhp': dragon.maxhp}
        self.assertEqual(dragon.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(dragon.hp, dragon.maxhp)

    def test_red_dragon_tail_swipe(self):
        dragon = monsters.RedDragon()
        dragon.tail_swipe(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 42)


    def test_red_dragon_breath_weapon(self):
        dragon = monsters.RedDragon()
        dragon.fire_breath(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 36)


    def test_create_green_dragon(self):
        dragon = monsters.GreenDragon()
        expected_stats = {'str': 12,
                          'con': 16,
                          'int': 8,
                          'spd': 18,

                          'maxhp': 100}
        actual_stats = {'str': dragon.strength,
                        'con': dragon.constitution,
                        'int': dragon.intelligence,
                        'spd': dragon.speed,
                        'maxhp': dragon.maxhp}
        self.assertEqual(dragon.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(dragon.hp, dragon.maxhp)

    def test_create_levelled_green_dragon(self):
        dragon = monsters.GreenDragon(level=5)
        expected_stats = {'str': 18,
                          'con': 24,
                          'int': 12,
                          'spd': 24,

                          'maxhp': 148}
        actual_stats = {'str': dragon.strength,
                        'con': dragon.constitution,
                        'int': dragon.intelligence,
                        'spd': dragon.speed,
                        'maxhp': dragon.maxhp}
        self.assertEqual(dragon.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(dragon.hp, dragon.maxhp)

    def test_green_dragon_tail_swipe(self):
        dragon = monsters.GreenDragon()
        dragon.tail_swipe(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 45)


    def test_green_dragon_breath_weapon(self):
        dragon = monsters.GreenDragon()
        dragon.poison_breath(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 36)

    def test_dragon_damage_reduction(self):
        red = monsters.RedDragon()
        green = monsters.GreenDragon()
        red.take_damage(4)
        green.take_damage(4)
        self.assertEqual(red.hp, red.maxhp)
        self.assertEqual(green.hp, green.maxhp)


class UndeadTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy = TargetDummy()

    def test_create_vampire(self):
        vampire = monsters.Vampire()
        expected_stats = {'str': 8,
                          'con': 2,
                          'int': 16,
                          'spd': 12,
                          'maxhp': 45}

        actual_stats = {'str': vampire.strength,
                        'con': vampire.constitution,
                        'int': vampire.intelligence,
                        'spd': vampire.speed,
                        'maxhp': vampire.maxhp}
        self.assertEqual(vampire.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(vampire.hp, vampire.maxhp)

    def test_create_levelled_vampire(self):
        vampire = monsters.Vampire(level=5)
        expected_stats = {'str': 12,
                          'con': 3,
                          'int': 24,
                          'spd': 16,
                          'maxhp': 51}

        actual_stats = {'str': vampire.strength,
                        'con': vampire.constitution,
                        'int': vampire.intelligence,
                        'spd': vampire.speed,
                        'maxhp': vampire.maxhp}
        self.assertEqual(vampire.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(vampire.hp, vampire.maxhp)

    def test_vampire_life_drain(self):
        vampire = monsters.Vampire()
        vampire.take_damage(1)
        self.assertNotEqual(vampire.hp, vampire.maxhp)
        vampire.life_drain(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 24)
        self.assertEqual(vampire.hp, vampire.maxhp)

    def test_vampire_bite(self):
        bite_damage = 24

        vampire = monsters.Vampire()
        vampire.take_damage(1)
        self.assertNotEqual(vampire.hp, vampire.maxhp)
        dummy_maxhp_prebite = self.dummy.maxhp
        vampire.bite(self.dummy)
        self.assertEqual(self.dummy.maxhp, dummy_maxhp_prebite - bite_damage)
        self.assertEqual(self.dummy.hp, dummy_maxhp_prebite - bite_damage)
        self.assertEqual(vampire.hp, vampire.maxhp)

    def test_create_skeleton(self):
        skeleton = monsters.Skeleton()
        expected_stats = {'str': 10,
                          'con': 2,
                          'int': 2,
                          'spd': 6,
                          'maxhp': 30}

        actual_stats = {'str': skeleton.strength,
                        'con': skeleton.constitution,
                        'int': skeleton.intelligence,
                        'spd': skeleton.speed,
                        'maxhp': skeleton.maxhp}
        self.assertEqual(skeleton.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(skeleton.hp, skeleton.maxhp)

    def test_create_levelled_skeleton(self):
        skeleton = monsters.Skeleton(level=5)
        expected_stats = {'str': 15,
                          'con': 3,
                          'int': 3,
                          'spd': 8,
                          'maxhp': 36}

        actual_stats = {'str': skeleton.strength,
                        'con': skeleton.constitution,
                        'int': skeleton.intelligence,
                        'spd': skeleton.speed,
                        'maxhp': skeleton.maxhp}
        self.assertEqual(skeleton.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(skeleton.hp, skeleton.maxhp)

    def test_skeleton_life_drain(self):
        skeleton = monsters.Skeleton()
        skeleton.take_damage(1)
        self.assertNotEqual(skeleton.hp, skeleton.maxhp)
        skeleton.life_drain(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 3)
        self.assertEqual(skeleton.hp, skeleton.maxhp)

    def test_skeleton_bash(self):
        skeleton = monsters.Skeleton()
        skeleton.bash(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 20)

    def test_undead_hurt_by_healind(self):
        vampire = monsters.Vampire()
        skeleton = monsters.Skeleton()
        self.assertEqual(vampire.hp, vampire.maxhp)
        self.assertEqual(skeleton.hp, skeleton.maxhp)
        vampire.heal_damage(5)
        skeleton.heal_damage(5)
        self.assertEqual(vampire.hp, vampire.maxhp - 5)
        self.assertEqual(skeleton.hp, skeleton.maxhp - 5)


class HumanoidTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy = TargetDummy()

    def test_create_troll(self):
        troll = monsters.Troll()
        expected_stats = {'str': 14,
                          'con': 12,
                          'int': 8,
                          'spd': 12,

                          'maxhp': 20}
        actual_stats = {'str': troll.strength,
                        'con': troll.constitution,
                        'int': troll.intelligence,
                        'spd': troll.speed,
                        'maxhp': troll.maxhp}
        self.assertEqual(troll.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(troll.hp, troll.maxhp)

    def test_create_levelled_troll(self):
        troll = monsters.Troll(level=5)
        expected_stats = {'str': 21,
                          'con': 18,
                          'int': 12,
                          'spd': 16,

                          'maxhp': 56}
        actual_stats = {'str': troll.strength,
                        'con': troll.constitution,
                        'int': troll.intelligence,
                        'spd': troll.speed,
                        'maxhp': troll.maxhp}
        self.assertEqual(troll.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(troll.hp, troll.maxhp)

    def test_troll_slash(self):
        troll = monsters.Troll()
        troll.slash(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 26)


    def test_troll_regenerate(self):
        troll = monsters.Troll()
        troll.take_damage(12)
        self.assertNotEqual(troll.hp, troll.maxhp)
        troll.regenerate()
        
    def test_create_orc(self):
        orc = monsters.Orc()
        expected_stats = {'str': 14,
                          'con': 8,
                          'int': 8,
                          'spd': 12,

                          'maxhp': 16}
        actual_stats = {'str': orc.strength,
                        'con': orc.constitution,
                        'int': orc.intelligence,
                        'spd': orc.speed,
                        'maxhp': orc.maxhp}
        self.assertEqual(orc.level, 1)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(orc.hp, orc.maxhp)

    def test_create_levelled_orc(self):
        orc = monsters.Orc(level=5)
        expected_stats = {'str': 21,
                          'con': 12,
                          'int': 12,
                          'spd': 16,

                          'maxhp': 40}
        actual_stats = {'str': orc.strength,
                        'con': orc.constitution,
                        'int': orc.intelligence,
                        'spd': orc.speed,
                        'maxhp': orc.maxhp}
        self.assertEqual(orc.level, 5)
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(orc.hp, orc.maxhp)

    def test_orc_slash(self):
        orc = monsters.Orc()
        orc.slash(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 26)


    def test_orc_blood_rage(self):
        orc = monsters.Orc()
        orc.blood_rage(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 28)
        self.assertEqual(orc.hp, orc.maxhp - 4)
