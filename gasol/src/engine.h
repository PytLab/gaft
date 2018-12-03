/*! \file engine.h
 *  \brief File for GA engine definition.
 */

#ifndef __ENGINE__
#define __ENGINE__

#include "population.h"
#include "individual.h"
#include "selection.h"
#include "crossover.h"
#include "mutation.h"

namespace gasol {
    
    /*! \brief The Genetic Algorithm engine class is the central object in GASol
     *         for running a genetic algorithm optimization. Once the poputlation
     *         with individuals and a set of genetic operators are setup, the engine
     *         unites them all and provides means for runing genetic algorithm
     *         optimization.
     */
    class Engine {

    public:
        /*! \brief Constructor.
         *  \param population: Population object contains different individuals.
         *  \param selection: The selection operator to select two candidates for
         *                    producing offsprings.
         *  \param crossover: The crossover operator to cross two selected individuals.
         *  \param mutation: The mutation operator to make an individual mutate.
         */ 
        Engine(Population & population, Selection & selection,
               Crossover & crossover, Mutation & mutation) :
            population_(population),
            selection_(selection),
            crossover_(crossover),
            mutation_(mutation)
        {}

        /*! \brief Bootup the engine to run genetic algorithm optimization.
         *  \param ng: Generation number for genetic algorithm iteration.
         */
        void run(int ng = 100);

        /*! \brief Query function for population.
         */
        Population & population() { return population_; }

        /*! \brief Query function for selection operator.
         */
        const Selection & selection() const { return selection_; }

        /*! \brief Query function for crossover operator.
         */
        const Crossover & crossover() const { return crossover_; }

        /*! \brief Query function for crossover operator.
         */
        const Mutation & mutation() const { return mutation_; }

    protected:

    private:
        /// Population in genetic algorithm engine.
        Population & population_;

        /// Selection operator.
        Selection & selection_;

        /// Crossover operator.
        Crossover & crossover_;

        /// Mutation operator.
        Mutation & mutation_;

        /// Private helper function to create a 2D solution matrix which is passed
        /// within MPI communicator.
        double ** __getSolutionMatrix(int nrows, int ncols);

    };
}

#endif  // __ENGINE__

