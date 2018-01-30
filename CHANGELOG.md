## Version: 0.5.4
### Date: 2018-01-30
1. Fixed important bugs in individual clone.

## Version: 0.5.3
### Date: 2018-01-15
1. Removed redundant calling of fitness function in iteration.
2. Improved the efficiency.

## Version: 0.5.2
### Date: 2017-12-15
1. Removed verboisty parameter for `BinaryIndividual` class.
2. Added unittest for decimal individual.

## Version: 0.5.1
### Date: 2017-12-13
1. Added `DecimalIndividual` class.
2. Added decimal encoding individual support for flip bit mutation classes.
3. Fixed some bugs.

## Version: 0.5.0
### Date: 2017-12-12
1. Changed class names:
    - `GAIndividual` -> `BinaryIndividual`
    - `GAPopulation` -> `Population`
    - `GASelection` -> `Selection`
    - `GACrossover` -> `Crossover`
    - `GAMutation` -> `Mutation`
    - `variants` -> `solution`

2. Added abstract Individual base class `IndividualBase`:
    - Users can inherit the `IndividualBase` class and add implementations of `encode` and `decode` methods to define you own custom individual class with different encoding methods.
