"""此文件内主要包含os或fs操作"""
import os
import re
import shutil
import sys
import time


def sort_files(names: list, key='name', reverse=False):
    """文件名排序。按操作系统习惯，目录排在文件前面"""
    num = len(names)
    i = 0
    l_d = []
    l_f = []

    while i < num:
        if os.path.isdir(names[i]):
            l_d.append(names[i])
        else:
            l_f.append(names[i])
        i += 1

    if key == 'name':
        l_d.sort(reverse=reverse)
        l_f.sort(reverse=reverse)

    l_d += l_f  # extend()效果一样
    return l_d


def filename_match(filename, pattern=None, fullmatch=True, fullpath_match=False):
    """
    文件名匹配。pattern可以是字符串，也可以是编译好的Pattern对象。

    注:如果pattern=''，也会强制匹配成功。因为python将空字符串视为False
    注意:文件名中每两个字符间都有一个''

    :param filename: 文件完整路径
    :param pattern: 用于匹配目标的正则表达式(不要使用*作为通配符!!!),None表示强制匹配成功
    :param fullmatch: 是否全字匹配
    :param fullpath_match: 匹配时是否包含路径
    :return:
    """
    if pattern:
        if fullpath_match:
            if fullmatch:
                if re.fullmatch(pattern, filename):
                    return True
                else:
                    return False
            else:
                if re.search(pattern, filename):
                    return True
                else:
                    return False
        else:
            if fullmatch:
                if re.fullmatch(pattern, os.path.split(filename)[1]):
                    return True
                else:
                    return False
            else:
                if re.search(pattern, os.path.split(filename)[1]):
                    return True
                else:
                    return False
    else:
        return True


def get_file_list(input_path, recursive=True, sort=True, file_pattern=None, dir_pattern=None, fullmatch=True,
                  fullpath_match=False, followlinks=True, abspath=False, *, file_only=True, dir_only=False):
    """
    获取指定目录(包括子目录)下所有文件的完整路径。返回一个列表

    dir_only的优先级比file_only高,是为了传参数时方便,不用再把file_only设为False
    file_only和dir_only同时为False(一般用于列出目录树)
    dir_only=True时通常不排序,需要自行设置sort=False

    pattern: 用于匹配目标的正则表达式(不要使用*作为通配符!!!),None表示所有文件(或目录)。file_pattern和dir_pattern分别用于文件和目录
    fullmatch: 是否全字匹配
    fullpath_match: 匹配时是否包含路径

    abspath: 是否返回绝对路径

    """
    # os.fwalk()和os.walk() 行为差不多，但前者返回一个四元素元组,后者返回三元素元组
    # 注意，python的os.walk默认不抛出异常，julia的walkdir默认抛出异常
    if dir_only:
        # 提高dir_only的优先级
        file_only = False

    try:
        if file_pattern:
            f_pattern = re.compile(file_pattern)
        else:
            f_pattern = None
        if dir_pattern:
            d_pattern = re.compile(dir_pattern)
        else:
            d_pattern = None
    except Exception as e:
        print(e)
        return []

    if abspath:
        input_path = os.path.abspath(input_path)

    result = []
    if recursive:
        if os.path.isdir(input_path):
            if file_only:
                for dirpath, dirnames, filenames in os.walk(input_path, followlinks=followlinks):
                    for filename in filenames:
                        f = os.path.join(dirpath, filename)
                        if filename_match(f, f_pattern, fullmatch, fullpath_match):
                            result.append(f)
            elif dir_only:
                for dirpath, dirnames, filenames in os.walk(input_path, followlinks=followlinks):
                    for dirname in dirnames:
                        d = os.path.join(dirpath, dirname)
                        if filename_match(d, d_pattern, fullmatch, fullpath_match):
                            result.append(d)
            else:
                for dirpath, dirnames, filenames in os.walk(input_path, followlinks=followlinks):
                    # 如果最后要排序,两个循环顺序无所谓;否则习惯上目录排在前面,文件排在后面
                    for dirname in dirnames:
                        d = os.path.join(dirpath, dirname)
                        if filename_match(d, d_pattern, fullmatch, fullpath_match):
                            result.append(d)
                    for filename in filenames:
                        f = os.path.join(dirpath, filename)
                        if filename_match(f, f_pattern, fullmatch, fullpath_match):
                            result.append(f)
            if sort:
                result.sort()
        elif os.path.isfile(input_path) and not dir_only:
            result.append(input_path)
        else:
            pass
    else:
        if os.path.isdir(input_path):
            if file_only:
                for name in os.listdir(path=input_path):
                    f_d = os.path.join(input_path, name)
                    if os.path.isfile(f_d):
                        if filename_match(f_d, f_pattern, fullmatch, fullpath_match):
                            result.append(f_d)
            elif dir_only:
                for name in os.listdir(path=input_path):
                    f_d = os.path.join(input_path, name)
                    if os.path.isdir(f_d):
                        if filename_match(f_d, d_pattern, fullmatch, fullpath_match):
                            result.append(f_d)
            else:
                for name in os.listdir(path=input_path):
                    f_d = os.path.join(input_path, name)
                    # result.append(f_d)
                    if os.path.isfile(f_d):  # 是文件
                        if filename_match(f_d, f_pattern, fullmatch, fullpath_match):
                            result.append(f_d)
                    else:  # 是目录
                        if filename_match(f_d, d_pattern, fullmatch, fullpath_match):
                            result.append(f_d)
                if not sort:  # 没错就是not
                    return sort_files(result)
            if sort:
                result.sort()
        elif os.path.isfile(input_path) and not dir_only:
            result.append(input_path)
        else:
            pass
    return result


