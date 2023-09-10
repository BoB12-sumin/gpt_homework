import struct

ft_list = [b"NTFS", b"FAT", b"exFAT", b"ext", b"APFS", b"HFS+"]
file_path = "mbr_128.dd"
offset = 0
address = 0
static_addr = 0

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
            print(
                "filesystem type : 0x07",
                "partition",
                hex(address + a[0] * 512),
                "size",
                (nsize[0] * 512) / 1024 / 1024,
            )
            print("=====================================")

    a = struct.unpack("<L", fc[8:12])

    # trace ebr
    fc = file.read((a[0] * 512) - offset)
    offset += (a[0] * 512) - offset
    # print("현재 EBR 주소", hex(offset))
    static_addr = offset
    address = static_addr

    while True:
        # print("offset : ", hex(offset))
        fc = file.read(446)
        offset += 446
        if (
            fc[:16]
            == b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        ):
            break
        else:
            while True:
                fc = file.read(0x10)
                offset += 0x10
                if 5 == fc[4]:
                    break
                elif 7 == fc[4]:
                    a = struct.unpack("<L", fc[8:12])
                    nsize = struct.unpack("<L", fc[12:16])

                    print(
                        "filesystem type : 0x07",
                        "partition",
                        hex(address + a[0] * 512),
                        "size",
                        (nsize[0] * 512) / 1024 / 1024,
                    )
                    print("=====================================")

            ebr = struct.unpack("<L", fc[8:12])
            fc = file.read(static_addr + (ebr[0] * 512) - offset)
            offset += static_addr + (ebr[0] * 512) - offset
            address = offset
