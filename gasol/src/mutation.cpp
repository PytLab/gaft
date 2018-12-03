/*! brief File for implementations of mutation operators.
 */

#include "mutation.h"
#include "individual.h"

#include <random>

namespace gasol {

    //--------------------------------------------------------------------------
    //
    void FlipBitMutation::mutate(Individual & indv) const
    {
        // Create a random number generator.
        std::mt19937 gen(seed());
        std::uniform_real_distribution<double> dis(0.0, 1.0);

        if (dis(gen) < pm())
        {
            for (size_t i = 0; i < indv.chromsome().size(); i++)
            {
                if (dis(gen) < pm())
                {
                    indv.flipGeneBit(i);
                }
            }

            // Update solution vector.
            indv.updateSolution();
        }
    }
}

