from .exceptions import *

class Hero(object):

    def __init__(self, level=1):
        """
        Sets stats up and levels up hero if necessary.
        """
        self.level = level
        self.strength = 6
        self.constitution = 6
        self.intelligence = 6
        self.speed = 6
        self.maxhp = 103
        self.maxmp = 53
        self.hp = 103
        self.mp = 53
        self.xp = 0
        self.abilities = ['fight']


    def xp_for_next_level(self):
        """
        Returns the number of xp at which the next level is gained.
        By default this should be 10 times current level, so 10 for
        level 1, 20 for level 2, etc.
        """
        return self.level * 10

    def fight(self, target):
        """
        Attacks target, dealing damage equal to the user's strength.
        """
        # self.dummy = target
        # target.hp = target.maxhp - self.strength
        # return target.hp
        target.take_damage(self.strength)

    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        while self.xp >= (self.xp_for_next_level()):
            self.level += 1
            self.xp -= self.xp_for_next_level()
            self.strength += 1
            self.constitution += 1
            self.intelligence += 1
            self.speed += 1
            self.maxhp += int(self.constitution/2)
            self.maxmp += int(self.intelligence/2)
            self.hp = self.maxhp
            self.mp = self.maxmp
        else:
            self.xp += xp


    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= damage
        if self.hp <= 0:
          return self.is_dead()

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        self.hp += healing
        if self.hp >= self.maxhp:
            self.hp = self.maxhp

    def is_dead(self):
        """
        Returns True if out of hp
        """
        if self.hp <= 0:
          return True
        else:
          return False


class Warrior(Hero):
    """
    Stat modifiers:
    strength +1
    intelligence -2
    constitution +2
    speed -1
    """
    def __init__(self, level=1):
        Hero.__init__(self, level)
        self.strength = 7
        self.intelligence = 4
        self.constitution = 8
        self.speed = 5
        self.maxhp = 104
        self.maxmp = 52
        self.hp = 104
        self.mp = 52
        self.xp = 0
        self.abilities.append('shield_slam')
        self.abilities.append('reckless_charge')

    def level_up(self):
        super(Warrior, self).level_up()
        while self.xp >= (self.level * 10):
            self.level += 1
            self.xp -= (self.level * 10)
            self.strength += 2
            self.constitution += 3
            self.intelligence += 1
            self.speed += 1
            self.maxhp += int(self.constitution/2)
            self.maxmp += int(self.intelligence/2)
            self.hp = self.maxhp
            self.mp = self.maxmp
        else:
            self.xp += xp


    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        self.dummy = target
        if self.mp <= 0 or (self.mp - 5) <= 0:
            raise InsufficientMP
        self.mp = self.maxmp - 5
        target.hp = target.maxhp - int(1.5 * self.strength)



    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 2 * strength
        """
        self.dummy = target
        self.hp = self.maxhp - 4
        target.hp = target.maxhp - int(2 * self.strength)

class Mage(Hero):
    """
    Stat modifiers
    strength -2
    inteligence +3
    constitution -2
    """
    def __init__(self, level=1):
        Hero.__init__(self, level)
        self.level = level
        self.strength = 4
        self.intelligence = 9
        self.constitution = 4
        self.speed = 6
        self.maxhp = 102
        self.maxmp = 54
        self.hp = 102
        self.mp = 54
        self.abilities = ['fight', 'fireball', 'frostbolt']


    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        self.dummy = target
        if self.mp <= 0 or (self.mp - 8) <= 0:
            raise InsufficientMP
        self.mp = self.maxmp - 8
        target.hp = target.maxhp - int(6 + (0.5 * self.intelligence))


    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        self.dummy = target
        if self.mp <= 0 or (self.mp - 3) <= 0:
            raise InsufficientMP
        self.mp = self.maxmp - 3
        target.hp = target.maxhp - 4


class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """
    def __init__(self, level=1):
        Hero.__init__(self, level)
        self.strength = 6
        self.intelligence = 6
        self.constitution = 7
        self.speed = 5
        self.maxhp = 103
        self.maxmp = 53
        self.hp = 103
        self.mp = 53
        self.abilities = ['fight', 'heal', 'smite']

    def heal(self, target):
        """
        cost: 4 mp
        healing: constitution
        """
        self.dummy = target
        if self.mp <= 0 or (self.mp - 4) <= 0:
            raise InsufficientMP
        self.mp = self.maxmp - 4
        target.hp += int(self.constitution)

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        self.dummy = target
        if self.mp <= 0 or (self.mp - 7) <= 0:
            raise InsufficientMP
        self.mp = self.maxmp - 7
        target.hp = target.maxhp - (4 + int(0.5 * (self.intelligence + self.constitution)))

class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """
    def __init__(self, level=1):
        Hero.__init__(self, level)
        self.strength = 7
        self.intelligence = 5
        self.constitution = 4
        self.speed = 8
        self.maxhp = 102
        self.maxmp = 52
        self.hp = 102
        self.mp = 52
        self.abilities = ['fight', 'backstab', 'rapid_strike']

    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        self.dummy = target
        if target.hp >= target.take_damage(0):
            target.hp = target.maxhp - int(2 * self.strength)
        else:
            raise InvalidTarget


    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        self.dummy = target
        if self.mp <= 0 or (self.mp - 5) <= 0:
            raise InsufficientMP
        self.mp = self.maxmp - 5
        target.hp = target.maxhp - int(4 + self.speed)
