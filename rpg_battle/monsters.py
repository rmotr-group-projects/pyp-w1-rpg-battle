from .exceptions import *

class Monster(object):
    
    command_queue = ['fight']
    
    def __init__(self, level=1):
        """
        Sets up stats and levels up the monster if necessary
        """
        self.attack_queue_index = 0
        self.level = 1
        
        self.strength = 8 * getattr(self, 'MODSTR', 1)
        self.intelligence = 8 * getattr(self, 'MODINT', 1)
        self.constitution = 8 * getattr(self, 'MODCON', 1)
        self.speed = 8 * getattr(self, 'MODSPD', 1)
        
        self.maxhp = getattr(self, 'BASE_HP', 10)
        self.hp = self.maxhp
        
        
        
        if level > 1:
            self.level = level
            
            self.strength = 8 * getattr(self, 'MODSTR', 1) + int((self.level - 1) * getattr(self, 'MODSTR', 1))
            self.intelligence = 8 * getattr(self, 'MODINT', 1) + int((self.level - 1) * getattr(self, 'MODINT', 1))
            self.speed = 8 * getattr(self, 'MODSPD', 1) + int((self.level - 1) * getattr(self, 'MODSPD', 1))
            self.constitution = 8 * getattr(self, 'MODCON', 1) + int((self.level - 1) * getattr(self, 'MODCON', 1))
            
            
            #Monster have a base HP of 10 (this may be overidden by monster families and subtypes, more on this later) to calculate their actual `maxhp` use the base hp + (level - 1) x (0.5x `constitution`), dropping fractions as usual
            
            self.maxhp = getattr(self, 'BASE_HP', 10) + int((self.level - 1) * (.5 * self.constitution))
            self.hp = self.maxhp
    

    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: (average of stats) + (maxhp % 10)
        """
        stats_avg = int((self.strength + self.constitution + self.speed + self.intelligence) / 4)
        return stats_avg + int(self.maxhp / 10)

    def fight(self, target):
        """
        Attacks target dealing damage equal to strength
        """
        dam = target.take_damage(self.strength)
        return dam, 'fight'


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
            

    def attack(self, target):
        """
        Attacks target using next ability in command queue
        """
        
        if self.attack_queue_index >= len(self.command_queue):
            self.attack_queue_index = 0
        attack_method = getattr(self, self.command_queue[self.attack_queue_index])
        
        dam, attack_type = attack_method(target)
        
        self.attack_queue_index += 1
        
        return "{monster} hits {target} with {ability} for {damage} damage!".format(monster = type(self).__name__, target = type(target).__name__, ability = attack_type, damage = dam)
        
        
        
        


class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    MODCON = 2
    BASE_HP = 100
    DAMAGE_REDUCTION = 5
    
    def take_damage(self, damage):
        """
        Reduce hp by damage taken.
        """
        if damage > self.DAMAGE_REDUCTION:
            self.hp -= damage - self.DAMAGE_REDUCTION
            return damage - self.DAMAGE_REDUCTION
        else:
            return 0
    

    def tail_swipe(self, target):
        """
        damage: strength + speed
        """
        dam = target.take_damage(self.strength + self.speed)
        return dam, 'tail swipe'


class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    command_queue = ['fire_breath', 'tail_swipe', 'fight']
    
    MODSTR = 2
    MODINT = 1.5
    
    name = 'RedDragon'
    
    def fire_breath(self, target):
        """
        damage: intelligence * 2.5
        """
        dam = target.take_damage(int(self.intelligence * 2.5))
        return dam, 'fire breath'
        


class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    MODSTR = 1.5
    MODSPD = 1.5
    
    
    command_queue = ['poison_breath', 'tail_swipe', 'fight']
    
    def poison_breath(self, target):
        """
        damage: (intelligence + constitution) * 1.5
        """
        dam = int((self.intelligence + self.constitution) * 1.5)
        target.take_damage(int((self.intelligence + self.constitution) * 1.5))
        return dam, 'poison breath'


class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own healing abilities
    """
    
    MODCON = 0.25
    
    def heal_damage(self, healing):
        """
        Decreases hp by healing 
        """
        self.hp -= healing
        
    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        dam = int(self.intelligence * 1.5)
        target.take_damage(dam)
        self.hp += int(self.intelligence * 1.5)
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return dam, 'life drain'
        
        


class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    MODINT = 2
    command_queue = ['fight', 'bite', 'life_drain']
    BASE_HP = 30
    
    name = 'Vampire'
    
    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        dam = int(self.speed * 0.5)
        target.take_damage(int(self.speed * 0.5))
        target.maxhp -= int(self.speed * 0.5)
        self.hp += int(self.speed * 0.5)
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return dam, 'bite'
        


class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    command_queue = ['bash', 'fight', 'life_drain']
    MODSTR = 1.25
    MODSPD = 0.5
    MODINT = 0.25
    
    name = 'Skeleton'
    
    def bash(self, target):
        """
        damage: strength * 2
        """
        dam = self.strength * 2
        target.take_damage(dam)
        return dam, 'bash'


class Humanoid(Monster):
    
    command_queue = ['slash']
    name = "Humanoid"
    
    def slash(self, target):
        """
        damage: strength + speed
        """
        dam = self.strength + self.speed
        target.take_damage(dam)
        return dam, 'slash'


class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    """
    
    MODSTR = 1.75
    MODCON = 1.5
    BASE_HP = 20
    
    command_queue = ['slash', 'fight', 'regenerate']
    
    def regenerate(self, *args):
        """
        heals self for constitution
        """
        heal_amount = self.constitution
        self.heal_damage(heal_amount)


class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    """
    MODSTR = 1.75
    BASE_HP = 16
    command_queue = ['blood_rage', 'slash', 'fight']
    
    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        dam = self.strength * 2
        
        self.hp -= int(0.5 * self.constitution)
        target.take_damage(dam)
        return dam, 'blood rage'

        