import webdefparser as wdp
import threading 

#with open(r'C:\Users\etzko\Documents\cs_projects\pythonscripts\data\cedict_ts.u8.txt', 'r',encoding="utf-8") as f:
with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\data\cedict_ts.u8', "r", encoding="utf-8") as f: 
    lines = f.readlines()

space_flag = 0
space_flag_down = 0
search_flag= 0
ret_string = ""
idx = 0
lines = lines[2404:]
fail_count = 0


with open(r"data\test.txt", "w", encoding="utf-8") as f:
    for line in lines:
        current_word = ""
        for char in line:
            _ord = ord(char)
            if _ord < 128:
                if space_flag and _ord==32 : 
                    space_flag_down = 1
                elif _ord == 32:
                    space_flag = 1
                
            if space_flag and not space_flag_down: 
                if _ord is not 32:
                    current_word += char
            if space_flag_down and not search_flag:
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


def process(): 
    pass 
            
#404 if search not found
#"https://www.zdic.net/e/sci/index.php?field=0&classid=8&keyboard={encodinghere}"
