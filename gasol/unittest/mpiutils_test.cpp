/*! \brief Unittest for GA engine.
 */ 

#include "engine.h"
#include "mpiutils.h"
#include "gtest/gtest.h"

#include <cmath>


namespace {

#define M 2
#define N 3

using namespace gasol;

class MPIUtilsTest : public ::testing::Test {

protected:
    virtual void SetUp() {}

    virtual void TearDown() {}

    double ** getMatrix(int m, int n)
    {
        double *data = new double[m*n]();
        double **matrix = new double*[m]();

        for (int i = 0; i < m; i++)
        {
            matrix[i] = &data[i*n];
        }

        return matrix;
    }
};

TEST_F(MPIUtilsTest, MPIInterfaces)
{
    MPIUtils::init();
#if RUNMPI == true
    EXPECT_TRUE(MPIUtils::initialized());
#else
    EXPECT_FALSE(MPIUtils::initialized());
#endif
    EXPECT_GE(MPIUtils::size(), 1);

    MPIUtils::finalize();
    EXPECT_TRUE(MPIUtils::finalized());
}

TEST_F(MPIUtilsTest, SplitOverProcesses)
{
    MPIUtils::init();
    int size = 50;
#if RUNMPI == true
#else
    auto ret_break_pts = MPIUtils::splitOverProcesses(size);
    std::pair<int, int> ref_break_pts = {0, size};
    EXPECT_EQ(ref_break_pts.first, ret_break_pts.first);
    EXPECT_EQ(ref_break_pts.second, ret_break_pts.second);
#endif
    MPIUtils::finalize();
}

TEST_F(MPIUtilsTest, JoinOverProcesses)
{
    MPIUtils::init();

    double **send = getMatrix(3, 2);
    double **recv = getMatrix(3, 2);

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            send[i][j] = i + j + 1;
        }
    }

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            EXPECT_DOUBLE_EQ(recv[i][j], 0.0);
        }
    }

#if RUNMPI == true
#else
    MPIUtils::joinOverProcesses(send, recv, M, N);

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            EXPECT_DOUBLE_EQ(recv[i][j], send[i][j]);
        }
    }
#endif

    delete [] send[0];
    delete [] send;
    delete [] recv[0];
    delete [] recv;

    MPIUtils::finalize();
}

} // namespace

