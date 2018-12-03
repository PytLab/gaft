/* File for implementations of selection operators functions.
 */

#include "individual.h"
#include "population.h"
#include "selection.h"

#include <random>
#include <algorithm>

namespace gasol {

    //--------------------------------------------------------------------------
    //
    Parents RouletteWheelSelection::select(Population & population)
    {
        // Create a fitness wheel roulette.
        std::vector<double> all_fits = population.allFitVals();
        const Individual & worst_indv = population.worstIndv();
        double min_fit = population.fitness()(worst_indv);

        std::vector<double> wheel;
        double accum = 0.0;
        for (auto fit: all_fits)
        {
            accum += (fit - min_fit);
            wheel.push_back(accum);
        }

        // Create a random number generator.
        std::mt19937 gen(seed());
        std::uniform_real_distribution<double> dis(0.0, accum);

        // Select parents.
        int father_idx = (std::upper_bound(wheel.cbegin(),
                                           wheel.cend(),
                                           dis(gen)) - wheel.cbegin()) % wheel.size();

        int mother_idx = (std::upper_bound(wheel.cbegin(),
                                           wheel.cend(),
                                           dis(gen)) - wheel.cbegin()) % wheel.size();

        return Parents(population.indvPtrs()[father_idx],
                       population.indvPtrs()[mother_idx]);
    }

}

