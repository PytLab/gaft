/*! brief File for crossover operators definitions.
 */

#ifndef __CROSSOVER__
#define __CROSSOVER__

#include <utility>
#include <random>

namespace gasol {

    // Forward declarations.
    class Individual;

    // Type alias.
    using Parents = std::pair<const Individual *, const Individual *>;

    /*! \brief Abstract base class for crossover operator.
     */
    class Crossover {
    public:
        /* \brief Constructor.
         * \param pc: Crossover probability.
         * \param seed: Random seed for the crossover operator. If seed < 0, then
         *              the random function would be used to generate a seed.
         */
        Crossover(double pc, int seed = -1) : pc_(pc)
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

        /*! \brief Pure virtual funciton for crossover operation on parents.
         *  \param parents: A pair of Individual pointers pointing to parents.
         */
        virtual std::pair<Individual, Individual> cross(Parents & parents) const = 0;

        /*! \brief Query function for random seed.
         */
        int seed() const { return seed_; }

        /*! \brief Query function for crossover probability.
         */
        int pc() const { return pc_; }

    protected:

    private:
        /// Random seed.
        int seed_;

        /// The probability of crossover.
        double pc_;
    };


    /* \brief Crossover operator implementation using uniform crossover algorithm.
     *        https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
     */
    class UniformCrossover : public Crossover {

    public:
        /* \brief Constructor for uniform crossover operator.
         * \param pc: The crossover probability, usually between 0.25 ~ 1.0
         * \param pe: The gene exchange probability.
         */
        UniformCrossover(double pc, double pe = 0.5, int seed = -1) :
            Crossover(pc, seed),
            pe_(pe)
        {}

        /*! \brief Crossover operation.
         *  \param parents: A pair of individual pointers as parent.
         */
        std::pair<Individual, Individual> cross(Parents & parents) const;

        /*! \brief Query function for gene exchange probability.
         */
        double pe() const { return pe_; }

    private:
        /// The probability of gene exchanging.
        double pe_;
    };
}

#endif  // __CROSSOVER__