def get_filename_list(input_path, recursive=True, sort=True, file_pattern=None, dir_pattern=None, fullmatch=True,
                      fullpath_match=False, abspath=False, *, file_only=True, dir_only=False):
    """
    仅返回文件名列表，不含路径

    因为不含路径，所以abspath参数无用，只是为了和get_file_list函数签名保持一致
    """
    file_list = get_file_list(input_path, recursive, sort, file_pattern, dir_pattern, fullmatch, fullpath_match,
                              abspath=False, file_only=file_only, dir_only=dir_only)
    filename_list = []
    for f in file_list:
        filename_list.append(os.path.split(f)[1])
    return filename_list


def path_join(path, *paths, platform=sys.platform):
    r"""
    实现类似os.path.join(a: AnyStr, *paths: AnyStr)的功能,但os.path.join支持bytes类型的路径,它的实现见ntpath.py和genericpath.py

    在所有标准库支持文件系统(fs)的编程语言中，表示路径分隔符时，'/'和'\\'是等价的

    >>> os.path.join('/usr/bin/','a')
    '/usr/bin/a'
    >>> os.path.join('/usr/bin\\','a')
    '/usr/bin\\a'
    >>> os.path.join('/usr/bin','a')  # win32下
    '/usr/bin\\a'
    >>> os.path.join('usr/bin','a')  # win32下
    'usr/bin\\a'
    >>> os.path.join('/usr/bin/',r'\a')
    '\\a'
    >>> os.path.join('/usr/bin/','/a')
    '/a'
    >>>

    :param path:
    :param paths:
    :param platform:
    :return:
    """
    if platform.startswith('win'):
        sep = '\\'
    else:
        sep = '/'
    rp = path
    last_not_have_sep = False if path[-1] in "\\/" else True  # 上一个路径末尾是否不含分隔符
    for p1 in paths:
        if p1[0] in "\\/":  # p1以'\\'或'/'开头
            rp = p1
            continue
        if last_not_have_sep:
            rp += sep
        rp += p1
        last_not_have_sep = False if p1[-1] in "\\/" else True
    return rp


def split_ext(file_path: str):
    """
    实现类似os.path.splitext(p: AnyStr)的功能,但os.path.splitext支持bytes类型的路径,它的实现见ntpath.py和genericpath.py

    返回的后缀带'.'(比如.txt而不是txt)。
    同样适用于empty或empty.或.empty.这些奇怪的名字。
    """

    # 未找到则返回-1
    dot = file_path.rfind('.')
    zheng = file_path.rfind('/')
    fan = file_path.rfind('\\')

    if dot > zheng and dot > fan:
        # file_name_suffix = file_path.split('.')[-1]  # 后缀
        # file_name_prefix = file_path[:len(file_path) - len(file_name_suffix) - 1]  # 前缀
        file_name_suffix = file_path[dot:]  # 后缀
        file_name_prefix = file_path[:dot]  # 前缀
        return file_name_prefix, file_name_suffix
    else:  # '.'未找到(dot是-1)
        return file_path, ''


def split_path(file_path: str):
    """实现os.path.split()类似的功能,但当file_path为已存在的目录名时返回(file_path,'')

    但os.path.split()支持bytes类型的路径,它的实现见ntpath.py
    """
    if os.path.isdir(file_path):
        return file_path, ''

    # 未找到则返回-1
    zheng = file_path.rfind('/')
    fan = file_path.rfind('\\')

    if zheng > fan:
        last = zheng
    elif fan > zheng:
        last = fan
    else:  # 全都未找到(都是-1),此时肯定不是linux目录
        mao = file_path.find(':')
        if mao > 0:
            ps_drive = file_path[:mao + 1]  # 驱动器名,含冒号;powershell的虚拟驱动器不止一个字符
            name1 = file_path[mao + 1:]  # 名称
            return ps_drive, name1
        else:
            return file_path, ''

    name1 = file_path[last + 1:]  # 名称
    dir1 = file_path[:last]  # 目录
    return dir1, name1


