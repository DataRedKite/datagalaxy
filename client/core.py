# Import
from enum import Enum

import requests
from datetime import *
import json


class DataGalaxyClient:

    def __init__(self, dgy_token):
        """ Init method """
        self.dgy_token = dgy_token
        self.token_expiration_date = None
        self.token = None
        self.authenticate()
        self.versionid = None

    def authenticate(self):
        """ Get token (valid 1 hour) """
        headers = {'Authorization': 'Bearer ' + self.dgy_token}
        request = requests.get('https://api.datagalaxy.com/v2/credentials', headers=headers)
        self.token = request.json()["accessToken"]
        self.token_expiration_date = datetime.now() + timedelta(hours=1)

    def refresh_token_if_obsolete(self):
        """ Refresh token if hour passed """
        current_date = datetime.now()
        if current_date > self.token_expiration_date:
            self.authenticate()

    def get_api(self, uri):
        """ A helper function to make the API request, request/response is encoded/decoded as JSON """
        # check token_expiration_date
        self.refresh_token_if_obsolete()
        # API authentication
        headers = {'Authorization': 'Bearer ' + self.token}
        try:
            response = requests.get(uri, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            raise error
        except requests.ConnectionError as error:
            raise error

    def post_api(self, uri, body):
        """ A helper function to make the API request, request/response is encoded/decoded as JSON """
        self.refresh_token_if_obsolete()
        headers = {'Authorization': 'Bearer ' + self.token}
        try:
            response = requests.post(uri, headers=headers, json=body)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            raise error
        except requests.ConnectionError as error:
            raise error

    def del_api(self, uri, body):
        """ A helper function to make the API request, request/response is encoded/decoded as JSON """
        self.refresh_token_if_obsolete()
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.delete(uri, headers=headers)
        return response.json()

    def get_required_workspaces(self, workspace_name):
        """
        function used to return the defaultVersionId of a workspace according to the given name

        Parameters
        __________
        workspace_name : str
            Name of the workspace we need the defaultVersionId from

        Returns
        ________
        String
            String of the defaultVersionId associated with the workspace
        """

        dict_workspaces = self.get_api("https://api.datagalaxy.com/v2/workspaces")
        for workspace in dict_workspaces['projects']:
            if workspace['name'] == workspace_name:
                versionid = workspace['defaultVersionId']
            else:
                pass
        return versionid

    def post_bulk_tree(self, workspace_name, src_name, src_type, children):
        """
        function which will post in a given workspace a json object representing the hierarchy between containers.
        If there is already a source with a matching src_name in your workspace, it will be updated (using the upsert
        method). Otherwise a new source will be created in that same workspace.

        Parameters
        __________
        workspace_name : str
            Name of the workspace we need the defaultVersionId from
        src_name : str
            The name of the source that will be updated OR created, depending on whether it already exists or not
        src_type : str
            The type of the source
        children : json
            The object representing the hierarchy between your containers
        Returns
        ________
        response : str
            The response message you get for your request
        """
        accepted_src_type = self.get_source_type()
        if src_type in accepted_src_type:
            version_id = self.get_required_workspaces(workspace_name)
            body = {
                "name": src_name,
                "type": src_type,
                "children": children
            }
            response = self.post_api("https://api.datagalaxy.com/v2/sources/bulktree/" + version_id, body)

        else:
            response = 'ERROR : source type not accepted by Datagalaxy'
            print(response)
        return response

    def get_all_sources(self, version_id):
        """
        function to get all the sources present on a given workspace (characterized by its version_id)

        Parameters
        __________
        version_id : str
            Id used to locate the workspace

        Returns
        ________
        sources_list : List(str)
            A list of all the sources present on your workspace
        """
        dict_sources = self.get_api("https://api.datagalaxy.com/v2/sources?versionId=" + version_id)
        sources_list = []
        for i in range(len(dict_sources['results'])):
            src_id = dict_sources['results'][i]['id']
            sources_list.append(src_id)
        return sources_list

    def post_new_source(self, src_name, version_id):
        """
        function to post a new source on a given workspace (characterized by its version_id)

        Parameters
        __________
        version_id : str
            Id used to locate the workspace
        src_name : str
            The name you want to give to your source

        Returns
        ________
        response : str
            The response message you get for your request
        """
        body = {
            "name": src_name,
            "technicalName": src_name,
            "type": "NonRelational",
            "description": "This is a description",
            "summary": "This is a summary",
            "tags": ["RGPD"],
            "children": []
        }
        response = self.post_api("https://api.datagalaxy.com/v2/sources/" + version_id, body)
        return response

    def get_all_containers(self, version_id, source_id):
        """
        function to get all the containers present on a given workspace in a given source (both characterized by their id)

        Parameters
        __________
        version_id : str
            Id used to locate the workspace
        source_id : str
            Id used to locate the source

        Returns
        ________
        container_list : List(str)
            A list of all the containers present on your workspace
        """
        dict_containers = self.get_api(
            "https://api.datagalaxy.com/v2/containers?versionId=" + version_id + "&parentId=" + source_id)
        container_list = []
        for i in range(len(dict_containers['results'])):
            cont_id = dict_containers['results'][i]['id']
            container_list.append(cont_id)
        return container_list

    def post_new_element(self, version_id, target_id, cont_name):
        """
        function to post a new container on a given workspace (characterized by its version_id) inside a source
        or another container (chosen from a list)

        Parameters
        __________
        version_id : str
            Id used to locate the workspace
        target_id : str
            Id used to locate the element (source or container) within which the new container will be created
        cont_name : str
            Name given to the new container

        Returns
        ________
        response : str
            The response message you get for your request
        """
        body = {
            "name": cont_name,
            "type": "Directory",
            "status": "Obsolete",
            "hyperlien": {
                "name": "a",
                "url": "https://www.google.com"
            }
        }
        response = self.post_api("https://api.datagalaxy.com/v2/containers/" + version_id + "/" + target_id, body)
        return response

    def get_source_type(self):
        """
        function to get the existing source types that are accepted by Datagalaxy

        Parameters
        __________
        None

        Returns
        ________
        response : List(Dictionaries)
            A list of dictionaries containing all the accepted workspaces and their accepted dependencies too
        """
        type_list = []
        response = self.get_api("https://api.datagalaxy.com/v2/sources/types")
        for index in range(len(response)):
            type_list.append(response[index]['type'])
        return type_list
