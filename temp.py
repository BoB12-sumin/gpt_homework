import struct

# 사용 예시
file_path = "gpt_128.dd"
offset = 0
GUID_list = []
ft_list = [b"NTFS", b"FAT", b"exFAT", b"ext", b"APFS", b"HFS+"]
s_gpt_list = []
size_list = []

with open(file_path, "rb") as file:
    fc = file.read(1024)
    offset += 1024
    while True:
        fc = file.read(0x80)
        offset += 0x80
        if (
            fc[:16]
            == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        ):
            break

        start_gpt = struct.unpack("<Q", fc[32:40])[0]
        end_gpt = struct.unpack("<Q", fc[40:48])[0]

        # GUID_list.append(struct.unpack("<QQ", fc[0:16]))
        GUID_list.append(fc[:16])
        s_gpt_list.append(start_gpt)
        size = end_gpt - start_gpt
        size_list.append(size)

    for idx, s in enumerate(s_gpt_list):
        fc = file.read((s * 512) - offset)
        fc = file.read(512)
        offset += (s * 512) - offset + 512

        matched_fs_type = None
        for fs_type in ft_list:
            if fs_type in fc[:8]:
                matched_fs_type = fs_type
                break

        if matched_fs_type:
            print(
                f"{GUID_list[idx].hex()} {matched_fs_type.decode('utf-8')} {hex(s * 512)} {((size_list[idx]+1)*512)//1024//1024}MB"
            )
        else:
            print(
                f"{GUID_list[idx].hex()} Unknown FileSystem Type {hex(s * 512)} {((size_list[idx]+1)*512)//1024//1024}MB"
            )
