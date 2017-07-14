from .heroes import Hero
from .monsters import Monster
from .exceptions import *
from operator import attrgetter
import random

class Battle(object):
    def __init__(self, participants):
        """
        determines initiative order using unit speed
        """
        self.participants = participants
        
        self.order = sorted(participants, key=attrgetter('speed'), reverse = True)
            
            
            

    def current_attacker(self):
        """
        returns unit at front of initiative queue
        """
        return self.order[0]
        
    def heroes_in_order_index(self):
        hero_index = []
        for n in range(len(self.order)):
            if isinstance(self.order[n], Hero):
                hero_index.append(n)
        return hero_index
            
    def rotate_order(self):
        rotated = self.order[0]
        order.remove(rotated)
        order.append(rotated)

    def start(self):
        target = None
        if isinstance(self.current_attacker(), Monster):
            if self.heroes_in_order():
                target = random.choice(self.heroes_in_order())
            else:
                
                raise Defeat()
                
            self.current_attacker().attack(self.order[target])
            self.rotate_order()
        else:
            pass

    def execute_command(self, command, target):
        """
        causes current hero to execute a command on a target
        raises InvalidCommand if unit does not have that command
        raises InvalidTarget if unit is dead
        """
        pass
