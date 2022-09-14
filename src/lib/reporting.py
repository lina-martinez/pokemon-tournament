import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Protocol

from lib.battle import BattleSummary


class WithName(Protocol):
    name: str


class Reporter:
    """Persists the results matches into permanent storage. """

    def __init__(self, dir: Path) -> None:
        self._filepath = dir / "report.json"
        self._report: Dict[str, List] = {}
        self._num_stages = 0

    def update(self, *, stage: int, results: Sequence[BattleSummary]) -> None:
        """
        Updates the internal registry of matches, as well as the num_stages
        property.
        """
        self._num_stages = stage
        if stage == 1:
            self._report['tournament'] = []
        for count, battleSummary in enumerate(results):
            summary = json.loads(json.dumps(battleSummary, default=lambda o: vars(o)))
            element = {'stage': stage, 'battle': count + 1, 'summary': summary}
            self._report['tournament'].append(element)

    def review_battle(self, p1: str, p2: str) -> str:
        """
        *Quickly* return the result of a particular match defined by the
        provided parameters.

        Raise a ValueError if the provided participants have not had a match.
        """
        if p1 == p2:
            raise ValueError('Un Pokemon no puede batallar consigo mismo.')

        for battle in self._report['tournament']:
            winner = battle['summary']['winner']['name']
            defeated = battle['summary']['defeated']['name']
            if winner == p1 and defeated == p2:
                return p1
            if winner == p2 and defeated == p1:
                return p2

        raise ValueError('Estos Pokemones no se enfrentaron en el torneo.')

    def review_stage(self, stage: int) -> List[Tuple[str, str]]:
        """Returns the battles at a particular stage. """
        battles = []
        for battle in self._report['tournament']:
            actual_stage = battle['stage']
            if actual_stage == stage:
                winner = battle['summary']['winner']['name']
                defeated = battle['summary']['defeated']['name']
                battles.append((winner, defeated))

        return battles

    #Metodo creado para obtener toda la información de un stage 
    def review_stage_summaries(self, stage: int) -> List[Dict[str, str]]:
        """Returns the battles at a particular stage. """
        summaries = []
        for battle in self._report['tournament']:
            actual_stage = battle['stage']
            if actual_stage == stage:
                summary = battle['summary']
                summaries.append(summary)

        return summaries

    @property
    def num_stages(self):
        return self._num_stages

    @property
    def report(self):
        return self._report
