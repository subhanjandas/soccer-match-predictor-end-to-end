# backend/matchpredictor/predictors/home_predictor.py

from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor

class HomePredictor(Predictor):
    """
    A simple predictor that always predicts the home team to win.
    Inherits from the base Predictor class.
    """

    def predict(self, fixture: Fixture) -> Prediction:
        """
        Predicts the outcome of a fixture, always favoring the home team.

        Args:
            fixture (Fixture): The fixture for which to predict the outcome.

        Returns:
            Prediction: A Prediction object with the outcome set to the home team win.
        """
        return Prediction(outcome=Outcome.HOME)
