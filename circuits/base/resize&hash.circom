pragma circom 2.0.0;

import "./resize.circom";
import "./poseidon_sponge.circom";

template Resize_Hash(hFull, wFull, hResize, wResize){

    signal input full_image[hFull][wFull][3];
    signal input resize_image[hResize][wResize][3];

    signal output out;

    component resize = Check_Resize(hFull, wFull, hResize, wResize);
    component hash = SpongeHash(hFull * wFull * 3);

    //** Resize Checker **//

    for (var i = 0; i < hFull; i++)
        for (var j = 0; j < wFull; j++) 
            for (var k = 0; k < 3; k++) 
                resize_checker.full_image[i][j][k] <== full_image[i][j][k];


    for (var i = 0; i < hResize; i++)
        for (var j = 0; j < wResize; j++) 
            for (var k = 0; k < 3; k++) 
                resize_checker.resize_image[i][j][k] <== low_image[i][j][k];

    //** Poseidon Hash **// 

    for (var i = 0; i < hResize; i++)
        for (var j = 0; j < wResize; j++) 
            for (var k = 0; k < 3; k++)
                hash.in[(i*wResize*3) + (j*3) + k] <== full_image[i][j][k];

    out <== hash.out;



}