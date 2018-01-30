====
GAFT
====

A **G**\ enetic **A**\ lgorithm **F**\ ramework in py\ **T**\ hon

.. image:: https://travis-ci.org/PytLab/gaft.svg?branch=master
    :target: https://travis-ci.org/PytLab/gaft
    :alt: Build Status

.. image:: https://img.shields.io/codecov/c/github/PytLab/gaft/master.svg
    :target: https://codecov.io/gh/PytLab/gaft
    :alt: Codecov

.. image:: https://landscape.io/github/PytLab/gaft/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PytLab/gaft/master
    :alt: Code Health

.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v0.5.4-blue.svg
    :target: https://pypi.python.org/pypi/gaft/
    :alt: versions


Introduction
------------

**GAFT** is a general Python Framework for genetic algorithm computation. It provides built-in genetic operators for target optimization and plugin interfaces for users to define your own genetic operators and on-the-fly analysis for algorithm testing.

**GAFT** is now accelerated using MPI parallelization interfaces. You can run it on your cluster in parallel with MPI environment.

Python Support
--------------

**GAFT** requires Python version 3.x (Python 2.x is not supported).

Installation
------------

1. Via pip::

    pip install gaft

2. From source::

    python setup.py install

See `INSTALL.md <https://github.com/PytLab/gaft/blob/master/INSTALL.md>`_ for more installation details.

Quick start
-----------

1. Importing
````````````

.. code-block:: python

    from gaft import GAEngine
    from gaft.components import BinaryIndividual, Population
    from gaft.operators import RouletteWheelSelection, UniformCrossover, FlipBitMutation

    # Analysis plugin base class.
    from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis

2. Define population
````````````````````

.. code-block:: python
    
    indv_template = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
    population = Population(indv_template=indv_template, size=50)
    population.init()  # Initialize population with individuals.

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
                      analysis=[FitnessStore])

5. Define and register fitness function
```````````````````````````````````````

.. code-block:: python

    @engine.fitness_register
    def fitness(indv):
        x, = indv.solution
        return x + 10*sin(5*x) + 7*cos(4*x)

or if you want to minimize it, you can add a minimization decorator on it

.. code-block:: python

    @engine.fitness_register
    @engine.minimize
    def fitness(indv):
        x, = indv.solution
        return x + 10*sin(5*x) + 7*cos(4*x)

6. Define and register an on-the-fly analysis (optional)
````````````````````````````````````````````````````````

.. code-block:: python

    @engine.analysis_register
    class ConsoleOutput(OnTheFlyAnalysis):
        master_only = True
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

Blogs(Chinese Simplified)
-------------------------
- `GAFT-一个使用Python实现的遗传算法框架 <http://pytlab.github.io/2017/07/23/gaft-%E4%B8%80%E4%B8%AA%E5%9F%BA%E4%BA%8EPython%E7%9A%84%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95%E6%A1%86%E6%9E%B6/>`_

- `使用MPI并行化遗传算法框架GAFT <http://pytlab.github.io/2017/08/02/%E4%BD%BF%E7%94%A8MPI%E5%B9%B6%E8%A1%8C%E5%8C%96%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95/>`_

- `遗传算法中几种不同选择算子的比较 <http://pytlab.github.io/2017/09/19/%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95%E4%B8%AD%E5%87%A0%E7%A7%8D%E4%B8%8D%E5%90%8C%E9%80%89%E6%8B%A9%E7%AE%97%E5%AD%90%E7%9A%84%E6%AF%94%E8%BE%83/>`_

- `遗传算法中适值函数的标定与大变异算法 <http://pytlab.github.io/2017/09/23/%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95%E4%B8%AD%E9%80%82%E5%80%BC%E5%87%BD%E6%95%B0%E7%9A%84%E6%A0%87%E5%AE%9A%E4%B8%8E%E5%A4%A7%E5%8F%98%E5%BC%82%E7%AE%97%E6%B3%95/>`_

- `遗传算法框架GAFT优化小记 <http://pytlab.github.io/2017/10/08/%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95%E6%A1%86%E6%9E%B6GAFT%E4%BC%98%E5%8C%96%E5%B0%8F%E8%AE%B0/>`_
- `机器学习算法实践-Platt SMO和遗传算法优化SVM <http://pytlab.github.io/2017/10/15/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E7%AE%97%E6%B3%95%E5%AE%9E%E8%B7%B5-Platt-SMO%E5%92%8C%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95%E4%BC%98%E5%8C%96SVM/>`_

TODO
----
1. ✅ Parallelization 
2. ✅ Add more built-in genetic operators with different algorithms
3. 🏃 Add C++ backend(See `GASol <https://github.com/PytLab/GASol>`_)

Obtain a copy
-------------

The GAFT framework is distributed under the GPLv3 license and can be obtained from the GAFT git repository or PyPI 

- https://github.com/PytLab/gaft
- https://pypi.python.org/pypi/gaft/

