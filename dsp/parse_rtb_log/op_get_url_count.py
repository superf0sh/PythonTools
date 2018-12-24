#!/usr/bin/env python

"""
This script find the show failed url and show success url for specified adid
print() is python 3.x built-in function, while in python < 3.x print is a operator
if you want to use print function, should use 'from __future__ import print_function'
"""
from __future__ import print_function
import string
import sys
import os
import logging
import time
import esm

import threading


class MyThread(threading.Thread):
    """
    define self Thread class to meet the requirement
    """

    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.res = None

    def run(self):
        logging.info("starting %s at: %s" % (self.name, time.ctime()))
        self.res = self.func(*self.args)
        logging.info("finished %s at: %s" % (self.name, time.ctime()))

    def get_result(self):
        return self.res


def init_logging():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-4d: %(message)s",
                        datefmt="%m-%d %H:%M:%S",
                        filename="show.log",
                        filemode="a")


def get_file_list(dir_name, filters_list):
    if dir_name is None or len(dir_name) == 0:
        return None

    index = esm.Index()
    for i in range(len(filters_list)):
        index.enter(filters_list[i])

    index.fix()
    files = []
    if os.path.isdir(dir_name):
        for parent, dirnames, filenames in os.walk(
                dir_name):  # three parameters return 1.parent directory, 2.directorys, 3.files
            for filename in filenames:  # display file information
                result = index.query(filename)
                if len(result) == 0:
                    continue
                files.append(os.path.join(parent, filename))
    else:
        if len(index.query(dir_name)) != 0:
            files.append(dir_name)

    return files


def get_show_url_file(ad_id, show_pushid_list, show_url_dict, file_name):
    """
    get the url that show ad success in file
    """
    if show_pushid_list is None or file_name is None or len(file_name) == 0:
        return

    # print("filter = " + string.join(id_filter))
    # filter *.tar.gz
    if string.find(file_name, ".tar.gz") != -1:
        return

    if not os.path.isfile(file_name):
        print(file_name + " is not a file!")
    else:
        if not string.find(file_name, "rtb_log_crit_", 0, len("rtb_log_crit_")):
            print(file_name + " is not rtb_log_crit log file")
            return
        with open(file_name) as fd:
            for line in fd:
                strs = string.split(line, sep="\1")
                strs[0] = string.strip(strs[0])
                if (0 == cmp(strs[0], "rtb_creative") and 0 ==
                    cmp(strs[6], ad_id) and (strs[7] in show_pushid_list)):
                    # unshow_url_dict[strs[7]] = (strs[4], strs[22], strs[23])
                    if None == show_url_dict.get(strs[23]):
                        show_url_dict[strs[23]] = 1
                    else:
                        show_url_dict[strs[23]] = show_url_dict.get(strs[23]) + 1;
    logging.info("[get_show_url_file]finish parse file: " + file_name)


def get_show_url(ad_id, show_pushid_list, show_url_dict, file_list):
    """
    get the url that show ad failed in directory
    """
    if (None == show_pushid_list or None == file_list or 0 == len(file_list)):
        return

    for file_name in file_list:
        get_show_url_file(ad_id, show_pushid_list, show_url_dict, file_name)


def get_unshow_url_file(ad_id, show_pushid_list, unshow_url_dict, file_name):
    """
    get the url that show ad failed in file
    """
    if (None == show_pushid_list or None == file_name or 0 == len(file_name)):
        return

    # print("filter = " + string.join(id_filter))
    # filter *.tar.gz
    if (-1 != string.find(file_name, ".tar.gz")):
        return

    if (not os.path.isfile(file_name)):
        print(file_name + " is not a file!")
    else:
        if (not string.find(file_name, "rtb_log_crit_", 0, len("rtb_log_crit_"))):
            print(file_name + " is not rtb_log_crit log file")
            return
        with open(file_name) as fd:
            for line in fd:
                strs = string.split(line, sep="\1")
                strs[0] = string.strip(strs[0])
                if (0 == cmp(strs[0], "rtb_creative") and (0 ==
                                                               cmp(strs[6], ad_id)) and (
                    strs[7] not in show_pushid_list)):
                    # unshow_url_dict[strs[7]] = (strs[4], strs[22], strs[23])
                    if None == unshow_url_dict.get(strs[23]):
                        unshow_url_dict[strs[23]] = 1;
                    else:
                        unshow_url_dict[strs[23]] = unshow_url_dict.get(strs[23]) + 1;
    logging.info("[get_unshow_url_file]finish parse file: " + file_name)


def get_unshow_url(ad_id, show_pushid_list, unshow_url_dict, file_list):
    """
    get the url that show ad failed in directory
    """
    if (None == show_pushid_list or None == file_list or 0 == len(file_list)):
        return

    for file_name in file_list:
        get_unshow_url_file(ad_id, show_pushid_list, unshow_url_dict, file_name)


