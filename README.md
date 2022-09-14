# Pokémon Tournament

An app to simulate a tournament between pokemons, giving you the opportunity to practice several programing concepts with Python. In particular, you will put into practice:
* Definitions of classes and functions.
* Concurrency (i.e. threading, asyncio and multiprocessing).
* Simulation of random processes. 
* Reading and writing files.
* Lazy computations.

We are giving you a template code so that you do not have to come up with everything from scratch, go ahead and implement all functions and classes defined in this project so that you can execute the tournament simulation wihout trouble. If you have implemented all of the source code correctly, you should be able to execute the `main.py` without trouble. 

Want some extra challenge? Try yo write test cases for the implementations defined in this project. Partner with a mentor to see if the test cases make sense!

## The Tournament

In this tournament we want to settle, once and for all, what are the strongest pokemon out there. We will setup of multiple battles that will help us figure out the strongest pokemon by different two factors: generation and type. We will also take the opportunity to gather some information about the Pokemon, we will see how they distribute over a certain area and other statistics about their abilities.

For this tournament we need to create a pyramid to define the battles of each pair of Pokémon, so there can only be one superior champion. Each battle will load a picture of each Pokémon into our application and define the winner following a particular rule, which will be explained in the function that defines the battle. The winner of each battle moves one step up in the tournament pyramid and the health points of each Pokémon is restored after each battle.