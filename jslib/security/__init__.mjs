
"use strict"

import {md4} from './md4.mjs'
import {md5} from './md5.mjs'
import {sha1} from './sha1.mjs'
import {sha256} from './sha256.mjs'
import {sha512} from './sha512.mjs'
import {crc32} from './crc32.mjs'
import {rmd160} from './ripemd160.mjs'
// "{}"不能省，即使上面每个文件只有一个导出的名称

// 同目录下的sha1,sha256,sha512,md4,md5,crc32均测试通过
// 😃是as4👀
// hex_sha512('😃是as4👀')
// 601b5fb6dced318ccc21de2823c51d190dd0c365a791f55b7a9517893995ee3a393b48bf4202181a69ac2c102ceff3d143830ba99119749a5a6f12ae3650b7af
// hex_md5('😃是as4👀')
// e9bd86ed40f1af7bc6a7bd12aad795fd
// crc32
// 36ab4bbd
// sha1
// 28d7fdd053a1471281ad012536627e79235eebd3
// sha256
// 4cbb0e0ca0b94222461470441591538a5bca4a3b60c6a7a53e1864bf0f283edb
// md4
// 6e9e642b2bcb68825144b14118666fef
// rmd160
// dcc3720430f93495f87539a7ed76f7c468044201

class cryptography{
    static md4=md4
    static md5=md5
    static sha1=sha1
    static sha256=sha256
    static sha512=sha512
    static crc32=crc32
    static rmd160=rmd160

    static valid_algorithm=['sha256','sha512','sha1','md5','md4','crc32','rmd160']

    static hash_str(s,algorithm='sha256'){
        if(this.valid_algorithm.includes(algorithm)){
            return eval(`${algorithm}.hex_${algorithm}('${s}')`)
        }
        return ""
    }

    
}

// export const security={
//     cryptography:cryptography
// }

export {cryptography}
