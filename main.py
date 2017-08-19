from rpg_battle import battle
from rpg_battle.heroes import *
from rpg_battle.monsters import *

from six.moves import input

from collections import deque

import random
import curses
import time

MAX_PARTY_SIZE = 4

CLASSES = {ord('1'): Warrior,
           ord('2'): Mage,
           ord('3'): Cleric,
           ord('4'): Rogue}



class PlayerWindow(object):
    _all = []

    def __init__(self, hero, x, y, height=7, width=13):
        self.window = curses.newwin(height, width, y, x)
        self.hero = hero
        self.redraw()
        self.__class__._all.append(self)

    def get_dimensions(self):
        y, x = self.window.getbegyx()
        height, width = self.window.getmaxyx()
        return x, y, height, width

    def redraw(self):
        self.window.clear()
        self.window.border(0)
        self.window.addstr(1, 1, self.hero.__class__.__name__)
        _, _, _, width = self.get_dimensions()
        self.window.addstr(1, width - 4, 'L{:02d}'.format(self.hero.level))
        if self.hero.hp > 0:
            self.window.addstr(2, 1, 'HP:')
            self.window.addstr(3, 2, '{hp}/{maxhp}'.format(hp=self.hero.hp,
                                                      maxhp=self.hero.maxhp))
            self.window.addstr(4, 1, 'MP:')
            self.window.addstr(5, 2, '{mp}/{maxmp}'.format(mp=self.hero.mp,
                                                      maxmp=self.hero.maxmp))
        else:
            self.window.addstr(2, 1, 'DEAD')
        self.window.refresh()
    
    def show_target(self, target):
        self.redraw()
        self.window.addstr(0, 0, target)
        self.window.refresh()

    @classmethod
    def show_targets(cls):
        targets = ('a)', 'b)', 'c)', 'd)')
        for idx, win in enumerate(cls._all):
            win.show_target(targets[idx])

    @classmethod
    def clear(cls):
        cls._all = []


class AbilityWindow(object):
    def __init__(self, x=35, y=1, height=7, width=20):
        self.width = width
        self.window = curses.newwin(height, width, y, x)

    def show_abilities(self, character_window):
        x, y, height, width = character_window.get_dimensions()
        x -= self.width
        self.window.clear()
        self.window.refresh()
        self.window.mvwin(y, x)
        self.window.border(0)
        self.window.addstr(0, 2, 'Choose Ability')
        for idx, ability in enumerate(character_window.hero.abilities):
            name = ability.replace('_', ' ').title()
            self.window.addstr(idx + 1, 1, '{num}) {name}'.format(num=idx + 1,
                                                                  name=name))
        self.window.refresh()

    def hide(self):
        self.window.clear()
        self.window.refresh()

class CombatLogWindow(object):
    def __init__(self, align_to):
        self.height = 12
        self.width = curses.COLS - 33
        self.x = 0
        a_x, a_y, a_height, a_width = align_to.get_dimensions()
        self.y = (a_y + a_height) - self.height
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        self.window.clear()
        self.window.border(0)
        self.window.refresh()
        self.log = deque()

    def add_message(self, message):
        messages = []
        while len(message) > self.width - 2:
            messages.append(message[:self.width - 2])
            message = message[self.width - 2:]
        messages.append(message)
        for msg in messages:
            if len(self.log) > self.height - 3:
                self.log.popleft()
            self.log.append(msg)
            self.redraw()
            time.sleep(0.35)

    def redraw(self):
        self.window.clear()
        self.window.border(0)
        self.window.addstr(0, 2, 'Combat Log')
        for idx, msg in enumerate(reversed(self.log)):
            self.window.addstr(self.height - (idx + 2), 1, msg)
        self.window.refresh()



class MonsterWindow(object):
    def __init__(self, monsters):
        win_height = len(monsters) * 3
        win_width = 32
        win_y = 1
        win_x = 1
        self.window = curses.newwin(win_height, win_width, win_y, win_x)
        self.monsters = monsters
        self.redraw()

    def redraw(self):
        self.window.clear()
        y_pos = 0
        x_pos = 0
        hp_bar_char = '*'
        hp_bar_char_lost = '-'
        for monster in self.monsters:
            self.window.addstr(y_pos, x_pos,"{name} (Lv. {level})".format(name=monster.__class__.__name__,
                                                                          level=monster.level))
            y_pos += 1
            if monster.hp > 0:
                bar_full = int(((monster.hp / monster.maxhp) * 100) / 4)
                bar_empty = 25 - bar_full
                hp_bar = 'HP: [{}{}]'.format(hp_bar_char * bar_full,
                                         hp_bar_char_lost * bar_empty)
                self.window.addstr(y_pos, x_pos, hp_bar)
            else:
                self.window.addstr(y_pos, x_pos, 'DEAD')
            y_pos += 1
        self.window.refresh()

    def show_targets(self):
        y_pos = 0
        x_pos = 0
        for idx, monster in enumerate(self.monsters):
            self.window.addstr(y_pos, x_pos, '{num}) {name} (Lv. {level})'.format(num=idx + 1,
                                                                                  name=monster.__class__.__name__,
                                                                                  level=monster.level))
            y_pos += 2
        self.window.refresh()

