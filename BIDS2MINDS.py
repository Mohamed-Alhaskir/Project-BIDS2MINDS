import os
import json, csv
import requests
import pprint
import BIDS2MINDS.minds4py as m


class BIDS:
    def __init__(self, folderpath):
        self.folderpath = folderpath
        self.metalist = []
        self.subslist = []
        self.subsmetalist = []
        self.truelist = []
        self.task_list = []
        self.list_files = []
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
    def mindify(self, data_set_name, location):
        g = m.MINDS(name='myminds', path=location)
        set_of_method = []
        for path, dirs, files in os.walk(self.folderpath):
            if 'func' in dirs:
                fmri_id = 'fMRI-01.json'
                set_of_method.append(fmri_id)
            else:
                fmri_id = ''
            if 'anat' in dirs:
                mri_id = 'MRI-01.json'
                set_of_method.append(mri_id)
            else:
                mri_id = ''
        for element in set(set_of_method):
            d = {'@id': element}
            self.data_set_metods.append(d)
        for element in self.metalist:
            for key in element.keys():
                if key == 'dataset':
                    for kkey in element[key].keys():
                        if 'Name' in element[key].keys():
                           name = element[key]['Name']
                        else:
                            name = ""
                        if 'License' in element[key].keys():
                           License = element[key]['License']
                        else:
                            License = ""
                        if 'Acknowledgements' in element[key].keys():
                           Acknowledgements = element[key]['Acknowledgements']
                        else:
                            Acknowledgements = ""
                        if 'HowToAcknowledge' in element[key].keys():
                           HowToAcknowledge = element[key]['HowToAcknowledge']
                        else:
                            HowToAcknowledge = ""
                        if 'ReferencesAndLinks' in element[key].keys():
                           ReferencesAndLinks = element[key]['ReferencesAndLinks']
                        else:
                            ReferencesAndLinks = ""
                        if 'Funding' in element[key].keys():
                           Funding = element[key]['Funding']
                        else:
                            Funding = ""
                        if 'DatasetDOI' in element[key].keys():
                            DatasetDOI = element[key]['DatasetDOI']
                        else:
                            DatasetDOI = ""
                        if 'Authors' in element[key].keys():
                            contributor = element[key]['Authors']
                            for x in element[key]['Authors']:
                                main_contact = element[key]['Authors'][0]
                                custodian = element[key]['Authors'][-1]
                        else:
                            contributor = ""
                            main_contact = ""
                            custodian = ""
                            contributor = ""
                    g.create_block(blocktemp=g.Dataset, id=data_set_name, name=data_set_name,
                                   license=[{'@id': '%s.json'% License}],
                                   funding_information=[{'@id': '%s.json'%'funding'}], doi=[{'@id': '%s.json'%'doi'}],
                                   description=str([Acknowledgements]),
                                   main_file_bundle=[{'@id': 'main filebundle.json'}],
                                   method=self.data_set_metods, publication=[{'@id': 'Publication.json'}],
                                   contributor=[{'@id': '%s.json' % contributor}], custodian=[{'@id': '%s.json' % custodian}],
                                   main_contact = [{'@id': '%s.json' %main_contact}] , project = [{'@id': 'coordinator.json'}])
                    g.create_block(blocktemp=g.Person, id= custodian, name= 'custodian', contributor = [{'@id': '%s.json' % contributor}], main_contact = [{'@id': '%s.json' %main_contact}], coordinator = [{'@id': '%s.json'% 'coordinator' }])
                    g.create_block(blocktemp=g.Person, id=str(contributor), name='contributor',custodian = [{'@id': '%s.json'% custodian}],  main_contact = [{'@id': '%s.json' %main_contact}] , coordinator = [{'@id': '%s.json'% 'coordinator' }])
                    g.create_block(blocktemp=g.Person, id=main_contact, name='main_contact',custodian = [{'@id': '%s.json'% custodian}],contributor = [{'@id': '%s.json' % contributor}], coordinator = [{'@id': '%s.json'% 'coordinator' }]  )
                    g.create_block(blocktemp=g.Fundinginformation, id='funding', name =str(Funding))
                    g.create_block(blocktemp=g.Publication, id='publication-01', url=str(ReferencesAndLinks),publication = [{'@id': 'ds001.json'}])
                    DOI_dict = {'__block_id': 'uniminds/options/doi/v1.0.0','__block_label': 'doi',
                                '@id': 'doi','@type': 'https://schema.hbp.eu/uniminds/options/doi/v1.0.0',
                                'citation': HowToAcknowledge, 'identifier': DatasetDOI}
                    license_def = {'CC0':'Freeing content globally without restrictions',
                                   'CC BY': ' Creative Commons with Attribution alone',
                                   'CC BY-SA': 'Creative Commons with Attribution and ShareAlike',
                                   'CC BY-NC': 'Creative Commons with Attribution and Noncommercial',
                                   'CC BY-NC-SA': 'Creative Commons with Attribution, Noncommercial and ShareAlike',
                                   'CC BY-ND': 'Creative Commons with Attribution and NoDerivatives',
                                   'CC BY-NC-ND': 'Creative Commons with Attribution, Noncommercial and NoDerivatives' }
                    for key, value in license_def.items():
                        if License.startswith(key):
                            fullname = value
                    License_dict = {'__block_id': 'uniminds/options/license/v1.0.0','__block_label': 'License', '@id': License,
                                    '@type': 'https://schema.hbp.eu/uniminds/options/license/v1.0.0',
                                    'identifier': License, 'fullname': fullname, 'url':'https://creativecommons.org/'}
                    # todo: check what is missing from last two blocks
                    g.new_minds_collection['minds_blocks'].append(DOI_dict)
                    g.new_minds_collection['minds_blocks'].append(License_dict)
                    for block in g.new_minds_collection['minds_blocks']:
                        if block['@id'] == '.json':
                            g.new_minds_collection['minds_blocks'].remove( block)
                        for key in block.keys():
                            if type(block[key]) == list:
                                for x in block[key]:
                                    if x['@id'] == '.json':
                                        block.pop(key)

        sub_MRI = []
        sub_fMRI = []
        group_list = []
        sex_list = []
        handedness_list = []
        age_category_list = []
        for element in self.truelist:
            element['data'] = []
            if 'participant_id' in element.keys():
                participant_id = element['participant_id']
            else:
                participant_id = ""
            if 'age' in element.keys():
                age = element['age']
                age_unit = element['age'] + ', unit: years'
                if int(age) >= 18:
                    age_category = "adult"
                    age_unit = element['age'] + ', unit: years'
                    age_category_list.append(age_category)
                elif int(age) < 18:
                    age_category = "juvenile"
                    age_category_list.append(age_category)
            else:
                age = ""
                age_category_list = []
            if 'sex' in element.keys():
                sex = element['sex']
                sex_list.append(sex)
                sex_list = []
            else:
                sex = ""
            if 'handedness' in element.keys():
                handedness = element['handedness']
                handedness_list.append(handedness)
            else:
                handedness = ""
                handedness_list = []
            if 'group' in element.keys():
                group = element['group']
                group_list.append(group)
            else:
                group = ""
                group_list = []
            for selement in self.subsmetalist:
                for key in selement.keys():
                    if key == element['participant_id']:
                     element['data'].append(selement)
            for x in element['data']:
                for key in x.keys():
                    for var in x[key]:
                        if var.startswith('ses'):
                            for something in x[key][var]:
                                if type(x[key][var]) == list:
                                    if 'nii' in x[key][var]:
                                        if something in ['T1w','T2w','inplaneT2','T1rho','T1map','T2map',
                                                             'T2star', 'FLAIR', 'FLASH', 'PD', 'PDmap',
                                                             'PDT2', 'inplaneT2','angio']:
                                                file_name= element['participant_id'] + '_' + var + '_' + something
                                                file_id = element['participant_id'] + '_' + var + '_' + '.'.join(x[key][var])
                                                sub_MRI.append(file_name)
                                                url = self.folderpath + '/' + element[
                                                    'participant_id'] + '/' + var + '/anat/' + element[
                                                          'participant_id'] + '_' + var + '_' + '.'.join(x[key][var])
                                                self.list_files.append(url)
                                                g.create_block(blocktemp=g.File, id=file_id, subject = [{'@id': '%s.json' % element['participant_id']}], url = url, name= file_name, method = [{'@id': '%s.json' % something}])
                                if type(x[key][var]) == dict:
                                    for y in x[key][var].keys():
                                        if y.startswith('task'):
                                           run = []
                                           if 'nii' in x[key][var][y] or 'tsv' in x[key][var][y]:
                                               for z in x[key][var][y]:
                                                   if type(z) != dict and z.startswith('run'):
                                                       run.append(z)

                                               file_name = element['participant_id']+'_'+var + '_' + y + '_' +''.join(run)
                                               file_id = element['participant_id'] + '-file-' + y+ '_' +''.join(run)+'_' + '.'.join(
                                                                  x[key][var][y][1:])
                                               sub_fMRI.append(file_name)
                                               url = self.folderpath + '/' + element[
                                                                  'participant_id']+'/'+var+  '/func/' + element['participant_id']+'_'+var + '_' + y + '_' +''.join(run)+'_' + '.'.join(
                                                                  x[key][var][y][1:])
                                               self.list_files.append(url)
                                               g.create_block(blocktemp=g.File, id=file_id,
                                                              subject=[{'@id': '%s.json' % element['participant_id']}],
                                                              method=[{'@id': 'fMRI-01.json'}],
                                                              url= url,  name= file_name)
                                           if 'json' in x[key][var][y]:
                                               crun = []
                                               filenamelist = []
                                               infolist = []
                                               for z in x[key][var][y]:
                                                   if type(z) == dict:
                                                       infolist.append(z)
                                                       x[key][var][y].remove(z)
                                                       filenamelist.append('.'.join(
                                                                  x[key][var][y][1:]))
                                                   if type(z) != dict and z.startswith('run'):
                                                       crun.append(z)
                                               file_name = element['participant_id']+'_'+var  + '_' + y + '_' +''.join(crun) +'_' +'.'.join(filenamelist)
                                               file_id = element['participant_id']+'_'+var  + '_' + y + '_' +''.join(crun) +'_' +'.'.join(filenamelist)
                                               sub_fMRI.append(file_name)
                                               url = self.folderpath + '/' + element['participant_id']+'/'+var + '/func/' + element['participant_id']+'_'+var  + '_' + y + '_' +''.join(crun) +'_' +'.'.join(filenamelist)
                                               self.list_files.append(url)
                                               g.create_block(blocktemp=g.File, id=file_id, subject=[{'@id': element['participant_id']}], method=[{'@id': 'fMRI-01.json'}],
                                                                 url=url, name =file_name )


                        elif var.startswith('task'):
                            run = []
                            if 'nii' in x[key][var] or 'tsv' in x[key][var]:
                                for z in x[key][var]:
                                    if type(z) != dict and z.startswith('run'):
                                           run.append(z)
                                file_name = element['participant_id'] + '_' + var + '_' +''.join(run)+ '_' + '.'.join(
                                                       x[key][var][1:])
                                file_id =  element['participant_id'] + '_' + var + '_' +''.join(run)+ '_' + '.'.join(
                                                       x[key][var][1:])
                                sub_fMRI.append(file_name)
                                url =self.folderpath + '/' + element['participant_id'] + '/func/' +element['participant_id'] + '_' + var + '_' +''.join(run)+ '_' + '.'.join(
                                                       x[key][var][1:])
                                self.list_files.append(url)
                                g.create_block(blocktemp=g.File, id=file_id,
                                                   subject=[{'@id': '%s.json' % element['participant_id']}],
                                                   method=[{'@id': 'fMRI-01.json'}],
                                                   url=url, name = file_name)
                            if 'json' in x[key][var]:
                                crun = []
                                filenamelist = []
                                infolist = []
                                for z in x[key][var]:
                                    if type(z) == dict:
                                        infolist.append(z)
                                        x[key][var].remove(z)
                                        filenamelist.append('.'.join(
                                            x[key][var][1:]))
                                    if type(z) != dict and z.startswith('run'):
                                        crun.append(z)
                                file_name = element['participant_id'] + '_' + var + '_' + ''.join(
                                    crun) + '_' + '.'.join(filenamelist)
                                file_id = element['participant_id'] + '_' + var + '_' + ''.join(
                                    crun) + '_' + '.'.join(filenamelist)
                                sub_fMRI.append(file_name)
                                url = self.folderpath + '/' + element['participant_id'] + '/func/' +element['participant_id'] + '_' + var + '_' + ''.join(
                                    crun) + '_' + '.'.join(filenamelist)
                                self.list_files.append(url)
                                g.create_block(blocktemp=g.File, id=file_id,
                                               subject=[{'@id': '%s.json' % element['participant_id']}], method=[{'@id': 'fMRI-01.json'}],
                                               url=url, name= file_name)
                        elif not var.startswith('ses') and not var.startswith('task'):
                            if 'nii' in x[key] or 'tsv' in x[key]:
                                if var in ['T1w','T2w','inplaneT2','T1rho','T1map','T2map',
                                                           'T2star', 'FLAIR', 'FLASH', 'PD', 'PDmap',
                                                            'PDT2', 'inplaneT2','angio']:
                                    file_name = element['participant_id'] + '_' + var
                                    file_id = element['participant_id'] + '_' + '.'.join(x[key])
                                    sub_MRI.append(file_name)
                                    url = self.folderpath + '/' + element['participant_id'] + '/anat/' + element[
                                        'participant_id'] + '_' + '.'.join(x[key])
                                    self.list_files.append(url)
                                    g.create_block(blocktemp=g.File, id= file_id,subject=[{'@id': '%s.json' % element['participant_id']}], url=url, name = file_name, method= [{'@id': '%s.json' % var}])


            file_list= []
            for element in sub_MRI:
                if element[0:6] == participant_id:
                    dic = {}
                    dic['@id'] = '%s.json' % element
                    file_list.append(dic)
            for element in sub_fMRI:
                if element[0:6] == participant_id:
                    dic = {}
                    dic['@id'] = '%s.json' % element
                    file_list.append(dic)
            g.create_block(blocktemp=g.Subject, id=participant_id)
            g.create_block(blocktemp=g.Subject, id=participant_id,
                           age=age_unit, sex=[{'@id': '%s.json' % sex}],age_category = [{'@id': '%s.json' % age_category}], handedness=[{'@id': '%s.json' % handedness}], subject = file_list, )
        for element in age_category_list:
            if element == 'juvenile':
                age_category_dict = {'@id': '%s.json' % element,'__block_label': 'Age_category',
                                     '@type': 'https://schema.hbp.eu/uniminds/options/Age_category/v1.0.0',
                                     '__block_id': 'uniminds/options/age_category/v1.0.0', 'Name': element}
                g.new_minds_collection['minds_blocks'].append(age_category_dict)
            elif element == 'adult':
                age_category_dict = {'@id': '%s.json' % element,'__block_label': 'Age_category',
                                     '@type': 'https://schema.hbp.eu/uniminds/options/Age_category/v1.0.0',
                                     '__block_id': 'uniminds/options/age_category/v1.0.0', 'Name': element}
                g.new_minds_collection['minds_blocks'].append(age_category_dict)
            else:
                continue
        for element in set(sex_list):
            if element == "M":
                sex_dict = {'@id': '%s.json' % element, '@type': 'https://schema.hbp.eu/uniminds/options/Sex/v1.0.0',
                            '__block_label': 'Sex',
                            '__block_id': 'uniminds/options/sex/v1.0.0', 'Name': 'Male',
                            "Description": "sex of the participant"}
                g.new_minds_collection['minds_blocks'].append(sex_dict)
            elif element == "F":
                sex_dict = {'@id': '%s.json' % element, '@type': 'https://schema.hbp.eu/uniminds/options/Sex/v1.0.0',
                            '__block_label': 'Sex',
                            '__block_id': 'uniminds/options/sex/v1.0.0', 'Name': 'Female',
                            "Description": "sex of the participant"}
                g.new_minds_collection['minds_blocks'].append(sex_dict)
            else:
                continue
        for element in set(handedness_list):
            if element == "L":
                handedness_dict = {'@id': '%s.json' % element,
                                   '@type': 'https://schema.hbp.eu/uniminds/options/Handness/v1.0.0',
                                   '__block_label': 'Handness',
                                   '__block_id': 'uniminds/options/handedness/v1.0.0', 'Name': 'Left',
                                   "Description": "handedness of the participant as reported by the participant"}
                g.new_minds_collection['minds_blocks'].append(handedness_dict)
            elif element == "R":
                handedness_dict = {'@id': '%s.json' % element,
                                   '@type': 'https://schema.hbp.eu/uniminds/options/Handness/v1.0.0',
                                   '__block_label': 'Handness',
                                   '__block_id': 'uniminds/options/handedness/v1.0.0', 'Name': 'Right',
                                   "Description": "handedness of the participant as reported by the participant"}
                g.new_minds_collection['minds_blocks'].append(handedness_dict)
            else:
                continue
        for element in set(group_list):
            ids = []
            age_cata = []
            selist = []
            handlist = []
            for xelement in self.truelist:
                if xelement['group'] == element:
                    dic = {'@id': xelement['participant_id']+'.json'}
                    ids.append(dic)
                    if int(xelement['age']) >= 18:
                        age_co= {'@id': 'adult.json'}
                        age_cata.append(age_co)
                    if int(xelement['age']) < 18:
                        age_co= {'@id': 'juvenile.json'}
                        age_cata.append(age_co)
                    if xelement['sex'] == 'F':
                        sex = {'@id': 'F.json'}
                        selist.append(sex)
                    if xelement['sex'] == 'M':
                        sex = {'@id': 'M.json'}
                        selist.append(sex)
                    if xelement['handedness'] == 'L':
                        hand = {'@id': 'L.json'}
                        handlist.append(hand)
                    if xelement['handedness'] == 'R':
                        hand = {'@id': 'R.json'}
                        handlist.append(hand)
            g.create_block(blocktemp=g.Subjectgroup, id=element, subjects = ids, age_category = age_cata,sex =selist, handedness= handlist)
        method_id = []
        for element in sub_MRI:
            ext = ['T1w','T2w','inplaneT2','T1rho','T1map','T2map','T2star', 'FLAIR', 'FLASH', 'PD', 'PDmap',
                   'PDT2', 'inplaneT2','angio']
            for x in ext:
                if element.endswith(x):
                     method_id.append(x)
        print(sub_MRI)
        sub_method_id = []
        for element in set(method_id):
            dic = {}
            dic['@id'] = '%s.json' % element
            sub_method_id.append(dic)
            method = []
            for x in sub_MRI:
                if x.endswith(element):
                    dic = {}
                    dic['@id']=  '%s.json' % x
                    method.append(dic)
            g.create_block(blocktemp=g.Method, id=element, method = method)
        method_fMRI = []
        for element in sub_fMRI:
            dic = {'@id': '%s.json' % element}
            method_fMRI.append(dic)
        for path, dirs, files in os.walk(self.folderpath):
            if 'func' in dirs:
                fmri_id = 'fMRI-01'
                g.create_block(blocktemp=g.Method, id=fmri_id, description = 'This the is main MRI method block connected to all other fMRI files', method= method_fMRI)
            if 'anat' in dirs:
                mri_id = 'MRI-01'
                g.create_block(blocktemp=g.Method, id=mri_id,
                               description='This the is main MRI method block connected to all other MRI files', method= [{'@id':'%s.json' % data_set_name }],sub_method = sub_method_id)
                break
        for element in self.task_list:
            flist = []
            for key in element.keys():
                identifier = key
                for skey in element[key].keys():
                    if skey == 'TaskName':
                        TaskName = element[key]['TaskName']
                    if 'TaskDescription' in element[key].keys():
                        descrip = element[key]['TaskDescription']
                    else:
                        descrip = ''
                    if 'RepetitionTime' in element[key].keys():
                        RepetitionTime = ' RepetitionTime: '+ str(element[key]['RepetitionTime'])
                    else:
                        RepetitionTime = ''
                    if 'CogAtlasID'in element[key].keys():
                        CogAtlasID = element[key]['CogAtlasID']
                    else:
                        CogAtlasID = ''
                    if 'Instructions'in element[key].keys():
                        Instructions = ' Instructions: '+ element[key]['Instructions']
                    else:
                        Instructions = ''
                for element in sub_fMRI:
                    if key in element:
                        fdic = {'@id': '%s.json' % element}
                        flist.append(fdic)
            g.create_block(blocktemp=g.Method, id=key, identifier =identifier, name= TaskName,method= flist, description= descrip +Instructions + RepetitionTime,publication = [{'@id': '%s-Pub.json' % key }])
            g.create_block(blocktemp=g.Publication, id=key + '-Pub', identifier = CogAtlasID+' '+key, url=CogAtlasID )
        g.create_block(blocktemp=g.Filebundle, id='main filebundle',
                       description='This filebundle contains all dataset URLs', name='main filebundle', url = str(self.list_files))
        pprint.pprint(g.new_minds_collection)
        print(g.uniminds_blocks)
        g.save_minds_collection()
        print(g.File.keys())
        print(g.Dataset.keys())
        print(g.Subject.keys())
        print(g.Subjectgroup.keys())
        print(g.Filebundle.keys())
        print(g.Method.keys())
        print(g.Person.keys())
        print(g.Project.keys())
        print(g.Publication.keys())
        print(g.Funding.keys())
        print(g.Study_target.keys())






p = BIDS(folderpath="C:/Users/Asus T102 H/Desktop/ds001")
p.mindify(data_set_name= 'ds001', location ="C:/Users/Asus T102 H/Desktop/trail")


