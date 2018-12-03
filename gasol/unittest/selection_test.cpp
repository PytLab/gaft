/*! \brief Unittest for Population class
 */ 
#include "population.h"
#include "individual.h"
#include "selection.h"
#include "gtest/gtest.h"


namespace {

double fitness(const gasol::Individual & indv)
{ return indv.solution()[0]*indv.solution()[1]; }

class SelectionTest : public ::testing::Test {

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

    std::vector<double> solution3_ {0.5, 2.0};
    gasol::Individual indv3_ = gasol::Individual(solution3_, ranges_, precisions_);

    // Fitness function pointer.
    gasol::Fitness *pfit_ = &fitness;
};

TEST_F(SelectionTest, RouletteWheelSelection)
{
    std::vector<gasol::Individual> indvs {indv1_, indv2_, indv3_};
    gasol::Population population(indvs, pfit_);

    // Select parents.
    gasol::RouletteWheelSelection selection(0);
    gasol::Parents parents1 = selection.select(population);
    const gasol::Individual *father1 = parents1.first;
    const gasol::Individual *mother1 = parents1.second;
    EXPECT_DOUBLE_EQ(fitness(*father1), 1.75);
    EXPECT_DOUBLE_EQ(fitness(*mother1), 1.3125);

    // Select again, should be the same.
    gasol::Parents parents2 = selection.select(population);
    const gasol::Individual *father2 = parents2.first;
    const gasol::Individual *mother2 = parents2.second;
    EXPECT_DOUBLE_EQ(fitness(*father2), 1.75);
    EXPECT_DOUBLE_EQ(fitness(*mother2), 1.3125);

    // Select with no seed provided.
    gasol::RouletteWheelSelection selection2(-1);
    selection2.select(population);
}

} // namespace

