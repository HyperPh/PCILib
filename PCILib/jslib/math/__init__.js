
"use strict"

//k阶乘
function factorial(n,k=1){
    if(k==0) return 0;
    let o=1;
    while(n>1){
        o*=n;
        n-=k;
    }
    return o;
}

export {factorial}
