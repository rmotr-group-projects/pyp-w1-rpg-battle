import unittest

from rpg_battle import heroes
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


class BaseHeroTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = heroes.Hero()
        self.dummy = TargetDummy()

    def test_base_creation(self):

        expected_stats = {'str': 6,
                          'con': 6,
                          'int': 6,
                          'spd': 6,
                          'maxhp': 103,
                          'maxmp': 53}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp_for_next_level(), 10)
        self.assertFalse(self.hero.is_dead())

    def test_fight(self):
        self.hero.fight(self.dummy)
        self.assertEqual(self.dummy.hp,
                         self.dummy.maxhp - self.hero.strength)

    def test_gain_level(self):
        self.hero.gain_xp(self.hero.xp_for_next_level())
        self.assertEqual(self.hero.level, 2)
        expected_stats = {'str': 7,
                          'con': 7,
                          'int': 7,
                          'spd': 7,
                          'maxhp': 106,
                          'maxmp': 56}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)
        self.assertEqual(self.hero.xp_for_next_level(), 20)

    def test_creation_at_certain_level(self):
        hero = heroes.Hero(level=5)
        self.assertEqual(hero.level, 5)

    def test_take_damage(self):
        self.hero.take_damage(5)
        self.assertEqual(self.hero.hp, self.hero.maxhp - 5)

    def test_heal_damage(self):
        self.hero.take_damage(5)
        self.assertNotEqual(self.hero.hp, self.hero.maxhp)
        self.hero.heal_damage(5)
        self.assertEqual(self.hero.hp, self.hero.maxhp)

    def test_heal_damage_overheal(self):
        self.hero.take_damage(5)
        self.hero.heal_damage(10)
        self.assertEqual(self.hero.hp, self.hero.maxhp)

    def test_dead_hero(self):
        self.hero.take_damage(9999)
        self.assertTrue(self.hero.is_dead())


class WarriorTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = heroes.Warrior()
        self.dummy = TargetDummy()

    def test_warrior_creation(self):
        expected_stats = {'str': 7,
                          'con': 8,
                          'int': 4,
                          'spd': 5,
                          'maxhp': 104,
                          'maxmp': 52}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp_for_next_level(), 10)
        self.assertEqual(set(self.hero.abilities), {'fight', 'shield_slam', 'reckless_charge'})

    def test_warrior_levelling(self):
        self.hero = heroes.Warrior(level=4)
        self.assertEqual(self.hero.level, 4)
        expected_stats = {'str': 13,
                          'con': 17,
                          'int': 7,
                          'spd': 8,
                          'maxhp': 124,
                          'maxmp': 60}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)

    def test_shield_slam(self):
        self.hero.shield_slam(self.dummy)
        self.assertEqual(self.hero.mp, self.hero.maxmp - 5)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 10)

    def test_shield_slam_insufficient_mp(self):
        self.hero.mp = 0
        with self.assertRaises(InsufficientMP):
            self.hero.shield_slam(self.dummy)

    def test_reckless_charge(self):
        self.hero.reckless_charge(self.dummy)
        self.assertEqual(self.hero.hp, self.hero.maxhp - 4)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 14)


class MageTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = heroes.Mage()
        self.dummy = TargetDummy()

    def test_mage_creation(self):
        expected_stats = {'str': 4,
                          'con': 4,
                          'int': 9,
                          'spd': 6,
                          'maxhp': 102,
                          'maxmp': 54}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp_for_next_level(), 10)
        self.assertEqual(set(self.hero.abilities), {'fight', 'frostbolt', 'fireball'})

    def test_mage_levelling(self):
        self.hero = heroes.Mage(level=4)
        self.assertEqual(self.hero.level, 4)
        expected_stats = {'str': 7,
                          'con': 7,
                          'int': 21,
                          'spd': 9,
                          'maxhp': 110,
                          'maxmp': 78}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)

    def test_fireball(self):
        self.hero.fireball(self.dummy)
        self.assertEqual(self.hero.mp, self.hero.maxmp - 8)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 10)

    def test_fireball_insufficient_mp(self):
        self.hero.mp = 0
        with self.assertRaises(InsufficientMP):
            self.hero.fireball(self.dummy)

    def test_frostbolt(self):
        self.hero.frostbolt(self.dummy)
        self.assertEqual(self.hero.mp, self.hero.maxmp - 3)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 4)

    def test_frostbot_insufficient_mp(self):
        self.hero.mp = 0
        with self.assertRaises(InsufficientMP):
            self.hero.frostbolt(self.dummy)


class ClericTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = heroes.Cleric()
        self.dummy = TargetDummy()

    def test_cleric_creation(self):
        expected_stats = {'str': 6,
                          'con': 7,
                          'int': 6,
                          'spd': 5,
                          'maxhp': 103,
                          'maxmp': 53}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp_for_next_level(), 10)
        self.assertEqual(set(self.hero.abilities), {'fight', 'heal', 'smite'})

    def test_cleric_levelling(self):
        self.hero = heroes.Cleric(level=4)
        self.assertEqual(self.hero.level, 4)
        expected_stats = {'str': 9,
                          'con': 13,
                          'int': 9,
                          'spd': 8,
                          'maxhp': 118,
                          'maxmp': 64}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)

    def test_heal(self):
        self.hero.take_damage(22)

        self.hero.heal(self.hero)
        self.assertEqual(self.hero.mp, self.hero.maxmp - 4)
        self.assertEqual(self.hero.hp, self.hero.maxhp - 1)

    def test_heal_insufficient_mp(self):
        self.hero.mp = 0
        with self.assertRaises(InsufficientMP):
            self.hero.heal(self.hero)

    def test_smite(self):
        self.hero.smite(self.dummy)
        self.assertEqual(self.hero.mp, self.hero.maxmp - 7)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 10)

    def test_smite_insufficient_mp(self):
        self.hero.mp = 0
        with self.assertRaises(InsufficientMP):
            self.hero.smite(self.dummy)


class RogueTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = heroes.Rogue()
        self.dummy = TargetDummy()

    def test_rogue_creation(self):
        expected_stats = {'str': 7,
                          'con': 4,
                          'int': 5,
                          'spd': 8,
                          'maxhp': 102,
                          'maxmp': 52}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp_for_next_level(), 10)
        self.assertEqual(set(self.hero.abilities), {'fight', 'backstab', 'rapid_strike'})

    def test_rogue_levelling(self):
        self.hero = heroes.Rogue(level=4)
        self.assertEqual(self.hero.level, 4)
        expected_stats = {'str': 13,
                          'con': 7,
                          'int': 8,
                          'spd': 17,
                          'maxhp': 110,
                          'maxmp': 62}
        actual_stats = {'str': self.hero.strength,
                        'con': self.hero.constitution,
                        'int': self.hero.intelligence,
                        'spd': self.hero.speed,
                        'maxhp': self.hero.maxhp,
                        'maxmp': self.hero.maxmp}
        self.assertEqual(actual_stats, expected_stats)
        self.assertEqual(self.hero.hp, self.hero.maxhp)
        self.assertEqual(self.hero.mp, self.hero.maxmp)

    def test_backstab(self):
        self.hero.backstab(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 14)

    def test_backstab_damaged_target(self):
        self.dummy.take_damage(1)
        with self.assertRaises(InvalidTarget):
            self.hero.backstab(self.dummy)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 1)

    def test_rapid_strike(self):
        self.hero.rapid_strike(self.dummy)
        self.assertEqual(self.hero.mp, self.hero.maxmp - 5)
        self.assertEqual(self.dummy.hp, self.dummy.maxhp - 12)

    def test_rapid_strike_insufficient_mp(self):
        self.hero.mp = 0
        with self.assertRaises(InsufficientMP):
            self.hero.rapid_strike(self.dummy)
