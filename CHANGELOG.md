## Version: 0.5.0
### Date: 2017-12-12
1. Changed class names:
    - `GAIndividual` -> `BinaryIndividual`
    - `GAPopulation` -> `Population`
    - `GASelection` -> `Selection`
    - `GACrossover` -> `Crossover`
    - `GAMutation` -> `Mutation`

2. Added abstract Individual base class `IndividualBase`:
    Users can inherit the `IndividualBase` class and add implementations of `encode` and `decode` methods to define you own custom individual class with different encoding methods.
