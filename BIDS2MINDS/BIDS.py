"""
Created on 01 August 2019
@author: Mohamed Alhaskir
"""
import json, csv, os

class BIDS:
    """
    This class will convert all forms of metadata in the BIDS dataset in one nested dict (metalist)
    -task metadata is not included in the metalist-
    :param folderpath: is the path to the BIDS dataset
    :type folderpath: string
    """
    def __init__(self, folderpath):
        self.folderpath = folderpath
        # a list that contains lists for every subject file name separated with commas
        self.subslist = []
        # a list contains dicts for every subject file name as nested accordingly(subsmetalist is part of true_list)
        self.subsmetalist = []
        # a list contains dicts for every entry of the participants.tsv file with a data(key) that has according
        # subsmetalist element as value
        self.truelist = []
        # a list that contains dictionaries for avaiable metdata
        self.metalist = []
        # a list contains dicts of each task with its according metdata
        self.task_list = []
        # list of all URL of the dataset  files
        self.list_files = []
        # list contains @ids of a all method of the dataset
        self.data_set_metods= []
        for path, dirs, files in os.walk(self.folderpath):
            for filename in files:
                self.a = filename.replace('_', '.').split('.')
                q = []
                for element in self.a:
                    q.append(element)
                c = dict.fromkeys(self.a, self.a)
                for key in list(c):
                    if key in ['dataset', 'participants']:
                        self.metalist.append(c)
                    else:
                        del c[key]
                if filename.startswith('dataset'):
                    fullpath = os.path.join(path, filename)
                    with open(fullpath, 'r') as jsonfile:
                        datastore = json.load(jsonfile)
                        for element in self.metalist:
                            for key in element.keys():
                                if key == 'dataset':
                                    element[key] = datastore
                elif filename.startswith('participants'):
                    fullpath = os.path.join(path, filename)
                    with open(fullpath) as tsvfile:
                        reader = csv.DictReader(tsvfile, delimiter='\t')
                        columns = {}
                        for row in reader:
                            for x in reader.fieldnames:
                                columns[x] = row.get(x)
                            self.truelist.append(columns.copy())
                        self.metalist[1]['participants'] = self.truelist
                elif filename.startswith('sub'):
                    self.subslist.append(q)
                    if filename.endswith('json'):
                        fullpath = os.path.join(path, filename)
                        with open(fullpath, 'r') as jsonfile:
                            datastore = json.load(jsonfile)
                            x = filename.replace('_', '.').split('.')
                            for element in x:
                                if element.startswith('task'):
                                    task_dic = {element : datastore}
                            self.task_list.append(task_dic)
                elif filename.startswith('task'):
                    if filename.endswith('json'):
                        fullpath = os.path.join(path, filename)
                        with open(fullpath, 'r') as jsonfile:
                            datastore = json.load(jsonfile)
                            x = filename.replace('_', '.').split('.')
                            for element in x:
                                if element.startswith('task'):
                                    task_dic = {element: datastore}
                            self.task_list.append(task_dic)
        for element in self.task_list:
            for key in element.keys():
                if key.startswith('task'):
                    task_id = {'@id': '%s.json' % key}
                    self.data_set_metods.append(task_id)

        for element in self.subslist:
            sub = {}
            if not element[1].startswith('ses') and not element[1].startswith('task'):
                sub[element[0]] = element[1:]
                self.subsmetalist.append(sub)
            elif element[1].startswith('ses'):
                ses = {}
                if not element[2].startswith('task'):
                    ses[element[1]] = element[2:]
                    sub[element[0]] = ses
                    self.subsmetalist.append(sub)
                elif element[2].startswith('task'):
                    task = {}
                    task[element[2]] = element[3:]
                    ses[element[1]] = task
                    sub[element[0]] = ses
                    self.subsmetalist.append(sub)
            elif element[1].startswith('task'):
                task = {}
                task[element[1]] = element[2:]
                sub[element[0]] = task
                self.subsmetalist.append(sub)
            for item in sub.values():
                if type(item)== dict:
                    for key in item.keys():
                        if key.startswith('task'):
                            if item[key][-1] == 'json':
                                for filename in files:
                                    if filename.endswith('.json'):
                                        fullpath = os.path.join(path, filename)
                                        with open(fullpath, 'r') as jsonfile:
                                            datastore = json.load(jsonfile)
                                        item[key].append(datastore)
                        elif key.startswith('ses'):
                            if type(item[key]) == dict:
                                for kkey in item[key].keys():
                                    if kkey.startswith('task'):
                                        if item[key][kkey][-1] == 'json':
                                            for filename in files:
                                                if filename.endswith('.json'):
                                                    fullpath = os.path.join(path, filename)
                                                    with open(fullpath, 'r') as jsonfile:
                                                        datastore = json.load(jsonfile)
                                                    item[key][kkey].append(datastore)


