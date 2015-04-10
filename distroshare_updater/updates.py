from git import Repo
from git.exc import GitCommandError
import os

class GitRepos:    
    _config = None
    _base_repo = None
    _machine_repo = None
    def __init__(self, config):
        """Takes a DUConfigParser object and initializes the git repos"""
        self._config = config
        self._base_repo = self.init_repo(config.get_git_base_repo(), 
                                    config.get_git_common_dir())
        self._machine_repo = self.init_repo(config.get_git_machine_repo(), 
                                       config.get_git_machine_dir())
    def init_repo(self, remote_addr, local_dir):
        try:
            repo = Repo.clone_from(remote_addr, local_dir)
        except GitCommandError:
            try:
                repo = Repo(local_dir)
            except GitCommandError:
                print "Git Error: " + str(GitCommandError)
                return None

        assert repo.__class__ is Repo
        assert repo.remotes.origin is not None

        return repo

    def update_repos(self):
        for repo in [self._base_repo, self._machine_repo]:
            if not repo:
                continue

            try:
                repo.git.reset('--hard')
                repo.remotes.origin.pull()
            except GitCommandError as e:
                print "Error retrieving updates: " + str(e)
