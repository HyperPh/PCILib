# -*- coding: UTF-8 -*-

"""PCILib"""

import os
import sys
import time
# import re
from .PCIosLib import (sort_files,filename_match,get_file_list,get_filename_list,path_join,split_ext,split_path,
                       find_not_exist_name,delete_file_with_log,rename_file_with_log,try_copy_file,try_move_file,
                       copy_under_all,move_under_all,rename_under_all,delete_under_all,
                       delete_empty_dir,delete_empty_dirs,is_valid_filename,try_mkdir,copy_dirtree,
                       get_env,get_useful_environ,get_normpath,get_abspath,get_realpath,cur_path,try_access_file,
                       set_file_time,remove_env,)

__version__ = '1.9.4.20220109'
__all__ = ['PCIosLib','PCIzen','PCImathLib','PCIhashLib','PCItextLib','PCIzlib']
PY3 = (sys.version_info[0] >= 3)
platform = sys.platform  # win32/linux/cygwin/darwin/os2


def get_time():
    """返回表示当前时间的字符串"""
    # return time.ctime(time.time())

    t = time.localtime(time.time())
    return f"{t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}:{t[5]}"


def get_pid():
    """返回当前进程的pid"""
    return os.getpid()
    # import multiprocessing
    # return multiprocessing.current_process().pid


def pcilib_path():
    r"""返回PCILib所在目录的路径"""
    return os.path.realpath(os.path.dirname(__file__))


def project_path():
    r"""返回PCILib所属项目的路径"""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))  # os.path.pardir=='..'


def get_version(silent=True):
    """返回当前python解释器版本"""
    v = f'Python {sys.version} on {sys.platform}'
    if not silent:
        print(v)
    return v


def get_sys_path():
    """python模块 import的搜寻路径"""
    return sys.path


def cwd():
    """返回当前工作目录(Current Working Directory)，是终端的pwd显示的位置"""
    return os.getcwd()  # 和os.path.abspath(os.path.curdir)结果一样


def is_linux():
    """判断是否为linux系统，推荐用startswith，因为python2的值是linux2"""
    return sys.platform.startswith('linux')


def is_win32():
    """判断是否为linux系统，推荐用startswith，因为python2的值是linux2"""
    return sys.platform.startswith('win32')


def elapsed_time(func, *args, **kwargs):
    import time
    start_time = time.time()
    result = func(*args, **kwargs)
    print(f"运行时间: {time.time() - start_time} s")
    return result

