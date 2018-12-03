/*! \file  mpih.h
 *  \brief Common MPI header wrapper for serial or parallel builds.
 */


#ifndef __MPIH__
#define __MPIH__


// NOTE: The RUNMPI flag is set from CMake. It is defined in the
//       CMake generated file mpiflag.h
#include "mpiflag.h"


#if RUNMPI == true
#include <mpi.h>
#else
using MPI_Comm = int;
#define MPI_COMM_WORLD 0
#endif // RUNMPI

#endif // __MPIH__