def find_not_exist_name(file_name):
    """从file_name开始找,直到找到filename (2)这样的不存在的文件名为止"""
    if not os.path.exists(file_name):
        return file_name
    i = 1
    file_name_prefix, file_name_suffix = os.path.splitext(file_name)
    while os.path.exists(file_name_prefix + f' ({i})' + file_name_suffix):
        i += 1
    file_name_new = file_name_prefix + f' ({i})' + file_name_suffix
    return file_name_new


def delete_file_with_log(file_path, log_delete=False, delete_log_path="delete_log.txt", print_delete=False):
    try:
        if print_delete:
            print(f"\ndelete {file_path}")
        if log_delete:
            with open(delete_log_path, 'a', encoding='utf-8') as f1:
                f1.write(file_path + "\n")
        os.remove(file_path)
        # do_something_after_delete()
    except Exception as ex:
        # 只读的文件删不掉
        print(ex)


def rename_file_with_log(old, new, log_rename=False, rename_log_path="rename_log.txt", print_rename=False):
    try:
        if print_rename:
            print(f"\nrename {old} to {new}")
        if log_rename:
            with open(rename_log_path, 'a', encoding='utf-8') as f1:
                f1.write(f'"{old}"->"{new}"\n')
        os.renames(old, new)
        # do_something_after_rename()
    # except FileExistsError as ex:
    #     # new已存在
    #     print(ex)
    # except FileNotFoundError as ex:
    #     # old不存在
    #     print(ex)
    except Exception as ex:
        # 只读的文件改不了
        print(ex)


def try_copy_file(file_name, dest_path):
    try:
        file_name_new = find_not_exist_name(os.path.join(dest_path, os.path.split(file_name)[1]))
        shutil.copyfile(file_name, file_name_new)
    except Exception as e:
        print(e)
        # sys.exit()


def try_move_file(file_name, dest_path):
    try:
        file_name_new = find_not_exist_name(os.path.join(dest_path, os.path.split(file_name)[1]))
        shutil.move(file_name, file_name_new)
    except Exception as e:
        print(e)
        # sys.exit()


def copy_under_all(src_path, dest_path, pattern=None):
    """
    复制src_path目录和子目录下所有名称符合pattern的文件到dest_path

    不再简单地使用shutil.copyfile(f1, dest_path)

    :param src_path: 源路径
    :param dest_path: 目标路径
    :param pattern: 用于匹配目标的正则表达式(不要使用*作为通配符!!!),None表示所有文件

    """
    # shutil.copyfile(r"E:\1\12.txt",r"e:\2\666.txt")会在复制同时改名
    file_list = get_file_list(src_path, file_pattern=pattern)
    for f1 in file_list:
        try_copy_file(f1, dest_path)


def move_under_all(src_path, dest_path, pattern=None):
    """
    移动src_path目录和子目录下所有名称符合pattern的文件到dest_path

    不再简单地使用shutil.move(f1, dest_path)

    :param src_path: 源路径
    :param dest_path: 目标路径
    :param pattern: 用于匹配目标的正则表达式(不要使用*作为通配符!!!),None表示所有文件

    """
    # shutil.move(r"E:\1\12.txt",r"e:\2\666.txt")会在移动同时改名
    file_list = get_file_list(src_path, file_pattern=pattern)
    for f1 in file_list:
        try_move_file(f1, dest_path)


def rename_under_all(dir_path, pattern='', replace='', full_path_replace=False, *, log_rename=True, rename_log_path="rename_log.txt", print_rename=False):
    """
    重命名dir_path目录和子目录下所有文件,pattern替换为replace

    :param dir_path: 目标路径
    :param pattern: 用于匹配目标的替换部分
    :param replace: 替换成的字符串
    :param full_path_replace: 是否替换整个路径。值为False时不替换前面的目录
    :param log_rename: 是否保存记录
    :param rename_log_path: 保存记录的文件路径
    :param print_rename: 是否打印记录
    """
    file_list = get_file_list(dir_path)

    if full_path_replace:
        for f1 in file_list:
            new_name = re.sub(pattern, replace, f1)
            rename_file_with_log(f1, new_name, log_rename, rename_log_path, print_rename)
    else:
        for f1 in file_list:
            path, name = os.path.split(f1)
            new_name = re.sub(pattern, replace, name)
            new_path = os.path.join(path, new_name)
            rename_file_with_log(f1, new_path, log_rename, rename_log_path, print_rename)


