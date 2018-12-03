/*! \file  individual.h
 *  \brief File for the GAIndividual class definition
 */

#ifndef __INDIVIDUAL__
#define __INDIVIDUAL__

#include <vector>
#include <utility>
#include <cstddef>

namespace gasol {

    // Type alias.
    using RangePairs = std::vector<std::pair<double, double>>;
    using GeneBreakPts = std::vector<std::pair<int, int>>;

    /*! \brief Class for defining an individual in genetic algorithm engine.
     */
    class Individual {

    public:
        /*! \brief Constructor for the genetic algorithm individual.
         * 
         *  \param solution: A possible solution vector in the solution space
         *                   where genetic algorithm runs.
         *  \param ranges: The value ranges for all components in solution candidate vector.
         *  \param precisions: The discrete precisions for all components in solution
         *                     candidate vector
         */
        Individual(std::vector<double> & solution,
                   const RangePairs & ranges,
                   const std::vector<double> & precisions);

        /*! \brief Another constructor for the genetic algorithm individual.
         * 
         *  \param solution: A possible solution vector in the solution space
         *                   where genetic algorithm runs.
         *  \param range: The value range for all components in solution candidate vector.
         *  \param precision: The discrete precision for all components in solution
         *                    candidate vector
         */
        Individual(std::vector<double> & solution,
                   const std::pair<double, double> & range,
                   double precision);

        /*! \brief Constructor without solution provided explicitly (solution is
         *         generated randomly).
         *  \param ranges: The value ranges for all components in solution candidate vector.
         *  \param precisions: The discrete precisions for all components in solution
         *                     candidate vector
         */
        Individual(const RangePairs & ranges,
                   const std::vector<double> & precisions);

        /*! \brief Another constructor without solution provided explicitly
         *         (solution is generated randomly).
         *  \param ndim: The dimension number of solution vector.
         *  \param range: The value range for all components in solution candidate vector.
         *  \param precision: The discrete precision for all components in solution
         *                    candidate vector
         */
        Individual(size_t ndim,
                   const std::pair<double, double> & range,
                   double precision);

        /*! \brief Flip a bit in chromsome bit sequence.
         */
        void flipGeneBit(int index)
        { chromsome_.at(index) = !chromsome_.at(index); }

        /*! \brief Helper funciton to update solution vector according to chromsome.
         */
        void updateSolution();

        /*! \brief Query function for original solution candidate.
         */
        const std::vector<double> & oriSolution() const
        { return ori_solution_; }

        /*! \brief Query function for solution candidate.
         */
        const std::vector<double> & solution() const { return solution_; }

        /*! \brief Query function for ranges.
         */
        const RangePairs & ranges() const
        { return ranges_; }

        /*! \brief Query function for original discrete precisions.
         */
        const std::vector<double> & originalPrecisions() const
        { return ori_precisions_; }

        /*! \brief Query function for precision loss flag.
         */
        bool precisionLoss() const
        { return precision_loss_; }

        /*! \brief Query function for gene lengths.
         */
        const std::vector<int> & geneLengths() const
        { return gene_lengths_; }

        /*! \brief Query function for gene fragment break points.
         */
        const GeneBreakPts & geneBreakPts() const
        { return gene_break_pts_; }

        /*! \brief Query function for discrete precisions.
         */
        const std::vector<double> & precisions() const
        { return precisions_; }

        /*! \brief Query function for chromsome sequence.
         */
        const std::vector<bool> & chromsome() const
        { return chromsome_; }

    protected:

    private:
        /// Original solution candidate provided by user.
        std::vector<double> ori_solution_;

        /// Solution candidate vector.
        std::vector<double> solution_;

        /// Ranges for all components in solution vector.
        RangePairs ranges_;

        /// Original discrete precisions for all components in solution.
        std::vector<double> ori_precisions_;

        /// Actual dsicrete precisions used in GA engine.
        std::vector<double> precisions_;

        /// Lengths of gene fragments.
        std::vector<int> gene_lengths_;

        /// The break points in gene sequence.
        GeneBreakPts gene_break_pts_;

        /// The chromsome contains gene sequence.
        std::vector<bool> chromsome_;

        /// Flag for precision loss.
        bool precision_loss_ = false;

        // ---------------------------------------------------------------------
        // Private functions
        // ---------------------------------------------------------------------

        /*! \brief Helper function to calculate gene fragment lengths for all
         *         components in solution.
         */
        void __calcGeneLengths();

        /*! \brief Helper function to adjust discrete precisions according to
         *         user-provided precisions and ranges.
         */
        void __adjustPrecisions();

        /*! \brief Helper function to create chromsome.
         */
        void __createChromsome();

        /*! \brief Function to convert a decimal number to binary one.
         *  \param decimal: The decimal number to be converted.
         *  \param floor: The floor of this decimal number. 
         *  \param precision: Precision for this component.
         *  \param length: The length of the gene fragement.
         */
        std::vector<bool> __decToBin(double decimal,
                                     double floor,
                                     double precision,
                                     int length) const;

        /*! \brief Function to convert a binary number to decimal number.
         *  \param binary: The binary number to be converted.
         *  \param floor: The floor of this component. 
         *  \param precision: Precision for this component.
         *  \param length: The length of the gene fragement.
         */
        double __binToDec(const std::vector<bool> & binary,
                          double floor,
                          double precision,
                          int length) const;
    };

}

#endif  // __INDIVIDUAL__

