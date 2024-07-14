# End-to-End Soccer Match Predictor with Machine Learning and Web Interface

<img width="1666" alt="Screenshot 2024-07-14 at 1 05 43 PM" src="https://github.com/user-attachments/assets/ba49c6b9-cd5a-447a-a9ed-fa1baf78ef89">

The Match Predictor is a web application that predicts the outcomes of soccer matches using various machine learning models. The backend is written in Python with Flask, and the frontend is built using TypeScript and React.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Available Make Tasks](#available-make-tasks)
- [Models](#models)
  - [Home Predictor](#home-predictor)
  - [Alphabet Predictor](#alphabet-predictor)
  - [Advanced Predictor](#advanced-predictor)
  - [Random Forest Predictor](#random-forest-predictor)
- [Testing](#testing)
- [Evaluation and Reporting](#evaluation-and-reporting)
- [Contributing](#contributing)
- [License](#license)
- [Images](#images)

## Features

- Predict outcomes of soccer matches using multiple models.
- Evaluate the performance of each model.
- Automatically fetch and preprocess soccer match data.
- Interactive front end to select teams and models, and view predictions.

## Project Structure

```bash
match-predictor/
├── backend/
│   ├── matchpredictor/
│   │   ├── app.py
│   │   ├── __main__.py
│   │   ├── model/
│   │   │   ├── model_provider.py
│   │   │   ├── models_api.py
│   │   ├── matchresults/
│   │   │   ├── result.py
│   │   │   ├── results_provider.py
│   │   ├── predictors/
│   │   │   ├── home_predictor.py
│   │   │   ├── alphabet_predictor.py
│   │   │   ├── advanced_predictor.py
│   │   │   ├── random_forest_predictor.py
│   │   │   ├── predictor.py
│   │   ├── evaluation/
│   │   │   ├── evaluator.py
│   │   │   ├── reporter.py
│   │   ├── health.py
│   │   ├── teams/
│   │   │   ├── teams_api.py
│   │   │   ├── teams_provider.py
│   │   ├── upcominggames/
│   │   │   ├── football_data_api_client.py
│   │   │   ├── upcoming_games_api.py
│   ├── tests/
│   │   ├── predictors/
│   │   │   ├── measure_home_predictor.py
│   │   │   ├── measure_alphabet_predictor.py
│   │   │   ├── measure_advanced_predictor.py
│   │   │   ├── measure_random_forest_predictor.py
│   │   ├── model/
│   │   │   ├── test_model_provider.py
│   │   │   ├── test_models_api.py
│   ├── env/
│   ├── requirements.txt
│   ├── Makefile
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── README_Original.md
```


## Setup Instructions

### Prerequisites

- Python 3.10
- Node.js (latest version recommended)

### Backend Setup

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/subhanjandas/soccer-match-predictor-end-to-end.git
cd match-predictor
```

2. Create a virtual environment and activate it:

```bash
python3.10 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
make install
```

4. Set up environment variables:

```bash
cp /.env.example backend/.env
# Edit /.env to add your FOOTBALL_DATA_API_KEY
```

### Frontend Setup

1. Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

## Running the Application

### Running Backend

Start the backend server:

```bash
make backend/run
```

### Running Frontend

Open a new terminal, navigate to the frontend directory, and start the frontend server: 

```bash
make frontend/run
```

#### Open http://localhost:3000 in your browser to view the application.

## Available Make Tasks

### Backend
- `make backend/install`: Install backend dependencies.
- `make backend/test`: Run backend tests.
- `make backend/measure`: Run backend measurement tests.
- `make backend/run`: Run the backend server.
- `make backend/report`: Run an accuracy report.

### Frontend
- `make frontend/install`: Install frontend dependencies.
- `make frontend/test`: Run frontend tests.
- `make frontend/run`: Run the frontend server.

### Integration Tests
- `make integration/test`: Run integration tests.
- `make integration/run`: Run integration tests in interactive mode.

## Models

### Home Predictor
The Home Predictor always predicts that the home team will win.

### Alphabet Predictor
The Alphabet Predictor predicts that the team whose name comes first alphabetically will win.

### Advanced Predictor
The Advanced Predictor uses a combination of past results, goal differences, recent performance, home/away form, and head-to-head records to make predictions.

### Random Forest Predictor
The Random Forest Predictor uses a Random Forest Classifier trained on match data to predict outcomes.

## Testing

Run the backend tests to ensure everything is working correctly:

```bash
make backend/test
```

Run the frontend tests:

```bash
make frontend/test
```

## Evaluation and Reporting

To evaluate the accuracy of the predictors, run:

```bash
make backend/measure
```

Generate an accuracy report:

```bash
make backend/report
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request. Add more predictors! 

## License

This project is part of the University of Colorado Boulder's Master of Science in Computer Science, Fundamentals of Software Architecture for Big Data course, available on Coursera.

#### This project is licensed under the University of Colorado Boulder and Coursera.

## Images 

- <img width="1666" alt="Screenshot 2024-07-14 at 1 06 38 PM" src="https://github.com/user-attachments/assets/0edf2b1a-8e09-49f0-b5a6-a249dc1e22a7">
- <img width="1618" alt="Screenshot 2024-07-14 at 11 40 17 AM" src="https://github.com/user-attachments/assets/12e4d0e4-1237-4630-b9b1-9fd90ee3bb08">


Hope you enjoy my submission and code!

Thanks, @subhanjan



