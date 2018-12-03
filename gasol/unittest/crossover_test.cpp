/*! \brief Unittest for crossover operatiors.
 */ 
#include "individual.h"
#include "crossover.h"
#include "gtest/gtest.h"


namespace {

class CrossoverTest : public ::testing::Test {

protected:
    virtual void SetUp() {}

    virtual void TearDown() {}

    // Individuals used in tests.
    gasol::RangePairs ranges_ {{0.0, 1.0}, {1.0, 2.0}};
    std::vector<double> precisions_ {0.125, 0.25};

    std::vector<double> solution1_ {1.0, 1.75};
    gasol::Individual indv1_ = gasol::Individual(solution1_, ranges_, precisions_);

    std::vector<double> solution2_ {0.875, 1.5};
    gasol::Individual indv2_ = gasol::Individual(solution2_, ranges_, precisions_);
};

TEST_F(CrossoverTest, UniformCrossover)
{
    gasol::Parents parents(&indv1_, &indv2_);

    // If crossover probability is 0.0, children should be the same with parents.
    gasol::UniformCrossover c1(0.0, 0.0, 1);
    std::pair<gasol::Individual, gasol::Individual> && children1 = c1.cross(parents);
    for (size_t i = 0; i < children1.first.chromsome().size(); i++)
    {
        EXPECT_EQ(children1.first.chromsome()[i], parents.first->chromsome()[i]);
    }
    for (size_t i = 0; i < children1.second.chromsome().size(); i++)
    {
        EXPECT_EQ(children1.second.chromsome()[i], parents.second->chromsome()[i]);
    }

    gasol::UniformCrossover c2(1.0, 1.0, 1);
    std::pair<gasol::Individual, gasol::Individual> && children2 = c2.cross(parents);

    // If crossover probability is 1.0, then there must be difference between children and parents.
    bool bit_different = false;
    for (size_t i = 0; i < children2.first.chromsome().size(); i++)
    {
        if (children2.first.chromsome()[i] != parents.first->chromsome()[i])
        {
            bit_different = true;
            break;
        }
    }
    EXPECT_TRUE(bit_different);

    bit_different = false;
    for (size_t i = 0; i < children2.second.chromsome().size(); i++)
    {
        if (children2.second.chromsome()[i] != parents.second->chromsome()[i])
        {
            bit_different = true;
            break;
        }
    }
    EXPECT_TRUE(bit_different);

    // Test crossover with no custom random seed.
    gasol::UniformCrossover c3(0.5, 0.5);
    c3.cross(parents);
}

} // namespace

