import unittest

from rpg_battle import heroes
from rpg_battle import monsters
from rpg_battle.battle import Battle
from rpg_battle.exceptions import *

class BattleTestCase(unittest.TestCase):
    def test_participants(self):
        participants = [heroes.Warrior(),
                        heroes.Mage(),
                        monsters.Orc(),
                        monsters.GreenDragon()]
        battle = Battle(participants)
        for unit in participants:
            self.assertIn(unit, battle.participants)

    def test_first_attacker(self):
        participants = [heroes.Warrior(),
                        heroes.Mage(),
                        monsters.Orc(),
                        monsters.GreenDragon()]
        battle = Battle(participants)
        self.assertTrue(isinstance(battle.current_attacker(), monsters.GreenDragon))

# initiatve order: GreenDragon, Orc, Mage, Warrior

    def test_one_round_of_combat(self):
        warr = heroes.Warrior()
        mage = heroes.Mage()
        orc = monsters.Orc()
        dragon = monsters.GreenDragon()
        participants = [warr, mage, orc, dragon]
        battle = Battle(participants)

        expected_output = [('GreenDragon hits', 'with poison breath for', 'damage!'),
                           ('Orc hits', 'with blood rage for', 'damage!'),
                           ('Orc takes', 'self-inflicted damage!'),
                           ("Mage's turn!",)]
        output = []
        while not battle.is_hero_turn():
            output.extend(battle.next_turn())
        else:
            output.extend(battle.next_turn())
        for line, expected in zip(output, expected_output):
            for item in expected:
                self.assertIn(item, line)

        expected_output = [('Mage hits Orc with fireball for', 'damage!'),
                           ("Warrior's turn!",)]
        output = battle.execute_command('fireball', orc)
        for line, expected in zip(output, expected_output):
            for item in expected:
                self.assertIn(item, line)

        expected_output = [('Warrior hits Orc with shield slam for', 'damage!'),
                           ('Orc dies!',),
                           ('XP rewarded!',),
                           ('is now level 2!',),
                           ('is now level 2!',),
                           ('GreenDragon hits', 'with tail swipe for','damage!'),
                           ("Mage's turn!")]
        output = battle.execute_command('shield_slam', orc)
        for line, expected in zip(output, expected_output):
            for item in expected:
                self.assertIn(item, line)

    def test_victory(self):
        rogue = heroes.Rogue(level=99)
        skeleton = monsters.Skeleton()
        participants = [rogue, skeleton]

        battle = Battle(participants)

        while not battle.is_hero_turn():
            battle.next_turn()
        else:
            battle.next_turn()

        with self.assertRaises(Victory):
            expected_output = 'Skeleton dies!'
            output = battle.execute_command('backstab', skeleton)
            self.assertIn(expected_output, output)
            battle.next_turn()

    def test_defeat(self):
        mage = heroes.Mage()
        dragon = monsters.RedDragon(level=99)
        participants = [mage, dragon]

        battle = Battle(participants)

        with self.assertRaises(Defeat):
            output = []
            while not battle.is_hero_turn():
                battle.next_turn()
            else:
                battle.next_turn()

    def test_xp_gain(self):
        cleric = heroes.Cleric()
        troll = monsters.Troll()
        troll.hp = 1
        participants = [cleric, troll]

        battle = Battle(participants)

        before_level = cleric.level

        while not battle.is_hero_turn():
            battle.next_turn()
        else:
            battle.next_turn()

        with self.assertRaises(Victory):
            battle.execute_command('smite', troll)
            battle.next_turn()
        after_level = cleric.level
        self.assertNotEqual(before_level, after_level)
