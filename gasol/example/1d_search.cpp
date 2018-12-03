/*! \brief GASol example for searching the maxima of f(x) = x + 10sin(5x) + 7cos(4x)
 */

#include "mpiutils.h"
#include "engine.h"

#include <iostream>
#include <cmath>
#include <vector>
#include <utility>
#include <ctime>

using namespace gasol;

// Define fitness function. 
double fitness(const Individual & indv)
{
    double x = indv.solution()[0];
    return x + 10*std::sin(5*x) + 7*std::cos(4*x);
}

int main()
{
    MPIUtils::init();
    if (MPIUtils::isMaster())
    {
        std::cout << "Process number: " << MPIUtils::size() << std::endl;
    }
    // Variable range.
    std::vector<std::pair<double, double>> ranges {{0.0, 100.0}};
    // Decrete precision.
    std::vector<double> precisions {0.001};

    // Create population.
    size_t size = 1000;
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

    // Run 100 generations.
    time_t start = time(NULL);
    engine.run(100);
    time_t end = time(NULL);

    const Individual & best_indv = engine.population().bestIndv();
    double best_fitness = engine.population().fitness()(best_indv);
    double solution = best_indv.solution()[0];

    if (MPIUtils::isMaster())
    {
        std::cout << "Solution: " << solution << ", fitness: " << best_fitness << std::endl;
        std::cout << "Time used: " << end - start << "s" << std::endl;
    }

    MPIUtils::finalize();

    return 0;
}

