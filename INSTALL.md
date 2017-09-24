# GAFT Installation Instruction

## 1. Install MPI implementations ([MPICH](http://www.mpich.org/downloads/), [OpenMPI](https://www.open-mpi.org/software/ompi/v3.0/))

### Ubuntu

``` shell
sudo apt install mpich
```

### macOS

``` shell
brew install mpich
```

### Windows

Download the [Microsoft MPI (MS-MPI)](http://msdn.microsoft.com/en-us/library/bb524831%28v=vs.85%29.aspx)

### Other platforms

See more details in http://www.mpich.org/downloads/

## 2. Install GAFT

### Via pip

``` shell
pip install gaft
```
### From source

``` shell
git clone git@github.com:PytLab/gaft.git

cd gaft

python setup.py install
```

## 3. Run test

``` shell
cd gaft

python tests/gaft_test.py
```

