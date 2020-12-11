Copyright (c) Facebook, Inc. and its affiliates.

This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.

[![CircleCI](https://circleci.com/gh/facebookincubator/beanmachine.svg?style=svg&circle-token=39d1796c9ba26c78bba42dea57a9559742723be5)](https://circleci.com/gh/facebookincubator/workflows/beanmachine)

# Overview

Bean Machine is a probabilistic programming language for inference over statistical models written in the Python language using a declarative syntax.

# Installing Bean Machine
On Linux:

    sudo apt-get install libboost-dev libeigen3-dev
    pip install numpy torch
    git clone https://github.com/facebookincubator/BeanMachine.git
    cd BeanMachine
    pip install .

On Mac, we recommend [conda](https://docs.conda.io/en/latest/) as a package manager and [Homebrew](https://brew.sh/) to install the Xcode dependencies:

    brew install boost eigen pybind11
    conda create -n {env name}; conda activate {env name}
    pip install numpy torch
    git clone https://github.com/facebookincubator/BeanMachine.git
    cd BeanMachine
    CC=$(LLVMBASE)/bin/clang -fopenmp CXX=$(LLVMBASE)/bin/clang++ -fopenmp CXX11=$(LLVMBASE)/bin/clang++ -fopenmp CXX14=$(LLVMBASE)/bin/clang++ -fopenmp \
    CXX17=$(LLVMBASE)/bin/clang++ -fopenmp CXX1X=$(LLVMBASE)/bin/clang++ -fopenmp \
    pip install . —global-option=build_ext —global-option='-Isrc:{INCLUDE_PATHS}'
    # example INCLUDE_PATHS: /usr/local/Cellar/eigen/3.3.7/include/eigen3:/usr/local/Cellar/boost/1.73.0/include:/usr/local/Cellar/pybind11/2.6.1/include

Further, if you would like to run the builtin unit tests:

    pip install pytest
    pytest --pyargs beanmachine
