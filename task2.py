import argparse #arguments
import urllib.request #url
import re # regex
import json # string to dict

# https://github.com/rust-lang/crates.io-index

parser = argparse.ArgumentParser()
parser.add_argument('-n','--packet_name', type=str)     # name
parser.add_argument('-u','--url_link_repo', type=str)   # url
parser.add_argument('-m','--repo_work_mode', type=str)  # !not used!
parser.add_argument('-v','--packet_version', type=str)  # version
parser.add_argument('-p','--packet_reqs', type=str)     # !not used!
parser.add_argument('-f','--packet_filter', type=str)   # !not used!
args = parser.parse_args()

print("Arguments: \n"+
      f"packet_name = {args.packet_name} \n"+
      f"url_link_repo = {args.url_link_repo} \n"+
      f"repo_work_mode = {args.repo_work_mode} \n"+
      f"packet_version = {args.packet_version} \n"+
      f"packet_reqs = {args.packet_reqs} \n"+
      f"packet_filter = {args.packet_filter} ")

if args.packet_name == None:
    print("no packet name")
    exit()
if args.url_link_repo == None:
    print("no repo link")
    exit()
if args.packet_version == None:
    print("no packet version")
    exit()

link = args.url_link_repo
if len(args.packet_name) >= 4:
    a = args.packet_name[0:2]
    b = args.packet_name[2:4]
elif len(args.packet_name) == 3:
    a = "3"
    b = args.packet_name[0]
else:
    a = str(len(args.packet_name))
    b = args.packet_name
link += "/raw/refs/heads/master/" + a + "/" + b + "/" + args.packet_name

print(link)

try:
    reading = urllib.request.urlopen(link)
    data = reading.read()
    data = data.decode("utf-8")
    print(data)
except urllib.error.URLError as e:
   print(e.reason)

result = None
for line in data.splitlines():
    if "\"vers\":\""+args.packet_version in line:
        result = line
if result == None:
    print("version not found")
    exit()

result = json.loads(result)
iterate = result.get("deps")
for item in iterate:
    print(item)

