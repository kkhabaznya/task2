import argparse #arguments
import urllib.request #url
import json # string to dict
import networkx as nx # graphs
import matplotlib.pyplot as plt # graphs visual

# https://github.com/rust-lang/crates.io-index

parser = argparse.ArgumentParser()
parser.add_argument('-n','--packet_name', type=str)     # name
parser.add_argument('-u','--url_link_repo',type=str,
                    default='https://github.com/rust-lang/crates.io-index')
                                                        # url
parser.add_argument('-m','--repo_test_mode', type=str)  # if not empty -> local repo mode
parser.add_argument('-v','--packet_version', type=str)  # version
parser.add_argument('-p','--packet_reqs', type=str)     # !not used!
parser.add_argument('-f','--packet_filter', type=str)   # filter by string in name
parser.add_argument('-o','--no_optionals',
                    default="True", type=str)           # filter optionals
parser.add_argument('-d','--no_devs',
                    default="True", type=str)           # filter dev
args = parser.parse_args()

print("Arguments: \n"+
      f"packet_name = {args.packet_name} \n"+
      f"url_link_repo = {args.url_link_repo} \n"+
      f"repo_test_mode = {args.repo_test_mode} \n"+
      f"packet_version = {args.packet_version} \n"+
      f"packet_reqs = {args.packet_reqs} \n"+
      f"packet_filter = {args.packet_filter} \n"+
      f"no_optionals = {args.no_optionals} \n"+
      f"no_devs = {args.no_devs} ")

if args.packet_name == None:
    print("no packet name")
    exit()
if args.url_link_repo == None and args.repo_test_mode == None:
    print("no repo link")
    exit()
if args.packet_version == None:
    print("no packet version")
    exit()
    
global Graph
Graph = nx.Graph()
global cycled
cycled = []

def getLink(name):
    link = args.url_link_repo
    if len(name) >= 4:
        a = name[0:2]
        b = name[2:4]
        link += "/raw/refs/heads/master/" + a + "/" + b + "/" + name
    elif len(name) == 3:
        a = "3"
        b = name[0]
        link += "/raw/refs/heads/master/" + a + "/" + b + "/" + name
    else:
        a = str(len(name))
        b = name
        link += "/raw/refs/heads/master/" + a + "/" + b

    return link

def findDependencies(name,version):
    if args.repo_test_mode != None:
        with open('test.txt', 'r') as f:
            for line in f:
                data = json.loads(line)
                if data.get('name') == name and data.get('vers') == version:
                    return data.get("deps")
        print("error while reading")
        exit()
    try:
        reading = urllib.request.urlopen(getLink(name))
        data = reading.read()
        data = data.decode("utf-8")
    except urllib.error.URLError as e:
        print(name,version)
        print(e.reason)
        exit()
    result = None
    if '=' in version or '>=' or '~' in version:
        version = version.replace('>',"")
        version = version.replace('=',"")
        version = version.replace('~',"")
        version = version.split(',')
        version = version[0]
    if '*' in version:
        version = version.replace('*',"0")
    for line in data.splitlines():
        if "\"vers\":\""+version in line or '^' in version:
            result = line
    if result == None:
        print(version)
        print("version not found")
        exit()
    result = json.loads(result)
    result = result.get("deps")
    return result

def BFSgraph(node,startNode,queue):
    global cycled
    global Graph
    print("\ncurrent node -->",node,"\n")
    cycled.append(node.get('name'))
    if node.get('package'):
        data = findDependencies(node.get('package'),node.get('req'))
    else:
        data = findDependencies(node.get('name'),node.get('req'))
    override_to_start = False
    if len(list(Graph.nodes)) == 1:
        override_to_start = True
    for item in data:
        if args.no_optionals    == "True" and item.get('optional') == True:
            continue
        if args.no_devs == "True" and item.get('kind') == 'dev':
            continue
        if args.packet_filter != None and args.packet_filter in item.get('name'):
            continue
        if item.get('name') not in cycled:
            cycled.append(item.get('name'))
            queue.append(item)
            Graph.add_node(item.get('name'))
        print(item)
        if override_to_start:
            Graph.add_edge(startNode,item.get('name'))
        else:
            Graph.add_edge(node.get('name'),item.get('name'))
    if len(queue) > 0:
        newNode = queue[0]
        del queue[0]
        BFSgraph(newNode,startNode,queue)

def buildDependenciesGraph(name,version):
    global Graph
    Graph.add_node(name)
    queue = []
    data = findDependencies(name,version)
    BFSgraph({'name':name,'req':version},name,queue)

buildDependenciesGraph(args.packet_name,args.packet_version)
nx.draw_shell(Graph, with_labels = True)
plt.show()
