from typing import Sequence, Dict, List

from lib.battle import Pokemon
from lib.reporting import Reporter


class Summary:
    def __init__(self, participants: Sequence[Pokemon], reporter: Reporter) -> None:
        self._paticipants = participants
        self._reporter = reporter

    @property
    def num_paticipants(self) -> int:
        return len(self._paticipants)

    @property
    def champion(self) -> str:
        last_stage = self._reporter.num_stages
        battle = self._reporter.review_stage(last_stage)

        return battle[0][0]

    @property
    def most_common_ability_used_in_battle(self) -> str:
        abilities = {}
        for battle in self._reporter.report['tournament']:
            for round in battle['summary']['rounds']:
                if round['ability'] in abilities:
                    abilities[round['ability']] += 1
                else:
                    abilities[round['ability']] = 1

        return max(abilities, key=abilities.get)

    @property
    def strongest_type(self) -> str:
        """The type that ranked better overall. """
        last_stage = self._reporter.num_stages
        summary = self._reporter.review_stage_summaries(last_stage)

        return summary[0]['winner']['type']

    @property
    def strongest_generation(self) -> str:
        """
        The generation that was most common in later stages of the
        tournament.
        """
        # top_fifty = []
        # reverse_reporter = self._reporter.report['tournament'][::-1]
        # for i, battle in enumerate(reverse_reporter):
        #
        #     if i == 50:
        #         break

        return "Pokèmon"

    @property
    def max_rounds_in_tournament(self) -> int:
        """The number of rounds """
        max_rounds = 0
        for battle in self._reporter.report['tournament']:
            if len(battle['summary']['rounds']) > max_rounds:
                max_rounds = len(battle['summary']['rounds'])

        return max_rounds

    @property
    def most_endurance(self) -> str:
        """Pokemon that resisted the most number of attacks in the tournament."""
        #Diccionario con el numero de ataques recibidos por cada pokemon en todo el torneo
        attacks_received = {}
        for battle in self._reporter.report['tournament']:
            for round in battle['summary']['rounds']:
                if round['defendant'] in attacks_received:
                    attacks_received[round['defendant']] += 1
                else:
                    attacks_received[round['defendant']] = 1

        return max(attacks_received, key=attacks_received.get)

    @property
    def participants_per_type(self) -> Dict[str, int]:
        types = {}
        for pokemon in self._paticipants:
            if pokemon.type in types:
                types[pokemon.type] += 1
            else:
                types[pokemon.type] = 1

        return types

    @property
    def in_top_fifty_per_type(self) -> Dict[str, int]:
        types = {}
        top_fifty = self.top_fifty_pokemons
        for pokemon in self._paticipants:
            if pokemon.name in top_fifty:
                if pokemon.type in types:
                    types[pokemon.type] += 1
                else:
                    types[pokemon.type] = 1

        return types

    @property
    def in_top_fifty_per_generation(self) -> Dict[str, int]:
        generations = {}
        top_fifty = self.top_fifty_pokemons
        for pokemon in self._paticipants:
            if pokemon.name in top_fifty:
                if pokemon.generation in generations:
                    generations[pokemon.generation] += 1
                else:
                    generations[pokemon.generation] = 1

        return generations

    @property
    # Metodo para obtener el top 50 de pokemones en el torneo
    def top_fifty_pokemons(self) -> List[str]:
        top_fifty = []
        # Reversando todas las batallas del torneo para recorrer desde el campeon
        reverse_reporter = self._reporter.report['tournament'][::-1]
        for battle in reverse_reporter:
            if len(top_fifty) < 50:
                if battle['summary']['winner']['name'] not in top_fifty:
                    top_fifty.append(battle['summary']['winner']['name'])
            if len(top_fifty) < 50:
                if battle['summary']['defeated']['name'] not in top_fifty:
                    top_fifty.append(battle['summary']['defeated']['name'])

        return top_fifty
