from .heroes import Hero
from .monsters import Monster
from .exceptions import *
from operator import attrgetter
import random

class Battle(object):
    
    battle_report = []
    
    def __init__(self, participants):
        """
        determines initiative order using unit speed
        """
        self.participants = participants
        
        self.order = sorted(participants, key=attrgetter('speed'), reverse = True)
        
        Battle.battle_report = []  
        
    def current_attacker(self):
        """
        returns unit at front of initiative queue
        """
        return self.order[0]
        
    def heroes_in_order_index(self):
        hero_index = []
        for n in range(len(self.order)):
            if isinstance(self.order[n], Hero) and not self.order[n].is_dead():
                hero_index.append(n)
        return hero_index
        
    def monsters_in_order_index(self):
        monster_index = []
        for n in range(len(self.order)):
            if isinstance(self.order[n], Monster) and not self.order[n].is_dead():
                monster_index.append(n)
        return monster_index
            
    def rotate_order(self):
        rotated = self.order[0]
        self.order.remove(rotated)
        self.order.append(rotated)
        
    def remove_from_order(self, target):
        dead_unit = self.order.pop(target)
        return dead_unit
        
    def monster_turn(self):
        if self.heroes_in_order_index() != []:
                target = random.choice(self.heroes_in_order_index())
                self.battle_report.append(self.current_attacker().attack(self.order[target]))
        self.end_turn()
        
    def end_turn(self):
        self.rotate_order()
        self.is_anyone_dead()
        
        
    def is_anyone_dead(self):
        for unit in self.order:
            if unit.is_dead():
                self.order.remove(unit)
                report = "{unit} dies!".format(unit = type(unit).__name__)
                self.battle_report.append(report)
                if isinstance(unit, Monster):
                    report = "{amount} XP rewarded!".format(amount = unit.xp())
                    self.battle_report.append(report)
                    self.award_xp(unit.xp())
                    if not self.monsters_in_order_index():
                        raise Victory
    
    def award_xp(self, amount):
        
        recipients = self.heroes_in_order_index()
        for h in recipients:
            report = self.order[h].gain_xp(amount)
            if report:
                self.battle_report.append(report)
                
    
    def start(self):
        
        while isinstance(self.current_attacker(), Monster):
            self.monster_turn()
                
            
                
                
            if not self.monsters_in_order_index():
                raise Victory()
                
            if not self.heroes_in_order_index():
                raise Defeat()
                
            
            
        if isinstance(self.current_attacker(), Hero):
            if not self.current_attacker().is_dead:
                st = "{hero}'s turn!".format(hero = type(current_attacker()).__name__)
                self.battle_report.append(st)
            else:
                pass
                
            
            
               
        return "\n".join(self.battle_report)
            

    def execute_command(self, command, target):
        """
        causes current hero to execute a command on a target
        raises InvalidCommand if unit does not have that command
        raises InvalidTarget if unit is dead
        """
        self.battle_report = []
        
        active_hero = self.current_attacker()
        
        
        if command not in active_hero.abilities:
            raise InvalidCommand()
            
        if target.is_dead():
            raise InvalidTarget()
        
        
        report = active_hero.attack(command, target)
        
        self.battle_report.append(report)
        
       
            
        self.end_turn()
        
        return "\n".join(self.battle_report)
        
         
            
            
            
            
            
        
        
