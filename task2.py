import argparse #arguments

parser = argparse.ArgumentParser()
parser.add_argument('-n','--packet_name', type=str)
parser.add_argument('-u','--url_link_repo', type=str)
parser.add_argument('-m','--repo_work_mode', type=str)
parser.add_argument('-v','--packet_version', type=str)
parser.add_argument('-p','--packet_reqs', type=str)
parser.add_argument('-f','--packet_filter', type=str)
args = parser.parse_args()

print("Arguments: \n"+
      f"packet_name = {args.packet_name} \n"+
      f"url_link_repo = {args.url_link_repo} \n"+
      f"repo_work_mode = {args.repo_work_mode} \n"+
      f"packet_version = {args.packet_version} \n"+
      f"packet_reqs = {args.packet_reqs} \n"+
      f"packet_filter = {args.packet_filter} ")
