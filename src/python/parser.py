ip_filename = "hls/aximaster/vector_addition.cpp"

ip_file = open(ip_filename, 'r')
lines = ip_file.readlines()

axilite_list = []
aximaster_list = []

#set the base custom ip address
BASE_ADDRESS = 0x10

for line in lines:
    if line[0] == "\n":
        continue
    if line[0:2] == "//":
        continue

    #find comm definition
    if "#pragma HLS INTERFACE" in line:
        params = {}
        parts = line.split()
        #if is axi master definition
        if parts[3] == "m_axi":
            #parse all parameters
            for el in parts[4:]:
                key, value = el.split('=')
                params[key] = value
            aximaster_list.append(params)

        #if is axi lite definition
        elif parts[3] == "s_axilite":
            #parse all parameters
            for el in parts[4:]:
                key, value = el.split('=')
                params[key] = value
            #if is not return ip compute the address for each axilite
            if params['port'] != 'return':
                params['address'] = hex(BASE_ADDRESS)
                BASE_ADDRESS += 0x8

            axilite_list.append(params)


print(axilite_list)