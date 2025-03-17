# ExactPy

This is a python implementation of the [ExactLearner](https://github.com/ExactLearner/ExactLearner).

### Java
ExactPy builds upon `Owlready2`. It uses the `HermiT` reasoner witch is a java program. In order to run this application you need to spesify the java interpreter is locaed. This is done by creating a file named `.env`. An example of this file can be found in `.env.example`.

### Dependencies

To handle dependencies, this project uses `pipenv`. 

Pipenv can be installed with `pip install pipenv`. To create a virtial

To create a virtual environment and install the dependencies, run:
`pipenv install`

To install dependencies for development purposes (e.g., testing tools), use:
`pipenv install --dev`

To enter the virtual environment where the dependencies are installed, run:
`pipenv shell`

### Tests
Tests can be run using `pytest` (remeber to run `pipenv install --dev` to install dependencies used during testing). If you want to see test coverage, use: `pytest --cov=src/data --cov=src/engine --cov=src/learner --cov=src/teacher`

`--cov` is used to specify which folders it should tests test coverage in.