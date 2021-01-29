
"use strict"

// js的string变量存储字符串使用的是unicode(utf-16)编码，要保存时必须选择其他编码后进行传输，比如转成utf-8,utf-32等。
//static方法调用必须加类名(类内部可以用this代替),否则报错ReferenceError

var pattern_str=/(['"`])[^'"`]*\1/
var pattern_hex=/[0-9a-fA-F]/
var pattern_letter=/[0-9a-zA-Z_]/

// emoji的字节字符占两个unicode(utf-16)字符(4个utf-8)。使用String.fromCharCode也可以实现，需要进行两次fromCharCode，没有fromPointCode方便。

/**
 * utf-8 unicode(utf-16) bytes数组 统一资源标识符(URI) 互相转换
 * 
 * utf-16是大端的
 * 
 * 一个字符最多占6个(utf-8)字节,js的pointCode还只支持至多4个字节
 * pointCodeAt(i)对于大于等于0xffff的字符来说，下次要i+=2，不方便。改用for of循环可以正确识别
 * 
 * 可以正确支持中文、emoji表情、英文混合的字符串编码互转
 */
class utf8{
    static int2hex(n,lower=true) {
        if(lower){
            return n.toString(16).toLowerCase();
        }
        else{
            return n.toString(16).toUpperCase();
        }
    }

    static encodeURIComponent=encodeURIComponent
    static decodeURIComponent=decodeURIComponent
    
    

    /**
     * unicode=>utf-8,与encodeURIComponent的不同之处就是%换成了\x,以及把[0-9A-Za-z]也换成了16进制表示(python的bytes并没有做此转换)
     * 
     * @param {string} unicodestr 
     * @returns {string}
     */
    static unicodestr_to_utf8str(unicodestr) {
        let uri=this.encodeURIComponent(unicodestr)
        return this.uriComponent_to_utf8str(uri)
    }

    //完美实现了内置函数encodeURIComponent
    static _encodeURIComponent(unicodestr){
        let b=this._unicodestr_to_bytes(unicodestr)
        let newStr=''
        for(let icode of b){
            if (icode < 0x10){
                newStr += "%0" + icode.toString(16).toUpperCase();
            }
            else if ((icode >= 0x30 && icode <= 0x39) || (icode >= 0x41 && icode <= 0x5A) || (icode >= 0x61 && icode <= 0x7A)){//[0-9A-Za-z]
                newStr += String.fromCharCode(icode);
            }
            else{
                newStr += "%" + this.int2hex(icode, false);
            }
        }
        return newStr
    }

    //完美实现了内置函数decodeURIComponent
    static _decodeURIComponent(uri){
        let b=this.uriComponent_to_bytes(uri)
        return this._bytes_to_unicodestr(b)
    }

    //uriComponent => python的b字节串,里面的[0-9A-Za-z]没有写成\x的形式
    static uriComponent_to_pythonbytes(uri){
        return uri.replace(/%/g,'\\x').toLowerCase()
    }

    static uriComponent_to_utf8str(uri){
        let b=this.uriComponent_to_bytes(uri)
        let s=''
        for(let i=0;i<b.length;i++){
            s+='\\x'+b[i].toString(16).toLowerCase()
        }
        return s
    }

    //unicodestr => python的b字节串,里面的[0-9A-Za-z]没有写成\x的形式
    static unicodestr_to_pythonbytes(unicodestr){
        return this.uriComponent_to_pythonbytes(this.encodeURIComponent(unicodestr))
    }

    static uriComponent_to_bytes(uri){
        var result = [], i = 0;
        while (i < uri.length) {
            var c = uri.charCodeAt(i++);

            // if it is a % sign, encode the following 2 bytes as a hex value
            if (c === 37) {
                result.push(parseInt(uri.substr(i, 2), 16))
                i += 2;

            // otherwise, just the actual byte(int)
            } else {
                result.push(c)
            }
        }
        return result
    }

    static unicodestr_to_bytes(unicodestr){
        let uri=this.encodeURIComponent(unicodestr)
        return this.uriComponent_to_bytes(uri)
    }

    static utf8str_to_bytes(utf8str){
        return utf8str.slice(2).split('\\x').map((hex)=>parseInt(hex,16))//先要去掉开头的\x
    }

    /**
    * 
    * @param utf8Bytes {Array{Number}}
    * @return {string}
    */
    static bytes_to_unicodestr(utf8Bytes){
        let s = utf8Bytes.reduce((prev, cur) => prev += `%${cur.toString(16)}`, '')//prev-前一个元素，cur-当前元素，参照python的functools.reduce
        return this.decodeURIComponent(s)
    }

    /**
     * utf-8 bytes => unicode string
     * 数组中每个数都是0~255(一个字节)
     * 解析方式是大端，这样才能使用fromCharCode(它是按大端解析的)
     * 
     * @param utf8Bytes
     * @returns {string}
     */
    static _bytes_to_unicodestr(utf8Bytes) {
        var unicodeStr = "";
        for (var pos = 0; pos < utf8Bytes.length;) {
            var flag = utf8Bytes[pos];
            var unicode = 0;
            if ((flag >>> 7) === 0) {//0xxxxxxx,即flag<128
                unicodeStr += String.fromCharCode(utf8Bytes[pos]);
                pos += 1;

            } else if ((flag & 0xFC) === 0xFC) {//即252<=flag(<=255)
                unicode = (utf8Bytes[pos] & 0x3) << 30;
                unicode |= (utf8Bytes[pos + 1] & 0x3F) << 24;
                unicode |= (utf8Bytes[pos + 2] & 0x3F) << 18;
                unicode |= (utf8Bytes[pos + 3] & 0x3F) << 12;
                unicode |= (utf8Bytes[pos + 4] & 0x3F) << 6;
                unicode |= (utf8Bytes[pos + 5] & 0x3F);
                unicodeStr += String.fromCodePoint(unicode);
                pos += 6;

            } else if ((flag & 0xF8) === 0xF8) {//即248<=flag(<252,因为是else if)
                unicode = (utf8Bytes[pos] & 0x7) << 24;
                unicode |= (utf8Bytes[pos + 1] & 0x3F) << 18;
                unicode |= (utf8Bytes[pos + 2] & 0x3F) << 12;
                unicode |= (utf8Bytes[pos + 3] & 0x3F) << 6;
                unicode |= (utf8Bytes[pos + 4] & 0x3F);
                unicodeStr += String.fromCodePoint(unicode);
                pos += 5;

            } else if ((flag & 0xF0) === 0xF0) {//即240<=flag(<248)
                unicode = (utf8Bytes[pos] & 0xF) << 18;
                unicode |= (utf8Bytes[pos + 1] & 0x3F) << 12;
                unicode |= (utf8Bytes[pos + 2] & 0x3F) << 6;
                unicode |= (utf8Bytes[pos + 3] & 0x3F);
                unicodeStr += String.fromCodePoint(unicode);
                pos += 4;

            } else if ((flag & 0xE0) === 0xE0) {//即224<=flag(<240)
                unicode = (utf8Bytes[pos] & 0x1F) << 12;;
                unicode |= (utf8Bytes[pos + 1] & 0x3F) << 6;
                unicode |= (utf8Bytes[pos + 2] & 0x3F);
                unicodeStr += String.fromCharCode(unicode);//少于4个(<=3)字节的unicode字符用fromCharCode也不会出错
                pos += 3;

            } else if ((flag & 0xC0) === 0xC0) {//即192<=flag(<224)
                unicode = (utf8Bytes[pos] & 0x3F) << 6;
                unicode |= (utf8Bytes[pos + 1] & 0x3F);
                unicodeStr += String.fromCharCode(unicode);
                pos += 2;

            } else {//即128<=flag(<192)
                unicodeStr += String.fromCharCode(utf8Bytes[pos]);
                pos += 1;
            }
        }
        return unicodeStr;
    }

    //utf-8 string => unicode string
    static utf8str_to_unicodestr(utf8str){
        let b=this.utf8str_to_bytes(utf8str)
        return this.bytes_to_unicodestr(b)
    }
     
    /**
     * unicode => utf-8 完整实现
     * @param {string} s 
     * @returns {Array} 数组中每个数都是0~255(一个字节)
     */
    static _unicodestr_to_bytes(s) {
        var t = [],k=0,r=0;
        for (let ch of s) {
            // r = e.charCodeAt(n);//错误,charCodeAt不能正确识别>=0xffff的字符(会截断高位)
            r = ch.codePointAt(0);
            if (r < 0x0000007F) {
                // * U-00000000 - U-0000007F:  0xxxxxxx
                t[k++]=r//r & 0x7F
            } else if (r >= 0x00000080 && r <= 0x000007FF) {
                // * U-00000080 - U-000007FF:  110xxxxx 10xxxxxx
                t[k++]=(r >> 6 | 192);//((r >> 6) & 0x1F) | 0xC0
                t[k++]=(r & 63 | 128)//(r & 0x3F) | 0x80
            } else if (r >= 0x00000800 && r < 0x0000FFFF) {
                // * U-00000800 - U-0000FFFF:  1110xxxx 10xxxxxx 10xxxxxx
                t[k++]=(r >> 12 | 224);//((r >> 12) & 0x0F) | 0xE0
                t[k++]=(r >> 6 & 63 | 128);//((r >>  6) & 0x3F) | 0x80
                t[k++]=(r & 63 | 128)//(r & 0x3F) | 0x80
            } else if (r >= 0x00010000 && r <= 0x001FFFFF) {
                // * U-00010000 - U-001FFFFF:  11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
                t[k++]=((r >> 18) & 0x07) | 0xF0
                t[k++]=((r >> 12) & 0x3F) | 0x80
                t[k++]=((r >>  6) & 0x3F) | 0x80
                t[k++]=(r & 0x3F) | 0x80
            } else if (r >= 0x00200000 && r <= 0x03FFFFFF) {
                // * U-00200000 - U-03FFFFFF:  111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
                t[k++]=(r >> 24 & 0x03 | 0xF8)
                t[k++]=(r >> 18 & 0x3F | 0x80)
                t[k++]=(r >> 12 & 0x3F | 0x80)
                t[k++]=(r >>  6 & 0x3F | 0x80)
                t[k++]=(r & 0x3F | 0x80)
            } else if ( r >= 0x04000000 && r <= 0x7FFFFFFF ) {
                // * U-04000000 - U-7FFFFFFF:  1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
                t[k++]=((r & 0x3F) | 0x80);
                t[k++]=(((r >>  6) & 0x3F) | 0x80);
                t[k++]=(((r >> 12) & 0x3F) | 0x80);
                t[k++]=(((r >> 18) & 0x3F) | 0x80);
                t[k++]=(((r >> 24) & 0x3F) | 0x80);
                t[k++]=(((r >> 30) & 0x01) | 0xFC);
            } else {//不可能出现的情况
                throw RangeError("error unicode")
            }
        }
        return t
    }




    /**
     * Array => Uint8Array
     * @param {Array} a 普通数组(无类型)
     * @returns {Uint8Array} Uint8Array类型(无符号8位整型)的数组
     */
    static array_to_Uint8Array(a) {
        function checkInt(value) {
            return (parseInt(value) === value);
        }
    
        function checkInts(arrayish) {
            if (!checkInt(arrayish.length)) { return false; }
    
            for (var i = 0; i < arrayish.length; i++) {
                if (!checkInt(arrayish[i]) || arrayish[i] < 0 || arrayish[i] > 255) {
                    return false;
                }
            }
    
            return true;
        }
    
        function coerceArray(arg, copy) {
    
            // ArrayBuffer view
            if (arg.buffer && arg.name === 'Uint8Array') {
    
                if (copy) {
                    if (arg.slice) {
                        arg = arg.slice();
                    } else {
                        arg = Array.prototype.slice.call(arg);
                    }
                }
    
                return arg;
            }
    
            // It's an array; check it is a valid representation of a byte
            if (Array.isArray(arg)) {
                if (!checkInts(arg)) {
                    throw new Error('Array contains invalid value: ' + arg);
                }
    
                return new Uint8Array(arg);
            }
    
            // Something else, but behaves like an array (maybe a Buffer? Arguments?)
            if (checkInt(arg.length) && checkInts(arg)) {
                return new Uint8Array(arg);
            }
    
            throw new Error('unsupported array-like object');
        }

        return coerceArray(a);
    }

    static encode_str=this.unicodestr_to_utf8str//返回字符串
    static decode_str=this.utf8str_to_unicodestr//输入字符串
    static encode=this.unicodestr_to_bytes//返回数组
    static decode=this.bytes_to_unicodestr//输入数组

}


class base64{
    // static base64_str = this._keyStr//起个别名(alias)

    static _keyStr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="//不加static定义的是实例属性
    //检验正确: base64.encode('我')=="5oiR" 可以用python验证
    static encode(e) {
        var t = "";
        var n, r, i, s, o, u, a;
        var f = 0;
        e = utf8.encode(e);
        while (f < e.length) {
            n = e[f++];
            r = e[f++];
            i = e[f++];
            s = n >> 2;
            o = (n & 3) << 4 | r >> 4;
            u = (r & 15) << 2 | i >> 6;
            a = i & 63;
            if (isNaN(r)) {
                u = a = 64
            } else if (isNaN(i)) {
                a = 64
            }
            t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a)
        }
        return t
    }
    static decode(e) {
        var t = [],k=0;
        var n, r, i;
        var s, o, u, a;
        var f = 0;
        e = e.replace(/[^A-Za-z0-9+/=]/g, "");//去除非法字符
        while (f < e.length) {
            s = this._keyStr.indexOf(e.charAt(f++));
            o = this._keyStr.indexOf(e.charAt(f++));
            u = this._keyStr.indexOf(e.charAt(f++));
            a = this._keyStr.indexOf(e.charAt(f++));
            n = s << 2 | o >> 4;
            r = (o & 15) << 4 | u >> 2;
            i = (u & 3) << 6 | a;
            t[k++]=(n);
            if (u != 64) {
                t[k++]=(r)
            }
            if (a != 64) {
                t[k++]=(i)
            }
        }
        return utf8.decode(t);
    }

}


class encoding{

    static encode(d,_encoding='utf-8'){
        switch(_encoding.toLowerCase()){
            case 'utf-8':
            case 'utf8':
                return utf8.encode_str(d)
            case 'base64':
            case 'b64':
                return base64.encode(d)
            default:
                return ''
        }
    }

    static decode(e,_encoding='utf-8'){
        switch(_encoding.toLowerCase()){
            case 'utf-8':
            case 'utf8':
                return utf8.decode_str(e)
            case 'base64':
            case 'b64':
                return base64.decode(e)
            default:
                return ''
        }
    }

}






export const pcitextlib={
    utf8:utf8,
    base64:base64,
    encoding:encoding,
}

//下面是一些细节解释

// 一般会在http路径采用encodeURI进行编码，但是在路径中携带的参数采用encodeURIComponent进行编码
// 总之如果搞不清就推荐使用URIComponent

// encodeURI和encodeURIComponent的区别:
// encodeURI()着眼于对整个URL进行编码，特殊含义的符号; / ? : @ & = + $ , #不进行编码
// encodeURIComponent()对URL的组成部分进行个别编码，所以; / ? : @ & = + $ , #在这里是可以进行编码
// decode的区别同理:
// encodeURI('#')
// "#"
// encodeURIComponent('#')
// "%23"
// decodeURI('%23')
// "%23"
// decodeURIComponent('%23')
// "#"



// 测试代码:

// <html>
// <body>
// <script type="text/javascript">
// document.write(encodeURI("http://www.w3school.com.cn")+ "<br />")
// document.write(encodeURI("http://www.w3school.com.cn/My first/")+ "<br />")
// document.write(encodeURI(",/?:@&=+$#")+ "<br />")
// 
// document.write(encodeURIComponent("http://www.w3school.com.cn")+ "<br />")
// document.write(encodeURIComponent("http://www.w3school.com.cn/My first/")+ "<br />")
// document.write(encodeURIComponent(",/?:@&=+$#")+ "<br />")
// </script>
// </body>
// </html>

// 结果:

// 使用encodeURI

// http://www.w3school.com.cn
// http://www.w3school.com.cn/My%20first/
// ,/?:@&=+$#

// 使用encodeURIComponent

// http%3A%2F%2Fwww.w3school.com.cn
// http%3A%2F%2Fwww.w3school.com.cn%2FMy%20first%2F
// %2C%2F%3F%3A%40%26%3D%2B%24%23



// 其实URIComponent就是字符的utf-8编码的16进制字符串形式
// 测试代码:
// javascript:
// encodeURI('我')
// "%E6%88%91"
// decodeURI("%E6%88%91")
// "我"
// 
// python:
// '我'.encode('utf-8')
// b'\xe6\x88\x91'
// 两者结果是一样的



// String.fromCodePoint(0x2F804)//注意: 你(单立人和尔拼起来的)!=你(正常的你)

//escape和encodeURI效果不一样，类似还有unescape和decodeURI
// escape('😃是as4👀f[撒 #旦 %')//"%uD83D%uDE03%u662Fas4%uD83D%uDC40f%5B%u6492%20%23%u65E6%20%25"
// encodeURI('😃是as4👀f[撒 #旦 %')//"%F0%9F%98%83%E6%98%AFas4%F0%9F%91%80f%5B%E6%92%92%20#%E6%97%A6%20%25"
// encodeURIComponent('😃是as4👀f[撒 #旦 %')//"%F0%9F%98%83%E6%98%AFas4%F0%9F%91%80f%5B%E6%92%92%20%23%E6%97%A6%20%25"
//escape里面字符、一字节%FF、两字节%uFFFF混杂，十分复杂，不推荐使用。


//base64测试


//python
// import base64

// def base64_encode(s, encoding='utf-8', return_byte=False):
    
//     """base64加密"""
//     if encoding is None:
//         b = s
//     else:
//         b = s.encode(encoding)
//     b1 = base64.b64encode(b)
//     # print(b1)
//     if return_byte:
//         return b1
//     else:
//         return b1.decode('utf-8')

// def base64_decode(s, encoding='utf-8', return_byte=False):
//     """base64解密"""
//     if encoding is None:
//         b = s
//     else:
//         b = s.encode(encoding)
//     b1 = base64.b64decode(b)
//     # print(b1)
//     if return_byte:
//         return b1
//     else:
//         return b1.decode('utf-8')


// if __name__=='__main__':
// 	s1="😃是as4👀f[撒 #旦 %"
// 	print(e:=base64_encode(s1))
// 	print(base64_decode(e).encode('utf-8'))
// 	print(s1.encode('utf-8'))

// 8J+Yg+aYr2FzNPCfkYBmW+aSkiAj5pemICU=
// b'\xf0\x9f\x98\x83\xe6\x98\xafas4\xf0\x9f\x91\x80f[\xe6\x92\x92 #\xe6\x97\xa6 %'
// b'\xf0\x9f\x98\x83\xe6\x98\xafas4\xf0\x9f\x91\x80f[\xe6\x92\x92 #\xe6\x97\xa6 %'


