/*! \file engine.cpp
 *  \brief Implementations for genetic algorithm engine.
 */

#include "mpiutils.h"
#include "engine.h"

#include <iostream>

namespace gasol {

    //--------------------------------------------------------------------------
    //
    double ** Engine::__getSolutionMatrix(int nrows, int ncols)
    {
        double * data = new double[nrows*ncols]();
        double ** matrix = new double*[nrows];

        for (int i = 0; i < nrows; i++)
        {
            matrix[i] = &(data[ncols*i]);
        }

        return matrix;
    }

    //--------------------------------------------------------------------------
    //
    void Engine::run(int ng)
    {
        // Individuals collector in genetic algorithm generation.
        const Individual & indv_template = population_.indvs()[0];
        std::vector<Individual> individuals(population_.size(), indv_template);

        for (int g = 0; g < ng; g++)
        {
#if RUNMPI == true
            // Initialize solution component vector for MPI passing.
            int nrows = population_.size();
            int ncols = indv_template.solution().size();
            double **local_solutions = __getSolutionMatrix(nrows, ncols);
            double **global_solutions = __getSolutionMatrix(nrows, ncols);

            // Endpoints for population size spliting.
            std::pair<int, int> && endpts = MPIUtils::splitOverProcesses(population_.size()/2,
                                                                         MPI_COMM_WORLD);
#else
            std::pair<int, int> endpts(0, population_.size()/2);
#endif
#pragma omp parallel for schedule(static)
            for (int idx = endpts.first; idx < endpts.second; idx++)
            {
                // Indices for individuals in new individual list.
                int i = 2*idx, j = 2*idx + 1;

                // Select father and mother.
                Parents parents = selection_.select(population_);

                // Crossover.
                std::pair<Individual, Individual> && children = crossover_.cross(parents);

                // Mutation.
                mutation_.mutate(children.first);
                mutation_.mutate(children.second);

                // Add to individuals.
                individuals[i] = children.first;
                individuals[j] = children.second;
            }
#if RUNMPI == true
            // Fill the local solutions.
            int start = 2*endpts.first;
            int end = 2*endpts.second;
            for (int i = start; i < end; i++)
            {
                for (int j = 0; j < ncols; j++)
                {
                    local_solutions[i][j] = individuals[i].solution()[j];
                }
            }

            // Merge solutions from all processes.
            MPIUtils::joinOverProcesses(local_solutions,
                                        global_solutions,
                                        nrows, ncols,
                                        MPI_COMM_WORLD);

            // Initialize new individuals from gathered solutions.
            std::vector<double> solution(ncols, 0.0);
            for (int i = 0; i < nrows; i++)
            {
                for (int j = 0; j < ncols; j++)
                {
                    solution[j] = global_solutions[i][j];
                }
                individuals[i] = Individual(solution,
                                            indv_template.ranges(),
                                            indv_template.precisions());
            }

            // Free memories.
            delete [] *local_solutions;
            delete [] local_solutions;
            delete [] *global_solutions;
            delete [] global_solutions;
#endif
            // Reserve the best indv.
            individuals[0] = population_.bestIndv();

            // Update population.
            population_.updateIndividuals(individuals);
        }
    }
}

