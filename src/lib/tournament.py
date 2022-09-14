import random
from typing import List, Sequence, Tuple

from joblib import Parallel, delayed  # type: ignore
from lib.battle import BattleSummary, Pokemon, simulate_battle


class Tournament:
    """A class to simulate a tournament between pokemons.

    Args:
        participants: the pokemons that will participate in the tournament.
        num_arenas: the available arenas to run battles simoultaneously.

    """

    def __init__(
            self, participants: Sequence[Pokemon], num_arenas: int, random_seed: int = 0
    ) -> None:
        self._paticipants = participants
        self._num_arenas = num_arenas
        self._next_matches = _create_matches(participants)
        random.seed(random_seed)

    def run_stage(self) -> List[BattleSummary]:
        """Runs all the battles defined in the current set of matches.

        After running this method, the property `current_matches` gets
        updated.

        This method returns the summary of each battle run during the stage.
        """
        results = Parallel(n_jobs=self._num_arenas)(
            delayed(simulate_battle)(p1, p2)
            for p1, p2 in self.next_matches
        )

        next_participants = [battle.winner for battle in results]
        next_matches = _create_matches(next_participants)
        if len(next_matches) == 1 and next_matches[0][0].name == next_matches[0][1].name:
            next_matches = []
        self._next_matches = next_matches
        return results

    @property
    def next_matches(self) -> List[Tuple[Pokemon, Pokemon]]:
        return self._next_matches


def _create_matches(participants: Sequence[Pokemon]) -> List[Tuple[Pokemon, Pokemon]]:
    """Takes a sequence of Pokémons and matches them randomly.

    If the sequence is not even then one participant will be matched with
    itself. No matter the input, this should happen at most once. If there

    `random_seed` is used for reproducible results.
    """
    participants = random.sample(participants, len(participants))
    matchs = []

    if len(participants) % 2:
        pokemon = participants.pop()
        matchs.append((pokemon, pokemon))

    while participants:
        matchs.append((participants.pop(), participants.pop()))

    return matchs
