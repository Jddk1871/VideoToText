import cv2
import os
import time
import multiprocessing
import pickle


def char_to_int(data):
    data_numbers = []
    for line in data:
        for zeichen in line:
            data_numbers.append(level_set_0.index(zeichen))
    return data_numbers


def find_double(data, mode, return_dictionary=None, part=None, min=None):
    max = len(data)
    index = 0

    if mode == 1:
        data_multi_numbers = [['del', 'del']]

        while True:
            if data[index] == data_multi_numbers[-1][1]:
                data_multi_numbers[-1][0] = data_multi_numbers[-1][0] + 1
            else:
                data_multi_numbers.append([1, data[index]])
            index += 1
            if index >= max:
                break
        data_multi_numbers.pop(0)

        return data_multi_numbers

    if mode == 2:
        double_dict = {}
        while True:
            key_i = f"{data[index]}, {data[index + 1]}"
            if double_dict.get(key_i) is None:
                double_dict[key_i] = 1
            else:
                double_dict[key_i] += 1
            index += 1
            print(end='\r' + f"{index} von {max} == {str((index / (max)))[:6]}%")
            if index >= max - 1:
                break
        print()
        double_dict = dict(sorted(double_dict.items(), key=lambda x: x[1], reverse=True))
        for a in double_dict.copy().keys():
            if double_dict[a] <= min:
                del double_dict[a]

        return_dictionary[part] = double_dict


def einlesen(des_path):
    data_in = []
    with open(os.path.join(os.path.dirname(__file__), des_path), 'r', encoding="UTF-8") as file:
        for line in file:
            data_in.append(line)

    data_numbers = char_to_int(data=data_in)

    data_multi_numbers = find_double(data_numbers, mode=1)

    data_run_set0 = []
    for pos in data_multi_numbers:
        char_times = pos[0]
        char_int = pos[1]
        if char_times <= 9:
            if char_int <= 4:
                p = f"2{char_int}{char_times}"
            elif 5 <= char_int <= 6:
                p = f"1{char_int + 3}{char_times}"
            elif char_int == 7:
                p = f"25{char_times}"
            data_run_set0.append(p)

        elif char_times >= 129:
            data_run_set0.append(80)
            data_run_set0.append(char_int)
            data_run_set0.append(char_times - 80)
            data_run_set0.append(char_int)

        else:
            data_run_set0.append(char_times)
            data_run_set0.append(char_int)

    print('--- Data_run_set0 erstellt')
    print("--- %s seconds --- " % (time.time() - start_time))
    return data_run_set0


def multi_count(cores, data, return_data, process_list, part_len, min_repeat):
    for worker in range(cores):
        if worker == cores - 1:
            list_part = data[worker * part_len:len(data)]
            p = multiprocessing.Process(target=find_double, args=(list_part, 2, return_data, worker, min_repeat))
            process_list.append(p)
            p.start()

        else:
            list_part = data[worker * part_len:(worker + 1) * part_len - 1]
            p = multiprocessing.Process(target=find_double, args=(list_part, 2, return_data, worker, min_repeat))
            process_list.append(p)
            p.start()

    for process in process_list:
        process.join()


def fusion_dict(dict):
    counter = 0
    comp_dict = {}
    comp_dict: dict[str,] = {}
    for dn in dict.values():
        if counter == 0:
            comp_dict = dn
            counter += 1
        else:
            for key_i in dn.keys():
                if comp_dict.get(key_i) is None:
                    comp_dict[key_i] = dn[key_i]

                else:
                    comp_dict[key_i] += dn[key_i]

    return comp_dict


def create_level_set(level_set_old, max_len):
    level_set_old = dict(sorted(level_set_old.items(), key=lambda x: x[1], reverse=True))
    index = 0
    for key_i in level_set_old.copy().keys():
        if index >= max_len:
            del level_set_old[key_i]
        index += 1
    return level_set_old


def level_set_fin(aus=False, min_rep=100, start_f=130, data=[]):
    print(f"--- {len(data)} elemente eingelesen ---")
    part_leng = round(len(data) / (thread_count))
    multi_count(cores=thread_count, data=data, return_data=return_dict, process_list=processes, part_len=part_leng,
                min_repeat=min_rep)

    print('--- Wiederholungen gefunden in:')
    print("--- %s seconds --- " % (time.time() - start_time))

    level_set_long = fusion_dict(return_dict)
    level_set_i = create_level_set(level_set_long, max_level_set_len)

    level_set = {}
    index = start_f
    for key_f in level_set_i:
        level_set[key_f] = index
        index += 1
        if index == 180:
            break

    if aus is True:
        print(len(level_set))
        print(level_set_i)
        print(level_set)
    print('--- Finales Level_set erstellt:')
    print("--- %s seconds --- " % (time.time() - start_time))
    return level_set


