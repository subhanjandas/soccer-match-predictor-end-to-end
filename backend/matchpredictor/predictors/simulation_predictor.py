# backend/matchpredictor/predictors/simulation_predictor.py

from typing import Iterable
from matchpredictor.matchresults.result import Fixture, Outcome, Result, Scenario
from matchpredictor.predictors.predictor import Predictor, Prediction, InProgressPredictor
from matchpredictor.predictors.simulators.scoring_rates import ScoringRates
from matchpredictor.predictors.simulators.simulator import Simulator, offense_simulator, offense_and_defense_simulator

class SimulationPredictor(InProgressPredictor):
    """
    A predictor that uses simulations to predict match outcomes.
    Inherits from InProgressPredictor to support in-progress match predictions.
    """
    def __init__(self, simulator: Simulator, simulations: int) -> None:
        """
        Initializes the SimulationPredictor with a simulator and number of simulations.

        Args:
            simulator (Simulator): The simulator function to use for predictions.
            simulations (int): The number of simulations to run for each prediction.
        """
        self.simulator = simulator
        self.simulations = simulations

    def predict(self, fixture: Fixture) -> Prediction:
        """
        Predicts the outcome of a fixture by simulating the match from the start.

        Args:
            fixture (Fixture): The fixture to predict.

        Returns:
            Prediction: The predicted outcome of the fixture.
        """
        return self.predict_in_progress(fixture, Scenario(0, 0, 0))

    def predict_in_progress(self, fixture: Fixture, scenario: Scenario) -> Prediction:
        """
        Predicts the outcome of a fixture given an in-progress scenario.

        Args:
            fixture (Fixture): The fixture to predict.
            scenario (Scenario): The current scenario of the in-progress match.

        Returns:
            Prediction: The predicted outcome of the fixture given the current scenario.
        """
        results = [self.simulator(fixture, scenario) for _ in range(self.simulations)]

        home_count = sum(map(lambda r: r is Outcome.HOME, results))
        away_count = sum(map(lambda r: r is Outcome.AWAY, results))
        draw_count = sum(map(lambda r: r is Outcome.DRAW, results))

        if home_count > away_count and home_count > draw_count:
            return Prediction(outcome=Outcome.HOME, confidence=home_count / self.simulations)
        if away_count > draw_count:
            return Prediction(outcome=Outcome.AWAY, confidence=away_count / self.simulations)
        else:
            return Prediction(outcome=Outcome.DRAW, confidence=draw_count / self.simulations)

def train_offense_predictor(results: Iterable[Result], simulations: int) -> Predictor:
    """
    Trains an offense-only simulation predictor.

    Args:
        results (Iterable[Result]): The past match results used to calculate scoring rates.
        simulations (int): The number of simulations to run for each prediction.

    Returns:
        Predictor: An instance of SimulationPredictor trained on the provided results.
    """
    return SimulationPredictor(offense_simulator(ScoringRates(results)), simulations)

def train_offense_and_defense_predictor(results: Iterable[Result], simulations: int) -> Predictor:
    """
    Trains an offense and defense simulation predictor.

    Args:
        results (Iterable[Result]): The past match results used to calculate scoring rates.
        simulations (int): The number of simulations to run for each prediction.

    Returns:
        Predictor: An instance of SimulationPredictor trained on the provided results.
    """
    return SimulationPredictor(offense_and_defense_simulator(ScoringRates(results)), simulations)
