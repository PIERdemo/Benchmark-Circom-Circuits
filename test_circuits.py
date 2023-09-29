#!/usr/bin/env python3

from scripts.util import append_to_csv, extract_contraints, generate_circuit, generate_input, measure_command
POT = './powersoftau/20.ptau'


def test_circuit(circuit_name, input_path,pot_path,verbose=True):
    r1cs_path = 'output/compiled_circuit/compiled_{}/{}.r1cs'

    t_c,m_c = measure_command(f'./scripts/compile_circuit.sh ./circuits/benchmark/{circuit_name}.circom {input_path} ')
    if verbose:
        print(f'[{circuit_name}] Compile Circuit: {t_c} seconds, {m_c} MB')
    constraints = extract_contraints(r1cs_path.format(circuit_name,circuit_name))

    t_sp,m_sp = measure_command(f'./scripts/proving_system/setup_prover.sh {circuit_name} {pot_path}')
    if verbose:
        print(f'[{circuit_name}] Setup Prover: {t_sp} seconds, {m_sp} MB')
    t_p,m_p = measure_command(f'./scripts/proving_system/prover.sh {circuit_name} ')
    if verbose:
        print(f'[{circuit_name}] Prover: {t_p} seconds, {m_p} MB')
    t_v,m_v = measure_command(f'./scripts/proving_system/verifier.sh {circuit_name}')
    if verbose:
        print(f'[{circuit_name}] Verifier: {t_v} seconds, {m_v} MB')
    
    return {'CIRCUIT':circuit_name,
           'INPUT SIZE':input_path.split('_')[-1].split('.')[0],
           'CONSTRAINTS':constraints,
           'COMPILE_TIME':t_c,
           'COMPILE_MEMORY':m_c,
           'SETUP_TIME':t_sp,
           'SETUP_MEMORY':m_sp,
           'PROVER_TIME':t_p,
           'PROVER_MEMORY':m_p,
           'VERIFIER_TIME':t_v,
           'VERIFIER_MEMORY':m_v}
    

if __name__ == '__main__':
    NUM = 50
    generate_circuit({'NUM':NUM},'./circuits/base/sha256_bytes.circom',id=NUM)
    generate_input(f'./input/input_{NUM}.json',NUM)
    measures = test_circuit(f'sha256_{NUM}',f'./input/input_{NUM}.json',POT)
    append_to_csv(measures,'./benchmark_circuits.csv')
    