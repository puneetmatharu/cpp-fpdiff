# cpp-fpdiff

## Building

To build the code you will need [CMake](https://cmake.org/download/)

```bash
cmake -B build && cmake --build build
```

If you have [Ninja](https://ninja-build.org), you can specify it as the build generator by running the following command instead:

```bash
cmake -G Ninja -B build && cmake --build build
```

If you are on an Apple MacBook with an M-series chip, you should run the command below instead to ensure the build is optimised for the Arm architecture:

```bash
CMAKE_APPLE_SILICON_PROCESSOR="arm64" cmake -G Ninja -B build && cmake --build build
```

In the build directory, you should now see the executables `fpdiff_zlib`, `fpdiff_miniz` and possibly `fpdiff_boost` (if you possess the Boost library). You can use these binaries when running the `validate.py` script.

## Validating

You can validate the built binaries using `validate.py`. To see the available commands, run `python3 validate.py --help`.

**Example:** Validate `fpdiff.py` and output to `validation.log`:

```bash
python3 validate.py -e fpdiff.py -o validation.log
```

**Example:** Validate `build/fpdiff_zlib` and output to `validation.log`:

```bash
python3 validate.py -e build/fpdiff_zlib -o validation.log --benchmark
```

The `validate.py` script will generate a bash script named `run_script.sh` to run the test cases. You can inspect this file to see the individual commands that are run. Notice that when `fpdiff.py` is specified, `python3` command is automatically prepended to each command.

## Benchmarking

Install [hyperfine](https://github.com/sharkdp/hyperfine) and run the `validate.py` with the `-b/--benchmark` flag to generate timings for the C/C++ and Python based `fpdiff` implementations:

**Example:** Validate `fpdiff.py` and output to `validation.log`:

```bash
❯ python3 validate.py -e fpdiff.py -o validation.log --benchmark
Found hyperfine: /opt/homebrew/bin/hyperfine

Running: '/opt/homebrew/bin/hyperfine --warmup=10 ./run_script.sh'

Benchmark 1: ./run_script.sh
  Time (mean ± σ):     682.5 ms ±  19.0 ms    [User: 441.5 ms, System: 178.9 ms]
  Range (min … max):   664.4 ms … 719.6 ms    10 runs
```

**Example:** Validate `build/fpdiff_zlib` and output to `validation.log`:

```bash
❯ python3 validate.py -e build/fpdiff_zlib -o validation.log --benchmark
Found hyperfine: /opt/homebrew/bin/hyperfine

Running: '/opt/homebrew/bin/hyperfine --warmup=10 ./run_script.sh'

Benchmark 1: ./run_script.sh
  Time (mean ± σ):      61.1 ms ±   7.1 ms    [User: 23.3 ms, System: 24.7 ms]
  Range (min … max):    47.1 ms …  75.5 ms    46 runs
```

## Results

| Tool                 | Time                |
|----------------------|---------------------|
| `fpdiff.py`          | 682.5 ms ±  19.0 ms |
| `build/fpdiff_boost` | 82.0 ms ± 6.3 ms    |
| `build/fpdiff_zlib`  | 61.1 ms ± 7.1 ms    |
| `build/fpdiff_miniz` |                     |

## License

The code in `fpdiff.py` has been borrowed from the [`oomph-lib`](https://github.com/oomph-lib/oomph-lib) repository and thus falls under the licensing conditions of that repository (see [LICENSE](./LICENCE)). The remaining code also falls under the purview of this license.
