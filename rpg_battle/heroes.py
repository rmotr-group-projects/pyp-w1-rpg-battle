from .exceptions import *

class Hero(object):
    
    baseStats = { 'strength': 6,
                  'intelligence': 6,
                  'speed': 6,
                  'constitution': 6}
    BASE_HP = 100
    BASE_MP = 50              
    
    def __init__(self, level=1):
        """
        Sets stats up and levels up hero if necessary.
        """
        for stat, base in Hero.baseStats.items():
            setattr(self, stat, base + getattr(self,stat.upper() +'_MOD', 0))
        self.maxhp = int(self.BASE_HP + (self.constitution * 0.5))
        self.hp = self.maxhp
        self.maxmp = int(self.BASE_MP + (self.intelligence * 0.5))
        self.mp = self.maxmp
        self.level = 1
        self.xp = 0
        for level in range(level-1):
            self._levelup()
            
    def _levelup(self):
        for stat in Hero.baseStats:
            increase = 1
            current = getattr(self, stat)
            mod = getattr(self, '{}_MOD'.format(stat.upper()), 0)
            new = current + increase + (mod if mod > 0 else 0)
            setattr(self, stat, new)
        self.maxhp += int(self.constitution * .5)
        self.hp = self.maxhp
        self.maxmp += int(self.intelligence * .5)
        self.mp = self.maxmp
        self.xp -= self.xp_for_next_level()
        self.level += 1
            
    def xp_for_next_level(self):
        """
        Returns the number of xp at which the next level is gained.
        By default this should be 10 times current level, so 10 for
        level 1, 20 for level 2, etc.
        """
        return 10 * self.level

    def fight(self, target):
        """
        Attacks target, dealing damage equal to the user's strength.
        """
        target.take_damage(self.strength)
        return self._attack_message(target, self.strength)

    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        while self.xp >= self.xp_for_next_level():
            self._levelup()
            
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
        return False
        
    def  _attack_message(self, target, damage, attack = None):
        hero = type(self).__name__
        target = type(target).__name__
        if attack:
            message = "{hero} hits {target} with {attack} for {damage} damage!\n"
            return message.format(hero = hero,
                                  target = target,
                                  attack = attack,
                                  damage = damage)
        else:
            return "{hero} attacks {target} for {damage}!\n".format(hero = hero,
                                                                    target = target,
                                                                    damage = damage)
                                                                    
                                                                    
    def attack(self, command, target):
        """
        Attacks target using next ability in command queue
        """
        attack_method = getattr(self, command, 'fight')
        
        dam, attack_type = attack_method(target)


class Warrior(Hero):
    """
    Stat modifiers:
    strength +1
    intelligence -2
    constitution +2
    speed -1
    """
    
    STRENGTH_MOD = 1
    INTELLIGENCE_MOD = -2
    CONSTITUTION_MOD = 2
    SPEED_MOD = -1
    
    abilities = ('fight', 'shield_slam', 'reckless_charge')
    
    def shield_slam(self, target):
        """
        cost: 5 mp
        damage: 1.5 * strength
        """
        cost = 5
        if self.mp < cost:
            raise InsufficientMP()
        damage = int(self.strength * 1.5)
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'shield slam')
        

    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 1.5 * strength
        """
        healthcost = 4
        damage = int(self.strength * 2)
        target.take_damage(damage)
        self.take_damage(healthcost)
        message = self._attack_message(target, damage, 'reckless charge')
        message += '{hero} takes {damage} self-inflicted damage!\n'.format(hero=type(self).__name__, damage = healthcost)
        
        return message

class Mage(Hero):
    """
    Stat modifiers
    strength -2
    inteligence +3
    constitution -2
    """
    
    STRENGTH_MOD = -2
    INTELLIGENCE_MOD = 3
    CONSTITUTION_MOD = -2
    
    abilities = ('fight', 'fireball', 'frostbolt')

    

    def fireball(self, target):
        """
        cost: 8 mp
        damage: 6 + (0.5 * intelligence)
        """
        cost = 8
        if self.mp < cost:
            raise InsufficientMP()
        damage = 6 + int(self.intelligence * .5)
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'fireball')

    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        cost = 3
        if self.mp < cost:
            raise InsufficientMP()
        damage = self.level + 3
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'frostbolt')
        

class Cleric(Hero):
    """
    Stat modifiers:
    speed -1
    constitution +1
    """
    
    CONSTITUTION_MOD = 1
    SPEED_MOD = -1
    
    abilities = ('fight', 'heal', 'smite')

    def heal(self, target):
        """
        cost: 4 mp
        healing: constitution
        """
        cost = 4
        if self.mp < cost:
            raise InsufficientMP()
        heal = self.constitution
        target.heal_damage(heal)
        self.mp -= cost
        return '{hero} heals {target} for {heal}!\n'.format(hero=type(self).__name__,
                                                               target=target,
                                                               heal=heal)

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        cost = 7 
        if self.mp < cost:
            raise InsufficientMP()
        damage = 4 + int(.5 * (self.constitution + self.intelligence))
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'smite')

class Rogue(Hero):
    """
    Stat modifiers:
    speed +2
    strength +1
    intelligence -1
    constitution -2
    """
    
    SPEED_MOD = 2
    STRENGTH_MOD = 1
    INTELLIGENCE_MOD = -1
    CONSTITUTION_MOD = -2

    abilities = ('fight', 'backstab', 'rapid_strike')
    
    def backstab(self, target):
        """
        cost: None
        restriction: target must be undamaged, else raise InvalidTarget
        damage: 2 * strength
        """
        
        if target.hp != target.maxhp:
            raise InvalidTarget()
        damage = 2 * self.strength
        target.take_damage(damage)
        return self._attack_message(target, damage, 'backstab')
        

    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        cost = 5
        if self.mp < cost:
            raise InsufficientMP()
        damage = 4 + self.speed
        target.take_damage(damage)
        self.mp -=cost
        return self._attack_message(target, damage, 'rapid strike')
