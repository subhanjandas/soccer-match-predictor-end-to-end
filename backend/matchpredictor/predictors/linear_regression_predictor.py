# backend/matchpredictor/predictors/linear_regression_predictor.py

from typing import List, Tuple, Optional
import numpy as np
from numpy import float64
from numpy.typing import NDArray
from sklearn.linear_model import LogisticRegression  # type: ignore
from sklearn.preprocessing import OneHotEncoder  # type: ignore

from matchpredictor.matchresults.result import Fixture, Outcome, Result, Team
from matchpredictor.predictors.predictor import Predictor, Prediction


class LinearRegressionPredictor(Predictor):
    """
    A predictor that uses logistic regression to predict match outcomes based on team names.
    """

    def __init__(self, model: LogisticRegression, team_encoding: OneHotEncoder) -> None:
        """
        Initializes the LinearRegressionPredictor with a logistic regression model and a team encoder.

        Args:
            model (LogisticRegression): The trained logistic regression model.
            team_encoding (OneHotEncoder): The encoder for team names.
        """
        self.model = model
        self.team_encoding = team_encoding

    def predict(self, fixture: Fixture) -> Prediction:
        """
        Predicts the outcome of a fixture using the logistic regression model.

        Args:
            fixture (Fixture): The fixture for which to predict the outcome.

        Returns:
            Prediction: The predicted outcome of the fixture.
        """
        encoded_home_name = self.__encode_team(fixture.home_team)
        encoded_away_name = self.__encode_team(fixture.away_team)

        if encoded_home_name is None:
            return Prediction(outcome=Outcome.AWAY)
        if encoded_away_name is None:
            return Prediction(outcome=Outcome.HOME)

        x: NDArray[float64] = np.concatenate([encoded_home_name, encoded_away_name], 1)
        pred = self.model.predict(x)

        if pred > 0:
            return Prediction(outcome=Outcome.HOME)
        elif pred < 0:
            return Prediction(outcome=Outcome.AWAY)
        else:
            return Prediction(outcome=Outcome.DRAW)

    def __encode_team(self, team: Team) -> Optional[NDArray[float64]]:
        """
        Encodes a team's name using the one-hot encoder.

        Args:
            team (Team): The team to encode.

        Returns:
            Optional[NDArray[float64]]: The one-hot encoded representation of the team's name,
                                        or None if the encoding fails.
        """
        try:
            result: NDArray[float64] = self.team_encoding.transform(np.array(team.name).reshape(-1, 1))
            return result
        except ValueError:
            return None


def build_model(results: List[Result]) -> Tuple[LogisticRegression, OneHotEncoder]:
    """
    Builds and trains a logistic regression model based on match results.

    Args:
        results (List[Result]): The list of match results to train the model on.

    Returns:
        Tuple[LogisticRegression, OneHotEncoder]: The trained logistic regression model and the team encoder.
    """
    home_names = np.array([r.fixture.home_team.name for r in results])
    away_names = np.array([r.fixture.away_team.name for r in results])
    home_goals = np.array([r.home_goals for r in results])
    away_goals = np.array([r.away_goals for r in results])

    team_names = np.array(list(home_names) + list(away_names)).reshape(-1, 1)
    team_encoding = OneHotEncoder(sparse=False).fit(team_names)

    encoded_home_names = team_encoding.transform(home_names.reshape(-1, 1))
    encoded_away_names = team_encoding.transform(away_names.reshape(-1, 1))

    x: NDArray[float64] = np.concatenate([encoded_home_names, encoded_away_names], 1)
    y = np.sign(home_goals - away_goals)

    model = LogisticRegression(penalty="l2", fit_intercept=False, multi_class="ovr", C=1)
    model.fit(x, y)

    return model, team_encoding


def train_regression_predictor(results: List[Result]) -> Predictor:
    """
    Trains a LinearRegressionPredictor using match results.

    Args:
        results (List[Result]): The list of match results to train the predictor on.

    Returns:
        Predictor: The trained LinearRegressionPredictor.
    """
    model, team_encoding = build_model(results)
    return LinearRegressionPredictor(model, team_encoding)
