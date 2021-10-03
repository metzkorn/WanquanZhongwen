import sys
import re 
######################## FILES OPENED THROUGHOUT EXPERIMENTATION ####################################
# with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\data\cedict.idx',"r", encoding="utf-8") as f:
#     lines_idx = f.readlines()
# with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\data\cedict_ts.u8', "r", encoding="utf-8") as f:
#     cedict_u8 = f.readlines()
# with open(r'data\testing.txt', "r", encoding="utf-8") as f: 
#    cedict_u8 = f.readlines()


# Used to create the fresh indices
##################################################################################
def generate_indices():
    idx = 1004
    start = 35
    with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\data\new_new_cedict_ts.u8.txt', "r", encoding="utf-8") as f:
        new_cedict_u8 = f.readlines()

    # Writes the entries and their corresponding line index into a new indices file
    with open(r"newindices.txt", "w", encoding = "utf-8") as f:
        for line in new_cedict_u8[start:]:
            entry = line.split()[0:2]
            f.write(f"{entry[0]},{idx}\n")
            if entry[0] != entry[1] : # avoiding duplicates, though I am curious as to how you would solve the merge lists problem 
                                      # without duplicates. Not sure how it'd be done without dictionaries (itertools maybe?). 
                                      # for some reason duplicate indices are still showing up 
                f.write(f"{entry[1]},{idx}\n")
            for char in line:
                idx += 2 if ord(char) >= 0x10000 else 1
            idx += 1

    # reads back the new indices and sorts them
    with open(r"newindices.txt", "r", encoding = "utf-8") as f:
        lines = f.readlines()
        lines.sort()
    # stores indices sorted
    # with open(r"data\sorted_indices.idx", "w", encoding="utf-8") as f:
    #     for line in lines:
    #         f.write(line)
##################################################################################
    # takes the first instance of a key (entry) and writes it back to an index file
    # TODO: Merge groups by key instead of taking only the first member of the group
    #       This will prevent other pinyin from being lost e.g. 都 du1 dou1 
    import itertools as it
    # with open(r"data\sorted_indices.idx", "r", encoding="utf-8") as f:
        #     lines = f.readlines()

    new_lines = [x.split(",") for x in lines]
    groups = []
    keys = []
    for k,g in it.groupby(new_lines, lambda x : x[0]):
        groups.append(list(g))
        keys.append(k)

    with open(r"C:\Users\etzko\Documents\cs_projects\zhongwen\data\new_cedict.idx", "w", encoding="utf-8") as f:
        for g in groups:
            clist = [x[1][:-1] for x in g]  # need to debug this. New lines showing up and indices repeating
            f.write(",".join([g[0][0]] + clist) + "\n")
            # f.write(",".join(g[0]))




# Tests that the two files have the same entry at each line. 
#####################################  
# idx = 0
# flag = 1
# with open(r'C:\Users\etzko\Documents\cs_projects\pythonscripts\data\new_cedict_ts.u8', "r", encoding="utf-8") as f:
#         new_cedict_u8 = f.readlines()
# with open(r'test.txt', "r", encoding="utf-8") as f:
#     test = f.readlines()
#     for line in test:
#         entry1 = line.split()[0]
#         entry2 = new_cedict_u8[idx].split()[0]
#         if entry1 != entry2 and flag:
#             print(line)
#             flag = 0
#         idx += 1
######################################

# print(cedict_u8[1004] == "□") -- testing indices to dictionary reads

# Determines when indices fail using a modified file of cedict_u8 that had spaces at the end of each line.
#########################################################################
# min = sys.maxsize
# for line in lines_idx:
#     curr = line.split(",")
#     if len(curr) > 2:
#         idx += 1
#     word = curr[0]

#     for index in curr[1:]:
#         if(int(index) < len(cedict_u8)):
#             try:
#                 nl_idx = cedict_u8.index('\n',int(index))
#             except:
#                 print("test")
#                 print(int(index))
#             else:
#                 if word not in cedict_u8[int(index):nl_idx]:
#                     if(min > int(index)):
#                         min = int(index)
# print(min)
# print(cedict_u8[min+1])
###################################################################


# one idea for creating the indices is by modifying the current index file using the offsets
###################################### PSEUDOCODE ###########################################
#for each line in cedict_old & cedict_new
#   curr_line.offset = cedict_new.curr_line.length - cedict_old.curr_line.length + prev_lines.offset

#for each index in cedict.idx
#   determine line num in old
#   newidx = oldidx + curr_line.offset
###################################### PSEUDOCODE ###########################################


# with open(r'data\testidx.txt', "w", encoding ="utf-8") as f:
#     for line in lines_idx:
#         curr = line.split(",")
#         word = curr[0]
#         word_found = False
#         max = len(cedict_u8)
#         for index in curr[1:]:
#         #     # while(not word_found):
#             if(int(index) > max):
#                 print(curr)

if __name__ == "__main__": 
    #with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\backup\new_new_cedict_ts.u8.txt', "r", encoding="utf-8") as f:
    #    prev_dict = f.readlines()
    #with open(r'C:\Users\etzko\Documents\cs_projects\zhongwen\data\new_new_cedict_ts.u8.txt', "w", encoding="utf-8") as f: 
        #for line in prev_dict: 
            #f.write(re.sub("//", "/没有定义/", line)) 
                # replace "// with definition"
    generate_indices()