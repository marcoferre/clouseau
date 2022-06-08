ip_filename = "hls/xadder_hw.h"

ip_file = open(ip_filename, 'r')
lines = ip_file.readlines()

ip_list = []

for line in lines:
    if line[0] == "\n":
        continue
    if line[0:2] == "//":
        continue
    if "#define" in line:
        el = line.split()
        el.pop(0)
        ip_list.append(el)

print(ip_list)