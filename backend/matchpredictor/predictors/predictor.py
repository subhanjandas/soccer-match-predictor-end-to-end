# backend/matchpredictor/predictors/predictor.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from matchpredictor.matchresults.result import Fixture, Outcome, Scenario

@dataclass
class Prediction:
    """
    A dataclass representing the prediction of a match outcome.
    
    Attributes:
        outcome (Outcome): The predicted outcome of the match (e.g., home win, away win, draw).
        confidence (Optional[float]): The confidence level of the prediction (default is None).
    """
    outcome: Outcome
    confidence: Optional[float] = None

class Predictor(ABC):
    """
    Abstract base class for all predictors. 
    All specific predictors should inherit from this class and implement the predict method.
    """
    @abstractmethod
    def predict(self, fixture: Fixture) -> Prediction:
        """
        Predicts the outcome of a fixture.

        Args:
            fixture (Fixture): The fixture to predict.

        Returns:
            Prediction: The predicted outcome of the fixture.
        """
        pass

class InProgressPredictor(Predictor):
    """
    Abstract base class for predictors that can also make in-progress predictions.
    Inherits from Predictor.
    """
    @abstractmethod
    def predict_in_progress(self, fixture: Fixture, scenario: Scenario) -> Prediction:
        """
        Predicts the outcome of a fixture given an in-progress scenario.

        Args:
            fixture (Fixture): The fixture to predict.
            scenario (Scenario): The current scenario of the in-progress match.

        Returns:
            Prediction: The predicted outcome of the fixture given the current scenario.
        """
        pass
