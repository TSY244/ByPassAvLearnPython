import ctypes


lib=ctypes.CDLL("./HelloDll.dll") # 记载dll 路径

lib.hello() # hello 是函数的名字