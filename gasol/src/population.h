/*! \file  population.h
 *  \brief File for Population class definition.
 */

#ifndef __POPULATION__
#define __POPULATION__


#include <vector>
#include <cstddef>

namespace gasol {

    // Forward declaration.
    class Individual;

    // Type alias of a fitness function.
    using Fitness = double (const Individual &);

    /*! \brief Class for population iterated in genetic algorithm engine.
     */
    class Population {

    public:
        /*! \brief Constructor for population with multiple individuals.
         *  \param individuals: List of individuals in population.
         *  \param pfit: Pointer of fitness function.
         */
        Population(std::vector<Individual> & individuals, Fitness *pfit);

        /*! \brief Constructor with an individual template proviede.
         */
        Population(const Individual & indv_template, size_t size, Fitness *pfit);

        /*! \brief Update individuals in population.
         *  \param indvs: New individuals.
         */
        void updateIndividuals(const std::vector<Individual> & indvs);

        /*! \brief Query function for population size.
         */
        int size() const { return size_; }

        /*! \brief Query function for fitness function.
         */
        Fitness *fitness() const { return pfit_; }

        /*! \brief Query function for all individuals.
         */
        const std::vector<Individual> & indvs() const { return indvs_; }

        /*! \brief Const query function for individual pointers.
         */
        const std::vector<Individual *> & indvPtrs() const { return indv_ptrs_; }

        /*! \brief Query function for individual pointers.
         */
        std::vector<Individual *> & indvPtrs() { return indv_ptrs_; }

        /*! \brief Return reference of the individual with max fitness value.
         */
        const Individual & bestIndv();

        /*! \brief Query function for the individual with min fitness value.
         */
        const Individual & worstIndv();

        /*! \brief Get all fitness values of individuals in population.
         *  NOTE: The order of returned fitness values is the same with that
         *        of individuals pointer in population.
         */
        std::vector<double> allFitVals() const;

    private:

        /// Individuals in population.
        std::vector<Individual> indvs_;

        /// Pointers pointing to all individuals.
        std::vector<Individual *> indv_ptrs_;

        /// Fitness function pointer.
        Fitness *pfit_ = nullptr;

        /// Population size.
        size_t size_;

        /// Pointer of the best individual.
        const Individual *best_indv_ = nullptr;

        /// Pointer of the worst individual.
        const Individual *worst_indv_ = nullptr;
    };
}

#endif  // __POPULATION__

