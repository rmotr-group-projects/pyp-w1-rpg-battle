[pyp-w1] RPG Battle System
===================

Today we will be creating a traditional RPG (*role-playing game*) battle system featuring Mages, Warriors, Dragons, and Skeletons!

**Running Tests**
=================
You may run the entire test suite by executing: `make test`

However it is **highly suggested** to run individual tests one at a time, write code to make the test pass, and then proceed to the next test, repeating the process.

You may run individual tests by executing:
```
PYTHONPATH=. py.test tests/[test file] -k [name of test]
```
So for example to run `test_base_creation` in `test_heroes.py` you would run:
```
PYTHONPATH=. py.test tests/test_heroes.py -k test_base_creation
```
The `-k` option indicates a keyword search. You could also use it to run **all** the creation tests in the `test_heroes.py` file by running:
```
PYTHONPATH=. py.test tests/test_heroes.py -k creation
```
Finally, you may also run specifically one test using the followind format:
```
PYTHONPATH=. py.test tests/[test file]::[test case]::[name of test function]
```
To run **only** the `test_base_creation` from `BaseHeroTestCase` you would run:
```
PYTHONPATH=. py.test tests/test_heroes.py::BaseHeroTestCase::test_base_creation
```


**Using getattr and setattr**
=================
`getattr` and `setattr` are useful tools for dynamically reading and setting attributes.

`getattr` is defined as such: `getattr(object, name[, default])` and allows you to retrieve an attribute from `object` named `name`, and optionally set a `default` value if the attribute doesn't exist. It is important to note that `name` is **a string**, this is what makes `getattr` so useful as you can manipulate the string however you want before giving it to `getattr`

