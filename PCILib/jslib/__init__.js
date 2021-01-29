

import * as pciutil from "./util/__init__.js"
import {pcitextlib as textlib} from "./pcitextlib.js"
import * as security from "./security/__init__.js"
// 注意 import "module-name"将运行模块中的全局代码, 但实际上不导入任何值。



class random{
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
}

export {random,str,elasped_time,has_strict_mode,is_valid_type}
export * as util from "./util/__init__.js"
export * from "./pcitextlib.js"
export * as security from "./security/__init__.js"
export * as math from "./math/__init__.js"
export * as datetime from "./datetime.js"
export const routine={
    doit:js_routine
}

