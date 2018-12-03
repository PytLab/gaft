/*! \brief Unittest for Population class
 */ 
#include "population.h"
#include "individual.h"
#include "gtest/gtest.h"


namespace {

double fitness(const gasol::Individual & indv)
{ return indv.solution()[0]*indv.solution()[1]; }

class PopulationTest : public ::testing::Test {

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

TEST_F(PopulationTest, Construction)
{
    std::vector<gasol::Individual> indvs {indv1_, indv2_, indv3_};
    gasol::Population population(indvs, pfit_);

    // Check size.
    EXPECT_EQ(population.size(), 3);

    // Check one pointer.
    const auto indv_ptr = population.indvPtrs()[0];
    std::vector<bool> ref_chromsome {1, 1, 1, 1, 0};
    for (size_t i = 0; i < ref_chromsome.size(); i++)
    {
        EXPECT_EQ(ref_chromsome[i], indv_ptr->chromsome()[i]);
    }

    // Check fitness function.
    EXPECT_DOUBLE_EQ(population.fitness()(indv3_), 1.0);
}

TEST_F(PopulationTest, ConstructionWithTemplate)
{
    gasol::Population population(indv1_, 10, pfit_);

    EXPECT_EQ(population.indvs().size(), 10);
    EXPECT_EQ(population.indvPtrs().size(), 10);
    EXPECT_EQ(population.size(), 10);
    EXPECT_EQ(population.fitness(), pfit_);
}

TEST_F(PopulationTest, UpdateIndividuals)
{
    std::vector<gasol::Individual> indvs {indv1_, indv2_};
    gasol::Population population(indvs, pfit_);

    for (size_t i = 0; i < indv1_.oriSolution().size(); i++)
    {
        EXPECT_DOUBLE_EQ(population.indvPtrs()[0]->oriSolution()[i],
                         indv1_.oriSolution()[i]);
        EXPECT_DOUBLE_EQ(population.indvPtrs()[1]->oriSolution()[i],
                         indv2_.oriSolution()[i]);
    }
    std::vector<gasol::Individual> indvs2 {indv3_, indv1_};
    population.updateIndividuals(indvs2);
    for (size_t i = 0; i < indv1_.oriSolution().size(); i++)
    {
        EXPECT_DOUBLE_EQ(population.indvPtrs()[0]->oriSolution()[i],
                         indv3_.oriSolution()[i]);
        EXPECT_DOUBLE_EQ(population.indvPtrs()[1]->oriSolution()[i],
                         indv1_.oriSolution()[i]);
    }
}

TEST_F(PopulationTest, BestIndividual)
{
    std::vector<gasol::Individual> indvs {indv1_, indv2_, indv3_};
    gasol::Population population(indvs, pfit_);

    const gasol::Individual & best_indv = population.bestIndv();

    EXPECT_DOUBLE_EQ(best_indv.solution()[0], indv1_.solution()[0]);
    EXPECT_DOUBLE_EQ(best_indv.solution()[1], indv1_.solution()[1]);
}

TEST_F(PopulationTest, AllFitValues)
{
    std::vector<gasol::Individual> indvs {indv1_, indv2_, indv3_};
    gasol::Population population(indvs, pfit_);

    std::vector<double> && all_fits = population.allFitVals();
    std::vector<double> ref_all_fits = {1.75, 1.3125, 1.0};
    for (size_t i = 0; i < all_fits.size(); i++)
    {
        EXPECT_DOUBLE_EQ(ref_all_fits[i], all_fits[i]);
    }
}

TEST_F(PopulationTest, WorstIndividual)
{
    std::vector<gasol::Individual> indvs {indv1_, indv2_, indv3_};
    gasol::Population population(indvs, pfit_);

    const gasol::Individual & worst_indv = population.worstIndv();

    EXPECT_DOUBLE_EQ(worst_indv.solution()[0], indv3_.solution()[0]);
    EXPECT_DOUBLE_EQ(worst_indv.solution()[1], indv3_.solution()[1]);
}

} // namespace

