# import replacedict


# for i in range(100):
#     with open(rf"data\test{i}.txt", "r", encoding="utf-8") as f:
#         lines = f.readlines()
#         if(len(lines) != 100):
#             print(i)
            # replacedict.process(i)


filenames = []
for i in range (1, 15):
    filenames.append(fr"data\run{i}.txt")

with open(rf"data\new_cedict_ts.u8", "w", encoding="utf-8") as outfile:
    for fname in filenames:
        with open(fname, "r", encoding = "utf-8") as infile:
            for line in infile: 
                # if(line[-1] != "\n"):
                #     print(line, infile)
                outfile.write(line)

# for i in range(1,14):
#     with open(rf"data\run{i}.txt", "r", encoding="utf-8") as outfile:
#         lines = outfile.readlines()
#         print(len(lines))
