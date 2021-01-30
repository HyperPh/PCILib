
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

// //计算x的m次幂（非递归实现）
// //很独特的一种解法
// function pow(x, m) {
//     var y = 1;
//     var bin = m.toString(2).split('');
//     //先将m转化成2进制形式
//     for (var j = 0; j < bin.length; j++) {
//         y *= 2;
//         //如果2进制的第j位是1，则再*x
//         if (bin[j] == "1") {
//             y = x * y
//         }
//     }
//     return y;
// }

export {factorial}
