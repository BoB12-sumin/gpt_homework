import struct
import sys

# file_path = sys.argv[1]

with open("ntfs.dd", "r+b") as file:
    fc = file.read(0x200)
    mft0_offset = struct.unpack("<H", fc[0x30:0x32])
    file.seek(mft0_offset[0] * 0x1000)
    fc = bytearray(file.read(0x400))
    offset_Fixup_array =fc[0x4] # Unpack the first element from the tuple
    Fixup_array_size = fc[0x6]  # Unpack the first element from the tuple
    offset_attr = fc[0x14]

    while Fixup_array_size >= 1:
        sec_end = 0x200
        print('변환 전', ' '.join('{:02x}'.format(b) for b in fc[sec_end - 2: sec_end]))
        fc[sec_end-2] =fc[offset_Fixup_array + 2]
        fc[sec_end-1] = fc[offset_Fixup_array + 3]
        print('변환 후', ' '.join('{:02x}'.format(b) for b in fc[sec_end-2 : sec_end]))
        offset_Fixup_array += 2
        Fixup_array_size -= 1
        sec_end+0x200

    i = 0
    while(True): #attribute
        attr_id=struct.unpack("<L", fc[offset_attr:offset_attr+4])[0]
        attr_next = struct.unpack("<L", fc[offset_attr+4:offset_attr+8])[0]
        if(attr_id==0x80):
            print("this is Data attribute")
            if(0x00 == fc[offset_attr + 0x8]):
                print("This is resident")
            elif (0x01 == fc[offset_attr + 0x8]):
                print("This is non-resident")
                offset_runlist=struct.unpack('H', fc[offset_attr+0x20:offset_attr+0x20+2])[0]
                total = 0
                while(True):
                    run_id = fc[offset_attr + offset_runlist]
                    if(run_id==0x00):
                        break
                    print(hex(run_id))
                    front_byte = (run_id >> 4) & 0x0F
                    # # 뒤 한 글자 추출
                    back_byte = run_id & 0x0F
                    # print(front_byte,back_byte)
                    # print(hex(offset_runlist))
                    # print(hex(offset_attr))

                    formats1 = ['B', 'H', '3B', 'L', '5B', '6B', '7B', 'LL', "9B", "10B", "11B", "12B", "13B", "14B", "15B"]
                    formats2 = ['b', 'h', '3b', 'l', '5b', '6b', '7b', 'll', "9b", "10b", "11b", "12b", "13b", "14b","15b"]
                    selected_format1 = formats2[front_byte - 1]  # 0부터 인덱스 시작이므로 1 빼줌
                    selected_format2 = formats1[back_byte - 1]
                    len_data1 = struct.unpack(selected_format2, fc[offset_attr + offset_runlist + 1:offset_attr + offset_runlist + 1 + back_byte])[0]
                    print("len data", (len_data1))

                    offset_data2 = struct.unpack(selected_format1, fc[offset_attr + offset_runlist + 1 + back_byte :offset_attr + offset_runlist + 1 + front_byte + back_byte])[0]
                    print("offset data", (offset_data2))
                    total+=offset_data2

                    offset_runlist = offset_runlist + 1 + front_byte + back_byte


        offset_attr += attr_next

        if fc[offset_attr] == 0 or struct.unpack("<L", fc[offset_attr:offset_attr+4])[0] == 0xffffffff:
            break






