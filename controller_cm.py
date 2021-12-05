# controller_cm.py
# This modules runs the project in command line mode (without GUI)

from model import RepoCreator, TokenManagerMother, TokenManagerText, LogConsole
from model import NameGeneratorMother, CollaboratorManagerMother
from os.path import exists
from db import SimpleDB
from pickle import load
from github.GithubException import GithubException
# load data from file or create if it's first time

if exists("db_class.bin"):
    with open("db_class.bin", "rb") as f:
        Db = load(f)
else:
    Db = SimpleDB
appdata = Db()


def exit_app():
    appdata.save()
    exit()


print("GithubRepoCreator - Welcome - CommandLine mode")
# check if there is token?
if "TokenManager" not in appdata:
    appdata["TokenManager"] = TokenManagerText
token_manager: TokenManagerMother = appdata["TokenManager"]()
if not token_manager.has_token():
    token = input("Looks like you don't have a token \n"
                  "Enter your github token:")
    if token:
        token_manager.set_token(token)
    else:
        exit_app()

logger = LogConsole()
rc = RepoCreator(token_manager, logger)


repo_master = input("Enter Organization Name or empty:").strip()
if repo_master == "exit":
    exit_app()


print("---- Available NameGenerators ----")
options = {}
for option in NameGeneratorMother.__subclasses__():
    options[option.name] = option

print(*options.keys(), sep=" - ")
while True:
    option = input("Enter NameGenerator Engine Name:").strip()
    if option == "exit":
        exit_app()
    if option in options:
        option = options[option]
        break
    else:
        print("Sorry, That didn't match! - you can type 'exit' any time..")

dict_params = {}
for name, info in option.entries:
    print(f"Field: {name}, Info: {info} from NameGenerator {option.name}")
    value = input("Enter Value for Field:").strip()
    dict_params[name] = value

name_generator = option(**dict_params)


print("---- General Info ----")
while True:
    count = input("Enter How Many Repos To Create:").strip()
    if count == "exit":
        exit_app()
    if count.isnumeric() and 0 < int(count) < 100:  # max repos to create is 100
        count = int(count)
        break
    else:
        print("Sorry, That didn't match! - you can type 'exit' any time..")

while True:
    private = input("Enter Are Repos Private (y or n):").strip()
    if private == "exit":
        exit_app()
    if private == "n":
        private = False
        break
    elif private == "y":
        private = True
        break
    else:
        print("Sorry, That didn't match! - you can type 'exit' any time..")

template = input("Enter Template Name for .gitignore file (empty for Python)").strip()
if template == "":
    template = "Python"

print("---- Collaborators ----")
while True:
    ans = input("Enter Are There Any Collaborators (y or n):").strip()
    if ans == "exit":
        exit_app()
    if ans == "n":
        ans = False
        break
    elif ans == "y":
        ans = True
        break
    else:
        print("Sorry, That didn't match! - you can type 'exit' any time..")

collaborator_manager = None
role = "maintain"
if ans:
    print("Collaborate Roles Are: 'admin', 'maintain', 'read', 'triage', 'write'")
    while True:
        role = input("Enter Collaborators Role (empty for maintain):").strip()
        if role == "":
            role = "maintain"
        if role == "exit":
            exit_app()
        if role in ("admin", "maintain", "read", "triage", "write"):
            break
        else:
            print("Sorry, That didn't match! - you can type 'exit' any time..")

    collaborator_managers = {}
    for cm in CollaboratorManagerMother.__subclasses__():
        collaborator_managers[cm.name] = cm
    print("Available CollaboratorManagers:")
    print(*collaborator_managers.keys(), sep=" - ")
    while True:
        cm = input("Enter Collaborator Manager Name:")
        if cm == "exit":
            exit_app()
        if cm in collaborator_managers:
            cm = collaborator_managers[cm]
            break
        else:
            print("Sorry, That didn't match! - you can type 'exit' any time..")

    dict_params = {}
    for name, info in cm.fields.items():
        print(f"Field: {name}, Info: {info} from CollaboratorManager {cm.name}")
        value = input("Enter Value for Field:").strip()
        dict_params[name] = value

    collaborator_manager = cm(**dict_params)


print("--- Starting ---")

error = False
try:
    if collaborator_manager:
        rc.start(count, repo_master, name_generator, collaborator_manager.get(), role, private, template)
    else:
        rc.start(count, repo_master, name_generator, [[]]*count, role, private, template)
except GithubException as exc:
    print("------ Error ------")
    print(repr(exc))
    error = True

print("----  Logs ----")
print(*logger.get_log(1000), sep="\n")

print("---- Finish ----")
if error:
    print("There Was An Error :(")

exit()
