import os
import git
import datetime
import random
import subprocess
import shutil


class GitUtils:
    def __init__(self,  logger, repo_url, tmp_dir='/tmp'):
        self.url = repo_url
        self.tmp_dir = tmp_dir
        self.log = logger
        self.repo_path = None

    def __del__(self):
        if self.repo_path is not None:
            shutil.rmtree(self.repo_path)

    def clone_repo(self, branch):
        tmp_name = "tmp_repo_{}_{}".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
                                           random.randint(100, 999999))
        self.repo_path = os.path.join(self.tmp_dir, tmp_name)
        print('Cloning repo {} to {}'.format(self.url, self.repo_path))

        os.mkdir(self.repo_path)
        git.Repo.clone_from(self.url, self.repo_path)

        cwd = os.getcwd()
        os.chdir(self.repo_path)
        subprocess.check_output(['git', 'checkout', branch])
        os.chdir(cwd)

        return self.repo_path

    def get_branch_diff(self, base_branch, branch_to):
        """
        Determines is there any diff between two remote branches in bitbucket

        :param base_branch: name of first remote branch
        :param branch_to: name of first remote branch
        :param url: git url, by default - gets from GIT_URL variable with usr and http url
        :return: True if diff found, False if doesn't
        """

        cwd = os.getcwd()
        os.chdir(self.repo_path)
        subprocess.check_output(['git', 'checkout', branch_to])
        subprocess.check_output(['git', 'pull', 'origin', branch_to])
        subprocess.check_output(['git', 'checkout', base_branch])

        result = subprocess.check_output(['git', 'diff', '--name-only', branch_to])
        os.chdir(cwd)

        print('Diff for branches: ', result)

        if result:
            print('Diff found between branches {} and {}'.format(base_branch, branch_to))
            return True
        else:
            print('Branches {} and {} have no diff'.format(base_branch, branch_to))
            return False
