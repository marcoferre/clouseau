#ip_filename = "hls/aximaster/vector_addition.cpp"
ip_filename = "hls/axistream/moving_average.cpp"
axistream_list_filename = "python/tools/axistream_list"

ip_file = open(ip_filename, 'r')
lines = ip_file.readlines()

axistream_list_file = open(axistream_list_filename, 'r')
axistream_list_types = axistream_list_file.readlines()

axilite_list = []
aximaster_list = []
axistream_list = []

#set the base custom ip address
BASE_ADDRESS = 0x10

for line in lines:
    if line[0:2] == "//":
        continue

    #find comm definition
    if "#pragma HLS INTERFACE" in line:
        params = {}
        parts = line.split()
        # parse all parameters
        for el in parts[4:]:
            if "=" in el:
                key, value = el.split('=')
                params[key] = value
            else:
                params[el] = 1

        #if is axi stream definition
        if parts[3] == "axis":
            axistream_list.append(params)
        #if is axi master definition
        if parts[3] == "m_axi":
            aximaster_list.append(params)

        #if is axi lite definition
        elif parts[3] == "s_axilite":
            #if is not return ip compute the address for each axilite
            if any(aximaster['port'] == params['port'] for aximaster in aximaster_list):
                params['type'] = 'aximaster'
            else:
                params['type'] = 'axilite'
            if params['port'] != 'return':
                params['address'] = hex(BASE_ADDRESS)
                BASE_ADDRESS += 0x8
                axilite_list.append(params)

if len(axistream_list) > 0:
    for idx in range(len(axistream_list)):
        axistream_list[idx]['type'] = axistream_list_types[idx].strip('\n')

### GENERATOR ###

from jinja2 import Environment, FileSystemLoader
file_loader = FileSystemLoader('python/templates')
env = Environment(loader=file_loader)
template = env.get_template('template.txt')
output = template.render(axilites=axilite_list, aximasters=aximaster_list, axistreams=axistream_list)

with open("python/out/out.py", "w") as text_file:
    text_file.write(output)
