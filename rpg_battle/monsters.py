from .exceptions import *

class Monster(object):
    
    def __init__(self, level=1):
        """Sets up stats and levels up the monster if necessary."""
        self.get_stats(level)
        self.commandqueue = [('attack', self.attack)]
        
    def xp(self):
        """
        Returns the xp value of monster if defeated.
        XP value formula: (average of stats) + (maxhp % 10)
        """
        return int(((self.strength + self.constitution + self.intelligence
                                    + self.speed) / 4) + (self.maxhp % 10))

    def fight(self, target):
        """Attacks target dealing damage equal to strength"""
        target.take_damage(self.strength)

    def take_damage(self, damage):
        """Reduce hp by damage taken."""
        self.hp -= int(damage)

    def heal_damage(self, healing):
        """Increase hp by healing but not exceeding maxhp"""
        self.hp += healing
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def is_dead(self):
        """Returns True if out of hp"""
        if self.hp <= 0:
            return True

    def attack(self, target):
        """Attacks target using next ability in command queue"""
        self.commandqueue[self.current_attack][1](target)
        self.current_attack += 1
        if self.current_attack >= len(self.commandqueue):
            self.current_attack = 0
            
    def attack_name(self):
        """Returns monster's attack's name for event_formatting."""
        moves_string = [name for name, func in self.commandqueue]
        name_of_move = moves_string[self.current_attack]
        return name_of_move
    
    def get_stats(self, level, strength = 1, intelligence = 1, 
                                constitution = 1, speed = 1, basehp = 10):
        """Sets up all the monster's __init__ variables"""
                                                
        def calculate_stat(level, multiplier):
            return int(8 * multiplier + (level - 1) * multiplier)
            
        def calculate_HP(level, constitution, basehp):
            return int(basehp + (level - 1) * (0.5 * constitution))
            
        self.level = level
        self.strength = calculate_stat(self.level, strength)
        self.intelligence = calculate_stat(self.level, intelligence)
        self.constitution = calculate_stat(self.level, constitution)
        self.speed = calculate_stat(self.level, speed)
        self.basehp = basehp
        self.maxhp = calculate_HP(self.level, self.constitution, self.basehp)
        self.hp = self.maxhp
        self.current_attack = 0
        self.character_type = 'Monster'
        
    def __repr__(self):
        return 'Monster'
        

class Dragon(Monster):
    """
    base hp: 100
    constitution multiplier: 2
    special feature: Reduce all damage taken by 5
    """
    def __init__(self, level=1):
        """Sets up stats and levels up the monster if necessary"""
        self.get_stats(level, constitution = 2, basehp = 100)
        self.commandqueue = [('tail swipe', self.tail_swipe),
                            ('fight', self.fight)]
        
    def take_damage(self, damage):
        """Reduce hp by damage taken."""
        if damage > 5:
            self.hp -= (damage - 5)
        
    def tail_swipe(self, target):
        """damage: strength + speed"""
        target.take_damage(self.strength + self.speed)
        
    def __repr__(self):
        return 'Dragon'

class RedDragon(Dragon):
    """
    strength multiplier: 2
    intelligence multiplier: 1.5
    command queue: fire_breath, tail_swipe, fight
    """
    def __init__(self, level=1):
        """Sets up stats and levels up the monster if necessary"""
        self.get_stats(level, strength = 2, intelligence = 1.5, 
                                            constitution = 2, basehp = 100)
                                            
        self.commandqueue = [('fire breath', self.fire_breath),
                            ('tail swipe', self.tail_swipe),
                            ('fight', self.fight)]
        
    def fire_breath(self, target):
        """damage: intelligence * 2.5"""
        target.take_damage(int(self.intelligence * 2.5))
        
    def __repr__(self):
        return 'RedDragon'

class GreenDragon(Dragon):
    """
    strength multiplier: 1.5
    speed multiplier: 1.5
    command queue: poison_breath, tail_swipe, fight
    """
    def __init__(self, level = 1):
        self.get_stats(level, strength = 1.5, constitution = 2, 
                                            speed = 1.5, basehp = 100)
  
        self.commandqueue = [('poison breath', self.poison_breath),
                            ('tail swipe', self.tail_swipe),
                            ('fight', self.fight)]
        
    def poison_breath(self, target):
        """damage: (intelligence + constitution) * 1.5"""
        target.take_damage((self.intelligence + self.constitution) * 1.5)
        
    def __repr__(self):
        return 'GreenDragon'