def generate_show_pushid_file(adid, show_pushid_list, file_name):
    """
    generate the pushid from the file specified by file_name which ad id is
    equvalent to the adid
    """
    if (None == show_pushid_list or None == file_name or 0 == len(file_name)):
        return

    # print("filter = " + id_filter)
    # filter *.tar.gz
    if (-1 != string.find(file_name, ".tar.gz")):
        return

    if (not os.path.isfile(file_name)):
        print(file_name + " is not a file!")
    else:
        if (not string.find(file_name, "rtb_log_crit_", 0, len("rtb_log_crit_"))):
            print(file_name + " is not rtb_log_crit log file")
            return
        with open(file_name) as fd:
            for line in fd:
                strs = string.split(line, sep="\1")
                strs[0] = string.strip(strs[0])
                if (0 != cmp(strs[0], "rtb_show") or 0 != cmp(strs[6], adid)):
                    # print("compare result of {0} and {1} is {2}".format(strs[0],
                    #    "rtb_show", cmp(strs[0], "rtb_show")))
                    # print("compare result {0} and {1} is {2}".format(strs[6],
                    #    adid, cmp(strs[6], adid)))
                    # print("find result is %d" % string.find(strs[0], id_filter))
                    # print(strs[0] + " != rtb_show")
                    continue
                else:
                    # print(strs[4] + "<>" + strs[6] + "<>" + strs[7] + "<>" + strs[22])
                    if (not strs[7] in show_pushid_list):
                        show_pushid_list.add(strs[7])
    logging.info("[generate_show_pushid_file]finish parse file: " + file_name)


def generate_show_pushid_thread(ad_id, file_list):
    """
    generate the pushid list
    """

    if (None == file_list or 0 == len(file_list)):
        return

    show_pushid_list = set()
    for file_name in file_list:
        generate_show_pushid_file(ad_id, show_pushid_list, file_name)

    return show_pushid_list


def print_url_dict(unshow_url_dict):
    for key in unshow_url_dict.keys():
        print('{0},{1}'.format(key, unshow_url_dict[key]))


def flush_url_dict(unshow_url_dict, file_name):
    with open(file_name, mode="w") as outfd:
        for key in unshow_url_dict.keys():
            print('{0},{1}'.format(unshow_url_dict[key], key), file=outfd)


def print_pushid_list(pushid_list):
    for pushid in pushid_list:
        print("{0}".format(pushid))


def flush_pushid_list(pushid_list, file_name):
    with open(file_name, mode="w") as outfd:
        for pushid in pushid_list:
            print("{0}".format(pushid), file=outfd)


FILES_PER_THREAD = 2

if __name__ == "__main__":
    init_logging()
    # file_name=raw_input("Please enter the file name: ");
    # print_file(file_name);
    """
    This dict's structure is as below:
    The key is adid, value is pushid
    """
    show_pushid_list = set()
    """
    This dict's structure is as below:
    The key is pushid, value is tuple, the tuple contains access time and url
    """
    show_url_dict = dict()
    unshow_url_dict = dict()
    out_dir = ""
    print(sys.argv)
    # first check the input argument
    if (len(sys.argv) < 4):
        print("Usage: " + os.path.basename(sys.argv[0]) + " <log_dir_name> <adid> <out_dir_name>")
        log_dir_name = raw_input("Please enter the directory name of the log file:\n")
        adid = raw_input("Please enter the adid to analysis:\n")
        out_dir = raw_input("Please enter the out put directory:\n")
    else:
        log_dir_name = sys.argv[1]
        adid = sys.argv[2]
        out_dir = sys.argv[3]

    filters = [""]
    if (len(sys.argv) > 4):
        filters = sys.argv[4:]
        logging.info("file name filter: {0}".format(filters))

    if out_dir[len(out_dir) - 1] != os.path.sep:
        out_dir = out_dir + os.path.sep

    if (not os.path.isdir(out_dir)):
        print("out directory is null!")
        out_dir = ""

    file_list = get_file_list(log_dir_name, filters)
    logging.info("number of log file is %d" % len(file_list))
    out_show_file = out_dir + "show_url_count.txt";
    out_unshow_file = out_dir + "unshow_url_count.txt";
    out_pushid_file = out_dir + "show_pushid.txt";
    threads = []
    thread_num = len(file_list) / FILES_PER_THREAD
    if ((len(file_list) % FILES_PER_THREAD) != 0):
        thread_num += 1

    logging.info("threads num: {0}".format(thread_num))
    for i in range(thread_num - 1):
        t = MyThread(generate_show_pushid_thread, (adid, file_list[i *
                                                                   FILES_PER_THREAD: (i + 1) * FILES_PER_THREAD]),
                     generate_show_pushid_thread.__name__ + "_" + str(i))
        threads.append(t)
    t = MyThread(generate_show_pushid_thread, (adid, file_list[(thread_num - 1) *
                                                               FILES_PER_THREAD: len(file_list)]),
                 generate_show_pushid_thread.__name__ + "_" + str(thread_num - 1))
    threads.append(t)

    for i in range(thread_num):
        threads[i].start()

    for i in range(thread_num):
        threads[i].join()
        temp_list = threads[i].get_result()
        logging.info("len of {0} temp_list is {1}".format(threads[i].getName(),
                                                          len(temp_list)))
        show_pushid_list.update(temp_list)

    logging.info("total show pushid num: {0}".format(len(show_pushid_list)))

    # generate_show_pushid(adid, show_pushid_list, log_dir_name)
    # print_pushid_list(show_pushid_list)
    flush_pushid_list(show_pushid_list, out_pushid_file)
    get_show_url(adid, show_pushid_list, show_url_dict, file_list)
    # print_url_dict(show_url_dict)
    flush_url_dict(show_url_dict, out_show_file)
    get_unshow_url(adid, show_pushid_list, unshow_url_dict, file_list)
    # print_url_dict(unshow_url_dict)
    flush_url_dict(unshow_url_dict, out_unshow_file)