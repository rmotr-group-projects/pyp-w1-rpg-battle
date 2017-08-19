import random
from collections import deque

from .heroes import Hero
from .monsters import Monster
from .exceptions import *


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

    def is_hero_turn(self):
        return isinstance(self.current_attacker(), Hero)

    def is_monster_turn(self):
        return isinstance(self.current_attacker(), Monster)

    def next_turn(self):
        self.raise_for_battle_over()
        battle_log = []
        if self.is_monster_turn():
            battle_log.extend(self._monster_turn())
        else:
            battle_log.append(self._hero_turn())

        return battle_log

    def _monster_turn(self):
        log = []
        monster = self.current_attacker()
        target = random.choice([unit for unit in self.participants if isinstance(unit, Hero) and not unit.is_dead()])
        log.extend(monster.attack(target))
        self._process_initiative()
        log.extend(self._process_dead())
        return log

    def raise_for_battle_over(self):
        if self._check_victory():
            raise Victory
        if self._check_defeat():
            raise Defeat

    def _hero_turn(self):
        return "{}'s turn!".format(type(self.current_attacker()).__name__)

    def _process_initiative(self):
        self.initiative_order.appendleft(self.initiative_order.pop())

    def _check_victory(self):
        return len([unit for unit in self.initiative_order if isinstance(unit, Monster)]) == 0

    def _check_defeat(self):
        return len([unit for unit in self.initiative_order if isinstance(unit, Hero)]) == 0

    def _process_dead(self):
        log = []
        corpses = [unit for unit in self.initiative_order if unit.is_dead()]
        for body in corpses:
            log.append('{} dies!'.format(type(body).__name__))
            if isinstance(body, Monster):
                log.extend(self._reward_xp(body.xp()))
        self.initiative_order = deque([unit for unit in self.initiative_order if not unit.is_dead()])
        if self._check_defeat():
            log.append('The party was defeated.')
        if self._check_victory():
            log.append('The party was victorious!')
        return log

    def _reward_xp(self, xp):
        log = ['{xp} XP rewarded!'.format(xp=xp)]
        for hero in [unit for unit in self.initiative_order if isinstance(unit, Hero) and not unit.is_dead()]:
            before_level = hero.level
            hero.gain_xp(xp)
            if hero.level > before_level:
                log.append('{hero} is now level {level}!'.format(hero=type(hero).__name__,
                                                                 level=hero.level))
        return log


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




