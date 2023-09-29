# Benchmark_Circuits

This repository contains the benchmark for circom circuits. In order to understand the time and memory consumption a report csv file is generated for each circuit. The report contains the following information:

- Circuit name
- Input size
- Number of constraints
- Time to compile and generate the witness
- Memory to compile and generate the witness
- Time to setup the proof
- Memory to setup the proof
- Time to generate the proof
- Memory to generate the proof
- Time to verify the proof
- Memory to verify the proof

## Setup

To easily launch the test takes care/configure the following paramenters:
* In `scripts/compile_circuit.sh`, properly set `CIRCOMLIB_PATH` path. If `circomlib` is not installed, run: `npm install circomlib`.
* In `test_circuits.py`, properly set `POT` variable with the path to the `*.ptau` file (download it from [here](https://github.com/iden3/snarkjs#7-prepare-phase-2)). It should be in `poweroftau` directory but it can be elsewhere.
* In `scripts/proving_system/prover.sh`, properly set `RAPIDSNARK` variable with the path to the `build/prover` executable. For information on how to install rapidsnark visit [here](https://github.com/iden3/rapidsnark)