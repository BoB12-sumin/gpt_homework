import struct
import sys

ft_list = [b"NTFS", b"FAT", b"exFAT", b"ext", b"APFS", b"HFS+"]
file_path = sys.argv[1]
partition_number = int(sys.argv[2])
fat1_addr = 0
cnt = 0

with open(file_path, "rb") as file:
    file.seek(14)
    fc = file.read(2)
    fat1_addr = struct.unpack("<H", fc[:2])
    file.seek(fat1_addr[0] * 512)

    while True:
        file.seek(fat1_addr[0] * 512 + (partition_number * 4))
        print(partition_number, " -> ", end=" ")
        fc = file.read(4)
        cnt += 1
        if b"\xFF\xFF\xFF\x0F" == fc[:4]:
            print("EOF")
            break
        partition_number = struct.unpack("<L", fc[:4])[0]
    print("total table :", cnt)
