from github import Github
from github.GithubException import UnknownObjectException
_name = ""  # just to avoid name not defined error by IDE
_desc = ""  # same


class RepoCreator:
    def __init__(self, token, organization):
        github = Github(token)
        self.org = github.get_organization(organization)

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