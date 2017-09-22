from .heroes import Hero
from .monsters import Monster
from .exceptions import *
from collections import deque
import random


class Battle(object):
    def __init__(self, participants):
        """
        determines initiative order using unit speed
        """
        self.participants = participants
        self.initiative = deque(sorted(participants, key = lambda x: x.speed, reverse = True))

    def current_attacker(self):
        """
        returns unit at front of initiative queue
        """
        return self.initiative[0]

    def is_hero_turn(self):
        """
        returns True if current_attacker is a Hero
        """
        return isinstance(self.current_attacker(), Hero)

    def is_monster_turn(self):
        """
        returns True if current_attacker is a Monster
        """
        return isinstance(self.current_attacker(), Monster)

    def next_turn(self):
        """
        Processes next unit's turn
        """
        self.raise_for_battle_over()
        
        messages = []
        if self.is_monster_turn():
            messages.extend(self._monster_turn())
        else:
            messages.extend(self._hero_turn())
        
        return messages    

    def _monster_turn(self):
        """
        Handles monster turn
        """
        messages = []
        monster = self.current_attacker()
        target = random.choice([unit for unit in self.initiative 
                    if isinstance(unit, Hero) and not unit.is_dead()])
                    
        messages.extend(monster.attack(target))      
        self._process_initiative()
        
        messages.extend(self._process_dead())
        return messages
        
    def raise_for_battle_over(self):
        """
        Raises Victory if all monsters defeated
        Raises Defeat if all party members defeated
        """
        if self._check_victory():
            raise Victory
        elif self._check_defeat():
            raise Defeat

    def _hero_turn(self):
        """
        Notifies of player turn
        """
        return "{}'s turn!".format(type(self.current_attacker()).__name__)

    def _process_initiative(self):
        """
        Handles adjusting initiative order at end of unit's turn
        """
        self.initiative.appendleft(self.initiative.pop())

    def _check_victory(self):
        """
        Returns True if all monsters defeated
        """
        victoryListLen = len([unit for unit in self.initiative if isinstance(unit, Monster)])
        if victoryListLen == 0:
            return True
        else:
            return False   

    def _check_defeat(self):
        """
        Returns True if all party members defeated
        """
        defeatListLen = len([unit for unit in self.initiative if (isinstance(unit, Hero))])
        if defeatListLen == 0:
            return True
        else:
            return False
            
    def _process_dead(self):
        """
        Handles removal of dead units from initiative queue and triggers xp rewards
        """
        messages = []
        
        corpses = [unit for unit in self.initiative if unit.is_dead()]
        
        for corp in corpses:
            messages.append('{} dies!'.format(type(corp).__name__))
            
            if isinstance(corp, Monster):
                messages.extend(self._reward_xp(corp.xp()))
                
        self.initiative = deque([unit for unit in self.initiative if not unit.is_dead()])
        
        if self._check_defeat():
            messages.append('The party was defeated.')
        
        if self._check_victory():
            messages.append('The party was victorious!')
        
        return messages
        

    def _reward_xp(self, xp):
        """
        Rewards xp to all living party members
        """
        messages = ['{xp} XP rewarded!'.format(xp=xp)]
        heroesList = [unit for unit in self.initiative if isinstance(unit, Hero) 
                            and (not unit.is_dead())] 
        for hero in heroesList:
            before_level = hero.level
            hero.gain_xp(xp)
            
            if hero.level > before_level:
                messages.append('{hero} is now level {level}!'.format(hero=type(hero).__name__,
                                                                 level=hero.level))
        return messages


    def execute_command(self, command, target):
        """
        causes current hero to execute a command on a target
        raises InvalidCommand if unit does not have that command
        raises InvalidTarget if unit is dead
        """
        if not hasattr(self.current_attacker(), command):
            raise InvalidCommand()
        
        if target.is_dead():
            raise InvalidTarget()
        
        log = getattr(self.current_attacker(), command)(target)
        self._process_initiative()
        log.extend(self._process_dead())
        
        return log




