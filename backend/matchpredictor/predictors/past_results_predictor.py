# backend/matchpredictor/predictors/past_results_predictor.py

from typing import Iterable, Dict
from matchpredictor.matchresults.result import Outcome, Fixture, Result, Team
from matchpredictor.predictors.predictor import Predictor, Prediction

class PointsTable:
    """
    A class to maintain the points table for teams based on past match results.
    """
    def __init__(self) -> None:
        self.points_dict: Dict[str, int] = {}

    def points_for(self, team: Team) -> int:
        """
        Retrieves the points for a given team.

        Args:
            team (Team): The team whose points are to be retrieved.

        Returns:
            int: The points of the team.
        """
        return self.points_dict.get(team.name, 0)

    def record_win(self, team: Team) -> None:
        """
        Records a win for a given team, awarding 3 points.

        Args:
            team (Team): The team that won the match.
        """
        self.__add_points(team, 3)

    def record_draw(self, team: Team) -> None:
        """
        Records a draw for a given team, awarding 1 point.

        Args:
            team (Team): The team that drew the match.
        """
        self.__add_points(team, 1)

    def __add_points(self, team: Team, points: int) -> None:
        """
        Adds points to a given team.

        Args:
            team (Team): The team to which points are to be added.
            points (int): The number of points to add.
        """
        previous_points = self.points_dict.get(team.name, 0)
        self.points_dict[team.name] = previous_points + points

class PastResultsPredictor(Predictor):
    """
    A predictor that uses past match results to predict the outcome of future fixtures.
    """
    def __init__(self, table: PointsTable) -> None:
        """
        Initializes the predictor with a points table.

        Args:
            table (PointsTable): The points table used for prediction.
        """
        self.table = table

    def predict(self, fixture: Fixture) -> Prediction:
        """
        Predicts the outcome of a fixture based on the points table.

        Args:
            fixture (Fixture): The fixture to predict.

        Returns:
            Prediction: The predicted outcome of the fixture.
        """
        home_points = self.table.points_for(fixture.home_team)
        away_points = self.table.points_for(fixture.away_team)

        if home_points > away_points:
            return Prediction(Outcome.HOME)
        elif home_points < away_points:
            return Prediction(Outcome.AWAY)
        else:
            return Prediction(Outcome.DRAW)

def calculate_table(results: Iterable[Result]) -> PointsTable:
    """
    Calculates the points table from past match results.

    Args:
        results (Iterable[Result]): An iterable of past match results.

    Returns:
        PointsTable: The calculated points table.
    """
    table = PointsTable()

    for result in results:
        if result.outcome == Outcome.HOME:
            table.record_win(result.fixture.home_team)
        elif result.outcome == Outcome.AWAY:
            table.record_win(result.fixture.away_team)
        else:
            table.record_draw(result.fixture.home_team)
            table.record_draw(result.fixture.away_team)

    return table

def train_results_predictor(results: Iterable[Result]) -> Predictor:
    """
    Trains the past results predictor using past match results.

    Args:
        results (Iterable[Result]): An iterable of past match results.

    Returns:
        Predictor: An instance of PastResultsPredictor trained on the provided results.
    """
    return PastResultsPredictor(calculate_table(results))
