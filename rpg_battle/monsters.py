from .exceptions import *

class Monster(object):
    multipliers = dict(strength=1, intelligence=1, constitution=1, speed=1)
    basehp=10
    damage_reduction = 0

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
        self.maxhp=10
        self.hp=self.maxhp
        for n in range(level):
            self.level_up()


    def level_up(self):
        for k,v in self.multipliers.items():
            # setattr(self, k, getattr(self, k) + 1 + (self.modifiers[k] if self.modifiers[k] > 0 else 0))
            setattr(self, k, int(8 * v + (self.level) * v))
        self.level +=1
        self.maxhp=self.basehp + (self.level - 1) * (0.5 * self.constitution)
        self.hp= self.maxhp





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
        total_damage = damage - self.damage_reduction
        if total_damage >0:
            self.hp-= total_damage



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
        if self.hp <= 0:
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
    multipliers = dict(strength=1, intelligence=1, constitution=2, speed=1)
    basehp= 100
    damage_reduction = 5
    def __init__(self, level=0):
        super().__init__()
        self.maxhp=100
        self.hp=self.maxhp
        for n in range(level-1):
            super().level_up()

    def tail_swipe(self, target):
        """
        damage: strength + speed
        """
        target.hp-=self.strength + self.speed


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    multipliers = dict(strength=2, intelligence=1.5, constitution=2, speed=1)

    # redDragon=Dragon()
    # redDragon.strength*=2
    # redDragon.intelligence*=1.5
    commandQueue=['fire_breath', 'tail_swipe', 'fight']


    def fire_breath(self, target):
        """
        damage: intelligence * 2.5
        """
        target.hp -= self.intelligence * 2.5

class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    multipliers = dict(strength=1.5, intelligence=1, constitution=2, speed=1.5)
    # greenDragon=Dragon()
    # greenDragon.strength*=1.5
    # greenDragon.speed*=1.5
    commandQueue=['poison_breath','tail_swipe','fight']


    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        target.hp -= (self.intelligence + self.constitution) * 1.5


class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    multipliers = dict(strength=1, intelligence=1, constitution=0.25, speed=1)

    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        damage = self.intelligence * 1.5
        target.hp-= damage
        self.hp += damage
        if self.hp >= self.maxhp:
            self.hp=self.maxhp
    def heal_damage(self, healing):
        self.hp-=healing



class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    multipliers = dict(strength=1, intelligence=2, constitution=0.25, speed=1)
    basehp=30
    commandQueue=['fight', 'bite','life_drain']

    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        damage=self.speed*0.5
        target.maxhp-=damage
        target.hp= target.maxhp
        self.hp+=damage
        if self.hp >= self.maxhp:
            self.hp=self.maxhp


class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    multipliers = dict(strength=1.25, intelligence=0.25, constitution=0.25, speed=0.5)

    commandQueue=['bash', 'fight', 'life_drain']

    def bash(self, target):
        """
        damage: strength * 2
        """
        target.hp-=self.strength*2


class Humanoid(Monster):
    def slash(self, target):
        """
        damage: strength + speed
        """
        target.hp -=self.strength + self.speed


class Troll(Humanoid):
    multipliers = dict(strength=1.75, intelligence=1, constitution=1.5, speed=1)
    basehp= 20
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    ['slash', 'fight', 'regenerate']
    """

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
    multipliers = dict(strength=1.75, intelligence=1, constitution=1, speed=1)

    basehp=16
    commandQueue=['blood_rage', 'slash', 'fight']

    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        self.hp-=self.constitution*0.5
        target.hp-=self.strength*2
