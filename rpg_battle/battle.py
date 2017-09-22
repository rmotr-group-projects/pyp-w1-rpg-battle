from .heroes import Hero
from .monsters import Monster
from .exceptions import *


class Battle(object):
    def __init__(self, participants):
        """
        determines initiative order using unit speed
        """
        self.participants = participants
        self.initiative = sorted(participants, key=lambda x: x.speed)


    def current_attacker(self):
        """
        returns unit at front of initiative queue
        """
        return self.initiative[-1]

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
        pass

    def _monster_turn(self):
        """
        Handles monster turn
        """
        pass

    def raise_for_battle_over(self):
        """
        Raises Victory if all monsters defeated
        Raises Defeat if all party members defeated
        """
        if self._check_victory():
            raise Victory
        if self._check_defeat():
            raise Defeat

    def _hero_turn(self):
        """
        Notifies of player turn
        """
        pass

    def _process_initiative(self):
        """
        Handles adjusting initiative order at end of unit's turn
        """

    def _check_victory(self):
        """
        Returns True if all monsters defeated
        """
        pass

    def _check_defeat(self):
        """
        Returns True if all party members defeated
        """
        pass

    def _process_dead(self):
        """
        Handles removal of dead units from initiative queue and triggers xp rewards
        """
        pass

    def _reward_xp(self, xp):
        """
        Rewards xp to all living party members
        """
        pass


    def execute_command(self, command, target):
        """
        causes current hero to execute a command on a target
        raises InvalidCommand if unit does not have that command
        raises InvalidTarget if unit is dead
        """
        pass




