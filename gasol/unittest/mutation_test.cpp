/*! \brief Unittest for mutation operatiors.
 */ 
#include "individual.h"
#include "mutation.h"
#include "gtest/gtest.h"


namespace {

class MutationTest : public ::testing::Test {

protected:
    virtual void SetUp() {}

    virtual void TearDown() {}

    // Individuals used in tests.
    gasol::RangePairs ranges_ {{0.0, 1.0}, {1.0, 2.0}};
    std::vector<double> precisions_ {0.125, 0.25};

    std::vector<double> solution_ {1.0, 1.75};
    gasol::Individual ref_indv_ = gasol::Individual(solution_, ranges_, precisions_);
};

TEST_F(MutationTest, FlipBigMuatation)
{
    // Test mutation with probability 1.0
    gasol::FlipBitMutation m1(1.0);
    gasol::Individual indv(ref_indv_);
    m1.mutate(indv);

    for (size_t i = 0; i < indv.chromsome().size(); i++)
    {
        EXPECT_NE(ref_indv_.chromsome()[i], indv.chromsome()[i]);
    }

    // Test mutation with mutation probability with 0.0
    gasol::FlipBitMutation m2(0.0);
    indv = ref_indv_;
    m2.mutate(indv);

    for (size_t i = 0; i < indv.chromsome().size(); i++)
    {
        EXPECT_EQ(ref_indv_.chromsome()[i], indv.chromsome()[i]);
    }
}

} // namespace

