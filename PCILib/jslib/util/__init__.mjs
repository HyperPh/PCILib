
"use strict"



function array_compare(a,b){
    if(!(a instanceof Array && b instanceof Array)){
        throw TypeError("array needed")
    }
    for(let i=0;i<a.length;i++){
        if(a[i] instanceof Array){
            if(!(b[i] instanceof Array)){

            }
            else{
                let k=array_compare(a[i],b[i])
                if(k!=0){
                    return k
                }
            }
        }

        if(a[i]<b[i]){
            return -1
        }
        else if(a[i]>b[i]){
            return 1
        }
        else{
            if(i==a.length-1){
                if (a.length<b.length){
                    return -1
                }
                else if(a.length>b.length){
                    return 1
                }
                else{
                    return 0
                }
            }
            
        }
    }
}



//the following code is partly copied from a js book (modefied by PCI Hyperbola)
class object{
    constructor(o){
        this.obj=this.deepcopy(o)
    }

    //仅自己的键列表,跳过继承的属性、方法
    static key_list(o){
        let a=[],i=0
        // for(a[i++] in o);
        for(k in o){
            if(!o.hasOwnProperty(k) || typeof o[k]=='function') continue;
            a[i++]=k
        }
        return a
    }

    //仅自己的值列表,跳过继承的属性、方法
    static value_list(o){
        let a=[],i=0
        // for(a[i++] in o);
        for(k in o){
            if(!o.hasOwnProperty(k) || typeof o[k]=='function') continue;
            a[i++]=o[k]
        }
        return a
    }



    // inherit() returns a newly created object that inherits properties from the
    // prototype object p.  It uses the ECMAScript 5 function Object.create() if
    // it is defined, and otherwise falls back to an older technique.
    static inherit(p) {
        if (p == null) throw TypeError('p must be a non-null object'); // p must be a non-null object
        if (Object.create)                // If Object.create() is defined...
            return Object.create(p);      //    then just use it.
        let t = typeof p;                 // Otherwise do some more type checking
        if (t !== "object" && t !== "function") throw TypeError('p must be object or function');
        function f() {};                  // Define a dummy constructor function.
        f.prototype = p;                  // Set its prototype property to p.
        return new f();                   // Use f() to create an "heir" of p.
    }

    /*
    * Copy the enumerable properties of p to o, and return o.
    * If o and p have a property by the same name, o's property is overwritten.
    * This function does not handle getters and setters or copy attributes.
    */
    //精简版，不复制描述符和setter,getter
    static extend_without_attributes(o, p) {
        for(let prop in p) {                         // For all props in p.
            o[prop] = p[prop];                   // Add the property to o.
        }
        return o;
    }

    /*
    * This method extends the object on which it is called by copying properties
    * from the object passed as its argument.  All property attributes are
    * copied, not just the property value.  All own properties (even non-
    * enumerable ones) of the argument object are copied unless a property
    * with the same name already exists in the target object.
    */
    //完整版的extend,书上写的那个是merge,它说错了
    static extend(o) {
        // Get all own props, even nonenumerable ones
        var names = Object.getOwnPropertyNames(o);
        // Loop through them
        for (var i = 0; i < names.length; i++) {
            // Get property description from o
            var desc = Object.getOwnPropertyDescriptor(o, names[i]);
            // Use it to create property on this
            Object.defineProperty(this, names[i], desc);
        }
    }

    //完整版的merge
    static merge(o) {
        // Get all own props, even nonenumerable ones
        var names = Object.getOwnPropertyNames(o);
        // Loop through them
        for (var i = 0; i < names.length; i++) {
            // Skip props already in this object
            if (names[i] in this) continue;
            // Get property description from o
            var desc = Object.getOwnPropertyDescriptor(o, names[i]);
            // Use it to create property on this
            Object.defineProperty(this, names[i], desc);
        }
    }

    /*
    * Copy the enumerable properties of p to o, and return o.
    * If o and p have a property by the same name, o's property is left alone.
    * This function does not handle getters and setters or copy attributes.
    */
    //精简版，不复制描述符和setter,getter
    static merge_without_attributes(o, p) {
        for(let prop in p) {                           // For all props in p.
            if (o.hasOwnProperty[prop]) continue;  // Except those already in o.
            o[prop] = p[prop];                     // Add the property to o.
        }
        return o;
    }

    /*
    * Remove properties from o if there is not a property with the same name in p.
    * Return o.
    */
    static restrict(o, p) {
        for(let prop in o) {                         // For all props in o
            if (!(prop in p)) delete o[prop];    // Delete if not in p
        }
        return o;
    }

    /*
    * For each property of p, delete the property with the same name from o.
    * Return o.
    */
    static subtract(o, p) {
        for(let prop in p) {                         // For all props in p
            delete o[prop];                      // Delete from o (deleting a
                                                // nonexistent prop is harmless)
        }
        return o;
    }

    /*
    * Return a new object that holds the properties of both o and p.
    * If o and p have properties by the same name, the values from o are used.
    */
    static union(o,p) { return extend(extend({},o), p); }

    /*
    * Return a new object that holds only the properties of o that also appear
    * in p. This is something like the intersection of o and p, but the values of
    * the properties in p are discarded
    */
    static intersection(o,p) { return restrict(extend({}, o), p); }

    //使用Object.keys()代替
    // /*
    //  * Return an array that holds the names of the enumerable own properties of o.
    //  */
    // function keys(o) {
    //     if (typeof o !== "object") throw TypeError();  // Object argument required
    //     let result = [];                 // The array we will return
    //     for(let prop in o) {             // For all enumerable properties
    //         if (o.hasOwnProperty(prop))  // If it is an own property
    //             result.push(prop);       // add it to the array.
    //     }
    //     return result;                   // Return the array.
    // }

    static classof(o) {
        // if (o === null) return "Null";
        // if (o === undefined) return "Undefined";
        //注意，toString一般被重载了，应该调用最原始的toString，找到它，调用它的call方法
        return Object.prototype.toString.call(o).slice(8,-1);
    }

    static shallowcopy(o,p=null){
        var p=p||{}
        for(key in o){//遍历对象的键
            p[key]=o[key]
        }
        return p
    }

    //存在的bug:
    //NaN,Infinity,undefined,函数会变成null;日期会变成字符串
    //RegExp,Error以及其他不可序列化对象会变成空对象{}
    //-0会变成0
    //BigInt会报错Uncaught TypeError: Do not know how to serialize a BigInt
    static deepcopy(o){
        return JSON.parse(JSON.stringify(o))
    }

}


class ndarray{
    // a=[]
    constructor(shape=0,dtype=Number){
        this.a=[]
    }

    static in1d(elem,a){
        return a.includes(elem)
    }
}


export {array_compare,object,ndarray}


