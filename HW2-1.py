import argparse
import os

#find all .txt files in test directory in bfs order
def bfs_find_txt(test_dir):
    #finish this function
    queue = [test_dir]
    txt_list = []

    while queue:
        current_dir = queue.pop(0)

        entries = sorted(os.listdir(current_dir)) # correct
        for entry in entries:
            full_path = os.path.join(current_dir, entry)
            if entry.endswith(".txt"):
                relative_path = os.path.relpath(full_path, test_dir)
                txt_list.append(f"{test_dir}/{relative_path}")
            elif os.path.isdir(full_path):
                queue.append(full_path)
    return txt_list #you may change return value as you wish

#find all .txt files in test directory in dfs order
def dfs_find_txt(test_dir):
    #finish this function
    stack = [test_dir]
    txt_list = []
    while stack:
        current_dir = stack.pop(-1)
        entries = sorted(os.listdir(current_dir))

        to_be_insert = []
        for entry in entries:
            full_path = os.path.join(current_dir, entry)
            if os.path.isdir(full_path):
                stack.insert(0, full_path)
            elif entry.endswith(".txt"):
                relative_path = os.path.relpath(full_path, test_dir)
                to_be_insert.append(f"{test_dir}/{relative_path}")
        to_be_insert.sort(reverse=True)
        # print(to_be_insert)
        for i in to_be_insert:
            txt_list.insert(0, i)
        # print("txt_list =", txt_list)
        # print("stack =", stack)
    return txt_list #you may change return value as you wish        

#execute with command line: python3 thisfile.py -t <path_to_testcase0X> -r <path_to_ans0X.txt> -s <"bfs" | "dfs">
#set path to result file and selective search method as required args
#set default path to test file as "./testcase00/"
#no default value for path to result and selective search method

parser = argparse.ArgumentParser(prog='HW2-1.py')

parser.add_argument("-t", "--test", default="./testcase00", required=False, help="path to test directory") #add arguments as requirement in homework
parser.add_argument("-r", "--result", required=True, help="path to result file") #reference: https://docs.python.org/3/library/argparse.html
parser.add_argument("-s", "--search", required=True, choices=["bfs", "dfs"], help="selective search method") 
args = parser.parse_args()

#create ans0X.txt if not exist, also create directory if not exist
result_file = args.result
result_file_path = os.path.join("./", result_file)
head_tail = os.path.split(result_file_path)
if not os.path.exists(head_tail[0]):
    os.mkdir(head_tail[0])
if not os.path.exists(result_file_path):
    with open(result_file_path, 'w') as file:
        file.write("")

#open result file
f = open(result_file_path, 'w')
#write all found .txt files in test directory into result file, in bfs or dfs order
if args.search == "bfs":
    output = bfs_find_txt(args.test)
    n = len(output)
    for i in range(n):
        f.write(output[i])
        if i != n-1:
            f.write("\n")
elif args.search == "dfs":
    output = dfs_find_txt(args.test)
    n = len(output)
    for i in range(n):
        f.write(output[i])
        if i != n-1:
            f.write("\n")
f.close()

# print(dfs_find_txt("./testcase00"))
