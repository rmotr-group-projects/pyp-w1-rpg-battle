from collections import deque

from .exceptions import *

class Monster(object):
    BASE_STATS = {'strength': 8,
             'constitution': 8,
             'intelligence': 8,
             'speed': 12}
    BASE_HP = 10
    XP_MULTIPLIER = 1

    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        pass

    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: ((average of stats) + (maxhp / 10)) * xp multiplier
        """
        pass

    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        pass


    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        pass

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        pass

    def is_dead(self):
        """
        Returns True if out of hp
        """
        pass

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        pass


class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    MULTIPLIERS = {'constitution': 2}
    BASE_HP = 100
    XP_MULTIPLIER = 2

    def tail_swipe(self, target):
        """
        damage: 1.5*(strength + speed)
        """
        pass


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    MULTIPLIERS = Dragon.MULTIPLIERS.copy()
    MULTIPLIERS.update({'strength': 2,
                        'intelligence': 1.5})
    
    def fire_breath(self, target):
        """
        damage: intelligence * 3
        """
        pass


class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    MULTIPLIERS = Dragon.MULTIPLIERS.copy()
    MULTIPLIERS.update({'strength': 1.5,
                        'speed': 1.5})
    
    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        pass



class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    MULTIPLIERS = {'constitution': 0.25}


    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        pass



class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    MULTIPLIERS = Undead.MULTIPLIERS.copy()
    MULTIPLIERS.update({'intelligence': 2})
    BASE_HP = 45

    def bite(self, target):
        """
        damage: speed * 2
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        pass



class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    MULTIPLIERS = Undead.MULTIPLIERS.copy()
    MULTIPLIERS.update({'strength': 1.25,
                        'speed': 0.5,
                        'intelligence': 0.25})
    BASE_HP = 30

    def bash(self, target):
        """
        damage: strength * 2
        """
        pass


class Humanoid(Monster):
    def slash(self, target):
        """
        damage: strength + speed
        """
        pass


class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    command queue: slash, fight, regenerate
    """
    MULTIPLIERS = {'strength': 1.75,
                   'constitution': 1.5}
    BASE_HP = 20

    def regenerate(self, *args):
        """
        heals self for constitution
        """
        pass


class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    command queue: blood_rage, slash, fight
    """
    MULTIPLIERS = {'strength': 1.75}
    BASE_HP = 16
    XP_MULTIPLIER = 0.5

    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        pass

        