from .exceptions import *

class Hero(object):
    BASE_STATS = {'strength': 6,
                  'intelligence': 6,
                  'speed': 6,
                  'constitution': 6}
    BASE_HP = 100
    BASE_MP = 50

    
    def __init__(self, level=1):
        
        modifiers = getattr(self, 'MODIFIERS', {})
        for stat, base in Hero.BASE_STATS.items():
            setattr(self, stat, base + modifiers.get(stat, 0))

        self.maxhp = self.BASE_HP + int(self.constitution / 2)
        self.maxmp = self.BASE_MP + int(self.intelligence / 2)
        self.hp = self.maxhp
        self.mp = self.maxmp
        self.level = 1
        self.xp = 0
        while level > 1:
            self._level_up()
            level -= 1
        

    def _level_up(self):
        """
        Helper method to handle levelling up
        """
        modifiers = getattr(self, 'MODIFIERS', {})
        
        for stat in Hero.BASE_STATS:
            increase = 1 
            modifier = modifiers.get(stat, 0)
            if modifier <= 0:
                modifier = 0
            current = getattr(self, stat)
            new = increase + current + modifier
            setattr(self, stat, new)
        self.maxhp += int(self.constitution / 2)
        self.maxmp += int(self.intelligence / 2)
        self.hp = self.maxhp
        self.mp = self.maxmp
        
        self.xp -= self.xp_for_next_level()
        self.level += 1

    def xp_for_next_level(self):
        """
        Returns the number of xp at which the next level is gained.
        By default this should be 10 times current level, so 10 for
        level 1, 20 for level 2, etc.
        """
        return  self.level * 10

    def fight(self, target):
        """
        Attacks target, dealing damage equal to the user's strength.
        """
        target.take_damage(self.strength)

    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        
        leveling = True
        while leveling:
            if self.xp >= self.xp_for_next_level():
                self.xp -= self.xp_for_next_level()
                self._level_up()
            else:
                leveling = False
                

    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        if self.is_dead():
            raise Defeat()
        heals = self.hp + healing
        if heals >= self.maxhp:
            self.hp = self.maxhp
        else:
            self.hp = heals

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
    MODIFIERS = {'strength': 1,
                 'intelligence': -2,
                 'constitution': 2,
                 'speed': -1}

    abilities = ('fight', 'shield_slam', 'reckless_charge')

    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        if self.mp > 4:
            self.mp -= 5
            target.take_damage(int(1.5 * self.strength))
        else:
            raise InsufficientMP()
            


    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 2 * strength
        """
        if self.hp > 3:
            self.hp -= 4
            target.take_damage(int(2 * self.strength))
        else:
            raise InvalidCommand()


class Mage(Hero):
    """
    Stat modifiers
    strength -2
    inteligence +3
    constitution -2
    """

    MODIFIERS = {'strength': -2,
                 'intelligence': 3,
                 'constitution': -2}

    abilities = ('fight', 'fireball', 'frostbolt')


    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        if self.mp > 7:
            self.mp -= 8
            target.take_damage(int(6 + ( self.intelligence * 0.5 )))
        else:
            raise InsufficientMP()


    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        if self.mp > 2:
            self.mp -= 3
            target.take_damage(3 + self.level)
        else:
            raise InsufficientMP()


class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """
    MODIFIERS = {'speed': -1,
                 'constitution': 1}

    abilities = ('fight', 'heal', 'smite')


    def heal(self, target):
        """
        cost: 4 mp
        healing: 3 * constitution
        """
        if self.mp > 3:
            self.mp -= 4
            target.heal_damage(3 * self.constitution)
        else:
            raise InsufficientMP()


    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        if self.mp > 6:
            self.mp -= 7
            target.take_damage(int(4 + 0.5 * (self.intelligence + self.constitution)))
        else:
            raise InsufficientMP()


class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """
    MODIFIERS = {'speed': 2,
                 'strength': 1,
                 'intelligence': -1,
                 'constitution': -2}

    abilities = ('fight', 'backstab', 'rapid_strike')


    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        if target.hp == target.maxhp:
            target.take_damage(2 * self.strength)
        else:
            raise InvalidTarget()


    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        if self.mp > 4:
            self.mp -= 5
            target.take_damage(4 + self.speed)
        else:
            raise InsufficientMP()


