from .exceptions import *

class Monster(object):

    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        self.level = level
        self.strength = 8
        self.constitution = 8
        self.intelligence = 8
        self.speed = 8
        self.hp = 10
        self.maxhp = self.hp + (self.level - 1) * (0.5 * self.constitution)
        self.xp = (self.maxhp % 10) + (self.strength + self.constitution + self.intelligence + self.speed) / 4

    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: (average of stats) + (maxhp % 10)
        """
        return self.xp


    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        self.dummy = target
        target.hp = target.maxhp - self.strength
        return target.hp

    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp = self.hp - damage
        if self.hp <= 0:
          return self.is_dead()

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        self.hp = self.hp + healing
        if self.hp + healing >= self.maxhp:
            self.hp = self.maxhp

    def is_dead(self):
        """
        Returns True if out of hp
        """
        if self.hp <= 0:
          return True
        else:
          return False

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        self.dummy = target
        target.abilities = []



class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    def __init__(self, level = 1):
        Monster.__init__(self, level)
        self.hp = 100
        self.constitution *= 2

    def tail_swipe(self, target):
        """
        damage: strength + speed
        """
        self.dummy = target
        target.hp = target.maxhp - self.strength - self.speed


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    def __init__(self, level = 1):
        Dragon.__init__(self, level)
        self.strength *= 2
        self.intelligence *= 1.5
        self.abilities = ['fire_breach', 'tail_swipe', 'fight']

    def fire_breath(self, target):
        """
        damage: intelligence * 2.5
        """
        self.dummy = target
        target.hp = target.maxhp - self.intelligence * 2.5


class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    def __init__(self, level = 1):
        Dragon.__init__(self, level)
        self.strength *= 1.5
        self.speed *= 1.5
        self.abilities = ['poison_breach', 'tail_swipe', 'fight']

    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        self.dummy = target
        target.hp = target.maxhp - (self.intelligence + self.constitution) * 1.5


class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    def __init__(self, level = 1):
        Monster.__init__(self, level)
        self.constitution *= 0.25

    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        self.dummy = target
        target.hp = target.maxhp - self.intelligence * 1.5
        return target.hp


class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    def __init__(self, level = 1):
        Undead.__init__(self, level)
        self.hp = 30
        self.intelligence *= 2
        self.abilities = ['fight', 'bite', 'life_drain']

    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        self.dummy = target
        target.hp = target.maxhp - self.speed * 0.5


class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    def __init__(self, level = 1):
        Undead.__init__(self, level)
        self.strength *= 1.25
        self.speed *= 0.5
        self.intelligence *= 0.25
        self.abilities = ['bash', 'fight', 'life_drain']


    def bash(self, target):
        """
        damage: strength * 2
        """
        self.dummy = target
        target.hp = target.maxhp - self.strength * 2
        return target.hp


class Humanoid(Monster):
    def slash(self, target):
        """
        damage: strength + speed
        """
        self.dummy = target
        target.hp = target.maxhp - self.strength - self.speed


class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    Troll fight sequence: ['slash', 'fight', 'regenerate']
    """
    def __init__(self, level = 1):
        Humanoid.__init__(self, level)
        self.strength *= 1.75
        self.constitution *= 1.5
        self.hp = 20
        self.abilities = ['slash', 'fight', 'regenerate']

    def regenerate(self, *args):
        """
        heals self for constitution
        """
        self.dummy = args
        args.hp = args.maxhp + self.constitution
        return args.hp



class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    Orc fight sequence: ['blood_rage', 'slash', 'fight']
    """
    def __init__(self, level = 1):
        Humanoid.__init__(self, level)
        self.strength *= 1.75
        self.hp = 16
        self.abilities = ['blood_rage', 'slash', 'fight']

    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        self.dummy = target
        self.hp = self.maxhp - self.constitution * 0.5
        target.hp = target.maxhp - self.strength * 2
        return target.hp


