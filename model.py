from github import Github
from github.GithubException import UnknownObjectException
from keyring import set_password, get_password
from keyring.errors import InitError
from typing import List, Optional, Tuple, Callable, Generator


class LogConsole:
    def __init__(self, max_size: int = 1000):
        # this list can be optimized using a Queue implemented with a linked list
        # although it is currently fast enough for usages bellow 1000 amount of log.
        self.lst: List[Optional[Tuple[str, str]]] = [None] * max_size
        self.pointer = 0
        self.callbacks: List[Callable[[Tuple[str, str]], None]] = []

    def get_log(self, count: int = 100):
        x = 0
        for i in range(self.pointer, -1, -1):
            x += 1
            if x >= count:
                return
            yield self.lst[i]

    def log(self, module: str = "Default", message: str = "N/A"):
        if self.pointer >= len(self.lst):  # out of space
            self.pointer -= 1
            self.lst.pop(0)
        self.lst[self.pointer] = (module, message)
        for i in self.callbacks:
            i((module, message))

    def attach_callback(self, callback: Callable[[Tuple[str, str]], None]) -> int:
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
    def __init__(self, token_manager: "TokenManagerMother"):
        self.token_manager = token_manager
        self.github = Github(token_manager.load_token())

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


class TokenManagerMother:
    """
    This is the base class of every TokenManager classes.
    Every Classes that is going to manage the way that token is being saved or loaded should
    inherit this class and implement 'load_token', 'set_token' and 'has_token' methods.
    """
    def load_token(self, name: str = "Default") -> str:
        """
        returns the user token.
        caching token in an attribute would make the class faster.
        :param name:  usually this param is not going to be used, if you want to add multiple tokens name is the key
        :return: GitHub token
        """
        raise NotImplemented

    def set_token(self, token: str, name: str = "Default") -> None:
        """
        is called whenever user wants to set or update the token.
        :param token: this is the new token
        :param name: usually this param is not going to be used, if you want to add multiple tokens name is the key
        :return: nothing
        """
        raise NotImplemented

    def has_token(self, name: str = "Default") -> bool:
        """
        Whether token exists or not.
        :param name:  usually this param is not going to be used, if you want to add multiple tokens name is the key
        :return: True if token exists, otherwise False
        """
        raise NotImplemented


class TokenManagerKeyring(TokenManagerMother):
    keyring_service_name = "PythonRepoCreator"

    def __init__(self, logger: LogConsole):
        self.token: Optional[str] = None
        self.logger = logger
        self.load_token()

    def load_token(self, name: str = "Default") -> str:
        if not self.token:
            try:
                self.token = get_password(self.keyring_service_name, "Token")
            except InitError as err:
                self.logger.log("TokenManager", f"Access to keyring denied."
                                                f"\n{repr(err)}")
        return self.token

    def set_token(self, token: str, name: str = "Default"):
        self.token = token
        set_password(self.keyring_service_name, "Token", token)
        self.logger.log("TokenManager", "New token has been set.")

    def has_token(self, name: str = "Default") -> bool:
        return bool(self.token)


class NameGeneratorMother:
    # This list contains entries needed for init method args to be passed.
    # For each entry a Tuple of 'entry name' and 'entry description' should be in list.
    # Currently only strings can be taken from user.
    entries: List[Tuple[str, str]] = []
    name: str = ""  # name of the option that the user can choose between options

    def __init__(self, **kwargs):
        """
        This is the mother class of 'name' and 'description' generator classes.
        These classes are used to generate name for new repositories.
        controller.py should automatically allow users to choose between all subclasses of this class.
        :param kwargs: all entries that described in entries attribute will be passed as kwargs
        """
        raise NotImplemented

    def generate(self) -> Generator[Tuple[str, str]]:
        """
        This is a generator function that return each repository 'name' and 'description'
        :return: a generator that contains tuples of 'name' and 'description'
        """
        raise NotImplemented
