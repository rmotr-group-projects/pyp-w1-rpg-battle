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
        modifiers = getattr(self, 'MODIFIERS', {})
        for stat, base in Hero.BASE_STATS.items():
            setattr(self, stat, base + modifiers.get(stat, 0))
        self.maxhp = int(self.BASE_HP + (self.constitution * 0.5))
        self.hp = self.maxhp
        self.maxmp = int(self.BASE_MP + (self.intelligence * 0.5))
        self.mp = self.maxmp
        self.level = 1
        self.xp = 0
        for l in range(level-1):
            self._level_up()

    def _level_up(self):
        modifiers = getattr(self, 'MODIFIERS', {})
        for stat in Hero.BASE_STATS:    
            base_increase = 1
            current = getattr(self, stat)
            modifier = modifiers.get(stat, 0)
            new_value = current + base_increase + (modifier if modifier > 0 else 0)
            setattr(self, stat, new_value)
        self.maxhp += int(self.constitution * 0.5)
        self.hp = self.maxhp
        self.maxmp += int(self.intelligence * 0.5)
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
        damage = self.strength
        target.take_damage(damage)
        return self._attack_message(target, damage)

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
        return self.hp <= 0

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

    def _has_enough_mp(self, req_mp):
        if self.mp < req_mp:
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
        cost = 5
        self._has_enough_mp(cost)
        damage = int(self.strength * 1.5)
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'shield slam')

    def reckless_charge(self, target):
        """
        cost: 4 hp
        damage: 2 * strength
        """
        health_cost = 4
        damage = self.strength * 2
        target.take_damage(damage)
        self.take_damage(health_cost)
        message = self._attack_message(target, damage, 'reckless charge')
        message.append('{hero} takes {damage} self-inflicted damage!'.format(hero=type(self).__name__,
                                                                               damage=health_cost))
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
        cost = 8
        self._has_enough_mp(cost)
        damage = 6 + int(self.intelligence * 0.5)
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'fireball')

    def frostbolt(self, target):
        """
        cost: 3 mp
        damage: 3 + level
        """
        cost = 3
        self._has_enough_mp(cost)
        damage = 3 + self.level
        target.take_damage(damage)
        self.mp -= cost
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
        cost = 4
        self._has_enough_mp(cost)
        healing = 3 * self.constitution
        target.heal_damage(healing)
        self.mp -= cost
        return ['{hero} heals {target} for {healing}!'.format(hero=type(self).__name__,
                                                                target=type(target).__name__,
                                                                healing=healing)]

    def smite(self, target):
        """
        cost: 7 mp
        damage: 4 + (0.5 * (intelligence + constitution))
        """
        cost = 7
        self._has_enough_mp(cost)
        damage = 4 + int((self.constitution + self.intelligence) * 0.5)
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
        damage = self.strength * 2
        target.take_damage(damage)
        return self._attack_message(target, damage, 'backstab')

    def rapid_strike(self, target):
        """
        cost: 5 mp
        damage: 4 + speed
        """
        cost = 5
        self._has_enough_mp(cost)
        damage = 4 + self.speed
        target.take_damage(damage)
        self.mp -= cost
        return self._attack_message(target, damage, 'rapid strike')

