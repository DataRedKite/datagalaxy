# Import
import pandas as pd
import numpy as np


def split_path_subpath(path):
    """
    function used to split a path into its sub-paths

    Parameters
    __________
    path : str
        Path which needs to be split

    Returns
    ________
    List(String)
        List of strings containing all the sub-paths linked with the given path
    """

    path_list = path.split(sep='/')
    subpath = []
    for i in path_list:
        if len(subpath) == 0:
            subpath.append(i)
        else:
            subpath.append(subpath[-1] + '/' + i)
    return subpath


def transform_dataframe(data):
    """
    function used to turn the dataframe into an object replicating the dataframe imbrication of folders

    Parameters
    __________
    data : dataframe with the following mandatory columns : ["path", "size", "nb_files", "nb_folders]

    Returns
    ________
    final_tree : List(dictionaries)
        List of nested dictionaries which will constitute the hierarchy for the chosen datagalaxy source
    """

    data["list_path"] = data["path"].apply(lambda x: split_path_subpath(x))
    data = data.explode("list_path")
    data = data.reset_index()

    data["technicalName"] = data["list_path"]
    data["drk_name"] = data["list_path"].apply(lambda x: x.split(sep='/')[-1])
    data["drk_deep"] = data["list_path"].apply(lambda x: len(x.split(sep='/')))
    data["drk_size"] = data["size"]
    data["drk_nb_files"] = data["nb_files"]
    data["drk_nb_folders"] = data["nb_folders"]
    data["type"] = "Directory"

    # filter dataframe to keep useful columns for deepest path
    data = data[["technicalName", "drk_deep", "drk_name", "drk_size", "drk_nb_files", "drk_nb_folders", "type"]]
    data_array = data.T.to_dict().values()

    # get distinct keys
    keys = [a_dict['drk_deep'] for a_dict in data_array]
    keys = np.unique(keys)

    # sort keys
    keys = sorted(keys, reverse=True)

    # get unique parents array
    is_parent = data['drk_deep'] < keys[0]
    df_parents = data[is_parent]
    array_parents = df_parents["technicalName"].unique()

    # loop deep
    for k in keys:
        # if not the deepest array
        if keys[0] != k:
            list_tmp_tmp = []
            items_list = list(filter(lambda d: len(d.split(sep='/')) == k, array_parents))
            for i in items_list:
                name_split = i.split(sep='/')[-1]
                obj = {'name': name_split, 'technicalName': i, 'type': 'Directory', 'drk_name': name_split, 'children': []}
                for j in list_tmp:
                    if i in j['technicalName']:
                        obj['children'].append(j)
                list_tmp_tmp.append(obj)
            list_tmp = list_tmp_tmp
        else:
            list_tmp = list(filter(lambda d: d['drk_deep'] == k, data_array))
            for dic in list_tmp:
                dic['name'] = dic['drk_name']
    final_tree = list_tmp
    return final_tree
