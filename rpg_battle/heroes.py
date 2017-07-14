from .exceptions import *

class Hero(object):
    
    def __init__(self, level=1):
        """
        Sets stats up and levels up hero if necessary.
        """
        self.level = 1
        
        # my_var = self.attr
        # my_var = getattr(self, 'attr')
            
        self.strength = 6 + getattr(self, 'MODSTR', 0)
        self.intelligence = 6 + getattr(self, 'MODINT', 0)
        self.constitution = 6 + getattr(self, 'MODCON', 0)
        self.speed = 6 + getattr(self, 'MODSPD', 0)
        
        self.maxmp = 50 + int(self.intelligence / 2)
        self.mp = self.maxmp
        
        self.xp = 0
        self.maxhp = 100 + int(self.constitution / 2)
        self.hp = self.maxhp
        
        if level > 1:
            while self.level < level:
                self.level_up()
            self.xp = 0
        

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
        target.take_damage(self.strength)

    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        if xp >= self.xp_for_next_level():
            self.level_up()
            
    def level_up(self):
        
        self.xp -= self.xp_for_next_level()
        
        
        self.level += 1
        
        
        if getattr(self, 'MODCON', 0) <= 0:
            self.constitution += 1
        else:
            self.constitution += 1 + getattr(self, 'MODCON')
            
        if getattr(self, 'MODINT', 0) <= 0:
            self.intelligence += 1
        else:
            self.intelligence += 1 + getattr(self, 'MODINT')
        
        if getattr(self, 'MODSPD', 0) <= 0:
            self.speed += 1
        else:
            self.speed += 1 + getattr(self, "MODSPD")
            
        if getattr(self, 'MODSTR', 0) <= 0:
            self.strength += 1
        else:
            self.strength += 1 + getattr(self, 'MODSTR')
        
        self.maxhp += int(self.constitution / 2)
        self.hp = self.maxhp
        
        self.maxmp += int(self.intelligence / 2)
        self.mp = self.maxmp
        
        
    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= damage

    def heal_damage(self, healing):
        """
        Increase hp by healing but not exceeding maxhp
        """
        self.hp += healing
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


class Warrior(Hero):
    """
    Stat modifiers:
    strength +1
    intelligence -2
    constitution +2
    speed -1
    """
    MODSTR = 1
    MODINT = -2
    MODSPD = -1
    MODCON = 2
    
    abilities = ['fight', 'shield_slam', 'reckless_charge']
    
    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        if self.mp >= 5:
            self.mp -= 5
            target.take_damage(int(1.5 * self.strength))
        else:
            raise InsufficientMP()
        

    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 2 * strength
        """
        target.take_damage(int(2 * self.strength))
        self.take_damage(4)

class Mage(Hero):
    """
    Stat modifiers
    strength -2
    inteligence +3
    constitution -2
    """
    MODSTR = -2
    MODINT = 3
    MODCON = -2
    
    abilities = ['fight', 'fireball', 'frostbolt']

    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        if self.mp >= 8:
            self.mp -= 8
            target.take_damage(int(6 + (0.5 * self.intelligence)))
        else:
            raise InsufficientMP()
        

    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        if self.mp >= 3:
            self.mp -= 3
            target.take_damage(3 + self.level)
        else:
            raise InsufficientMP()

#srikanth
class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """
    MODCON = 1
    MODSPD = -1
    
    abilities = ['fight', 'heal', 'smite']

    def heal(self, target):
        """
        cost: 4 mp
        healing: constitution
        """
        if self.mp >= 4:
            self.mp -= 4
            target.heal_damage(self.constitution)
        else:
            raise InsufficientMP()

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        if self.mp >= 7:
            self.mp -= 7
            target.take_damage(int(.5 * self.intelligence + self.constitution))
        else:
            raise InsufficientMP()

#srikanth
class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """
    MODSTR = 1
    MODINT = -1
    MODCON = -2
    MODSPD = 2
    
    abilities = ['fight', 'backstab', 'rapid_strike']

    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        if target.hp == target.maxhp:
            target.take_damage(int(2 * self.strength))
        else:
            raise InvalidTarget()

    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        if self.mp >= 5:
            self.mp -= 5
            target.take_damage(int(4 + self.speed))
        else:
            raise InsufficientMP()