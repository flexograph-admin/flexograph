# FlexoGraph

To build this project, go to the build directory, and update the paths in paths.sh to reflect your setup.

Then execute the runner.sh script.

## Configuration

Before running benchmarks or preprocessing scripts, copy the example config files and fill in your paths:

```bash
cp config.json.example config.json
cp env.sh.example env.sh
# Edit both files with your local paths
source env.sh
```

## Requirements
- g++11
```
add-apt-repository -y ppa:ubuntu-toolchain-r/test
apt-get update
apt-get install g++-11
```
- [cmake](https://cmake.org/install/)
- [Boost](https://www.boost.org/)  (1.80.0 or higher)