def replace_double(levels, replace_data):
    final_list = []
    index = 0
    ende = len(replace_data) - 1
    while True:
        ind = f"{replace_data[index]}, {replace_data[index + 1]}"
        if levels.get(ind) != None:
            final_list.append(int(levels.get(ind)))
            index += 1

        else:
            final_list.append(int(replace_data[index]))

        index += 1
        if index == ende:
            break
    print('--- Out_list:')
    print("--- %s seconds --- " % (time.time() - start_time))
    return final_list


def write_data(save, out, level_save, level_set):
    with open(os.path.join(os.path.dirname(__file__), level_save), "wb") as file0:
        pickle.dump(level_set, file0)

    with open(os.path.join(os.path.dirname(__file__), save), "wb") as file1:
        pickle.dump(out, file1)

    print('--- Saved ---')
    print("--- %s seconds --- " % (time.time() - start_time))


def start_conversion(save, level_save, save_in, minimum_repeat=100, max_normal_i=130):
    print('Start:')

    data_in = einlesen(save_in)
    level_set = level_set_fin(aus=False, min_rep=minimum_repeat, start_f=max_normal_i, data=data_in)

    out_list = replace_double(levels=level_set, replace_data=data_in)
    binary_format = bytearray(out_list)

    print(f"{len(binary_format)} kb")
    print('--- Binary ---')
    print("--- %s seconds --- " % (time.time() - start_time))

    write_data(save=save, out=binary_format, level_save=level_save, level_set=level_set)


def play(data_set, time_delta):
    data_set = data_set.split('\n\n')
    for a in data_set:
        print(a)
        time.sleep(time_delta)


def read_compressed_data(main_data, level_set_data, time_delta_d=0.01):
    with open(os.path.join(os.path.dirname(__file__), main_data), "rb", ) as f:
        bin_in = pickle.load(f)

    with open(os.path.join(os.path.dirname(__file__), level_set_data), "rb", ) as f1:
        level_set = pickle.load(f1)

    print('--- Daten eingelesen ---')
    print("--- %s seconds --- " % (time.time() - start_time))
    #print()

    data_in_int = []
    p_count = 0
    p_max = len(list(bin_in))
    p_part = round(p_max / 100)
    p_cur = 0
    for num in list(bin_in):
        if num <= 129 or num >= 180:
            data_in_int.append(num)

        else:
            num_i = list(level_set.keys())[list(level_set.values()).index(num)]
            num_a = num_i.replace("'", '').split(', ')
            data_in_int.append(int(num_a[0]))
            data_in_int.append(int(num_a[1]))

        if p_count == p_cur:
            print(end='\r' + f"{p_count} von {p_max} == {str(p_count/p_max)[0:4]}%")
            p_cur += p_part
        p_count += 1

    print()
    print('--- Data in int list ---')
    print("--- %s seconds --- " % (time.time() - start_time))

    data_int = []
    p_count = 0
    p_max = len(data_in_int)
    p_part = round(p_max / 100)
    p_cur = 0
    for data in data_in_int:
        if data >= 180:
            if data < 200:
                num_l = str(data)[1:3]
                data_int.append(int(num_l[1]))
                data_int.append(int(num_l[0]) - 3)
            elif 200 <= data < 250:
                num_l = str(data)[1:3]
                data_int.append(int(num_l[1]))
                data_int.append(int(num_l[0]))
            elif 250 <= data <= 255:
                num_l = str(data)[1:3]
                data_int.append(int(num_l[1]))
                data_int.append(int(num_l[0]) + 2)

        else:
            data_int.append(data)

        if p_count == p_cur:
            print(end='\r' + f"{p_count} von {p_max} == {str(p_count/p_max)[0:4]}%")
            p_cur += p_part
        p_count += 1
    print()
    print('--- Data int list ---')
    print("--- %s seconds --- " % (time.time() - start_time))

    index = 0
    data_char = ''
    max_l = len(data_int)
    p_count = 0
    p_max = len(data_int)
    p_part = round(p_max / 100)
    p_cur = 0
    while True:
        num = data_int[index]
        char = data_int[index + 1]
        index += 2
        print(num)
        print(data_char)
        print(char)

        for a in range(num):
            print(a)
            data_char += level_set_0[char]

        if index >= max_l - 1:
            break

        if p_count == p_cur:
            print(end='\r' + f"{p_count} von {p_max} == {str(p_count/p_max)[0:4]}%")
            p_cur += p_part
        p_count += 1

    print()
    print('--- Start play ---')
    print("--- %s seconds --- " % (time.time() - start_time))

    play(data_set=data_char, time_delta=time_delta_d)


def save_file(save_loc, data, count):
    data = dict(sorted(data.items()))
    line_dat = ''
    for a in range(count):
        line_dat += data.get(a)

    char_matrix = line_dat.split('+')
    with open(os.path.join(os.path.dirname(__file__), save_loc), "w") as file:
        for pic in char_matrix:
            file.write(pic)


