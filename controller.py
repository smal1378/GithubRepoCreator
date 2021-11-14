from os.path import exists
from model import RepoCreator

# Get or Load token
if exists("token.txt"):
    with open("token.txt") as f:
        token = f.read()
else:
    token = input("Please Enter your token:")
    with open("token.txt") as f:
        f.write(token)

count = int(input("Count:"))
org_name = input("Organization Name:")
if not org_name:
    exit()
users = input("Users file list name (or empty):")
users_lst = []
if users:
    with open(users) as f:
        for i in f:
            lst = i.split(",")
            for index, name in zip(range(len(lst)), lst):
                lst[index] = name.strip()
            users_lst.append(lst)
if not users_lst:
    users_lst = None
x = RepoCreator(token, org_name)
x.create_repos(count, collaborators=users_lst)
