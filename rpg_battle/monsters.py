from .exceptions import *

class Monster(object):

    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        self.level=level
        self.strength=8+(level-1)
        self.constitution=8+(level-1)
        self.intelligence=8+(level-1)
        self.speed=8+(level-1)
        self.basehp=10
        self.maxhp=self.basehp+((level-1)*(0.5*self.constitution))
        self.hp=self.maxhp

    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: (average of stats) + (maxhp % 10)
        """
        return ((self.strength+self.constitution+self.intelligence+self.speed)/4+(self.maxhp%10))

    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        target.hp-=self.strength
        

    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= damage
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

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        commandQueue=['fight', 'bash', 'slash']


class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """


    def tail_swipe(self, target):
        """
        damage: strength + speed
        """
        damage= self.strength + self.speed


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """

    def fire_breath(self, target):
        """
        damage: intelligence * 2.5
        """
        damage= self.intelligence * 2.5

class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """


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

    def bite(self, target):
        """
        damage: speed * 0.5
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
    ['slash', 'fight', 'regenerate']    
    """

    def regenerate(self, *args):
        """
        heals self for constitution
        """
        pass


class Orc(Humanoid):
    """

    strength multiplier: 1.75
    base hp: 16
    ['blood_rage', 'slash', 'fight']
    """

    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        pass
