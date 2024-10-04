import requests
import json

headers = {'Content-Type': 'application/xml'}


class TCBuildsUtils:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def tc_create_build(self, xml, proj_id):
        """
        Creates teamcity build in specified project

        :param xml: xml converted into string with build parameters
        :param proj_id: project id, where build_id should be created
        :return: None
        """
        tc_create_build_url = '{}/httpAuth/app/rest/buildTypes'.format(self.url, proj_id)
        try:
            print('Creating build configuration\nPOST\nURL: {}\nHEADERS: {}\nBODY: {}'.format(tc_create_build_url, headers, xml))
            r = requests.post(tc_create_build_url, auth=(self.user, self.password), data=xml, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print('Request failed, response is: \n', r.content)

    def tc_get_build_xml(self, build_id):
        """
        Returns build configuration info in xml

        :param build_id: build_id of teamcity build
        :return: string with build xml
        """
        tc_get_build_url = '{}/app/rest/buildTypes/id:{}'.format(self.url, build_id)
        try:
            print('Getting tc build xml, URL: {}'.format(tc_get_build_url))
            r = requests.get(tc_get_build_url, auth=(self.user, self.passwordD), headers=headers)
            r.raise_for_status()
            return r.content
        except requests.exceptions.HTTPError:
            print('Request failed, response is: \n', r.content)

    def tc_get_build_status(self, build_id):
        """
        Gets status of teamcity build by id. If unfinished, doesnt return status
        Return: Unicode with status of TC build

        :param build_id: build_id of teamcity build
        :return: string with status of build - UNFINISHED, SUCCESS, FAILURE
        """
        tc_get_build_status_url = '{host}/httpAuth/app/rest/builds/id:{id}?fields=status,state'.\
            format(host=self.url, id=build_id)
        print('Getting TC build {} status'.format(build_id))
        try:
            r = requests.get(tc_get_build_status_url,
                                            auth=(self.user, self.password),
                                            headers={'Accept': 'application/json'})
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print('Request failed, response is: \n', r.content)

        tc_get_info_response_json = json.loads(r.content.decode('utf-8'))
        state = tc_get_info_response_json['state']
        status = tc_get_info_response_json['status']
        print("TC build {} status is '{}', state is '{}'".format(build_id, status, state))
        if state != 'finished':
            return 'UNFINISHED'
        else:
            return status

    def tc_run_build(self, xml, build_id):
        """
        Triggers Teamcity build

        :param xml: xml converted into string with build parameters
        :param build_id: build_id of triggering build
        :return: None
        """
        tc_run_build_url = '{}/app/rest/buildQueue'.format(self.url)

        try:
            print('Running build, URL: \n{}\ndata: \n {}'.format(tc_run_build_url, xml))
            r = requests.post(tc_run_build_url, auth=(self.user, self.password), data=xml, headers=headers)
            r.raise_for_status()
            return r.content
        except requests.exceptions.HTTPError:
            print('Request failed, response is: \n', r.content)
