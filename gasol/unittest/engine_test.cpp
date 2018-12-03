/*! \brief Unittest for GA engine.
 */ 

#include "engine.h"
#include "mpiutils.h"
#include "gtest/gtest.h"

#include <cmath>
#include <random>
#include <iostream>


namespace {

double fitness(const gasol::Individual & indv)
{ 
    double x = indv.solution()[0];
    return x + 10*std::sin(5*x) + 7*std::cos(4*x);
}

class EngineTest : public ::testing::Test {

protected:
    virtual void SetUp()
    {
        int size = 50;
        for (int i = 0; i < size; i++)
        {
            gasol::Individual indv(ranges_, precisions_);
            individuals_.push_back(indv);
        }
    }

    virtual void TearDown() {}

    // Individuals used in tests.
    std::vector<std::pair<double, double>> ranges_ {{0.0, 10.0}};
    std::vector<double> precisions_ = {0.001};
    std::vector<gasol::Individual> individuals_;
};

TEST_F(EngineTest, Run)
{
    gasol::Population population(individuals_, &fitness);
    gasol::RouletteWheelSelection selection;
    gasol::UniformCrossover crossover(0.8, 0.5);
    gasol::FlipBitMutation mutation(0.1);

    gasol::Engine engine(population, selection, crossover, mutation);
    gasol::MPIUtils::init();
    engine.run(100);
    gasol::MPIUtils::finalize();

//    std::cout << "best fitness: "
//              << engine.population().fitness()(engine.population().bestIndv())
//              << std::endl;
}

} // namespace

