pragma circom 2.0.3;

include "./poseidon2/poseidon2_hash.circom";

template Poseidon(n){
    signal input in[n];
    signal output out;

    component poseidon2_hash = Poseidon2_hash(n);
    
    for(var i = 0; i < n; i++)
        poseidon2_hash.inp[i] <== in[i];
    out <== poseidon2_hash.out;
}

//MAIN component main = Poseidon(NUM);