class BattleCursesClient(object):
    def __init__(self):
        self.victory_count = 0

    def run(self, main_window):
        self.victory_count = 0
        self.main_window = main_window
        curses.curs_set(0)
        self.main_window.clear()
        self.main_window.refresh()
        self.create_party()
        self.main_window.refresh()
        self.ability_window = AbilityWindow()
        self.combat_log = CombatLogWindow(align_to=self.party_windows[-1])
        self.new_battle()

        

    def new_battle(self):
        self.main_window.clear()
        self.main_window.refresh()
        for win in self.party_windows:
            win.redraw()
        try:
            self.generate_battle()
            self.run_battle()
        except Victory:
            self.victory_count += 1
            self.victory_window()
        except Defeat:
            self.defeat_window()

    def run_battle(self):
        while True:
            while self.battle.is_monster_turn():
                self.process_turn(self.battle.next_turn())
            else:
                self.process_turn(self.battle.next_turn())

            self.process_turn(self.player_turn())

    def victory_window(self):
        title = 'Victory!'
        message = "Do you wish to continue fighting? [Y/N]"
        if self._dialog_window(title, message):
            self.new_battle()

    def defeat_window(self):
        title = 'Defeat!'
        message = 'Would you like to try again? [Y/N]'
        if self._dialog_window(title, message):
            self.run(self.main_window)




    def _dialog_window(self, title, message):
        height = 4
        width = len(message) + 4
        y = int((self.combat_log.y + self.combat_log.height - height) / 2)
        x = int((curses.COLS - width) / 2)
        dialog = curses.newwin(height, width, y, x)
        dialog.clear()
        dialog.border()
        dialog.addstr(0, int((width - len(title)) / 2), title)
        dialog.addstr(1, int((width - len(message)) / 2), message)
        dialog.refresh()
        valid_response = (ord('y'), ord('Y'), ord('n'), ord('N'))
        response = None
        while response not in valid_response:
            response = dialog.getch()
        dialog.clear()
        dialog.refresh()
        dialog = None
        if response in (ord('y'), ord('Y')):
            return True


    def redraw(self):
        for win in self.party_windows:
            win.redraw()
        self.monster_window.redraw()

    def create_party(self):
        PlayerWindow.clear()
        self.party = []
        self.party_windows = []
        win_x = curses.COLS - 13
        win_y = 0
        party_win = curses.newwin(7, 34, 1, 1)
        while len(self.party) < MAX_PARTY_SIZE:
            party_win.clear()
            party_win.border(0)
            party_win.addstr(1, 1, 'Creating new hero, select class:')
            party_win.addstr(2, 2, '1) Warrior')
            party_win.addstr(3, 2, '2) Mage')
            party_win.addstr(4, 2, '3) Cleric')
            party_win.addstr(5, 2, '4) Rogue')
            party_win.refresh()
            party_win.refresh()
            char_class = party_win.getch()
            if char_class not in CLASSES:
                continue
            character = CLASSES[char_class]()
            self.party.append(character)
            self.party_windows.append(PlayerWindow(character, win_x, win_y))
            win_y += 6
        party_win.clear()
        party_win.refresh()
        party_win = None

    def generate_monsters(self):
        party_level = int(sum([char.level for char in self.party]) / len(self.party))
        monster_combinations = [(Orc, Orc, Orc),
                                (Orc, Troll),
                                (Skeleton, Skeleton),
                                (Vampire,),
                                (RedDragon,),
                                (GreenDragon,)]
        self.monsters = [monster(level=party_level + 1) for monster in random.choice(monster_combinations)]
        self.monster_window = MonsterWindow(self.monsters)

    def generate_battle(self):
        self.generate_monsters()
        participants = [char for char in self.party if char.hp > 0] + self.monsters
        self.battle = battle.Battle(participants=participants)



    def player_turn(self):
        try:
            self.combat_log.add_message('Select ability.')
            # Map ord('1') to int(0) to match ability use
            ability_map = {ord(str(x + 1)): x for x in range(4)}
            ability_choice = None
            self.ability_window.show_abilities([win for win in self.party_windows if win.hero == self.battle.current_attacker()][0])
            
            while ability_choice not in ability_map:
                ability_choice = self.main_window.getch()
            

            PlayerWindow.show_targets()
            self.monster_window.show_targets()
            self.combat_log.add_message('Select target.')
            target_map = {ord(str(x + 1)): self.monsters[x] for x in range(len(self.monsters))}
            target_map.update({ord('a'): self.party[0],
                               ord('A'): self.party[0],
                               ord('b'): self.party[1],
                               ord('B'): self.party[1],
                               ord('c'): self.party[2],
                               ord('C'): self.party[2],
                               ord('d'): self.party[3],
                               ord('D'): self.party[3]})
            target = None
            while target not in target_map:
                target = self.main_window.getch()
            self.ability_window.hide()

            return self.battle.execute_command(self.battle.current_attacker().abilities[ability_map[ability_choice]],
                                               target_map[target])
        except InsufficientMP:
            self.combat_log.add_message('Insufficient MP to use that.')
            return self.player_turn()
        except InvalidTarget:
            self.combat_log.add_message('That is an invalid target.')
            return self.player_turn()

    def process_turn(self, messages):
        for msg in messages:
            self.combat_log.add_message(msg)
        self.redraw()





        



client = BattleCursesClient()
curses.wrapper(client.run)
print("You were victorious {} times in a row!".format(client.victory_count))
curses.endwin()
