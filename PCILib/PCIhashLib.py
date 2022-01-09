# -*- coding: UTF-8 -*-
"""
虽然目前python默认返回小写hash值,但以后可能有变
因此所有函数中使用lower()确保小写
"""

import os
import hashlib
import zlib


smallfile_maxsize = 2**20  # 1MiB
commonfile_maxsize = 100 * 2**20  # 100MiB
bigfile_maxsize = 30 * 2**30  # 30GiB

pci_algorithms = ['crc32', 'md5', 'sm3', 'whirlpool', 'shake_128', 'md5-sha1', 'sha3_256', 'blake2b', 'sha512_224', 'sha3_512', 'blake2s', 'md4', 'sha1', 'sha384', 'sha3_224', 'sha256', 'sha512', 'sha512_256', 'sha3_384', 'mdc2', 'sha224', 'shake_256', 'ripemd160']


def to_bytes(s, encoding):
    if (encoding is None) or (encoding == "bytes"):
        return s
    return s.encode(encoding)


def remove_invalid_algorithms(algorithms: list, override=True, default_algo=hashlib.algorithms_available):
    """去除不存在的hash算法"""
    if override:
        i = 0
        while i < len(algorithms):
            if algorithms[i] != "crc32" and algorithms[i] not in default_algo:
                algorithms.pop(i)
                i -= 1
            i += 1
        return algorithms
    else:
        valid_algorithms = []
        for i in range(0, len(algorithms)):
            if algorithms[i] == "crc32" or algorithms[i] in default_algo:
                valid_algorithms.append(algorithms[i])
        return valid_algorithms


def PCIHashString(s, encoding="utf-8", algorithm="sha256", upper=False, silent=True):
    """encoding=None或'bytes'时将s视为字节串"""
    if algorithm == "crc32":
        out1 = format(zlib.crc32(to_bytes(s, encoding)), "08x")  # 必须是08x,0表示前面不足位补0,8x或者x都会导致前面的0丢失
    elif algorithm in hashlib.algorithms_available:
        out1 = hashlib.new(algorithm, to_bytes(s, encoding)).hexdigest()
    else:
        print("不支持的算法:" + algorithm)
        return None

    out2 = out1.upper() if upper else out1.lower()

    if not silent:
        print(f"[{algorithm}]: {out2} *{s}")
    return out2


def allhash_str(s, algorithms, encoding="utf-8", upper=False, silent=True):
    algorithms = remove_invalid_algorithms(algorithms)
    num = len(algorithms)
    out2 = {}
    for i in range(0, num):
        if algorithms[i] == "crc32":
            tmp = format(zlib.crc32(to_bytes(s, encoding)), "08x")
        else:
            tmp = hashlib.new(algorithms[i], to_bytes(s, encoding)).hexdigest()
        tmp2 = tmp.upper() if upper else tmp.lower()
        out2[algorithms[i]] = tmp2
        if not silent:
            print(f"[{algorithms[i]}]: {tmp2} *{s}")
    return out2


def hash_file(filename, algorithm="sha256", upper=False, silent=True):
    """
    计算小文件的hash值，一次读入整个文件
    """

    try:
        size1 = os.path.getsize(filename)  # 字节B
        if not silent:
            print(f"{filename}: {size1}B")
        if size1 > commonfile_maxsize:
            print("文件太大")
            return None
        with open(filename, "rb") as f:
            if algorithm == 'crc32':
                out1 = format(zlib.crc32(f.read()), "x")  # crc32()返回十进制int值，要转化为16进制值的字符串，x表示格式化为16进制小写(X表示大写)
            elif algorithm in hashlib.algorithms_available:
                hash_obj = hashlib.new(algorithm)
                hash_obj.update(f.read())
                out1 = hash_obj.hexdigest()
            else:
                print("不支持的算法:" + algorithm)
                return None
    except FileNotFoundError:
        print("未找到文件 " + filename)
        return None
    except Exception as ex:
        print("Unknown error:", ex)
        return None

    out2 = out1.upper() if upper else out1.lower()
    if not silent:
        print(f"[{algorithm}]: {out2} *{filename}")
    return out2


def PCIHashBigFile(filename, algorithm="sha256", block_size=1024*512, upper=False, silent=True):
    """
    python计算大文件的hash值

    block_size单位字节(B)
    """

    try:
        size1 = os.path.getsize(filename)  # 字节(B)
        if not silent:
            print(f"{filename}: {size1}B")
        if size1 > bigfile_maxsize:
            print("文件太大")
            return None
        with open(filename, "rb") as f:
            if algorithm == 'crc32':
                crc32sum = 0
                while True:
                    s = f.read(block_size)
                    if not s:
                        break
                    crc32sum = zlib.crc32(s, crc32sum)
                out1 = "%08x" % (crc32sum & 0xFFFFFFFF)
            elif algorithm in hashlib.algorithms_available:
                hash_obj = hashlib.new(algorithm)
                # hash_obj.update(f.read())
                while True:
                    data = f.read(block_size)
                    if not data:
                        break
                    hash_obj.update(data)  # 更新哈希对象所要计算的数据，多次调用为累加效果
                # out1 = codecs.encode(hash_obj.digest(),'hex')
                out1 = hash_obj.hexdigest()
            else:
                print("不支持的算法:" + algorithm)
                return None
    except FileNotFoundError:
        print("未找到文件 " + filename)
        return None
    except Exception as ex:
        print("Unknown error:", ex)
        return None

    out2 = out1.upper() if upper else out1.lower()
    if not silent:
        print(f"[{algorithm}]: {out2} *{filename}")
    return out2


def allhash_bigfile(filename, algorithms, block_size=1024*512, upper=False, silent=True):
    """
    python一次性计算大文件的所有hash值

    block_size单位字节(B)
    """
    algorithms = remove_invalid_algorithms(algorithms)
    num = len(algorithms)
    out2 = {}

    if num != 0:
        try:
            checksum = []
            for algorithm in algorithms:
                if algorithm == "crc32":
                    checksum.append(0)
                else:
                    checksum.append(hashlib.new(algorithm))

            size1 = os.path.getsize(filename)  # 字节(B)
            if not silent:
                print(f"{filename}: {size1}B")
            if size1 > bigfile_maxsize:
                print("文件太大")
                return None
            with open(filename, "rb") as f:
                while True:
                    data = f.read(block_size)
                    if not data:
                        break
                    for i in range(0, num):
                        if algorithms[i] == "crc32":
                            checksum[i] = zlib.crc32(data, checksum[i])
                        else:
                            checksum[i].update(data)  # 更新哈希对象所要计算的数据，多次调用为累加效果

                for i in range(0, num):
                    if algorithms[i] == "crc32":
                        tmp = "%08x" % (checksum[i] & 0xFFFFFFFF)
                    else:
                        tmp = checksum[i].hexdigest()
                    tmp2 = tmp.upper() if upper else tmp.lower()
                    out2[algorithms[i]] = tmp2
                    if not silent:
                        print(f"[{algorithms[i]}]: {tmp2} *{filename}")
        except FileNotFoundError:
            print("未找到文件 " + filename)
            return None
        except Exception as ex:
            print("Unknown error:", ex)
            return None
    else:
        return None

    return out2

