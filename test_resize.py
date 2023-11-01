#!/usr/bin/python3.10

from scripts.util import append_to_csv, extract_contraints, generate_circuit, generate_input, measure_command, generate_resize_input


def test_circuit(circuit_name, input_path,pot_path, input_array=[],verbose=True):
    r1cs_path = 'output/compiled_circuit/compiled_{}/{}.r1cs'
    print(f'./scripts/compile_circuit.sh ./circuits/benchmark/{circuit_name}.circom {input_path} ')
    t_c,m_c = measure_command(f'./scripts/compile_circuit.sh ./circuits/benchmark/{circuit_name}.circom {input_path} ')
    if verbose:
        print(f'[{circuit_name}] Compile Circuit: {t_c} seconds, {m_c} KB')
    constraints = extract_contraints(r1cs_path.format(circuit_name,circuit_name))
    if verbose:
        print(f'[{circuit_name}] Constraints: {constraints}')
        
    print(f'./scripts/proving_system/setup_prover.sh {circuit_name} {pot_path}')
    t_sp,m_sp = measure_command(f'./scripts/proving_system/setup_prover.sh {circuit_name} {pot_path}')
    if verbose:
        print(f'[{circuit_name}] Setup Prover: {t_sp} seconds, {m_sp} KB')
    t_p,m_p = measure_command(f'./scripts/proving_system/prover.sh {circuit_name} ')
    if verbose:
        print(f'[{circuit_name}] Prover: {t_p} seconds, {m_p} KB')
    t_v,m_v = measure_command(f'./scripts/proving_system/verifier.sh {circuit_name}')
    if verbose:
        print(f'[{circuit_name}] Verifier: {t_v} seconds, {m_v} KB')
    t_p, m_p, t_v, m_v = 0,0,0,0
    
    return {'CIRCUIT':circuit_name,
           'INPUT SIZE': input_array[0] * input_array[1],
           'RESIZE SIZE':input_array[2] * input_array[3],
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
    POT = 'powersoftau/28pot.ptau'
    steps = 4
    HFULL, WFULL, HRESIZE, WRESIZE = (4+1),(4+1),(2+1),(2+1)
    circuit_name = f'resize_and_hash_optimized'

    generate_circuit({'HFULL': HFULL, 'WFULL':WFULL, 'HRESIZE':HRESIZE, 'WRESIZE' : WRESIZE },f'./circuits/base/{circuit_name}.circom',id=HFULL*WFULL)
    #generate_input(f'./input/input_{NUM}.json',NUM)
    input_file = f'./input/input_{HFULL}_{WFULL}.json'
    generate_resize_input(input_file,HFULL, WFULL, HRESIZE, WRESIZE)
    measures = test_circuit(f'{circuit_name}_{HFULL*WFULL}',input_file,POT, [HFULL, WFULL, HRESIZE, WRESIZE])
    measures['DIM_FULL'] = f'{int(HFULL)}*{int(WFULL)}*3' 
    measures['DIM_RES'] = f'{int(HRESIZE)}*{int(WRESIZE)}*3' 
    append_to_csv(measures,'./benchmark_circuits_resize.csv')