def pic_processing(part_list, ret_dict, index, level_set_t):
    factor = 6
    max = len(part_list)
    char_matrix = ""
    index_pic = 0
    for temp_img in part_list:
        for y in range(temp_img.shape[0] - 1):
            for x in range(temp_img.shape[1] - 2):

                wert = temp_img[y, x]
                new_wert = round(factor * wert / 255) * (255 / factor)

                quant_error = wert - new_wert
                temp_img[y, x:x + 1] = new_wert

                p1 = temp_img[y, x + 1] + quant_error * 7 / 16
                if 255 - p1 > 255:
                    p1 = 0
                elif 255 - p1 < 0:
                    p1 = 255
                temp_img[y, x + 1:x + 2] = p1

                p2 = temp_img[y + 1, x - 1] + quant_error * 3 / 16
                if 255 - p2 > 255:
                    p2 = 0
                elif 255 - p2 < 0:
                    p2 = 255
                temp_img[y + 1, x - 1:x] = p2

                p3 = temp_img[y + 1, x] + quant_error * 5 / 16
                if 255 - p3 > 255:
                    p3 = 0
                elif 255 - p3 < 0:
                    p3 = 255
                temp_img[y + 1, x:x + 1] = p3

                p4 = temp_img[y + 1, x + 1] + quant_error * 1 / 16
                if 255 - p4 > 255:
                    p4 = 0
                elif 255 - p4 < 0:
                    p4 = 255
                temp_img[y + 1, x + 1:x + 2] = p4

        str_pic = []


        for y in range(temp_img.shape[0]):
            row = []
            for x in range(temp_img.shape[1]):
                pos_i = round(float(temp_img[y, x]) / (255 / factor))
                char = level_set_t[pos_i]
                row.append(char)
            str_pic.append(row)

        char_list = ""

        for char_lane in str_pic:
            char_part = ""
            for char in char_lane:
                char_part += str(char)
            char_list += char_part + '\n'

        char_matrix += '\n' + char_list + '+'
        index_pic += 1
        print(end='\r' + f"{index_pic} von {max} == {str((index_pic / (max)))[:6]}%")

    ret_dict[index] = char_matrix


def dimensions(width, capture_dev):
    #print(width)
    #print(capture_dev.get(1))
    #print(capture_dev.get(2))
    #print(capture_dev.get(3))

    scale_ratio = float(width / capture_dev.get(3))
    width = int((capture_dev.get(3) * scale_ratio) * 2)
    height = int((capture_dev.get(4) * scale_ratio) / 2)
    dim = (width, height)
    return dim


def multi_pic(cap_source, total_width, thread, ret_pr_dict, process_list, save, level_set_tt):
    cap = cv2.VideoCapture(cap_source)
    #print(cap.get(3))
    current_frame = 0
    dim = dimensions(total_width, cap)
    vid_frames = []

    while (cap.isOpened()):
        print(end="\r" f"Reading rame: {current_frame} von {cap.get(7)}")
        current_frame += 1
        ret, frame = cap.read()

        if frame is None:
            print()
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
        vid_frames.append(resized)

    part_len = round(len(vid_frames) / thread)

    for worker in range(thread):
        if worker == thread - 1:
            list_part = vid_frames[worker * part_len:len(vid_frames)]
            p = multiprocessing.Process(target=pic_processing, args=(list_part, ret_pr_dict, worker, level_set_tt))
            process_list.append(p)
            p.start()

        else:
            list_part = vid_frames[worker * part_len:(worker + 1) * part_len - 1]
            p = multiprocessing.Process(target=pic_processing, args=(list_part, ret_pr_dict, worker, level_set_tt))
            process_list.append(p)
            p.start()

    for process in process_list:
        process.join()

    save_file(save_loc=save, data=ret_pr_dict, count=thread)


if __name__ == '__main__':
    level_set_0 = [' ', '"', ',', '(', 'S', '#', '@', '\n']
    max_normal = 130
    max_level_set_len = 180 - max_normal
    start_time = time.time()

    manager = multiprocessing.Manager()
    return_pic_dict = manager.dict()
    return_dict = manager.dict()
    processes_pic = []
    processes = []

    thread_count = multiprocessing.cpu_count()

    breite = 120
    ordner = "02"
    vid_path = f"Zusatz\\{ordner}\\vid.mp4"
    save_vidtotext = f"Zusatz\\{ordner}\\temp.txt"
    save_ft = f"Zusatz\\{ordner}\\ft.bin"
    save_fl = f"Zusatz\\{ordner}\\fl.bin"




    #multi_pic(cap_source=vid_path, total_width=breite, thread=thread_count, ret_pr_dict=return_pic_dict, process_list=processes_pic, save=save_vidtotext, level_set_tt=level_set_0)
    #start_conversion(save_in=save_vidtotext, save=save_ft, level_save=save_fl, minimum_repeat=100, max_normal_i=max_normal)
    read_compressed_data(main_data=save_ft, level_set_data=save_fl, time_delta_d=0.03)

    print('--- Ende ---')
    print("--- %s seconds --- " % (time.time() - start_time))

