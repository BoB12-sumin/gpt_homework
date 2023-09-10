import struct
import sys

ft_list = [b"NTFS", b"FAT", b"exFAT", b"ext", b"APFS", b"HFS+"]
file_path = sys.argv[1]
offset = 0
address = 0
static_addr = 0
partition = list()
part_type = list()
sector = list()
sector_size = list()
endflag = False

with open(file_path, "rb") as file:
    fc = file.read(446)
    offset += 446
    while True:
        fc = file.read(0x10)
        offset += 0x10
        if 5 == fc[4]:
            break
        elif 7 == fc[4]:
            a = struct.unpack("<L", fc[8:12])
            nsize = struct.unpack("<L", fc[12:16])
            partition.append(a[0] * 512)
            sector.append(hex(address + a[0] * 512))
            sector_size.append((nsize[0] * 512) / 1024 / 1024)

    a = struct.unpack("<L", fc[8:12])
    # print(hex(offset))
    for i in partition:
        file.seek(i)
        offset = file.tell()
        fc = file.read(8)
        part_type.append(fc[:8])
    # trace ebr
    fc = file.seek(a[0] * 512)
    offset = file.tell()
    static_addr = offset
    address = static_addr

    while True:
        fc = file.read(446)
        offset += 446
        if endflag == True:
            break

        while True:
            fc = file.read(0x10)
            offset += 0x10
            if 5 == fc[4]:
                break
            elif 7 == fc[4]:
                a = struct.unpack("<L", fc[8:12])
                nsize = struct.unpack("<L", fc[12:16])
                partition.append(address + a[0] * 512)
                sector.append(hex(address + a[0] * 512))
                sector_size.append((nsize[0] * 512) / 1024 / 1024)
            elif 0 == fc[4]:
                endflag = True
                break

        ebr = struct.unpack("<L", fc[8:12])
        file.seek(address + a[0] * 512)
        fc = file.read(8)
        offset = file.tell()
        part_type.append(fc[:8])
        fc = file.seek(static_addr + (ebr[0] * 512))
        offset = file.tell()
        address = offset

for p, s, sz in zip(part_type, sector, sector_size):
    matched_fs_type = None
    for fs_type in ft_list:
        if fs_type in p:
            matched_fs_type = fs_type
            break
    if matched_fs_type:
        print(matched_fs_type.decode("UTF-8"), s, sz)
        print("=====================================")
