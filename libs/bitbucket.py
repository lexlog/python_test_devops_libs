import stashy
import re


class BitBucketTools:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def create_branch(self, branch, project, repo):
        """
        Creates branch in specified repo

        :param branch: branch name, string
        :param project: bitbucket project name, string
        :param repo: bitbucket repository name, string
        :return: None
        """
        stash = stashy.connect(self.url, self.user, self.password)
        stash.projects[project].repos[repo].create_branch(branch)

    def create_pr(self, project, repo, branch_from, branch_to, title, description):
        """
        Creates Pull-Request from branch_from to branch_to and
        returns json with information about created PR

        :param project: project name in Bitbucket
        :param repo: repository name in Bitbucket
        :param branch_from: branch name, from which pull-request creates
        :param branch_to: branch name, to which pull-request creates
        :param title: title of pull-request
        :param description: description of pull-request
        :return: JSON with Pull-Request info
        """
        stash = stashy.connect(self.url, self.user, self.password)
        #todo get reviewers from commits and product issue
        return(stash.projects[project].repos[repo].pull_requests.create(title, branch_from,
                                                                        branch_to, description=description))
    
    def get_pr_info(self, project, repo, pr_id):
        """
        Returns json with Pull-Request meta-info

        :param project: bitbucket project name
        :param repo: bitbucket repository name
        :param id: id of pull-request
        :return:
        """
        stash = stashy.connect(self.url, self.user, self.password)
        return stash.projects[project].repos[repo].pull_requests[pr_id].get

    def decline_pr(self, project, repo, pr_id):
        """
        Declines specified Pull-Request

        :param project: project name in Bitbucket
        :param repo: repository name in Bitbucket
        :param pr_id: pull-request id
        :return:
        """
        stash = stashy.connect(self.url, self.user, self.password)
        stash.projects[project].repos[repo].pull_requests[pr_id].decline

    def merge_pr(self, project, repo, pr_id):
        """
        Merges specified Pull-Request

        :param project: project name in Bitbucket
        :param repo: repository name in Bitbucket
        :param pr_id: pull-request id
        :return:
        """
        stash = stashy.connect(self.url, self.user, self.password)
        stash.projects[project].repos[repo].pull_requests[pr_id].merge(0)

    def is_pr_exists(self, project, repo, branch_from, branch_to):
        """
        :param project:
        :param repo:
        :param branch_from:
        :param branch_to:
        :return: True if PR open from branch_from to branch_to, other way return False
        """
        stash = stashy.connect(self.url, self.user, self.password)
        pr_list = list(stash.projects[project].repos[repo].pull_requests.all())
        for l in pr_list:
            if l['fromRef']['displayId'] == branch_from and l['toRef']['displayId'] == branch_to:
                return True
        return False

    def get_head_commit(self, project, repo, branch):
        """
        Returns json with Pull-Request meta-info

        :param project: bitbucket project name
        :param repo: bitbucket repository name
        :param id: id of pull-request
        :return:
        """
        stash = stashy.connect(self.url, self.user, self.password)
        commits = stash.projects[project].repos[repo].branches(branch)

        for commit in commits:
            return commit['latestCommit']

    def get_matched_branch(self, project, repo, regexp):
        """
        Returns first matched branch to regex

        :param project:
        :param repo:
        :param issue_id:
        :param branch_regex:
        :return:
        """
        stash = stashy.connect(self.url, self.user, self.password)
        for br in list(stash.projects[project].repos[repo].branches()):
            if re.search(regexp, br['displayId']):
                return br['displayId']
        return ""