Very basic example, say we had a Person class with the attributes `name`, `phone`, `address`, `email`:
```
person = Person(name='John', email='example@example.com')
for attr in ('name', 'phone', 'address', 'email'):
    print("{name}: {value}".format(name=attr, value=getattr(person, attr, 'N/A')))
```
The above would print the following:
```
name: John
phone: N/A
address: N/A
email: example@example.com
```
`setattr` is the counterpart to `getattr` and is defined as: `getattr(object, name, value)

If we wanted to define the People class from above so that we could take **any** keyword arguments when intialising we could write it like this:
```
class People(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
```

It's important to note how this relates to inheritance. You can use getattr to read values in your base class that may or may not have been set in your child classes.

**Overview**
============
We will be breaking the project down into three primary parts: **Heroes**, **Monsters**, and **Battles**.

**Heroes** represent player characters, they can be one of four classes, **Warrior**, **Mage**, **Cleric**, or **Rogue**. Depinding on a hero's class they will have different stats and abilities, for example a Warrior is stronger and more durable than a mage and therefore they have a higher *strength* and *constitution*. These statistics effect how their various abilities work. As heroes defeat monsters they gain xp (experience points) and if they gain enough experience they level up and become stronger.

**Monsters** are what the heroes fight. They can be classified into monster families (like *dragons* and *undead*) as well as individual monster types within those families (like Red Dragons and Vampires). Monsters have their own abilities depending on a combination of their family and type.

**Battles** This is what brings everything together. Participants will perform actions in order of their `speed` attribute - faster units go before slower units. Hero abilities are user determined, monster abilities are used according to their *command queue* (described below) and target heroes randomly. Battle continues until either all the heroes or all the monsters are wiped out.


**Heroes**
======
> **Features common to all Heroes:**
> *When initialising a Hero you may pass a `level` parameter to specify what level of hero you would like.*

> - Stats:
>  - `strength`
>  - `constitution`
>  - `intelligence`
>  - `speed`
> - `hp` - current hit points
> - `maxhp` - maximum hit points
> - `mp` - current magic points
> - `maxmp` - maximum magic points
> - `level` - current character level
> - `xp` - current experience points
> - `xp_for_next_level()` - when xp == this it causes the hero to level up (should be equal to `level * 10`)
> - `gain_xp(xp)`- causes the hero to gain `xp` experience points, should also handle the process of levelling up
> - `fight(target)` - Basic attack dealing damage equal to the hero's `strength` to the `target`
> - `abilities` - a collection of strings representing the hero's combat abilities. For example a `Mage`'s `abilities` would be something like `('fight', 'fireball', 'frostbolt')`
> - `take_damage(damage)` - hero takes `damage` amount of damage, having it subtracted from their current hp
> - `heal_damage(healing)` - hero heals `healing` hit points, but not beyond their `maxhp`
> - `is_dead()` - if the hero's hp have been completely depleted this returns `True`



----------


>**Stats**
Base level stats (strength, constitution, intelligence, speed) for a level 1 Hero start at 6 and may be modified by child classes.


----------


>**Hit Points**
Base level hit points for a level 1 Hero start at 100 + 1/2 of the hero's `constitution`, dropping any fractions.


----------


>**Magic Points**
Base level magic points for a level 1 Hero start at 50 + 1/2 of the hero's `intelligence`, dropping any fractions.

----------

>**Levelling Up**
When a hero has `xp` greater than or equal to `xp_for_next_level` they level up. Any excess xp is carried over after their xp is set to 0. Upon level up all stats are increased by one (or more if the hero has a stat modifier, this will be explained later). Their `maxhp` is increased by 1/2 their new `constitution` and their `hp` is brought back up to full. `maxmp` is also increased by 1/2 the new `intelligence`, mp also being filled. *When increasing `maxhp` or `maxmp` remember to drop any fractions*.

*Hero Subclasses*
-----------------------

> **Stat Modifiers**
> Subclasses can apply modifiers to the hero's stats, either increasing or decreasing them. Modifiers should be added directly to the base value of the appropriate stat. At level up if the modifier is positive it is added to to the standard +1 received at level up. **Example:** *If a subclass had a +1 `strength` modifier it would have 7 `strength` at level 1 and would gain 2 `strength` each time it levelled up.*


----------
> **Special Abilities**
> Each subclass has its own unique special abilities. Many of these abilities have an `mp` cost, if the hero does not have enough mp to use the ability an `InsufficientMP` error should be raised. When calculating damage, drop fractions from final damage number.

Warrior
----------
> **Stat Modifiers**

> - `strength` +1
> - `intelligence` -2
> - `constitution` +2
> - `speed` -1


----------
> `shield_slam(target)`

> - Cost: 5 MP
> - Damage: 1.5x `strength`


----------
> `reckless_charge(target)`

> - Cost: 4 **HP**
> - Damage: 2x `strength`

Mage
-------
> **Stat Modifiers**

> - `strength` -2
> - `intelligence` +3
> - `constitution` -2


----------
> `fireball(target)`

> - Cost: 8 MP
> - Damage: 6 + 0.5x `intelligence`


----------
> `frostbolt(target)`

> - Cost: 3 MP
> - Damage: 3 + `level`

Cleric
--------
> **Stat Modifiers**

> - `speed` -1
> - `constitution` +1


----------
> `heal(target)`

> - Cost: 4 MP
> - Heals target for 3 * `constitution`


----------
> `smite(target)`

> - Cost: 7 MP
> - Damage: 4 + 0.5x (`intelligence + constitution`)

Rogue
---------
> **Stat Modifiers**

> - `speed` +2
> - `strength` +1
> - `intelligence` -1
> - `constitution` -2


----------
> `backstab(target)`

> - Cost: None
> - **Special requirement:** Target must be undamaged. If target is damaged must raise `InvalidTarget`
> - Damage: 2x `strength`


----------
> `rapid_strike(target)`

> - Cost: 5 MP
> - Damage: 4 + `speed`

**Monsters**
===========
> **Features common to all monsters:**
> *When initialising a Monster you may pass a `level` parameter to specify what level of monster you would like.*

> - Stats:
>   - `strength`
>   - `constitution`
>   - `intelligence`
>   - `speed`
> - `maxhp`
> - `hp`
> - `level`
> - `xp()` - returns the xp that would be earned if this monster were to be defeated
> - `fight(target)`
> - `take_damage(damage)`
> - `heal_damage(healing)`
> - `is_dead()`
> - `attack(target)` - Attacks the target using the next ability in the monster's command queue (explained later)
> *Note: Monsters do not use MP*


----------

> **Stats**
> Monsters start with a base stat level of 8 for all stats except speed versus the 6 that heroes receive, monster speed has a base of 12. Instead of receiving stat modifiers like heroes, monsters may receive stat multiplier instead. These are applied in the following manner: At level 1 a stat is set to `base value` x the stat multiplier. For levelled monsters set the stat to `base value` X multiplier + `(level - 1)` x multiplier, dropping fractions.
> Monster have a base HP of 10 (this may be overidden by monster families and subtypes, more on this later) to calculate their actual `maxhp` use the base hp + (level - 1) x (0.5x `constitution`), dropping fractions as usual.
> 


----------
> **XP**
> A monster's xp value may be calculated by taking the average of their stats (`strength`, `constitution`, `intelligence`, `speed`) and adding it to `maxhp / 10`. Finally we take this all and multiply it by the `XP_MULTIPLIER`.


----------
> **Command Queue**
> The command queue determines in which order a Monster uses its abilities. When an ability is used it cycles out to the end of the queue. **Example:** *If a monster had a queue of `['fight', 'bash', 'slash']` the first time it attacked it would use `fight`, the next time it would use `bash` and so on.*

*Monster Families and Subtypes*
-------------------------------------------
Monsters are divided into families before being separated into individual monster types. Monster families can have multipliers, abilities, and other special features that apply to all of their members.

**Dragons**
-----------------
> **Family features**

> - Base HP: 100
> - `constitution` multiplier: 2
> - `xp` multiplier: 2
> - **Special feature:** Dragons have damage reduction, all damage they take is reduced by 5.
> - `tail_swipe(target)` : Deals 1.5 * (`strength` + `speed`) damage


----------
> **RedDragon**

> - `strength` multiplier: 2
> - `intelligence` multiplier: 1.5
> - `fire_breath(target)`: deals 3x `intelligence` damage


----------
> **GreenDragon**

> - `strength` multiplier: 1.5
> - `speed` multiplier: 1.5
> - `poison_breath(target)`: deals 1.5x (`intelligence` + `constitution`) damage

**Undead**
--------------
> **Family Features**

> - `constitution` multiplier: 0.25
> - **Special feature:** Undead take damage from attempts to heal them. *Note: The Undead's own special healing abilities do not damage it*
> - `life_drain(target)`: Damages the target for 1.5x `intelligence`, healing the Undead for the same amount.


----------
>**Vampire**

> - `intelligence` multiplier: 2
> - Base HP: 45
> - `bite(target)`: Deals 2x `speed` damage to the target, healing the Vampire for the same amount. **Permanently lowers the target's `maxhp` by an amount equal to the damage dealt.**


----------
>**Skeleton**

> - `strength` multiplier: 1.25
> - `speed` multiplier: 0.5
> - `intelligence` multiplier: 0.25
> - Base HP: 30
> - `bash(target)`: deal 2x `strength` damage

**Humanoid**
-------------------
>**Family Features**

> - `slash(target)`: deal `strength + speed` damage


----------
>**Troll**

> - `strength` multiplier: 1.75
> - `constitution` multiplier: 1.5
> - Base HP: 20
> - `regenerate(*args)`: Restores `constitution` health to the Troll.


----------
>**Orc**

> - `strength` multiplier: 1.75
> - Base HP: 16
> - `blood_rage(target)`: Deals 2x `strength` damage to the target while dealing 0.5x `constitution` damage to the Orc


**Battle System**
==============
Preparing a battle should be as simple as creating a new `Battle` while passing in a list of participants. The battle should handle sorting the participants in order of `speed` and then cycle through the list, moving units to the end of the line as they take turns performing actions.

A Battle should have the following outward facing interface:

- `next_turn()`: processes the next unit's turn
- `current_attacker()`: returns the unit at the front of the initiative queue
- `is_hero_turn()`: returns `True` if `current_attacker` is a `Hero`
- `is_monster_turn()`: returns `True` if `current_attacker` is a `Monster`
- `execute_command(command, target)`: uses an ability on the target
- `raise_for_battle_over()`: raises `Victory` if all monsters are defeated, and raises `Defeat` if all heroes are defeated

The following helper methods are recomended to break the project into smaller, more manageable chunks:

- `_monster_turn()`: handles a monster's turn
- `_hero_turn()`: announces (adds to the event log) that it is a hero's turn
- `_process_initiative()`: handles rearranging the initiative after a unit's turn
- `_process_dead()`: handles removing dead units from the initiative queue and triggers xp rewards
- `_reward_xp()`: handles rewarding xp to living members of the party
- `_check_victory()`: returns `True` if 0 monsters in initiative queue
- `_check_defeat(): returns `True` if 0 heroes in initiative queue

Upon running the `next_turn` command the program should check to see if the current attacker is a monster, if it is it will pick a hero target at random and use the monster's next attack in its command queue. It will then repeat the process until it reaches a hero's turn. At this point it returns a multi-line string containing all the events that have happened so far and stating what hero's turn it is. (Details on event formatting below.) It is then up to the user to select a target and action and then `execute_command`. This will run the corresponding command (throwing any appropriate errors, including `InvalidCommand` if the command doesn't exist) and then resume the cycle of moving through the initiative queue until it reaches a Hero again. At the end of each unit's turn all dead units should be removed from the initiative queue and xp should be rewarded to all heroes for any monsters killed, triggering level ups if appropriate. If at the start of a turn all the monsters are dead the program should raise a Victory, if all the heroes are dead it should raise a Defeat.

> **Event formatting**
> Each event should be recorded as a new entry in the list that is returned

> - *`fight` command used: `{monster} attacks {target} for {damage}!`
> - other attack ability used: `{monster} hits {target} with {ability} for {damage} damage!`
> - unit dies: `{unit} dies!`
> - XP is rewarded: `{xp} XP rewarded!`
> - Hero levels up: `{hero} is now level {level}!`
> - Unit ability causes damage to self: `{unit} takes {damage} self-inflicted damage!`
> - Hero's turn: `{hero}'s turn!`
