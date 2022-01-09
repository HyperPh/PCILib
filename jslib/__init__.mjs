

// import {io as pciio} from "./io.mjs"

// 注意:光是 import "module-name"将只会运行模块中的全局代码, 但实际上不导入任何值。

var __version__='1.0.0.20210130'
var __all__=['math','text','security']

class random{
    static letters='QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890_'

    static rand(){
        return Math.random()
    }
    
    static randint(a=0,b=1){
        return Math.floor(Math.random()*(b-a+1))+a;
    }

    static choice(a){
        let i=random.randint(0,a.length-1)
        return a[i]
    }

    static shuffle(input){
        for (let i = input.length - 1; i >= 0; i--) {
            let randomIndex = Math.floor(Math.random() * (i + 1));
            let itemAtIndex = input[randomIndex];
            input[randomIndex] = input[i];
            input[i] = itemAtIndex;
        }
        return input;
    }

    static int16(){
        return random.randint(-32768,32767)
    }

    static uint16(){
        return random.randint(0,65535)
    }

    static int8(){
        return random.randint(-128,127)
    }

    static uint8(){
        return random.randint(0,255)
    }

    static randstr(length){
        if(length===undefined){
            length=random.uint8()
        }
        let tmp=''
        for (let i = 0; i < length; i++) {
            tmp += random.letters.charAt(random.randint(0,random.letters.length-1));
        }
        return tmp;
    }

}


class str{
    /**
     * 字符串添加引号
     * @param {*} s 输入的字符串(不是字符串则返回原值)
     */
    static add_quote(s){
        return (typeof s=='string')?"'"+s+"'":s
    }

    /**
     * 字符串删除引号
     * @param {string} s 输入的字符串(不是字符串则报错)
     */
    static remove_quote(s){
        return s.replace(/^(["'])(.*)\1$/,'$2')
    }

    static raw2literal(s){
        // return s.replace(/\\/g,'\\\\')
        return String.raw(s)
    }

    //此方法没用
    static literal2raw(s){
        return s.replace(/\\\\/g,'\\')
    }
}


/** 
 * 计时,args是数组,缺省以调用无参func
 * 
 * 例子: elasped_time(factorial,[677890000])//运行时间: 2.727 s
 */
function elasped_time(func,args=[]){
    let start=new Date();//无参构造函数可以省略圆括号()
    func(...args);//展开args，传入多个参数而不是一个数组
    let s1='运行时间: '+(new Date()-start)/1000+' s';
    print(s1);
    return s1;
}

/**
 * 判断是否有严格模式
 */
function has_strict_mode(){
    "use strict"//这是一条启用严格模式的指令，不是一个表达式
    return this===undefined//严格模式下函数中的this是undefined，否则是全局对象window
}

function is_valid_type(type_str){
    return ['undefined','object','boolean','number','string','function','symbol'].includes(type_str)
}

//常用的扩展内置对象的操作
function js_routine(){
    // Array.prototype.shuffle=()=>random.shuffle(this)
    Array.prototype.shuffle=function(){return random.shuffle(this)}

    //数组去重，同时去掉undefined空洞
    Array.prototype.unique = function(){
        let newArr = [];
        this.forEach((x)=>{
            if (!newArr.includes(x)) {
                newArr.push(x);
            }
        });
        return newArr;
    }

    //NaN和任何数比较大小都是false(包括NaN自身)
    Array.prototype.max=function(return_i=false){
        let k=0
        for(let i=1;i<this.length;i++){
            if(this[i]>this[k] || isNaN(this[k])){
                k=i
            }
        }

        if(return_i){
            return k
        }
        else{
            return this[k]
        }
    }

    Array.prototype.min=function(return_i=false){
        let k=0
        for(let i=1;i<this.length;i++){
            if(this[i]<this[k] || isNaN(this[k])){
                k=i
            }
        }

        if(return_i){
            return k
        }
        else{
            return this[k]
        }
    }

    Array.prototype.most_common = function(){
        let count_arr=[];
        let k;
        for(let j=0;j<this.length;j++){
            if ((k=this.slice(0,j).indexOf(this[j]))>=0) {
                count_arr[k]++
            }
            else{
                count_arr[j]=1
            }
        }
        return this[count_arr.max(true)];
    }
}

export {__version__,__all__,random,str,elasped_time,has_strict_mode,is_valid_type}
// export * as util from "./util/__init__.mjs"
export * from "./util/__init__.mjs"
export * as text from "./pcitextlib.mjs"
export * as security from "./security/__init__.mjs"
export * as math from "./math/__init__.mjs"
// export * as datetime from "./datetime.mjs"
export * from "./datetime.mjs"
export const routine={
    doit:js_routine
}

