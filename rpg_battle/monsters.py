from .exceptions import *
from collections import deque

class Monster(object):
    BASE_STATS = {'strength': 8,
             'constitution': 8,
             'intelligence': 8,
             'speed': 8}
    BASE_HP = 10
    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        for stat, base in Monster.BASE_STATS.items():
            multipier = getattr(self, '{}_MULTIPLIER'.format(stat.upper()), 1)
            setattr(self, stat, int(base * multipier) + int((level - 1) * multipier))
        self.maxhp = self.BASE_HP + int((level - 1) * self.constitution * 0.5)
        self.hp = self.maxhp
        self.level = level

    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: (average of stats) + (maxhp % 10)
        """
        return int((sum([getattr(self, stat) for stat in self.BASE_STATS]) / 4) + (self.maxhp % 10))

    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        damage = self.strength
        target.take_damage(damage)
        return self._attack_message(target, damage)


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

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        command = self.fight_sequence.popleft()
        ability = getattr(self, command)
        message = ability(target)
        self.fight_sequence.append(command)
        return message

    def _attack_message(self, target, damage, attack=None):
        monster = type(self).__name__
        target_name = type(target).__name__
        if attack:
            message = "{monster} hits {target} with {attack} for {damage} damage!\n"
            return message.format(monster=monster, target=target_name, attack=attack, damage=damage)
        else:
            return "{monster} attacks {target} for {damage}!\n".format(monster=monster, target=target_name, damage=damage)



class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    CONSTITUTION_MULTIPLIER = 2
    BASE_HP = 100

    # Dragons have damage reduction
    def take_damage(self, damage):
        damage = damage - 5
        if damage > 0:
            super(Dragon, self).take_damage(damage)

    def tail_swipe(self, target):
        """
        damage: strength + speed
        """
        damage = self.strength + self.speed
        target.take_damage(damage)
        return self._attack_message(target, damage, 'tail swipe')


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    STRENGTH_MULTIPLIER = 2
    INTELLIGENCE_MULTIPLIER = 1.5
    def __init__(self, *args, **kwargs):
        super(RedDragon, self).__init__(*args, **kwargs)
        self.fight_sequence = deque(['fire_breath', 'tail_swipe', 'fight'])

    def fire_breath(self, target):
        """
        damage: intelligence * 2.5
        """
        damage = int(self.intelligence * 2.5)
        target.take_damage(damage)
        return self._attack_message(target, damage, 'fire breath')


class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    STRENGTH_MULTIPLIER = 1.5
    SPEED_MULTIPLIER = 1.5
    def __init__(self, *args, **kwargs):
        super(GreenDragon, self).__init__(*args, **kwargs)
        self.fight_sequence = deque(['poison_breath', 'tail_swipe', 'fight'])
    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        damage = int((self.intelligence + self.constitution) * 1.5)
        target.take_damage(damage)
        return self._attack_message(target, damage, 'poison breath')


class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    CONSTITUTION_MULTIPLIER = 0.25
    # Undead take damage from healing
    def heal_damage(self, healing):
        self.take_damage(healing)

    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        damage = int(self.intelligence * 1.5)
        target.take_damage(damage)
        super(Undead, self).heal_damage(damage)
        message = self._attack_message(target, damage, 'drain life')
        message += '{monster} heals for {healing}!\n'.format(monster=type(self).__name__, healing=damage)
        return message


class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    INTELLIGENCE_MULTIPLIER = 2
    BASE_HP = 30
    def __init__(self, *args, **kwargs):
        super(Vampire, self).__init__(*args, **kwargs)
        self.fight_sequence = deque(['fight', 'bite', 'life_drain'])
    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        damage = int(self.speed * 0.5)
        target.take_damage(damage)
        target.maxhp -= damage
        Monster.heal_damage(self, damage)
        message = self._attack_message(target, damage, 'bite')
        message += "{target}'s maximum hp has been reduced by {damage}!\n".format(target=target, damage=damage)
        message += "{monster} heals for {healing}!\n".format(monster=type(self).__name__, healing=damage)
        return message


class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    STRENGTH_MULTIPLIER = 1.25
    SPEED_MULTIPLIER = 0.5
    INTELLIGENCE_MULTIPLIER = 0.25
    def __init__(self, *args, **kwargs):
        super(Skeleton, self).__init__(*args, **kwargs)
        self.fight_sequence = deque(['bash', 'fight', 'life_drain'])
    def bash(self, target):
        """
        damage: strength * 2
        """
        damage = self.strength * 2
        target.take_damage(damage)
        return self._attack_message(target, damage, 'bash')


class Humanoid(Monster):
    def slash(self, target):
        """
        damage: strength + speed
        """
        damage = self.strength + self.speed
        target.take_damage(damage)
        return self._attack_message(target, damage, 'slash')


class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    """
    STRENGTH_MULTIPLIER = 1.75
    CONSTITUTION_MULTIPLIER = 1.5
    BASE_HP = 20
    def __init__(self, *args, **kwargs):
        super(Troll, self).__init__(*args, **kwargs)
        self.fight_sequence = deque(['slash', 'fight', 'regenerate'])
    def regenerate(self, *args):
        """
        heals self for constitution
        """
        healing = self.constitution
        self.heal_damage(healing)
        return '{monster} regenerates {healing} health!\n'.format(monster=type(self).__name__, healing=healing)


class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    """
    STRENGTH_MULTIPLIER = 1.75
    BASE_HP = 16
    def __init__(self, *args, **kwargs):
        super(Orc, self).__init__(*args, **kwargs)
        self.fight_sequence = deque(['blood_rage', 'slash', 'fight'])
    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        damage = self.strength * 2
        health_cost = int(self.constitution / 2)
        target.take_damage(damage)
        self.take_damage(health_cost)
        message = self._attack_message(target, damage, 'blood rage')
        message += '{monster} takes {damage} self-inflicted damage!\n'.format(monster=type(self).__name__, damage=health_cost)
        return message
