# datagalaxy SDK v1.0
	
## Description

This SDK can be used to perform a variety of operations using Datagalaxy's API : get the workspace id of the workspace you are looking for, get the source id of all the sources present in your workspace, get the container id of all the containers present in a given source in a given workspace. You will also be able to create new sources, containers or create in one go a new source with its complete hierarchy of containers.
The SDK also automatically refresh for you your access token token if it is obsolete.


## Usage

You can use this sdk in all your python projects.

### Parameters to use

You will only need a token, provided on your DataGalaxy account, to initialise the sdk.
The 1h token, initialize with https://api.datagalaxy.com/v2/credentials, will be automatically refresh for you.


## Description of the main functions used in the script :

get_required_workspaces(self, workspace_name):

        function used to return the defaultVersionId of a workspace according to the given name

        Parameters
        __________
        workspace_name : str
            Name of the workspace we need the defaultVersionId from

        Returns
        ________
        String
            String of the defaultVersionId associated with the workspace


post_bulk_tree(self, workspace_name, path, sep, src_name):

        function which loads and transform a csv-file. From its 'path' column a hierarchy of files will
        be established. Using this hierarchy and the src_name, a json object will be posted using the
        datagalaxy API in the given workspace. If there is already a source with a matching src_name in you
        workspace, it will be updated (using the upsert method). Otherwise a new source will be created in that
        same workspace.

        Parameters
        __________
        workspace_name : str
            Name of the workspace we need the defaultVersionId from
        path : str
            Path leading to the csv-file we want to transform
        sep : str
            Separator used in the csv-file
        src_name : str
            The name of the source that will be updated OR created, depending on whether it already exists or not
            
        Returns
        ________
        response : str
            The response message you get for your request


get_all_sources(self, version_id):

        function to get all the sources present on a given workspace (characterized by its version_id)

        Parameters
        __________
        version_id : str
            Id used to locate the workspace

        Returns
        ________
        sources_list : List(str)
            A list of all the sources present on your workspace


post_new_source(self, src_name, version_id):

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


get_all_containers(self, version_id, source_id):

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


post_new_element(self, version_id, target_id, cont_name):

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


get_source_type(self):

        function to get the existing source types that are accepted by Datagalaxy

        Parameters
        __________
        None

        Returns
        ________
        response : List(Dictionaries)
            A list of dictionaries containing all the accepted workspaces and their accepted dependencies too


## Roadmap
Once it is available using the datagalaxy API, we will add the possibility for users to create through this SDK custom data properties.


## Authors
[Alexandre BERGERE](https://github.com/Alexkuva) and [Tristan CARIOU](https://github.com/TPCariou) from DataRedKite
