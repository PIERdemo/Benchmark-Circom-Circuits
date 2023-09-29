#!/usr/bin/env python3

from scripts.util import generate_circuit, generate_input, measure_command
POT = './powersoftau/pot_15.ptau'


def test_circuit(circuit_name, input_path,pot_path):
    t_c,m_c = measure_command(f'./scripts/compile_circuit.sh ./circuits/benchmark/{circuit_name}.circom {input_path} ')
    print(f'[{circuit_name}] Compile Circuit: {t_c} seconds, {m_c} MB')
    t_sp,m_sp = measure_command(f'./scripts/proving_system/setup_prover.sh {circuit_name} {pot_path}')
    print(f'[{circuit_name}] Setup Prover: {t_sp} seconds, {m_sp} MB')
    t_p,m_p = measure_command(f'./scripts/proving_system/prover.sh {circuit_name} ')
    print(f'[{circuit_name}] Prover: {t_p} seconds, {m_p} MB')
    t_v,m_v = measure_command(f'./scripts/proving_system/verifier.sh {circuit_name}')
    print(f'[{circuit_name}] Verifier: {t_v} seconds, {m_v} MB')
    


if __name__ == '__main__':
    NUM = 50
    generate_circuit({'NUM':NUM},'./circuits/base/sha256_bytes.circom',id=NUM)
    generate_input(f'./input/input_{NUM}.json',NUM)
    test_circuit(f'sha256_{NUM}',f'./input/input_{NUM}.json',POT)
    