====
GAFT
====

A **G**\ enetic **A**\ lgorithm **F**\ ramework in py\ **T**\ hon

.. image:: https://travis-ci.org/PytLab/gaft.svg?branch=master
    :target: https://travis-ci.org/PytLab/gaft
    :alt: Build Status

.. image:: https://codecov.io/gh/PytLab/gaft/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/PytLab/gaft

.. image:: https://landscape.io/github/PytLab/gaft/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PytLab/gaft/master
    :alt: Code Health

.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v0.2.3-blue.svg
    :target: https://pypi.python.org/pypi/gaft/
    :alt: versions


Introduction
------------

**gaft** is a Python Framework for genetic algorithm computation. It provide built-in genetic operators for genetic algorithm optimization and plugin interfaces for users to define your own genetic operators and on-the-fly analysis for algorithm testing.

**gaft** is now accelerated using MPI parallelization interfaces. You can run it on your cluster in parallal with MPI environment.

Installation:
-------------

1. Via pip::

    pip install gaft

2. From source::

    python setup.py install

Example:
--------

1. Importing
````````````

.. code-block:: python

    from gaft import GAEngine
    from gaft.components import GAIndividual
    from gaft.components import GAPopulation
    from gaft.operators import RouletteWheelSelection
    from gaft.operators import UniformCrossover
    from gaft.operators import FlipBitMutation

    # Analysis plugin base class.
    from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis

2. Define population
````````````````````

.. code-block:: python
    
    indv_template = GAIndividual(ranges=[(0, 10)], encoding='binary', eps=0.001)
    population = GAPopulation(indv_template=indv_template, size=50)

3. Create genetic operators
```````````````````````````

.. code-block:: python

    # Use built-in operators here.
    selection = RouletteWheelSelection()
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    mutation = FlipBitMutation(pm=0.1)

4. Create genetic algorithm engine to run optimization
``````````````````````````````````````````````````````

.. code-block:: python

    engine = GAEngine(population=population, selection=selection,
                      crossover=crossover, mutation=mutation,
                      analysis=[FitnessStoreAnalysis])

5. Define and register fitness function
```````````````````````````````````````

.. code-block:: python

    @engine.fitness_register
    def fitness(indv):
        x, = indv.variants
        return x + 10*sin(5*x) + 7*cos(4*x)

6. Define and register an on-the-fly analysis (optional)
````````````````````````````````````````````````````````

.. code-block:: python

    @engine.analysis_register
    class ConsoleOutputAnalysis(OnTheFlyAnalysis):
        interval = 1
        def register_step(self, ng, population, engine):
            best_indv = population.best_indv(engine.fitness)
            msg = 'Generation: {}, best fitness: {:.3f}'.format(ng, engine.fitness(best_indv))
            engine.logger.info(msg)

7. Run
``````

.. code-block:: python

    if '__main__' == __name__:
        engine.run(ng=100)

8. Evolution curve
``````````````````

.. image:: https://github.com/PytLab/gaft/blob/master/examples/ex01/envolution_curve.png

9. Optimization animation
`````````````````````````

.. image:: https://github.com/PytLab/gaft/blob/master/examples/ex01/animation.gif

See `example 01 <https://github.com/PytLab/gaft/blob/master/examples/ex01/ex01.py>`_ for a one-dimension search for the global maximum of function `f(x) = x + 10sin(5x) + 7cos(4x)`

Global maximum search for binary function
-----------------------------------------

.. image:: https://github.com/PytLab/gaft/blob/master/examples/ex02/surface_animation.gif

See `example 02 <https://github.com/PytLab/gaft/blob/master/examples/ex02/ex02.py>`_ for a two-dimension search for the global maximum of function `f(x) = y*sin(2*pi*x) + x*cos(2*pi*y)`

Plugins
-------

You can define your own genetic operators for GAFT and run your algorithm test.

The plugin interfaces are defined in `/gaft/plugin_interfaces/ <https://github.com/PytLab/gaft/tree/master/gaft/plugin_interfaces>`_, you can extend the interface class and define your own analysis class or genetic operator class. The `built-in operators <https://github.com/PytLab/gaft/tree/master/gaft/operators>`_ and `built-in on-the-fly analysis <https://github.com/PytLab/gaft/tree/master/gaft/analysis>`_ can be treated as an official example for plugins development.

TODO
----
1. ✅ Parallelization 
2. 🏃 Add more built-in genetic operators with different algorithms (-)
3. 🏃 Add C++ backend (-)

