import random
from dataclasses import dataclass
from typing import List

from lib.pokemon import Pokemon


@dataclass
class BattleRound:
    attacker: str
    defendant: str
    damage: float
    ability: str


@dataclass
class BattleSummary:
    winner: Pokemon
    defeated: Pokemon
    rounds: List[BattleRound]


def simulate_battle(p1: Pokemon, p2: Pokemon, random_seed: int = 0) -> BattleSummary:
    """This function simulates a single battle between two Pokémons.

    A battle consists of several rounds, at each round there is only one Pokémon
    doing the attack, while the other is defending. The role at each turn
    is defined randomly and each participant has a random chance of being
    selected as the attacker, weigthed by the amount abilities of the
    participant over the total number of abilities of both participants. For
    example, if `p1` has 2 abilities, while `p2` has only one, then `p1` is
    expected to be selected as the attacker 66.66% of the time.

    Since a battle is a random process, we will repeat each battle a thousand
    times and pick the winner as the most common winner in all battles, as well
    as picking the least number of rounds in which the winner won.

    Each battle comes to an end whenever the health points of any of the
    Pokémons reaches 0 or there are 100 rounds. At each turn of the battle,
    the health points of the attacker remain the same, while the ones for the
    defendant are computed as:

        damage = attacker.attack * random.betavariate(1, 5)
        HP_t+1 = HP_t - damage (Health points of the defendant at time t)


    This function is provided a random_seed value, so that the battle always
    yields the same results.
    """
    if p1.name == p2.name:
        return BattleSummary(winner=p1, defeated=p2, rounds=[])
    random.seed(random_seed)
    winners = {p1.name: 0, p2.name: 0}
    rounds = {p1.name: [], p2.name: []}
    total_abilities = len(p1.abilities) + len(p2.abilities)
    weights = [len(p1.abilities) / total_abilities,
               len(p2.abilities) / total_abilities]

    for i in range(0, 1000):
        summary = generate_battle(p1=p1, p2=p2, weights=weights)
        winner_name = summary.winner.name
        winners[winner_name] += 1
        if rounds[winner_name]:
            if len(rounds[winner_name]) > len(summary.rounds):
                rounds[winner_name] = summary.rounds
        else:
            rounds[winner_name] = summary.rounds

    winner = p1 if winners[p1.name] >= winners[p2.name] else p2
    defeated = p1 if winners[p1.name] <= winners[p2.name] else p2
    winner_rounds = rounds[winner.name]
    return BattleSummary(winner=winner, defeated=defeated, rounds=winner_rounds)


def generate_battle(p1: Pokemon, p2: Pokemon, weights: List[float]) -> BattleSummary:
    round_count = 0
    rounds = []
    healths = {p1.name: p1.health_points, p2.name: p2.health_points}
    while 1:
        attacker = random.choices([p1, p2], weights)[0]
        defender = list(filter(lambda pokemon: (
                pokemon != attacker), [p1, p2]))[0]
        if not defender:
            defender = p1
        ability = random.choices(attacker.abilities)[0]
        damage = attacker.attack * random.betavariate(1, 5)
        healths[defender.name] -= damage
        rounds.append(BattleRound(
            attacker.name, defender.name, damage, ability))
        round_count += 1
        if healths[defender.name] <= 0:
            return BattleSummary(winner=attacker, defeated=defender, rounds=rounds)
        if round_count >= 100:
            winner = attacker if healths[attacker.name] >= healths[defender.name] else defender
            defeated = defender if healths[defender.name] >= healths[attacker.name] else attacker
            return BattleSummary(winner=winner, defeated=defeated, rounds=rounds)
