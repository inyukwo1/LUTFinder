import pyopencl as cl
import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'


class PyOpenCLRunner:
    def __init__(self):
        self.platform = None
        self.device = None
        self.context = None
        self.queue = None
        self.setup()

    def setup(self):
        platforms = cl.get_platforms()
        print("<<<Platforms>>>")
        for i in range(len(platforms)):
            print("[%d]: " % i, platforms[i])
        platform_num = int(input("type platform number:"))
        platform = platforms[platform_num]
        devices = platform.get_devices()
        print("<<<Devices>>>")
        for i in range(len(devices)):
            print("[%d]: " % i, devices[i])
        device_num = int(input("type device number:"))
        device = devices[device_num]
        context = cl.Context([device])
        queue = cl.CommandQueue(context)

        self.platform = platform
        self.device = device
        self.context = context
        self.queue = queue

    def build_program(self, program):
        return cl.Program(self.context, program).build()

    def alloc_buf(self, flag, size):
        return cl.Buffer(self.context, flag, size)

    def read_buf(self, src_device, dst_host):
        cl.enqueue_copy(self.queue, dst_host, src_device)

    def write_buf(self, src_host, dst_device):
        cl.enqueue_copy(self.queue, dst_device, src_host)

    def exec_program(self, func, global_size, *args):
        func(self.queue, global_size, None, *args)

    def finish(self):
        self.queue.finish()