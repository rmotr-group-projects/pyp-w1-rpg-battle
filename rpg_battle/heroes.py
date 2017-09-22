from .exceptions import *

class Hero(object):
    BASE_STATS = {'strength': 6,
                  'intelligence': 6,
                  'speed': 6,
                  'constitution': 6}
    BASE_HP = 100
    BASE_MP = 50

    
    def __init__(self, level=1):
        """
        Sets stats up and levels up hero if necessary.
        """
        
        for stat, statValue in self.BASE_STATS.iteritems():
            if hasattr(self, 'MODIFIERS'):
                modifier = self.MODIFIERS.get(stat, 0)
            else:
                modifier = 0
                
            setattr(self, stat, statValue + modifier)
            
        self.maxhp = self.BASE_HP + int(0.5 * self.constitution)
        self.hp = self.maxhp
        
        self.maxmp = self.BASE_MP + int(0.5* self.intelligence)
        self.mp = self.maxmp
        
        self.xp = 0
        self.level = 1
        while self.level< level:
            self._level_up()
            
        
    def _level_up(self):
        """
        Helper method to handle levelling up
        """
        for stat, statValue in self.BASE_STATS.iteritems():
            if hasattr(self, 'MODIFIERS'):
                modifier = self.MODIFIERS.get(stat, 0)
            else:
                modifier = 0
            
            if modifier < 0:
                modifier = 0
            setattr(self, stat, getattr(self, stat)+1+modifier)
        
        self.maxhp += int(0.5*self.constitution)
        self.hp = self.maxhp
        
        self.maxmp += int(0.5*self.intelligence)
        self.mp = self.maxmp
        
        self.xp -= self.xp_for_next_level()
        self.level += 1

    def xp_for_next_level(self):
        """
        Returns the number of xp at which the next level is gained.
        By default this should be 10 times current level, so 10 for
        level 1, 20 for level 2, etc.
        """
        return self.level*10

    def fight(self, target):
        """
        Attacks target, dealing damage equal to the user's strength.
        """
        deal_damage = self.strength
        target.take_damage(deal_damage)
        return self._attack_message(target, deal_damage)
        
    def _attack_message(self, target, damage, attack=None):
        hero = type(self).__name__
        target_name = type(target).__name__
        if attack:
            message = "{hero} hits {target} with {attack} for {damage} damage!"
            return [message.format(hero=hero,
                                  target=target_name,
                                  attack=attack,
                                  damage=damage)]  
        else:
            return ["{hero} attacks {target} for {damage}!".format(hero=hero,
                                                                    target=target_name,
                                                                    damage=damage)]
                                                                    
    def gain_xp(self, xp):
        """
        Increases current xp total, triggers level up if necessary,
        rolling over any excess xp. Example: If a level 1 hero received
        enough xp to increase its total to 12 xp it would level up and
        then have an xp total of 2.
        """
        self.xp += xp
        while self.xp >= self.xp_for_next_level():
            self._level_up()

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

    def _mpRaiseError_(self, mp):
        if self.mp < mp:
            raise InsufficientMP()

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
        self._mpRaiseError_(5)
        self.mp -= 5
        
        damage = int(1.5 * self.strength)
        target.take_damage(damage)
        
        return self._attack_message(target, damage, 'shield_slam')


    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 2 * strength
        """
        cost = 4
        self.take_damage(cost)
        
        damage = int(2*self.strength)
        target.take_damage(damage)

        message = self._attack_message(target, damage, 'reckless charge')
        message.append('{hero} takes {damage} self-inflicted damage!'.format(hero=type(self).__name__,
                                                                               damage = cost))
        return message

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
        self._mpRaiseError_(8)
        self.mp -= 8
        
        damage = 6 + int(0.5 * self.intelligence)
        target.take_damage(damage)

        return self._attack_message(target, damage, 'fireball')


    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        self._mpRaiseError_(3)
        self.mp -= 3
        
        damage = 3 + self.level
        target.take_damage(damage)
        
        return self._attack_message(target, damage, 'frostbolt')


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
        self._mpRaiseError_(4)
        self.mp -= 4
        
        healing = int(3 * self.constitution)
        target.heal_damage(healing)

        return ['{hero} heals {target} for {healing}!'.format(hero=type(self).__name__,
                                                                target=type(target).__name__,
                                                                healing=healing)]

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        self._mpRaiseError_(7)
        self.mp -= 7
        
        damage = 4 + int(0.5 * (self.intelligence + self.constitution))
        target.take_damage(damage)
        
        return self._attack_message(target, damage, 'smite')



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
        self._mpRaiseError_(5)
        self.mp -= 5
        
        damage = 4 + self.speed
        target.take_damage(damage)
        
        return self._attack_message(target, damage, 'rapid strike')



