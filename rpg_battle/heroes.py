from .exceptions import *

class Hero(object):
    modifiers = dict(strength=0, intelligence=0, constitution=0, speed=0)

    def __init__(self, level=1, base=6):
        # self.strength = 6 * level + str_modifier

        for k,v in self.modifiers.items():
            if v >= 0:
                # setattr(self, k, ((base + self.modifiers[k]) + (level -1) * (self.modifiers[k] +1)))
                setattr(self, k, base-1)
            else:
                setattr(self, k, ((base + self.modifiers[k] -1)))
        # self.strength =
        # self.constitution = (base + cons_modifier) + (level -1) * (cons_modifier +1)
        # self.intelligence = (base + int_modifier) + (level -1) * (int_modifier +1)


        self.level= 0
        self.maxmp=50
        self.maxhp=100
        # def recursion_hp(x):
        #     if x <= 6:
        #         return 0
        #     else:
        #         return int(0.5 *x) + int(recursion(x-3))
        # self.speed = (base + speed_modifier) + (level -1) * (speed_modifier +1)

        # self.maxhp+= recursion_hp(self.constitution)
        # self.maxmp+= recursion(self.intelligence)
        self.hp = (self.maxhp)
        self.mp = (self.maxmp)

        self.xp = 0
        for n in range(level):
            self.level_up()

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def mp(self):
        return self._mp
    @mp.setter
    def mp(self, value):
        self._mp = value

    def level_up(self):
        for k,v in self.modifiers.items():
            setattr(self, k, getattr(self, k) + 1 + (self.modifiers[k] if self.modifiers[k] > 0 else 0))
        self.maxhp+=  int(0.5*self.constitution)
        self.maxmp+= int(0.5*self.intelligence)
        self.hp= self.maxhp
        self.mp = self.maxmp
        self.level +=1




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
        return target.take_damage(self.strength)

    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        attributes = ['strength', 'constitution', 'speed', 'intelligence', 'level']
        if self.xp >= self.xp_for_next_level():
            self.xp = self.xp - self.xp_for_next_level()
            self.level_up()
        #     for stat in attributes:
        #         setattr(self, stat, getattr(self, stat) + 1)
        # self.maxhp+=  int(0.5*self.constitution)
        # self.maxmp+= int(0.5*self.intelligence)
        # self.hp= self.maxhp
        # self.mp = self.maxmp




    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp = self.hp - damage
        if self.hp <0:
            self.hp=0

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        self.hp+= healing
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def is_dead(self):
        """
        Returns True if out of hp
        """
        if self.hp == 0:
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
    modifiers = dict(strength=1, intelligence=-2, constitution=2, speed=-1)
    abilities = {'fight', 'shield_slam', 'reckless_charge'}
        # self.strength = self.strength + 1
        # self.intelligence = self.intelligence -2
        # self.constitution = self.constitution + 2
        # self.speed = self.speed - 1
        # self.maxmp=int(50 + 0.5 * self.intelligence)
        # self.maxhp=int(100 + 0.5 * self.constitution)
        # self.hp = int(self.maxhp)
        # self.mp = int(self.maxmp)




    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        pass

    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 1.5 * strength
        """
        pass

class Mage(Hero):
    """
    Stat modifiers
    strength -2
    inteligence +3
    constitution -2
    """

    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        pass

    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        pass

class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """

    def heal(self, target):
        """
        cost: 4 mp
        healing: constitution
        """
        pass

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        pass

class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """

    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        pass

    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        pass
