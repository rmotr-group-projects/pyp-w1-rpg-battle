from .exceptions import *

class Monster(object):
    multipliers = dict(strength=1, intelligence=1, constitution=1, speed=1)

    def __init__(self, level=1, base =8):
        """
        Sets up stats and levels up the monster if necessary
        """
        for k,v in self.multipliers.items():
            setattr(self, k, base*v)
        self.level=0
        # self.strength=8+(level-1)
        # self.constitution=8+(level-1)
        # self.intelligence=8+(level-1)
        # self.speed=8+(level-1)
        self.basehp=10
        self.maxhp=self.basehp+((level-1)*(0.5*self.constitution))
        self.hp=self.maxhp
        for n in range(level):
            self.level_up()


    def level_up(self):
        for k,v in self.multipliers.items():
            # setattr(self, k, getattr(self, k) + 1 + (self.modifiers[k] if self.modifiers[k] > 0 else 0))
            setattr(self, k, int(8 * v + (self.level) * v))
        self.maxhp+=  0
        self.hp= self.maxhp
        self.level +=1




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
    thisDragon=Monster()
    thisDragon.constitution*=2
    thisDragon.basehp=100
    damage=-5

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
    redDragon=Dragon()
    redDragon.strength*=2
    redDragon.intelligence*=1.5
    commandQueue=['fire_breath', 'tail_swipe', 'fight']


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
    greenDragon=Dragon()
    greenDragon.strength*=1.5
    greenDragon.speed*=1.5
    commandQueue=['poison_breath','tail_swipe','fight']


    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        damage= (self.intelligence + self.constitution) * 1.5


class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    constitution=8*0.25

    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        damage=self.intelligence*1.5
        self.hp+=1


class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    basehp=30
    intelligence=8*2
    commandQueue=['fight', 'bite','life_drain']

    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        damage=speed*0.5
        target.maxhp-=damage
        self.hp+=1


class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    strength=8*1.25
    speed=8*0.5
    intelligence=8*0.25
    commandQueue=['bash', 'fight', 'life_drain']

    def bash(self, target):
        """
        damage: strength * 2
        """
        damage=self.strength*2


class Humanoid(Monster):
    def slash(self, target):
        """
        damage: strength + speed
        """
        damage=self.strength+speed


class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    ['slash', 'fight', 'regenerate']
    """
    strength=8*1.75
    constitution=8*1.5
    basehp=20
    commandQueue=['slash', 'fight', 'regenerate']

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
    strength=8*1.75
    basehp=16
    commandQueue=['blood_rage', 'slash', 'fight']

    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        self.hp-=self.constitution*0.5
        damage=self.strength*2