def delete_under_all(dir_path, pattern=None, delete=True, *, log_delete=True, delete_log_path="delete_log.txt", print_delete=False):
    """
    删除dir_path目录和子目录下所有名称符合(或不符合,此时delete=False)pattern的文件
    注意:文件名采用全字匹配

    :param dir_path: 目标路径
    :param pattern: 用于匹配目标的正则表达式(不要使用*作为通配符!!!),None表示所有文件
    :param delete: 值为False时删除不符合pattern的文件
    :param log_delete: 是否保存删除的文件名
    :param delete_log_path: 保存删除记录的文件路径
    :param print_delete: 是否打印删除的文件名
    """
    print('请检查pattern是否正确,None表示所有文件,若不正确则会错删,请在下次输入时取消')
    t1 = '删除符合pattern的文件' if delete else '删除不符合pattern的文件'
    print(f'目录:{dir_path}')
    print(f'{t1}, pattern:{pattern}')
    if input("此操作可能有删除数据的行为,请按y继续") != 'y':
        print("操作取消")
        return
    file_list = get_file_list(dir_path)
    if pattern is None:
        if delete:
            for f1 in file_list:
                delete_file_with_log(f1, log_delete, delete_log_path, print_delete)
        # else:
        #     # pattern=None相当于什么都不删
    else:
        try:
            pattern_obj = re.compile(pattern)
        except Exception as e:
            print(e)
            return
        if delete:
            for f1 in file_list:
                if re.fullmatch(pattern_obj, os.path.split(f1)[1]):
                    delete_file_with_log(f1, log_delete, delete_log_path, print_delete)
        else:
            for f1 in file_list:
                if re.fullmatch(pattern_obj, os.path.split(f1)[1]):
                    continue
                delete_file_with_log(f1, log_delete, delete_log_path, print_delete)
    return


def delete_empty_dir(dir1: str, delete_self=True):
    """
    delete_self=True时尝试删除自身(自身也可能为空目录，非空不做处理)
    """
    for name in os.listdir(dir1):
        f_d = os.path.join(dir1, name)
        if os.path.isdir(f_d):
            delete_empty_dir(f_d, True)

    if delete_self:
        try:
            os.rmdir(dir1)  # 尝试删除自身(自身也可能为空目录),非空目录抛出OSError
        except OSError as ex:
            pass  # 非空目录抛出OSError,不做处理
        except Exception as ex:
            print(ex)


def delete_empty_dirs(dirs: list, delete_self=True):
    """
    delete_self=True时尝试删除自身(自身也可能为空目录，非空不做处理)
    """
    for dir1 in dirs:
        delete_empty_dir(dir1, delete_self)


def is_valid_filename(filename):
    """判断合法文件名，即目录存在且名称不为空"""
    if os.path.isdir(filename):
        return False
    dir1, name1 = os.path.split(filename)
    if os.path.isdir(dir1) and name1 != '':
        return True
    else:
        return False


def try_mkdir(path, create_intermediate=False):
    """create_intermediate=True时将同时创建给定路径中所有不存在的中间目录"""
    try:
        if create_intermediate:
            os.makedirs(path)  # 自动创建不存在的中间目录
        else:
            os.mkdir(path)  # 目录已存在时抛出FileExistsError，中间目录不存在时创建失败但不抛出异常
    except FileExistsError:
        pass  # 目录已存在时忽略
    except Exception as e:
        print(e)


