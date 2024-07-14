# backend/matchpredictor/predictors/advanced_predictor.py

from typing import Iterable, List, Dict
from matchpredictor.matchresults.result import Fixture, Outcome, Result
from matchpredictor.predictors.predictor import Predictor, Prediction
from matchpredictor.predictors.linear_regression_predictor import train_regression_predictor

class AdvancedPointsTable:
    def __init__(self) -> None:
        self.points_dict: Dict[str, int] = {}
        self.goal_diffs: Dict[str, int] = {}
        self.recent_performance: Dict[str, int] = {}
        self.home_form: Dict[str, float] = {}
        self.away_form: Dict[str, float] = {}
        self.head_to_head: Dict[str, Dict[str, float]] = {}

    def points_for(self, team: str) -> int:
        return self.points_dict.get(team, 0)

    def goal_diff_for(self, team: str) -> int:
        return self.goal_diffs.get(team, 0)

    def recent_form_for(self, team: str) -> int:
        return self.recent_performance.get(team, 0)

    def home_form_for(self, team: str) -> float:
        return self.home_form.get(team, 0.0)

    def away_form_for(self, team: str) -> float:
        return self.away_form.get(team, 0.0)

    def head_to_head_for(self, team1: str, team2: str) -> float:
        return self.head_to_head.get(team1, {}).get(team2, 0.0)

    def record_result(self, fixture: Fixture, outcome: Outcome, home_goals: int, away_goals: int) -> None:
        if outcome == Outcome.HOME:
            self.__add_points(fixture.home_team.name, 3)
            self.__update_recent_form(fixture.home_team.name, 1)
            self.__update_recent_form(fixture.away_team.name, -1)
            self.__update_home_away_form(fixture.home_team.name, fixture.away_team.name, 1.0, -1.0)
        elif outcome == Outcome.AWAY:
            self.__add_points(fixture.away_team.name, 3)
            self.__update_recent_form(fixture.home_team.name, -1)
            self.__update_recent_form(fixture.away_team.name, 1)
            self.__update_home_away_form(fixture.home_team.name, fixture.away_team.name, -1.0, 1.0)
        else:
            self.__add_points(fixture.home_team.name, 1)
            self.__add_points(fixture.away_team.name, 1)
            self.__update_recent_form(fixture.home_team.name, 0)
            self.__update_recent_form(fixture.away_team.name, 0)
            self.__update_home_away_form(fixture.home_team.name, fixture.away_team.name, 0.0, 0.0)

        self.__add_goal_diff(fixture.home_team.name, home_goals - away_goals)
        self.__add_goal_diff(fixture.away_team.name, away_goals - home_goals)
        self.__update_head_to_head(fixture.home_team.name, fixture.away_team.name, outcome)

    def __add_points(self, team: str, points: int) -> None:
        self.points_dict[team] = self.points_dict.get(team, 0) + points

    def __add_goal_diff(self, team: str, goal_diff: int) -> None:
        self.goal_diffs[team] = self.goal_diffs.get(team, 0) + goal_diff

    def __update_recent_form(self, team: str, result: int) -> None:
        self.recent_performance[team] = self.recent_performance.get(team, 0) + result

    def __update_home_away_form(self, home_team: str, away_team: str, home_result: float, away_result: float) -> None:
        self.home_form[home_team] = self.home_form.get(home_team, 0.0) + home_result
        self.away_form[away_team] = self.away_form.get(away_team, 0.0) + away_result

    def __update_head_to_head(self, home_team: str, away_team: str, outcome: Outcome) -> None:
        if home_team not in self.head_to_head:
            self.head_to_head[home_team] = {}
        if away_team not in self.head_to_head:
            self.head_to_head[away_team] = {}

        if outcome == Outcome.HOME:
            self.head_to_head[home_team][away_team] = self.head_to_head.get(home_team, {}).get(away_team, 0.0) + 1.0
            self.head_to_head[away_team][home_team] = self.head_to_head.get(away_team, {}).get(home_team, 0.0) - 1.0
        elif outcome == Outcome.AWAY:
            self.head_to_head[home_team][away_team] = self.head_to_head.get(home_team, {}).get(away_team, 0.0) - 1.0
            self.head_to_head[away_team][home_team] = self.head_to_head.get(away_team, {}).get(home_team, 0.0) + 1.0
        else:
            self.head_to_head[home_team][away_team] = self.head_to_head.get(home_team, {}).get(away_team, 0.0) + 0.0
            self.head_to_head[away_team][home_team] = self.head_to_head.get(away_team, {}).get(home_team, 0.0) + 0.0

class AdvancedPredictor(Predictor):
    def __init__(self, table: AdvancedPointsTable, linear_regression_predictor: Predictor) -> None:
        self.table = table
        self.linear_regression_predictor = linear_regression_predictor

    def predict(self, fixture: Fixture) -> Prediction:
        # Advanced Points Table Prediction
        home_points = self.table.points_for(fixture.home_team.name)
        away_points = self.table.points_for(fixture.away_team.name)
        home_goal_diff = self.table.goal_diff_for(fixture.home_team.name)
        away_goal_diff = self.table.goal_diff_for(fixture.away_team.name)
        home_recent_form = self.table.recent_form_for(fixture.home_team.name)
        away_recent_form = self.table.recent_form_for(fixture.away_team.name)
        home_form = self.table.home_form_for(fixture.home_team.name)
        away_form = self.table.away_form_for(fixture.away_team.name)
        head_to_head = self.table.head_to_head_for(fixture.home_team.name, fixture.away_team.name)

        home_score = (home_points * 0.3) + (home_goal_diff * 0.2) + (home_recent_form * 0.2) + (home_form * 0.2) + (head_to_head * 0.1)
        away_score = (away_points * 0.3) + (away_goal_diff * 0.2) + (away_recent_form * 0.2) + (away_form * 0.2) + (-head_to_head * 0.1)

        if home_score > away_score:
            advanced_prediction = Outcome.HOME
        elif home_score < away_score:
            advanced_prediction = Outcome.AWAY
        else:
            advanced_prediction = Outcome.DRAW

        # Linear Regression Prediction
        linear_regression_prediction = self.linear_regression_predictor.predict(fixture).outcome

        # Ensemble Prediction: Weighted Average
        weights = {'advanced': 0.6, 'linear_regression': 0.4}
        prediction_scores = {
            Outcome.HOME: 0.0,
            Outcome.AWAY: 0.0,
            Outcome.DRAW: 0.0
        }
        prediction_scores[advanced_prediction] += weights['advanced']
        prediction_scores[linear_regression_prediction] += weights['linear_regression']

        final_prediction = max(prediction_scores, key=lambda outcome: prediction_scores[outcome])

        return Prediction(outcome=final_prediction)

def calculate_advanced_table(results: Iterable[Result]) -> AdvancedPointsTable:
    table = AdvancedPointsTable()
    for result in results:
        home_goals = result.home_goals
        away_goals = result.away_goals
        outcome = result.outcome
        table.record_result(result.fixture, outcome, home_goals, away_goals)
    return table

def train_advanced_predictor(results: Iterable[Result]) -> Predictor:
    advanced_table = calculate_advanced_table(results)
    linear_regression_predictor = train_regression_predictor(list(results))  # Convert to list
    return AdvancedPredictor(advanced_table, linear_regression_predictor)
