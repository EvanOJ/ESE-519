import mmap
import numpy as np
from ctypes import *

import os.path
import os
import time





class ShareMemWriter:

    def __init__(self, fid, data, tag_name):
        self.fid = fid
        self.data = data
        self.tag_name = tag_name
        self.mm = None
        self.wbyte = 0
        self.rbyte = 0
        self.dbyte = 0
        self.size = 0
        self.data_size = 0

    def calculate_size(self):
        size = 8 * 5  # data_header_size
        self.data_size = 8 * len(self.data)
        self.size = size + self.data_size


    def create_mapping(self):

        print(self.size)
        print(self.fid.fileno())
        self.mm = mmap.mmap(self.fid.fileno(), access=mmap.ACCESS_WRITE, length=self.size)

    def write_string(self):
        #for test purpose
        self.mm.write(b"hello world")
        self.mm.flush()

    def write_data_header(self):

        print(self.mm.tell())
        print("this is size")
        print(self.size)
        self.mm.seek(0)
        self.mm.write(cast(self.size, POINTER(c_int64)))


        self.mm.write(cast(self.data_size, POINTER(c_int64)))
        self.mm.write(cast(self.wbyte, POINTER(c_int64)))
        self.mm.write(cast(self.rbyte, POINTER(c_int64)))
        self.mm.write(cast(self.dbyte, POINTER(c_int64)))
        print(self.mm.tell())



    def write_data(self, data):
        print("pointer is here", self.mm.tell())
        #buffer_data = self.data.astype(np.double)
        buffer_data = data.astype(np.double)
        #print(self.mm.tell())
        print("data size is ", len(data))
        self.mm.write(buffer_data)
        self.mm.flush()

        return 0

    def reset(self):
        self.mm.seek(0)



class ShareMemReader:

    def __init__(self,fid,  tag_name):
        self.fid = fid
        self.size = 8
        self.tag_name = tag_name
        self.mm = None
        self.content = None
        self.content_idx = 0

    def create_mapping(self):

        self.mm = mmap.mmap(self.fid.fileno(), length=self.size, access=mmap.ACCESS_COPY)
        #self.mm = mmap.mmap(-1, length=, prot=mmap.PROT_WRITE | mmap.PROT_READ)


    def read_data_size(self):

        print(self.mm.tell())
        self.mm.seek(0)
        temp_cont = self.mm.read(8)
        data_temp_filesz = cast(temp_cont, POINTER(c_int64))
        print(self.mm.tell())
        self.size = data_temp_filesz.contents.value
        print(self.size)
        self.mm.close()
        self.mm = None

        return 0

    def char_2_int(self):
        o_temp = cast(self.content[self.content_idx:self.content_idx + 8], POINTER(c_int64))
        o_value = o_temp.contents.value
        self.content_idx = self.content_idx + 8
        return o_value

    def copy_buffer(self):

        print("current pos", self.mm.tell())
        self.content = self.mm.read(self.size)
        self.content_idx = 0

    def read_data_header(self):

        data_int = []

        for i in range(5):
            data_int.append(self.char_2_int())

    def read_data_body(self):
        data_buffer = self.content[self.content_idx:len(self.content)]
        print(len(data_buffer))
        data = np.frombuffer(data_buffer, dtype= np.double, count = 100)
        return data

    def reset(self):
        self.mm.seek(0)

    def close(self):
        self.mm.close()


def check_mem_exists(cur_path):
    result = os.path.isfile(cur_path)
    print(result)
    return result

def create_mem_file(cur_path):


    with open(cur_path, "w+b") as f:
        st = np.arange(400).astype(np.double)
        f.write(st)
    size = os.path.getsize(cur_path)
    print("create file size of ", size)

def main():
    cur_dir = os.getcwd()
    cur_path = os.path.join(cur_dir, "memorymap", "sharemem.txt")


    x = input()
    name = "sharemem"

    if (x == "w"):
        if not check_mem_exists(cur_path):
            print("create new memory map ")
            create_mem_file(cur_path)

        with open(cur_path, "r+", encoding="UTF-8") as fshare:
            print("write data into memory")
            data = np.array([1000.1,2000.0, -3000.0])

            smw = ShareMemWriter(fshare, data, name)

            print("start writing --------------------------")
            smw.calculate_size()
            smw.create_mapping()
            tic = time.process_time()
            #smw.write_string()
            smw.write_data_header()
            smw.write_data(data)
            toc = time.process_time()
            print("time used", 1000*(toc - tic))
            print("writing finished -----------------------")
            input("Press Enter to continue...")

    else:

        with open(cur_path, "r+", encoding="UTF-8") as fshare:
            smr = ShareMemReader(fshare, name)
            print("start reading --------------------------")
            smr.create_mapping()

            smr.read_data_size()




            while(True):

                tic = time.clock()
                smr.create_mapping()
                smr.copy_buffer()
                smr.read_data_header()
                result = smr.read_data_body()
                toc = time.clock()
                print(np.array(result))
                print("time", 1000*(tic - toc))
                smr.reset()
                smr.close()
                time.sleep(0.2)



if __name__ == "__main__":
    main()