def copy_dirtree(src_path, dest_path, pattern=None, fullpath_match=False, full_tree=False, copy_root=False):
    """
    注意：dest_path后面有没有'/'或'\\'应该和src_path一样，否则可能复制到其他目录去，因此在函数中加入了判断和自动修正

    fullpath_match默认为False，不匹配整个路径，只匹配目录名

    full_tree=False时复制当前一级目录结构
    full_tree=True时复制整个目录结构

    copy_root=True时会先在dest_path新建一个名称是源目录名的目录

    仅复制目录树，不复制文件

    pattern: 用于匹配目标的正则表达式(不要使用*作为通配符!!!),None表示所有文件
    """
    if not os.path.isdir(src_path) or not os.path.isdir(dest_path):
        return
    if dest_path[-1] not in ('/','\\'):
        dest_path+='/'#python好像能处理"E:\\\\a\\\\b"这种多了几个斜杠的路径，所以只要保证dest_path后面有'/'就不会复制到其他目录去

    if full_tree:
        dir_list = get_file_list(src_path, recursive=True, sort=False, dir_pattern=pattern, fullpath_match=fullpath_match, dir_only=True)
    else:
        dir_list = get_file_list(src_path, recursive=False, sort=False, dir_pattern=pattern, fullpath_match=False, dir_only=True)#不递归的话前面路径是一样的，fullpath_match是False才有意义

    if copy_root:
        root_name = os.path.split(src_path)[1]
        if root_name != '':
            new_dest_path = os.path.join(dest_path, root_name)
            try_mkdir(new_dest_path)#不需要create_intermediate=True
            for d1 in dir_list:
                d = d1.replace(src_path, new_dest_path)
                try_mkdir(d,full_tree)
        else:  # root_name==''说明src_path本身是根目录，比如'E:\'或'/'
            print(f'操作失败,"{src_path}"本身是根目录,不可复制其名称')
    else:
        for d1 in dir_list:
            d = d1.replace(src_path, dest_path)
            try_mkdir(d,full_tree)


def try_access_file(path):
    if not os.access(path, os.R_OK):
        print('access denied: '+path)
        return False
    return True


def get_env(readonly=False):
    """返回环境变量"""
    if readonly:
        return dict(os.environ)
    else:
        return os.environ  # environ是一个字符串所对应环境的映射(mapping)对象，可以用os.environ.keys()获取所有键


def get_useful_environ():
    """文件系统读写的搜寻路径, 当前用户主目录, 临时目录路径, 可执行文件扩展名, 系统主目录, 用户主目录, 机器名, 命令行的提示符"""
    return os.environ['PATH'], os.environ['HOMEPATH'], os.environ['TEMP'], os.environ['PATHEXT'], os.environ['SYSTEMROOT'], os.environ['USERPROFILE'], os.environ['LOGONSERVER'], os.environ['PROMPT']


def get_normpath(path='.', platform='linux'):
    r"""
    返回指定路径的规范path字符串形式路径
    为了避免出现路径字符串中混用正斜杠、反斜杠，使用os.path.normpath进行格式化(win32是\\，linux是/)
    为了全部转换为Linux兼容格式，格式化后，替换掉反斜线(因为有时在网络的服务器端，遇到\\会解析出错，最好全部使用/)
    """
    if platform=='win32':
        return os.path.normpath(path)
    else:
        return os.path.normpath(path).replace('\\', '/')


def get_abspath(path='.'):
    """返回指定路径的绝对路径，可以含软链接路径"""
    return os.path.abspath(path)


def get_realpath(path='.'):
    """返回指定路径的真实路径(不是软链接路径)

    os.path.realpath()
    返回指定文件的标准路径，而非软链接所在的路径
    Return the canonical path of the specified filename, eliminating any
    symbolic links encountered in the path.
    """
    return os.path.realpath(path)


def cur_path():
    """
    返回当前工作目录，是终端的pwd显示的位置，不含软链接
    注: os.path.curdir=='.'
    """
    return os.path.realpath(os.path.curdir)


def file_stat(filename):
    return os.stat(filename)


def file_mtime(filename, timestamp=False):
    """最后修改时间(modify time)"""
    st = os.stat(filename)
    if timestamp:
        return st.st_mtime
    else:
        import datetime
        return datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")


def file_atime(filename, timestamp=False):
    """最后访问时间(access time)"""
    st = os.stat(filename)
    if timestamp:
        return st.st_atime
    else:
        import datetime
        return datetime.datetime.fromtimestamp(st.st_atime).strftime("%Y-%m-%d %H:%M:%S")


def set_file_time(filename, atime=None, mtime=None):
    """设置文件的atime和mtime，在win10上可能无法正确设置atime(有一瞬间被改掉了，但立刻又变成了系统当前时间)"""
    st = os.stat(filename)
    if atime is None:
        atime=st.st_atime
    elif isinstance(atime, str):
        atime = time.mktime(time.strptime(atime.replace('/', '-'), "%Y-%m-%d %H:%M:%S"))
    if mtime is None:
        mtime=st.st_mtime
    elif isinstance(mtime, str):
        mtime = time.mktime(time.strptime(mtime.replace('/', '-'), "%Y-%m-%d %H:%M:%S"))

    os.utime(filename, (atime, mtime))


def file_size(filename):
    """单位 字节(B)"""
    return os.path.getsize(filename) or os.stat(filename).st_size


def remove_env(v):
    """取消环境变量"""
    os.unsetenv(v)
