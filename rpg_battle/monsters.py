from collections import deque

from .exceptions import *

class Monster(object):
    BASE_STATS = {'strength': 8,
             'constitution': 8,
             'intelligence': 8,
             'speed': 12}
    BASE_HP = 10
    XP_MULTIPLIER = 1

    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        for stat, statValue in self.BASE_STATS.iteritems():
            if hasattr(self, 'MULTIPLIERS'):
                multiplier = self.MULTIPLIERS.get(stat, 1)
            else:
                multiplier = 1
            setattr(self, stat, int((statValue * multiplier) + multiplier* (level - 1)))
            
        self.maxhp = self.BASE_HP + int(0.5 * self.constitution * (level - 1))
        self.hp = self.maxhp
        
        self.level = level
        
    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: ((average of stats) + (maxhp / 10)) * xp multiplier
        """
        return int(((sum([getattr(self, stat) for stat in self.BASE_STATS]) / 4) + (self.maxhp / 10)) * self.XP_MULTIPLIER)

    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        damage = self.strength
        target.take_damage(damage)
        return self._combat_message(target,'fight', damage)

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

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        attackVal = self.command_queue.popleft()
        ability = getattr(self, attackVal)
        log = ability(target)
        self.command_queue.append(attackVal)
        
        return log
        
        
    def _combat_message(self, target, ability, damage):
        
        if ability == 'fight':
            return ["{monster} attacks {target} for {damage}!".format(
                monster = self.__class__.__name__,
                target = target.__class__.__name__,
                damage = damage)]
                
        return ["{monster} hits {target} with {ability} for {damage}!".format(
            monster = self.__class__.__name__,
            target = target.__class__.__name__,
            ability = ability,
            damage = damage)]


class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    MULTIPLIERS = {'constitution': 2}
    BASE_HP = 100
    XP_MULTIPLIER = 2

    def tail_swipe(self, target):
        """
        damage: 1.5*(strength + speed)
        """
        damage = int(1.5* (self.strength + self.speed))
        target.take_damage(damage)
        return self._combat_message(target,'tail swipe', damage)

    
    def take_damage(self, damage):
        damage -= 5
        if damage > 0:
            super(Dragon, self).take_damage(damage)

class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    MULTIPLIERS = Dragon.MULTIPLIERS.copy()
    MULTIPLIERS.update({'strength': 2,
                        'intelligence': 1.5})
    
    def __init__(self, *args, **kwargs):
        super(RedDragon, self).__init__(*args, **kwargs)
        self.command_queue = deque(['fire breath', 'tail swipe', 'fight'])
    
    def fire_breath(self, target):
        """
        damage: intelligence * 3
        """
        damage = self.intelligence * 3
        target.take_damage(damage)
        return self._combat_message(target,'fire breath', damage)



class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    MULTIPLIERS = Dragon.MULTIPLIERS.copy()
    MULTIPLIERS.update({'strength': 1.5,
                        'speed': 1.5})
    
    
    def __init__(self, *args, **kwargs):
        super(GreenDragon, self).__init__(*args, **kwargs)
        self.command_queue = deque(['poison breath', 'tail swipe',  'fight'])
        
    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        damage = int(1.5 * (self.intelligence + self.constitution))
        target.take_damage(damage)
        return self._combat_message(target,'poison breath', damage)




class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    MULTIPLIERS = {'constitution': 0.25}


    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        damage = int(1.5*self.intelligence)
        target.take_damage(damage)
        super(Undead, self).heal_damage(damage)
        message = self._combat_message(target, damage, 'drain life')
        message.append('{monster} heals for {healing}!'.format(monster=type(self).__name__,
                                                               healing=damage))
        return message
        
    def heal_damage(self, healing):
        self.take_damage(healing)

class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    MULTIPLIERS = Undead.MULTIPLIERS.copy()
    MULTIPLIERS.update({'intelligence': 2})
    BASE_HP = 45

    
    def __init__(self, *args, **kwargs):
        super(Vampire, self).__init__(*args, **kwargs)
        self.command_queue = deque([ 'fight', 'bite', 'life drain'])
        
        
    def bite(self, target):
        """
        damage: speed * 2
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        damage = 2 * self.speed
        target.take_damage(damage)
        target.maxhp -= damage
        
        Monster.heal_damage(self, damage)
        message = self._combat_message(target, damage, 'bite')
        message.append("{target}'s maximum hp has been reduced by {damage}!".format(target=target.__class__.__name__,
                                                                                    damage=damage))
        message.append("{monster} heals for {healing}!".format(monster=type(self).__name__,
                                                               healing=damage))
        return message

class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    MULTIPLIERS = Undead.MULTIPLIERS.copy()
    MULTIPLIERS.update({'strength': 1.25,
                        'speed': 0.5,
                        'intelligence': 0.25})
    BASE_HP = 30

    def __init__(self, *args, **kwargs):
        super(Skeleton, self).__init__(*args, **kwargs)
        self.command_queue = deque(['bash', 'fight', 'life drain'])
     
    def bash(self, target):
        """
        damage: strength * 2
        """
        damage = 2 * self.strength
        target.take_damage(damage)
        return self._combat_message(target,'bash', damage)


        

class Humanoid(Monster):
    def slash(self, target):
        """
        damage: strength + speed
        """
        damage = self.strength + self.speed
        target.take_damage(damage)
        return self._combat_message(target,'slash', damage)



class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    command queue: slash, fight, regenerate
    """
    MULTIPLIERS = {'strength': 1.75,
                   'constitution': 1.5}
    BASE_HP = 20

    def __init__(self, *args, **kwargs):
        super(Troll, self).__init__(*args, **kwargs)
        self.command_queue = deque([ 'slash', 'fight', 'regenerate'])
     
    def regenerate(self, *args):
        """
        heals self for constitution
        """
        healing = self.constitution
        self.heal_damage(healing)
        return ['{monster} regenerates {healing} health!'.format(monster=type(self).__name__,
                                                                   healing=healing)]


class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    command queue: blood_rage, slash, fight
    """
    MULTIPLIERS = {'strength': 1.75}
    BASE_HP = 16
    XP_MULTIPLIER = 0.5

    
    def __init__(self, *args, **kwargs):
        super(Orc, self).__init__(*args, **kwargs)
        self.command_queue = deque(['blood rage', 'slash', 'fight'])
        
        
    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        damage = 2 * self.strength
        target.take_damage(damage)
        
        cost = int(0.5*self.constitution)
        self.take_damage(cost)
        message = self._combat_message(target,'blood rage', damage)
        message.append('{monster} takes {damage} self-inflicted damage!'.format(monster=type(self).__name__,
                                                                                damage=cost))
        return message

        