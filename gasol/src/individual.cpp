/*! \file individual.cpp
 *  \brief File for implementations of GAIndividual class.
 */

#include <cmath>
#include <random>
#include <cstddef>

#include "individual.h"

namespace gasol {
    //--------------------------------------------------------------------------
    //
    Individual::Individual(std::vector<double> & solution,
                           const RangePairs & ranges,
                           const std::vector<double> & precisions) :
        ori_solution_(solution),
        solution_(solution.size(), 0.0),
        ranges_(ranges),
        ori_precisions_(precisions)
    {
        // Calculate lengths of all gene fragments.
        __calcGeneLengths();
        // Get actual precisions which is used in GA engine.
        __adjustPrecisions();
        // Create chromsome.
        __createChromsome();
        // Update solution candiate according to chromsome.
        updateSolution();
    }

    //--------------------------------------------------------------------------
    //
    Individual::Individual(std::vector<double> & solution,
                           const std::pair<double, double> & range,
                           double precision) :
        Individual(solution,
                   RangePairs(solution.size(), range),
                   std::vector<double>(solution.size(), precision))
    {}

    //--------------------------------------------------------------------------
    //
    Individual::Individual(const RangePairs & ranges,
                           const std::vector<double> & precisions) :
        ori_solution_(ranges.size(), 0.0),
        solution_(ranges.size(), 0.0),
        ranges_(ranges),
        ori_precisions_(precisions)
    {
        // Generate original solution randomly.
        std::random_device rd;
        std::mt19937 gen(rd());
        for (size_t i = 0; i < ori_solution_.size(); i++)
        {
            std::uniform_real_distribution<double> dis(ranges[i].first, ranges[i].second);
            ori_solution_[i] = dis(gen);
        }

        // Calculate lengths of all gene fragments.
        __calcGeneLengths();
        // Get actual precisions which is used in GA engine.
        __adjustPrecisions();
        // Create chromsome.
        __createChromsome();
        // Update solution candiate according to chromsome.
        updateSolution();
    }

    //--------------------------------------------------------------------------
    //
    Individual::Individual(size_t ndim,
                           const std::pair<double, double> & range,
                           double precision) :
        Individual(RangePairs(ndim, range),
                   std::vector<double>(ndim, precision))
    {}

    //--------------------------------------------------------------------------
    //
    void Individual::__calcGeneLengths()
    {
        // Function to check an integer is the power of 2.
        auto power_of_2 = [](int n) { return !(n & (n - 1)); };

        // Calculate gene fragment lengths for all component in solution.
        auto range_it = ranges_.cbegin();
        auto prec_it = ori_precisions_.cbegin();

        // Gene fragment index cursor.
        int cursor = 0;

        for (; range_it != ranges_.end() && prec_it != ori_precisions_.end();
                range_it++, prec_it++)
        {
            double span = range_it->second - range_it->first;

            // The number of possible values for this component.
            // *****************************************************************
            // NOTE: EXCEPT the start point. For example, if precision is 0.2
            //       and range is [0.0, 1.0], then the n_info equals to 5 (5 numbers):
            //       0.2, 0.4, 0.6, 0.8, 1.0 not include 0.0
            // *****************************************************************
            int n_info = (int)(span/(*prec_it));

            if (!power_of_2(n_info))
            {
                precision_loss_ = true;
            }

            int length = (int)(std::log2(n_info));
            gene_lengths_.push_back(length);

            // Get gene fragment break points.
            int start = cursor;
            int end = cursor + length - 1;
            cursor += length;
            gene_break_pts_.push_back(std::pair<int, int>(start, end));
        }
    }

    //--------------------------------------------------------------------------
    //
    void Individual::__adjustPrecisions()
    {
        if (precision_loss_)
        {
            auto range_it = ranges_.cbegin();
            auto len_it = gene_lengths_.cbegin();

            for (; range_it != ranges_.end() && len_it != gene_lengths_.end();
                    range_it++, len_it++)
            {
                // Ajusted precision.
                double precision = (range_it->second - range_it->first)/std::pow(2, *len_it);
                precisions_.push_back(precision);
            }
        }
        else
        {
            precisions_ = ori_precisions_;
        }
    }

    //--------------------------------------------------------------------------
    //
    void Individual::__createChromsome()
    {
        for (size_t i = 0; i < ori_solution_.size(); i++)
        {
            // Get gene fragment.
            double decimal = ori_solution_[i];
            double floor = ranges_[i].first;
            double precision = precisions_[i];
            int length = gene_lengths_[i];
            std::vector<bool> && gene_fragment = __decToBin(decimal, floor, precision, length);

            // Append new gene fragment to chromsome.
            chromsome_.reserve(chromsome_.size() + gene_fragment.size());
            chromsome_.insert(chromsome_.end(),
                              gene_fragment.begin(),
                              gene_fragment.end());
        }
    }

    //--------------------------------------------------------------------------
    //
    std::vector<bool> Individual::__decToBin(double decimal,
                                             double floor,
                                             double precision,
                                             int length) const
    {
        std::vector<bool> binary;

        int ncount = (decimal - floor)/precision - 1;
        for (int i = length-1; i >= 0; i--)
        {
            binary.push_back( (ncount >> i) & 1 );
        }

        return binary;
    }

    //--------------------------------------------------------------------------
    //
    double Individual::__binToDec(const std::vector<bool> & binary,
                                  double floor,
                                  double precision,
                                  int length) const
    {
        int ncount = 0;
        for (int i = 0; i < length; i++)
        {
            int idx =  length - i - 1;
            ncount += int(binary[idx])*std::pow(2, i);
        }

        return floor + precision*(ncount + 1);
    }

    //--------------------------------------------------------------------------
    //
    void Individual::updateSolution()
    {
        for (size_t i = 0; i < solution_.size(); i++)
        {
            // Get gene fragment.
            int start = gene_break_pts_[i].first;
            int end = gene_break_pts_[i].second;
            std::vector<bool> gene_fragment;
            for (int j = start; j <= end; j++)
            {
                gene_fragment.push_back(chromsome_[j]);
            }

            // Convert to decimal number.
            double floor = ranges_[i].first;
            double precision = precisions_[i];
            int length = gene_lengths_[i];

            double component = __binToDec(gene_fragment, floor, precision, length);

            // Update.
            solution_[i] = component;
        }
    }
}  // namespace gasol

