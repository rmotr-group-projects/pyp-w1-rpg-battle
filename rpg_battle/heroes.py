from .exceptions import *

class Hero(object):
    STAT_MODIFIERS = {'strength' : 0, 'intelligence' : 0, 'constitution' : 0,
                                                            'speed' : 0}
    def __init__(self, level=1):
        """
        Sets stats up and levels up hero if necessary.
        """
        self.calculate_stats(level, **self.STAT_MODIFIERS)
        self.abilities = {'fight': self.fight}
        
    def __repr__(self):
        return 'Hero'

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
        if self.xp >= self.xp_for_next_level():
            self.level_up(**self.STAT_MODIFIERS)
            
    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        self.hp -= int(damage)

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
            
    def calculate_stats(self, level = 1, **kwargs):
        def individual_stat(value):
            if value > 0:
                stat = 5 + (level *(value+1))
            elif value <= 0:
                stat = 5 + level + value
            return stat
            
        def calculate_HP(level, constitution):
            maxhp = 100
            if constitution > 0:
                 for lvl in range(1, level + 1):
                    maxhp += int(.5 * (5+(lvl * (1 + constitution))))
            else:
                for lvl in range(1, level + 1):
                    maxhp += int(.5 * ((5 + constitution) + lvl))
            return maxhp
            
        def calculate_MP(level, intelligence):
            maxmp = 50
            if intelligence > 0:
                 for lvl in range(1, level + 1):
                    maxmp += int(.5 * (5+(lvl * (1 + intelligence))))
            else:
                for lvl in range(1, level + 1):
                    maxmp += int(.5 * ((5 + intelligence) + lvl))
            return maxmp
            
        for key, value in kwargs.items():
            if key == 'strength':
                self.strength = individual_stat(value)
            if key == 'intelligence':
                self.intelligence = individual_stat(value)
            if key == 'constitution':
                self.constitution = individual_stat(value)
            if key == 'speed':
                self.speed = individual_stat(value)
        
        self.level = level
        _constitution = self.STAT_MODIFIERS['constitution']  
        _intelligence = self.STAT_MODIFIERS['intelligence']
        self.maxhp = calculate_HP(self.level, _constitution)
        self.maxmp = calculate_MP(self.level, _intelligence)
        self.hp = self.maxhp
        self.mp = self.maxmp
        self.xp = 0
        self.character_type = 'Hero'
        
    def level_up(self, **kwargs):
        self.xp = self.xp - self.xp_for_next_level()
        self.level += 1
            
        for key, value in kwargs.items():
                if key == 'strength' and value >= 0:
                    self.strength += value + 1
                elif key == 'strength' and value < 0:
                    self.strength += 1
                if key == 'intelligence' and value >= 0:
                    self.intelligence += value + 1
                elif key == 'intelligence' and value < 0:
                    self.intelligence += 1
                if key == 'constitution' and value >= 0:
                    self.constitution += value + 1
                elif key == 'constitution' and value < 0:
                    self.constitution += 1
                if key == 'speed' and value >= 0:
                    self.speed += value + 1
                elif key == 'speed' and value < 0:
                    self.speed += 1
                    
        self.maxhp += int(.5 * self.constitution)
        self.maxmp += int(.5 * self.intelligence)
        self.hp = self.maxhp
        self.mp = self.maxmp
        
class Warrior(Hero):
    """
    Stat modifiers:
    strength +1
    intelligence -2
    constitution +2
    speed -1
    """
    STAT_MODIFIERS = {'strength' : 1, 'intelligence' : -2, 'constitution' : 2,
                                                            'speed' : -1}
    def __init__(self, level=1):
        self.calculate_stats(level, **self.STAT_MODIFIERS)
        self.abilities = {'fight': self.fight, 'shield_slam' : 
            self.shield_slam, 'reckless_charge' : self.reckless_charge}
    
    def __repr__(self):
        return 'Warrior'
    
    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        if self.xp >= self.xp_for_next_level():
            self.level_up(**self.STAT_MODIFIERS)
        
    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        
        if self.mp < 5:
            raise InsufficientMP()
        else:
            self.mp -= 5
            target.take_damage(int(self.strength * 1.5))
        
    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 2 * strength
        """
        self.hp -= 4
        target.take_damage(int(self.strength * 2))

class Mage(Hero):
    """
    Stat modifiers
    strength -2
    inteligence +3
    constitution -2
    """
    STAT_MODIFIERS = {'strength' : -2, 'intelligence' : 3, 
                                'constitution' : -2, 'speed' : 0}
    def __init__(self, level=1):
        self.calculate_stats(level, **self.STAT_MODIFIERS)
        self.abilities = {'fight': self.fight, 'fireball' : self.fireball,
                                            'frostbolt' : self.frostbolt}
    
    def __repr__(self):
        return 'Mage'
        
    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        if self.xp >= self.xp_for_next_level():
            self.level_up(**self.STAT_MODIFIERS)
        
    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        if self.mp < 8:
            raise InsufficientMP
        self.mp -= 8
        target.take_damage(int(6 + (.5 * self.intelligence)))

    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        if self.mp < 3:
            raise InsufficientMP
        self.mp -= 3
        target.take_damage(int(3 + self.level))

class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """
    STAT_MODIFIERS = {'strength' : 0, 'intelligence' : 0, 'constitution' : 1,
                                                            'speed' : -1}
    def __init__(self, level=1):
        self.calculate_stats(level, **self.STAT_MODIFIERS)
        self.abilities = {'fight': self.fight, 'heal': self.heal,
                                                    'smite' : self.smite}
    
    def __repr__(self):
        return 'Cleric'
        
    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        if self.xp >= self.xp_for_next_level():
            self.level_up(**self.STAT_MODIFIERS)

    def heal(self, target):
        """
        cost: 4 mp
        healing: constitution
        """
        if self.mp < 4:
            raise InsufficientMP()
        self.mp -= 4
        target.heal_damage(self.constitution)

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        if self.mp < 7:
            raise InsufficientMP()
        self.mp -= 7
        target.take_damage(int(4 + (.5 * (self.intelligence + 
                                                    self.constitution))))

class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """
    STAT_MODIFIERS = {'strength' : 1, 'intelligence' : -1, 
                                    'constitution' : -2, 'speed' : 2}
    def __init__(self, level=1):
        self.calculate_stats(level, **self.STAT_MODIFIERS)
        self.abilities = {'fight': self.fight, 'backstab' : self.backstab,
                                        'rapid_strike' : self.rapid_strike}
        
    def __repr__(self):
        return 'Rogue'
        
    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        if self.xp >= self.xp_for_next_level():
            self.level_up(**self.STAT_MODIFIERS)

    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        if target.hp == target.maxhp:
            target.take_damage(int(2 * self.strength))
        else: raise InvalidTarget()

    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        if self.mp < 5:
            raise InsufficientMP()
        self.mp -= 5
        target.take_damage(int(4 + self.speed))