class Undead(Monster):
    """
    constitution multiplier: 0.25
    special feature: undead take damage from healing except their own
    healing abilities.
    """
    def __init__(self, level = 1):
        self.get_stats(level, constitution = .25)
        self.commandqueue = [('life drain', self.life_drain),
                            ('fight', self.fight)]
        
    def heal_damage(self, healing):
        self.take_damage(healing)
        
    def life_drain(self, target):
        """
        damage: intelligence * 1.5
        heals unit for damage done
        """
        initial_target_hp = target.hp
        target.take_damage(self.intelligence * 1.5)
        final_target_hp = target.hp
        if final_target_hp < 0:
            amount_to_heal = initial_target_hp
        else:
            amount_to_heal = initial_target_hp - final_target_hp
        self.undead_heal(amount_to_heal)

    def undead_heal(self, amount_to_heal):
        Monster.heal_damage(self, amount_to_heal)
            
    def __repr__(self):
        return 'Undead'
    
class Vampire(Undead):
    """
    base hp: 30
    intelligence multiplier: 2
    command queue: fight, bite, life_drain
    """
    def __init__(self, level = 1):
        self.get_stats(level, intelligence = 2, constitution = .25,
                                                            basehp = 30)
        self.commandqueue = [('bite', self.bite),
                            ('life drain', self.life_drain),
                            ('fight', self.fight)]
        
    def bite(self, target):
        """
        damage: speed * 0.5
        also reduces target's maxhp by amount equal to damage done
        heals unit for damage done
        """
        initial_target_hp = target.hp
        target.take_damage(self.speed * .5)
        final_target_hp = target.hp
        if final_target_hp < 0:
            damage_done = initial_target_hp
        else:
            damage_done = initial_target_hp - final_target_hp
        target.maxhp -= damage_done
        self.undead_heal(damage_done)

    def __repr__(self):
        return 'Vampire'
        
class Skeleton(Undead):
    """
    strength multiplier: 1.25
    speed multiplier: 0.5
    intelligence multiplier: 0.25
    command queue: bash, fight, life_drain
    """
    def __init__(self, level = 1):
        self.get_stats(level, strength = 1.25, intelligence = .25, 
                                        constitution = .25, speed = .5)
                                        
        self.commandqueue = [('bash', self.bash),
                            ('life drain', self.life_drain),
                            ('fight', self.fight)]
        
    def bash(self, target):
        """damage: strength * 2"""
        target.take_damage(self.strength * 2)
        
    def __repr__(self):
        return 'Skeleton'

class Humanoid(Monster):
    def __init__(self, level = 1):
        self.get_stats(level)
        self.commandqueue = [('slash', self.slash),
                            ('fight', self.fight)]
        
    def slash(self, target):
        """damage: strength + speed"""
        target.take_damage(self.strength + self.speed)
        
    def __repr__(self):
        return 'Humanoid'

class Troll(Humanoid):
    """
    strength multiplier: 1.75
    constitution multiplier: 1.5
    base hp: 20
    """
    def __init__(self, level = 1):
        self.get_stats(level, strength = 1.75, constitution = 1.5, basehp = 20)
        self.commandqueue = [('slash', self.slash),
                            ('fight', self.fight),
                            ('regenerate', self.regenerate)]
        
    def regenerate(self, *args):
        """heals self for constitution"""
        self.hp += self.constitution
        
    def __repr__(self):
        return 'Troll'

class Orc(Humanoid):
    """
    strength multiplier: 1.75
    base hp: 16
    """
    def __init__(self, level = 1):
        self.get_stats(level, strength = 1.75, basehp = 16)
        self.commandqueue = [('blood rage', self.blood_rage),
                            ('slash', self.slash),
                            ('fight', self.fight)]
        
    def blood_rage(self, target):
        """
        cost: constitution * 0.5 hp
        damage: strength * 2
        """
        self.take_damage(self.constitution * .5)
        target.take_damage(self.strength * 2)
        
    def __repr__(self):
        return 'Orc'