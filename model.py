from github import Github
from github.GithubException import UnknownObjectException
from keyring import set_password, get_password
from keyring.errors import InitError
_name = ""  # just to avoid name not defined error by IDE
_desc = ""  # same
keyring_service_name = "PythonRepoCreator"


class LogConsole:
    def __init__(self, max_size: int = 1000):
        self.lst = [None] * 1000  # this list can be optimized using a Queue implemented with a linked list
        self.pointer = 0
        self.callbacks = []

    def get_log(self, count: int = 100):
        x = 0
        for i in range(self.pointer, -1, -1):
            if x > i:
                return
            yield self.lst[i]

    def log(self, module: str = "Default", message: str = "N/A"):
        if self.pointer >= len(self.lst):  # out of space
            self.pointer -= 1
            self.lst.pop(0)
        self.lst[self.pointer] = (module, message)
        for i in self.callbacks:
            i((module, message))

    def attach_callback(self, callback) -> int:
        """
        Will call the callback whenever a new log message has been added.
        :param callback: callback(Tuple[str, str]), Tuple contains module name and message text
        :return: callback id.
        """
        self.callbacks.append(callback)
        return len(self.callbacks) - 1

    def detach_callback(self, _id: int):
        self.callbacks.pop(_id)


class RepoCreator:
    def __init__(self):
        self.token = None
        self.load_token()
        # github = Github(token)
        # self.org = github.get_organization(organization)

    def create_repos(self, count: int, names: str = "G{'0'*(2-len(str(i)))}{i}T3",
                     description: str = "DS4001 - Group {'0'*(2-len(str(i)))}{i} - Test 3",
                     collaborators: list = None):
        # TODO: make names and description arguments work :|
        assert isinstance(count, int)
        assert 1 <= count
        assert isinstance(names, str)
        assert isinstance(description, str)
        if not collaborators:
            collaborators = [[]] * count
        assert isinstance(collaborators, list)
        assert len(collaborators) == count
        for i in range(count):
            rep = self.org.create_repo(f"G{'0'*(2-len(str(i+1)))}{i+1}T3",
                                       f"DS4001 - Group {'0'*(2-len(str(i+1)))}{i+1} - Test 3",
                                       private=True,
                                       gitignore_template="Python", auto_init=True)
            for collaborator_name in collaborators[i]:
                if not collaborator_name:
                    continue
                try:
                    rep.add_to_collaborators(collaborator_name, "maintain")
                except UnknownObjectException as exc:
                    print(f"Log: error while adding collaborator at number {i}"
                          f" - collaborator {collaborator_name} \n Exception:"
                          f"{repr(exc)}")

    def load_token(self):
        try:
            self.token = get_password(keyring_service_name, "Token")
        except InitError as err:
            # TODO: Log In Console
            pass

    def set_token(self, token: str):
        self.token = token
        set_password(keyring_service_name, "Token", token)

    def has_token(self):
        return bool(self.token)
