/*! \brief Implementations of uniform crossover operator.
 */

#include "individual.h"
#include "crossover.h"

#include <random>
#include <cstddef>

namespace gasol {

    //--------------------------------------------------------------------------
    //
    std::pair<Individual, Individual> UniformCrossover::cross(Parents & parents) const
    {
        const Individual *father = parents.first;
        const Individual *mother = parents.second;

        // Children to return.
        Individual child1(*father);
        Individual child2(*mother);

        // Create a random number generator.
        std::mt19937 gen(seed());
        std::uniform_real_distribution<double> dis(0.0, 1.0);

        double rnd = dis(gen);
        if (rnd > pc())
        {
            return std::pair<Individual, Individual>(child1, child2);
        }
        else
        {
            for (size_t i = 0; i < child1.chromsome().size(); i++)
            {
                if (child1.chromsome()[i] != child2.chromsome()[i])
                {
                    child1.flipGeneBit(i);
                    child2.flipGeneBit(i);
                }
            }
            return std::pair<Individual, Individual>(child1, child2);
        }
    }
}

