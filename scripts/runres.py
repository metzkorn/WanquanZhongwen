# for i in range(100):
#     with open(rf"data\test{i}.txt", "r", encoding="utf-8") as f:
#         lines = f.readlines()
#         if(len(lines) is not 50):
#             print(i)
filenames = []
for i in range (100):
    filenames.append(f'test{i}.txt')

