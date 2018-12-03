# GASol

A general **G**enetic **A**lgorithm **Sol**ver in C++ 

## Build

#### Clone GASol

``` shell
git clone --recursive git@github.com:PytLab/GASol.git
```

#### Create dir for building.

``` shell
cd GASol
mkdir build
cd build
```
#### Build GASol

- Serial version
``` shell
cmake ..
make
```

- MPI parallel version
```
export CXX=/<mpi_path>/mpicxx
cmake -DMPI=true ..
make
```

#### Run test
``` shell
make unittest
./unittest/unittest
```
#### Run example

``` shell
make example
./example/example
```

## Quick start

#### Find the maxima of f(x) = x + 10sin(5x) + 7cos(4x)

``` cpp
#include "mpiutils.h"
#include "engine.h"

#include <cmath>
#include <vector>
#include <utility>

using namespace gasol;

// Define fitness function. 
double fitness(const Individual & indv)
{
    double x = indv.solution()[0];
    return x + 10*std::sin(5*x) + 7*std::cos(4*x);
}

int main()
{
    // Initialize MPI environment.
    MPIUtils::init();
    // Variable range.
    std::vector<std::pair<double, double>> ranges {{0.0, 10.0}};
    // Decrete precision.
    std::vector<double> precisions {0.001};

    // Create population.
    size_t size = 50;
    std::vector<Individual> individuals;
    for (size_t i = 0; i < size; i++)
    {
        gasol::Individual indv(ranges, precisions);
        individuals.push_back(indv);
    }
    Population population(individuals, &fitness);

    // Genetic operators.
    RouletteWheelSelection selection;
    UniformCrossover crossover(0.8, 0.5);
    FlipBitMutation mutation(0.1);

    // Create engine.
    Engine engine(population, selection, crossover, mutation);

    // Run 1000 generations.
    engine.run(1000);

    // Finalize MPI env.
    MPIUtils::finalize();

    return 0;
}
```

