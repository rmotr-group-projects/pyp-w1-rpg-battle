from .heroes import Hero
from .monsters import Monster
from .exceptions import *

import random
from collections import deque

class Battle(object):
    def __init__(self, participants):
        """
        determines initiative order using unit speed
        """
        self.participants = participants
        self.initiative_order = deque(sorted(participants, key=lambda x: x.speed))

    def current_attacker(self):
        """
        returns unit at front of initiative queue
        """
        return self.initiative_order[-1]

    def start(self):
        return self.next_turn()

    def next_turn(self):
        message = ''
        while isinstance(self.current_attacker(), Monster):
            message += self._monster_turn()
        
        message +=self._player_turn()

        return message

    def _monster_turn(self):
        monster = self.current_attacker()
        target = random.choice([unit for unit in self.participants if isinstance(unit, Hero) and not unit.is_dead()])
        message = monster.attack(target)
        self._process_initiative()
        message += self._process_dead()
        return message

    def _player_turn(self):
        return "{}'s turn!\n".format(type(self.current_attacker()).__name__)

    def _process_initiative(self):
        self.initiative_order.appendleft(self.initiative_order.pop())

    def _process_dead(self):
        message = ''
        corpses = [unit for unit in self.initiative_order if unit.is_dead()]
        for body in corpses:
            message += '{} dies!\n'.format(type(body).__name__)
            if isinstance(body, Monster):
                message += self._reward_xp(body.xp())
        self.initiative_order = deque([unit for unit in self.initiative_order if not unit.is_dead()])
        if len([unit for unit in self.initiative_order if isinstance(unit, Hero)]) == 0:
            raise Defeat
        if len([unit for unit in self.initiative_order if isinstance(unit, Monster)]) == 0:
            raise Victory
        return message

    def _reward_xp(self, xp):
        message = '{xp} XP rewarded!\n'.format(xp=xp)
        for hero in [unit for unit in self.initiative_order if isinstance(unit, Hero) and not unit.is_dead()]:
            before_level = hero.level
            hero.gain_xp(xp)
            if hero.level > before_level:
                message += '{hero} is now level {level}!\n'.format(hero=type(hero).__name__,
                                                                   level=hero.level)
        return message

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
        message = getattr(self.current_attacker(), command)(target)
        self._process_initiative()
        message += self._process_dead()
        message += self.next_turn()
        return message
