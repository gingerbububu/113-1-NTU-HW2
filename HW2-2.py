import zipfile
import os
import argparse

parser = argparse.ArgumentParser(prog='HW2-2.py')
parser.add_argument("-t", "--test", required=True, help="path to test case") #add arguments as requirement in homework
parser.add_argument("-r", "--result", required=True, help="path to result file") #reference: https://docs.python.org/3/library/argparse.html
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


#get password form .txt file in test directory and put .zip file in queue
current_dir = args.test
queue = [] # whole path
entries = os.listdir(args.test)
used_password = []
for entry in entries:
    if entry.endswith(".zip"):
        full_path = os.path.join(current_dir, entry)
        queue.append(full_path)

def get_password(entries):
    for entry in entries:
        if entry.endswith(".txt"):
            full_path = os.path.join(current_dir, entry)
            if full_path in used_password:
                continue
            else:
                password_file = full_path
                used_password.append(password_file)
                with open(password_file, 'r') as f:
                    password = f.read().strip()
    return password

password = get_password(entries)

#open .zip file in queue and extract it while queue is not empty
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

#write secret key into result file
f = open(result_file_path, 'w')
f.write(secret)
f.close()