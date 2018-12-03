/*! \file  mpiutils.cpp
 *  \brief File for the implementation code of the common MPI routines.
 */


#include "mpiutils.h"
#include <vector>

namespace gasol {

// -----------------------------------------------------------------------------
//
void MPIUtils::init()
{
    if (initialized())
    {
        return;
    }

#if RUNMPI == true
    int argc = 0;
    char **argv;
    MPI_Init(&argc, &argv);
#endif
}


// -----------------------------------------------------------------------------
//
bool MPIUtils::finalized()
{
#if RUNMPI == true
    int flag = 0;
    return MPI_Finalized(&flag);
#else
    return true;
#endif
}


// -----------------------------------------------------------------------------
//
bool MPIUtils::initialized()
{
#if RUNMPI == true
    int flag = 0;
    return MPI_Initialized(&flag);
#else
    return false;
#endif
}


// -----------------------------------------------------------------------------
//
void MPIUtils::finalize()
{
    if (finalized())
    {
        return;
    }

#if RUNMPI == true
    MPI_Finalize();
#endif
}


// -----------------------------------------------------------------------------
//
int MPIUtils::myRank(MPI_Comm comm)
{
#if RUNMPI == true
    int rank;
    MPI_Comm_rank(comm, &rank);
    return rank;
#else
    return comm = 0;
#endif
}


// -----------------------------------------------------------------------------
//
int MPIUtils::size(MPI_Comm comm)
{
#if RUNMPI == true
    int size;
    MPI_Comm_size(comm, &size);
    return size;
#else
    return comm = 1;
#endif
}


// -----------------------------------------------------------------------------
//
void MPIUtils::barrier(MPI_Comm comm)
{
#if RUNMPI == true
    MPI_Barrier(comm);
#else
    comm += 0;
#endif
}


// -----------------------------------------------------------------------------
//
std::pair<int, int> MPIUtils::splitOverProcesses(int n, MPI_Comm comm)
{
    int start = 0, end = n;

#if RUNMPI == true
    int nprocs = size(comm);
    int rank = myRank(comm);
    int residual = n % nprocs;
    std::vector<int> chunk_sizes(nprocs, n/nprocs);

    for (int i = 0; i < residual; i++)
    {
        chunk_sizes[i] += 1;
    }

    for (int i = 0; i < rank; i++)
    {
        start += chunk_sizes[i];
    }
    end = start + chunk_sizes[rank];
#else
    comm += 0;
#endif

    return std::pair<int, int>(start, end);
}

void MPIUtils::joinOverProcesses(double **send,
                                 double **recv,
                                 int nrows,
                                 int ncols,
                                 MPI_Comm comm)
{
#if RUNMPI == true
    MPI_Allreduce(*send, *recv, nrows*ncols, MPI_DOUBLE, MPI_SUM, comm);
#else
    comm += 0;
    for (int i = 0; i < nrows*ncols; i++)
    {
        (*recv)[i] = (*send)[i];
    }
#endif
}

}

