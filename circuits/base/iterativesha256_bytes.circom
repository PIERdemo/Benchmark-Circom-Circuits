pragma circom 2.0.3;

include "./sha256_bytes.circom";

template IterativeSha256(n,iterations){
    signal input in[n];
    signal output out[32 * iterations];

    component sha_256[iterations];
    for(var i = 0; i < iterations; i++){
        sha_256[i] = Sha256Bytes(n);

        for(var j = 0; j < n; j++)
            sha_256[i].in[j] <== in[j];
        
        for(var j = 0; j < 32; j++)
            out[(32*i)+j] <== sha_256[i].out[j];
    }
}

//MAIN component main = IterativeSha256(NUM,ITER);