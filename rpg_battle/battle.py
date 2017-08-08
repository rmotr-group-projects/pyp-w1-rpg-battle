from .heroes import Hero
from .monsters import Monster
from .exceptions import *
import random


class Battle(object):
    def __init__(self, participants):
        """Determines initiative order using unit speed"""
        self.participants = sorted(participants, key=lambda participant:
                                    participant.speed, reverse = True)
        self.heroes = []
        for participant in self.participants:
            if getattr(participant, 'character_type', None) == 'Hero':
                self.heroes.append(participant)
        self.place_in_queue = 0
        self.event_formatting = ''

    def start(self):
        """Starts the battle using members of self.participants"""
        while self.test_game_continues():
            attacker = self.current_attacker()
            
            if attacker.character_type == 'Monster':
                hero_to_attack = self.choose_random_hero()
                name_of_monsters_attack = attacker.attack_name()
                monster_health_before_move = attacker.hp
                hero_health_before_move = hero_to_attack.hp
                attacker.attack(hero_to_attack)
                monster_health_after_move = attacker.hp
                hero_health_after_move = hero_to_attack.hp
                hero_lost_health = (hero_health_before_move - 
                                            hero_health_after_move)
                self.document_attack(attacker, hero_to_attack, 
                                    hero_lost_health, name_of_monsters_attack)
                self.document_monster_hurts_itself(attacker, 
                        monster_health_before_move, monster_health_after_move)
                self.test_death(attacker, hero_to_attack)
                self.test_game_over()
                
            elif attacker.character_type == 'Hero':
                self.event_formatting += "{hero}'s turn!".format(
                                                    hero=attacker.__repr__())
                return self.event_formatting
                
    def execute_command(self, command, target):
        """
        Causes current hero to execute a command on a target.
        Raises InvalidCommand if unit does not have that command.
        Raises InvalidTarget if unit is dead.
        """
        self.event_formatting = ''
        command_string = self.convert_command_to_string(command)
        if command not in self.attackers_turn.abilities:
            raise InvalidCommand
        if target.hp <= 0:
            raise InvalidTarget
        monster_HP_initial = target.hp
        self.attackers_turn.abilities[command](target)
        monster_HP_final = target.hp
        monster_lost_HP = monster_HP_initial - monster_HP_final
        self.document_attack(self.attackers_turn, target, monster_lost_HP,
                                                            command_string)
        self.test_death(target, self.attackers_turn)
        self.test_game_over()
        self.start()
        return self.event_formatting
        
    def test_death(self, monster, hero):
        '''
        Tests if hero and/or monster have died and adds the appropriate
        event formatting. 
        Also gives out xp and levels heros if necessary.
        '''
        if hero.is_dead() and monster.is_dead():
            self.event_formatting += '{} dies!\n{} dies!\n'.format(
                                        monster.__repr__(), hero.__repr__())
            self.heroes.remove(hero)
            self.participants.remove(hero)
            self.participants.remove(monster)
            
        elif monster.is_dead():
            self.event_formatting += '{} dies!\n'.format(monster.__repr__())
            xp_given = monster.xp()
            self.event_formatting += '{xp} XP rewarded!\n'.format(xp=xp_given)
            for good_guy in self.heroes:
                hero_level_before_xp = good_guy.level
                good_guy.gain_xp(xp_given)
                hero_level_after_xp = good_guy.level
                if hero_level_after_xp > hero_level_before_xp:
                    self.event_formatting += \
                        '{hero} is now level {level}!\n'.format(
                        hero=good_guy.__repr__(), level=good_guy.level)
            self.participants.remove(monster)
            
        elif hero.is_dead():
            self.event_formatting += '{} dies!\n'.format(hero.__repr__())
            self.heroes.remove(hero)
            self.participants.remove(hero)
            
    def current_attacker(self):
        """Returns unit at front of initiative queue"""
        if self.place_in_queue >= len(self.participants): 
            self.place_in_queue = 0
        self.attackers_turn = self.participants[self.place_in_queue]
        self.place_in_queue += 1
        return self.attackers_turn

    def choose_random_hero(self):
        """Chooses a hero at random"""
        return random.choice(self.heroes)
        
    def is_hero_alive(self):
        """Returns True if >= 1 Hero is alive, False otherwise"""
        self.hero_alive = False
        for participant in self.participants:
            if participant.character_type == 'Hero':
                self.hero_alive = True
        return self.hero_alive
                
    def is_monster_alive(self):
        """Returns True if >= 1 Monster is alive, False otherwise"""
        self.monster_alive = False
        for participant in self.participants:
            if participant.character_type == 'Monster':
                self.monster_alive = True
        return self.monster_alive
    
    def document_attack(self, attacker, defender, damage, name_of_attack):
        """Documents attack in event_formatting"""
        if name_of_attack == 'fight':
            self.event_formatting += \
            '{attacker} attacks {defender} for {damage}!\n'.format(
                attacker=attacker.__repr__(), defender=defender.__repr__(), 
                                                        damage=damage)
                                                        
        elif name_of_attack != 'fight':
            self.event_formatting += \
            '{attacker} hits {defender} with {ability} for {damage} damage!\n'\
            .format(attacker=attacker.__repr__(), defender=defender.__repr__(), 
                                        ability=name_of_attack, damage=damage)
                                    
    def document_monster_hurts_itself(self, monster, HP_before, HP_after):
        """
        Checks if monster's attack did damage to itself and logs
        any damage done in event_formatting.
        """
        if HP_after < HP_before:
            HP_lost = HP_before - HP_after
            self.event_formatting += '{monster} takes {damage} \
            self-inflicted damage!\n'.format(monster=monster.__repr__(), 
                                                            damage=HP_lost)
                                                            
    def test_game_continues(self):
        """
        Returns True if at least one hero and one monster are alive.
        Checks if game is over if there are no heros or no monsters."""
        if self.is_hero_alive() and self.is_monster_alive():
            return True
        self.test_game_over()
    
    def test_game_over(self):
        """Convenient way to check for victory or defeat."""
        self.test_victory()
        self.test_defeat()
                
    def test_victory(self):
        """
        Raises Victory exception if at least one hero is alive and
        no monsters are alive.
        """
        if self.is_hero_alive():
            if not self.is_monster_alive():
                raise Victory
                
    def test_defeat(self):
        """
        Raises Defeat exception if at least one monster is alive and
        no heros are alive.
        """
        if not self.is_hero_alive():
            if self.is_monster_alive():
                raise Defeat
                
    def convert_command_to_string(self, command):
        """Replaces '_' with a space for event_formatting."""
        move_string = ''
        for char in command:
            if char == '_':
                move_string += ' '
            else:
                move_string += char
        return move_string
