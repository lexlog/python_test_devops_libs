from jira import *

JIRA_URL = 'https://jira.billing.ru'


class JiraUtils:
    def __init__(self, logger, user, password):
        self.log = logger
        self.user = user
        self.password = password

    def make_comment(self, issue_id, comment):
        jira = JIRA(basic_auth=(self.user, self.password), options={'server': 'https://jira.billing.ru'})
        issue = jira.issue(issue_id)
        jira.add_comment(issue, comment)

    def change_status(self, issue_id, transition_code):
        jira = JIRA(basic_auth=(self.user, self.password), options={'server': 'https://jira.billing.ru'})
        issue = jira.issue(issue_id)
        jira.transition_issue(issue, transition_code)
