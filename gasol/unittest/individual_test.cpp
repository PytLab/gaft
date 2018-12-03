/*! \brief File unittest for Individual class
 */

#include "individual.h"
#include "gtest/gtest.h"

namespace {

class IndividualTest : public ::testing::Test {
protected:
    virtual void SetUp()
    {
        solution_ = {1.0, 1.75};
        ranges_ = {{0.0, 1.0}, {1.0, 2.0}};
        precisions_ = {0.1, 0.2};
    }

    virtual void TearDown() {}

    // Data used in fixture.
    std::vector<double> solution_;
    gasol::RangePairs ranges_;
    std::vector<double> precisions_;
};

TEST_F(IndividualTest, ConstructionWithMultiVals)
{
    // {{{
    // Construct an individual.
    gasol::Individual indv(solution_, ranges_, precisions_);

    // Check solution candidate.
    for (size_t i = 0; i < solution_.size(); ++i)
    {
        double ref_component = solution_[i];
        double ret_component = indv.oriSolution()[i];
        EXPECT_DOUBLE_EQ(ref_component, ret_component);
    }

    // Check ranges.
    for (size_t i = 0; i < ranges_.size(); i++)
    {
        double ref_floor = ranges_[i].first;
        double ref_ceiling = ranges_[i].second;
        double ret_floor = indv.ranges()[i].first;
        double ret_ceiling = indv.ranges()[i].second;
        EXPECT_DOUBLE_EQ(ref_floor, ret_floor);
        EXPECT_DOUBLE_EQ(ref_ceiling, ret_ceiling);
    }

    // Check original precisions.
    for (size_t i = 0; i < precisions_.size(); i++)
    {
        double ref_prec = precisions_[i];
        double ret_prec = indv.originalPrecisions()[i];
        EXPECT_DOUBLE_EQ(ref_prec, ret_prec);
    }

    // Check gene fragment lengths.
    std::vector<int> ref_lengths = {3, 2};
    for (size_t i = 0; i < ref_lengths.size(); i++)
    {
        EXPECT_EQ(ref_lengths[i], indv.geneLengths()[i]);
    }

    // Check precision loss.
    EXPECT_TRUE(indv.precisionLoss());

    // Check actual precisions.
    std::vector<double> ref_precisions = {0.125, 0.25};
    for (size_t i = 0; i < ref_precisions.size(); i++)
    {
        EXPECT_DOUBLE_EQ(ref_precisions[i], indv.precisions()[i]);
    }

    // Check chromsome.
    std::vector<bool> ref_chromsome {1, 1, 1, 1, 0};
    for (size_t i = 0; i < ref_chromsome.size(); i++)
    {
        EXPECT_EQ(ref_chromsome[i], indv.chromsome()[i]);
    }

    // Check gene fragment break points.
    gasol::GeneBreakPts ref_break_pts = {{0, 2}, {3, 4}};
    for (size_t i = 0; i < ref_break_pts.size(); i++)
    {
        EXPECT_EQ(ref_break_pts[i].first, indv.geneBreakPts()[i].first);
        EXPECT_EQ(ref_break_pts[i].second, indv.geneBreakPts()[i].second);
    }

    // Check adjusted solution vector.
    std::vector<double> ref_solution {1.0, 1.75};
    for (size_t i = 0; i < ref_solution.size(); i++)
    {
        EXPECT_DOUBLE_EQ(ref_solution[i], indv.solution()[i]);
    }
    // }}}
}

TEST_F(IndividualTest, ConstructionWithSingleVal)
{
    // {{{
    // Construct an individual.
    std::vector<double> solution {1.0, 2.0};
    gasol::RangePairs ref_ranges {{0.0, 2.0}, {0.0, 2.0}};
    std::vector<double> ref_precisions {0.001, 0.001};
    std::pair<double, double> range {0.0, 2.0};
    double precision = 0.001;
    gasol::Individual indv(solution, range, precision);

    // Check solution candidate.
    for (size_t i = 0; i < solution.size(); ++i)
    {
        double ref_component = solution[i];
        double ret_component = indv.oriSolution()[i];
        EXPECT_DOUBLE_EQ(ref_component, ret_component);
    }

    // Check ranges.
    for (size_t i = 0; i < ref_ranges.size(); i++)
    {
        double ref_floor = ref_ranges[i].first;
        double ref_ceiling = ref_ranges[i].second;
        double ret_floor = indv.ranges()[i].first;
        double ret_ceiling = indv.ranges()[i].second;
        EXPECT_DOUBLE_EQ(ref_floor, ret_floor);
        EXPECT_DOUBLE_EQ(ref_ceiling, ret_ceiling);
    }

    // Check precisions.
    for (size_t i = 0; i < ref_precisions.size(); i++)
    {
        double ref_prec = ref_precisions[i];
        double ret_prec = indv.originalPrecisions()[i];
        EXPECT_DOUBLE_EQ(ref_prec, ret_prec);
    }
    // }}}
}

TEST_F(IndividualTest, ConstructionWithRandomSolution)
{
    gasol::Individual indv1(ranges_, precisions_);
    gasol::Individual indv2(ranges_, precisions_);

    // Two individuals should be different.
//    bool different = false;
//    for (size_t i = 0; i < indv1.chromsome().size(); i++)
//    {
//        if (indv1.chromsome()[i] != indv2.chromsome()[i])
//        {
//            different = true;
//            break;
//        }
//    }
//
//    EXPECT_TRUE(different);
}

TEST_F(IndividualTest, GeneBitFlip)
{
    // {{{
    gasol::Individual indv(solution_, ranges_, precisions_);
    std::vector<bool> chromsome_before = {1, 1, 1, 1, 0};
    for (size_t i = 0; i < chromsome_before.size(); i++)
    {
        EXPECT_EQ(chromsome_before[i], indv.chromsome()[i]);
    }

    // Flip one bit in chromsome.
    indv.flipGeneBit(2);
    std::vector<bool> chromsome_after = {1, 1, 0, 1, 0};
    for (size_t i = 0; i < chromsome_after.size(); i++)
    {
        EXPECT_EQ(chromsome_after[i], indv.chromsome()[i]);
    }
    // }}}
}

} // namespace

