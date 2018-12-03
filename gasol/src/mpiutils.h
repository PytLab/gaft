/*! \file  mpiutils.h
 *  \brief Intrerfaces of the common MPI routines.
 */


#ifndef __MPIUTILS__
#define __MPIUTILS__

#include "mpih.h"

#include <utility>

namespace gasol {
/// Struct for handling MPI functions to be wrapped.
struct MPIUtils {

    /*! \brief Wrapps MPI_INIT
     */
    static void init();

    /*! \brief Wrap MPI::Is_initialized
     */
    static bool initialized();

    /*! \brief Wrapps MPI_FINALIZE
     */
    static void finalize();

    /*! \brief Wrap MPI::Is_finialized
     */
    static bool finalized();

    /*! \brief Wrapps MPI_COMM_RANK
     *  \param comm: The communicator to use.
     *  \return: The rank of this process withing the given communicator.
     */
    static int myRank(MPI_Comm comm = MPI_COMM_WORLD);

    /*! \brief Wrapps MPI_COMM_SIZE
     *  \param comm: The communicator to use.
     *  \return: The sise of the communicator (the total number of processes).
     */
    static int size(MPI_Comm comm = MPI_COMM_WORLD);

    /*! \brief Wrapps MPI_BARRIER, syncronizing processes.
     *  \param comm: The communicator to use.
     */
    static void barrier(MPI_Comm comm = MPI_COMM_WORLD);

    /*! \brief Returns true if the calling process is the master.
     *  \param comm: The communicator to use.
     */
    static bool isMaster(MPI_Comm comm = MPI_COMM_WORLD)
    { return (myRank(comm) == 0); }

    /*! \brief Split a size to different chunks over all processes in communicator.
     *  \param size: Size to be splitted.
     *  \param comm: The communicator to use.
     */
    static std::pair<int, int> splitOverProcesses(int size,
                                                  MPI_Comm comm = MPI_COMM_WORLD);

    /*! \brief Join all solutions together from all processes in communicator.
     *  \param send: local data in each process.
     *  \param recv: global data in each process.
     *  \param nrows: column number, population size.
     *  \param ncols: row number, solution dimension.
     *  \param comm: The communicator to use.
     */
    static void joinOverProcesses(double **send,
                                  double **recv,
                                  int nrows,
                                  int ncols,
                                  MPI_Comm comm = MPI_COMM_WORLD);

};

}

#endif // __MPIUTILS__

