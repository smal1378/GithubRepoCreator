from model import RepoCreator, TokenManagerMother, TokenManagerText
from os.path import exists
from view import AskString, UserPanel
from db import SimpleDB
from pickle import load
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


user = UserPanel()

if "TokenManager" not in appdata:
    appdata["TokenManager"] = TokenManagerText
token_manager: TokenManagerMother = appdata["TokenManager"]()
if not token_manager.has_token():
    token = AskString(user, "Please create a token in GitHub and enter it here:",
                      "Ask For Token").get_answer()
    if token:
        token_manager.set_token(token)
    else:
        exit_app()

user.mainloop()
