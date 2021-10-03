import webdefparser as wdp
import threading 
import signal

# exit_event = threading.Event()

#with open(r'C:\Users\etzko\Documents\cs_projects\pythonscripts\data\cedict_ts.u8.txt', 'r',encoding="utf-8") as f:
# with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\data\cedict_ts.u8', "r", encoding="utf-8") as f: 
#     lines = f.readlines()






def update_defs():
    with open(r'C:\Users\etzko\Documents\cs_projects\pythonscripts\data\new_cedict_ts.u8', "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(r'test.txt', "a", encoding = "utf-8") as f:
        # for i in range(35): for when file was write
        #     f.write(lines[i])
        for line in lines[100151:]:
            entry = line.split()[0:3]
            if len(entry[0]) == 1:
                ret_string = wdp.find_def(entry[1])
                f.write(' '.join(entry))
                f.write(f" /{ret_string}/\n")
            else:
                f.write(line)

            

def process(i): 
    start = 0 # determines starting point for dictionary
    step_size = 100 # determines how many entries to read for each thread
    ret_string = ""
    idx = 0
    space_flag = 0
    space_flag_down = 0
    search_flag= 0
    fail_count = 0
    beg = start + i*step_size
    if(beg > 119578):
        return
    end = beg + step_size  if beg+step_size <= 119578 else 119578

    with open(rf"data\test{i}.txt", "w", encoding="utf-8") as f:
         
        portion = lines[beg:end]
        for line in portion:
            current_word = ""
            for char in line:                                # Realizing I could've used
                _ord = ord(char)                             # line.split()[1] to get current_word much faster
                if _ord < 128:                               # ¯\_(ツ)_/¯
                    if space_flag and _ord==32 : 
                        space_flag_down = 1
                    elif _ord == 32:
                        space_flag = 1

                if space_flag and not space_flag_down: 
                    if _ord is not 32:
                        current_word += char
                if space_flag_down and not search_flag:
                    if(i == 0):
                        print(f"Current idx: {idx} Current fail_count: {fail_count}")
                    ret_string = wdp.find_def(current_word)
                    search_flag = 1
                if search_flag and _ord == 93:
                    f.write(char)
                    if(ret_string == "没有定义"):
                        fail_count += 1
                    f.write(f" /{ret_string}/\n")
                    break 
                f.write(char)

            search_flag = 0
            space_flag = 0
            space_flag_down = 0
            idx += 1
#             if(exit_event.is_set()):
#                 break

# def signal_handler(signum, frame):
#     exit_event.set()

# signal.signal(signal.SIGINT, signal_handler)

def run_threads(): 
    threads = []
    for i in range(100):
        t = threading.Thread(target = process, args = [i])
        t.daemon = True 
        threads.append(t) 

    for i in range(100): 
        threads[i].start()
    for i in range(100):
        threads[i].join()


if __name__ == '__main__':
    update_defs()


            
#404 if search not found
#"https://www.zdic.net/e/sci/index.php?field=0&classid=8&keyboard={encodinghere}"
