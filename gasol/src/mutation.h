/*! \brief File for mutation operators definition.
 */

#ifndef __MUTATION__
#define __MUTATION__

#include <random>

namespace gasol {

    // Forward declarations.
    class Individual;

    /*! brief Abstract base class for mutation operator.
     */
    class Mutation {

    public:
        /*! \brief Constructor.
         *  \param pm: The mutation probability.
         *  \param seed: Random seed for the crossover operator. If seed < 0, then
         *               the random function would be used to generate a seed.
         */
        Mutation(double pm, int seed = -1) : pm_(pm)
        {
            if (seed < 0)
            {
                std::random_device rd;
                seed_ = rd();
            }
            else
            {
                seed_ = seed;
            }
        }

        /*! \brief A pure virtual function to mutate an individual.
         *  \param indv: An individual to be mutated.
         */
        virtual void mutate(Individual & indv) const = 0;

        /*! \brief Query function for random seed.
         */
        int seed() const { return seed_; }

        /*! \brief Query function for mutation probability.
         */
        int pm() const { return pm_; }

    protected:

    private:
        /// Ranom seed.
        int seed_;

        /// Mutation probability.
        double pm_;
    };


    /*! \brief Mutation operator with flip bit mutation implementation.
     */
    class FlipBitMutation : public Mutation {

    public:
        /*! \brief Constructor.
         */
        FlipBitMutation(double pm, int seed = -1) : Mutation(pm, seed) {}

        /*! \brief Mutate an individual with flip bit method.
         */
        void mutate(Individual & indv) const;

    protected:

    private:

    };
}

#endif

