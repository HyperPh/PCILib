
"use strict"

/**
 * 字符串转日期格式
 * @param {*} strDate 要转为日期格式的字符串
 */
function getDate(strDate){
    var date = eval('new Date(' + strDate.replace(/\d+(?=-[^-]+$)/, (a)=>{ return parseInt(a, 10) - 1; }).match(/\d+/g) + ')');
    return date;
}

export {getDate}
