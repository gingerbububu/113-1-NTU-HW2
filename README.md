# 113-1-NTU-HW2

## HW2-1 
### Description
* HW2-1.py traverses directories with BFS or DFS algorithm.  <br>
* The goal is to find all .txt files in the initial directory and its subdirectory.

### Executing program
* In order to run the program, execute with command line:  <br>
`python3 HW2-1.py -t <path_to_testcase0X> -r <path_to_ans0X> -s <"bfs"|"dfs">`  <br>
* Path to result file (-r) and selective search method (-s) are required args
* Default path to test file is set as "./testcase00/"
* No default value for path to result and selective search method
* If you had any problems with the parameters, run this:  <br>
`python3 HW2-1.py -h`  <br>

### Code explanation
1. Import the modules
```
import argparse
import os
```
2. Define the bfs function to find .txt files
```
def bfs_find_txt(test_dir):
    queue = [test_dir]
    txt_list = []

    while queue:
        current_dir = queue.pop(0)

        entries = sorted(os.listdir(current_dir))
        for entry in entries:
            full_path = os.path.join(current_dir, entry)
            if entry.endswith(".txt"):
                relative_path = os.path.relpath(full_path, test_dir)
                txt_list.append(f"{test_dir}/{relative_path}")
            elif os.path.isdir(full_path):
                queue.append(full_path)
    return txt_list
```
3. Define the dfs function to find .txt files
```
def dfs_find_txt(test_dir):
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
        for i in to_be_insert:
            txt_list.insert(0, i)
    return txt_list
```
4. Set the parser
```
parser = argparse.ArgumentParser(prog='HW2-1.py')

parser.add_argument("-t", "--test", default="./testcase00/", required=False, help="path to test directory") #add arguments as requirement in homework
parser.add_argument("-r", "--result", required=True, help="path to result file") #reference: https://docs.python.org/3/library/argparse.html
parser.add_argument("-s", "--search", required=True, choices=["bfs", "dfs"], help="selective search method") 
args = parser.parse_args()
```
5. Create ans0X.txt (result file) if not exist, also create directory if not exist
```
result_file = args.result
result_file_path = os.path.join("./", result_file)
head_tail = os.path.split(result_file_path)
if not os.path.exists(head_tail[0]):
    os.mkdir(head_tail[0])
if not os.path.exists(result_file_path):
    with open(result_file_path, 'w') as file:
        file.write("")
```
6. Open the result file, and write found .txt files into result file
```
f = open(result_file_path, 'w')

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
```

## HW2-2
### Description
* HW2-2.py extract .zip recursively to get the secret key.  <br>

### Executing program
* In order to run the program, execute with command line:  <br>
`python3 HW2-2.py -t <path_to_testcase0X> -r <path_to_ans0X>`
* Path to test case (-t) and path to result file (-r) are required args
* If you had any problems with the parameters, run this:  <br>
`python3 HW2-1.py -h`  <br>

### Code explanation
1. Import the modules
```
import zipfile
import os
import argparse
```
2. Set the parser
```
parser = argparse.ArgumentParser(prog='HW2-2.py')
parser.add_argument("-t", "--test", required=True, help="path to test case") #add arguments as requirement in homework
parser.add_argument("-r", "--result", required=True, help="path to result file") #reference: https://docs.python.org/3/library/argparse.html
args = parser.parse_args()
```
3. Create ans0X.txt (result file) if not exist, also create directory if not exist
```
result_file = args.result
result_file_path = os.path.join("./", result_file)
head_tail = os.path.split(result_file_path)
if not os.path.exists(head_tail[0]):
    os.mkdir(head_tail[0])
if not os.path.exists(result_file_path):
    with open(result_file_path, 'w') as file:
        file.write("")
```
4. Define the function to get password
```
current_dir = args.test

def get_password(entries):
    for entry in entries:
        if entry.endswith(".txt"):
            full_path = os.path.join(current_dir, entry)
            password_file = full_path
            with open(password_file, 'r') as f:
                password = f.read().strip()
    return password
```
5. Put the .zip file in queue, and get password from the first .zip file
```
queue = [] # whole path
entries = os.listdir(args.test)

for entry in entries:
    if entry.endswith(".zip"):
        full_path = os.path.join(current_dir, entry)
        queue.append(full_path)

password = get_password(entries)
```
6. Open .zip file in queue and extract it while queue is not empty
```
while queue:
    zip_file = queue.pop(0)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        extracted = zip_ref.namelist()
        zip_ref.extractall(path=current_dir, pwd=password.encode('utf-8'))
        password = get_password(extracted)
        # print(extracted)
        for entry in extracted:
            if entry == "secret.txt":
                secret_file_path = os.path.join(current_dir, entry)
                with open(secret_file_path, 'r') as secret_file:
                    secret = secret_file.read().strip()
                    queue = []
                    break
            if entry.endswith(".zip"):
                full_path = os.path.join(current_dir, entry)
                queue.append(full_path)
```
7. Write secret key into result file
```
f = open(result_file_path, 'w')
f.write(secret)
f.close()
```
## Authors
B12502083 蔡濬澤, b12502083@ntu.edu.tw
