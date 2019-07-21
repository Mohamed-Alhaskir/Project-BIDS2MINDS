"""
Created on 01 August 2019
@author: Mohamed Alhaskir
"""
import sys
from BIDS import *
sys.path.append('C:\\Users\\Asus T102 H\\PycharmProjects\\Project-MINDS4PY')
from MINDS4PY.MINDS4PY import *

class BIDS2MINDS(BIDS):
    '''
    The class BIDS2MINDS inherits the __init__ function of the BIDS.BIDS class
    '''
    def __init__(self, folderpath):
        BIDS.__init__(self, folderpath)
    def mindify(self, data_set_name, location):
        """
        The method mindify calls MINDS2PY.MINDS class
        :param data_set_name: The name of the BIDS standardized dataset
        :type data_set_name: str
        :param location: path to save MINDS graph repository
        :type location: str
        :return self.graph: BIDS dataset metadata will be returned in form of MINDS graph
        :type self.grapf: dict
        """
        self.g = MINDS(name=data_set_name, path=location)
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
                            for x in element[key]['Authors']:
                                main_contact = element[key]['Authors'][0]
                                custodian = element[key]['Authors'][-1]
                        else:
                            contributor = ""
                            main_contact = ""
                            custodian = ""
                            contributor = ""
                    self.g.create_block(blocktemp=self.g.Dataset, id=data_set_name, name=data_set_name,
                                   license=[{'@id': '%s.json' % License}],
                                   funding_information=[{'@id': '%s.json' % 'funding'}],
                                   doi=[{'@id': '%s.json' % 'doi'}],
                                   description=str([Acknowledgements]),
                                   main_file_bundle=[{'@id': 'main filebundle.json'}],
                                   method=self.data_set_metods, publication=[{'@id': 'Publication.json'}],
                                   custodian=[{'@id': '%s.json' % custodian}],
                                   main_contact=[{'@id': '%s.json' % main_contact}],
                                   species=[{'@id': 'species.json'}], identifier='ds001')
                    self.g.create_block(blocktemp=self.g.Person, id=custodian, name=custodian,
                                   main_contact=[{'@id': '%s.json' % main_contact}],
                                   custodian=[{'@id': 'ds001.json'}], family_name=custodian.rsplit(None)[-1],
                                   given_name=custodian.rsplit(None)[0], identifier='cus')
                    self.g.create_block(blocktemp=self.g.Person, id=main_contact, name=main_contact,
                                   family_name=main_contact.rsplit(None)[-1], given_name=main_contact.rsplit(None)[0],
                                   custodian=[{'@id': '%s.json' % custodian}], main_contact=[{'@id': 'ds001.json'}],
                                   identifier='mc')
                    self.g.create_block(blocktemp=self.g.Fundinginformation, id='funding', name=str(Funding),
                                   funding_information=[{'@id': 'ds001.json'}],
                                   identifier='FI')
                    self.g.create_block(blocktemp=self.g.Publication, id='publication-01', url=str(ReferencesAndLinks),
                                   publication=[{'@id': 'ds001.json'}], identifier='Pub')
                    species = {'__block_id': 'uniminds/options/species/v1.0.0', '__block_label': 'species',
                               '@id': 'species', '@type': 'https://schema.hbp.eu/uniminds/options/species/v1.0.0',
                               'name': 'Homo sapiens', 'Identifier': 'HS', 'species': [{'@id': 'ds001'}]}
                    DOI_dict = {'__block_id': 'uniminds/options/doi/v1.0.0', '__block_label': 'doi',
                                '@id': 'doi', '@type': 'https://schema.hbp.eu/uniminds/options/doi/v1.0.0',
                                'citation': HowToAcknowledge, 'identifier': DatasetDOI}
                    license_def = {'CC0': 'Freeing content globally without restrictions',
                                   'CC BY': ' Creative Commons with Attribution alone',
                                   'CC BY-SA': 'Creative Commons with Attribution and ShareAlike',
                                   'CC BY-NC': 'Creative Commons with Attribution and Noncommercial',
                                   'CC BY-NC-SA': 'Creative Commons with Attribution, Noncommercial and ShareAlike',
                                   'CC BY-ND': 'Creative Commons with Attribution and NoDerivatives',
                                   'CC BY-NC-ND': 'Creative Commons with Attribution, Noncommercial and NoDerivatives'}
                    for key, value in license_def.items():
                        if License.startswith(key):
                            fullname = value
                    License_dict = {'__block_id': 'uniminds/options/license/v1.0.0', '__block_label': 'License',
                                    '@id': License,
                                    '@type': 'https://schema.hbp.eu/uniminds/options/license/v1.0.0',
                                    'identifier': License, 'fullname': fullname, 'url': 'https://creativecommons.org/'}
                    self.g.new_minds_collection['minds_blocks'].extend((DOI_dict, species, License_dict))
                    for block in self.g.new_minds_collection['minds_blocks']:
                        if block['@id'] == '.json':
                            self.g.new_minds_collection['minds_blocks'].remove(block)
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
                                        if something in ['T1w', 'T2w', 'inplaneT2', 'T1rho', 'T1map', 'T2map',
                                                         'T2star', 'FLAIR', 'FLASH', 'PD', 'PDmap',
                                                         'PDT2', 'inplaneT2', 'angio']:
                                            file_name = element['participant_id'] + '_' + var + '_' + something
                                            file_id = element['participant_id'] + '_' + var + '_' + '.'.join(
                                                x[key][var])
                                            sub_MRI.append(file_name)
                                            url = self.folderpath + '/' + element[
                                                'participant_id'] + '/' + var + '/anat/' + element[
                                                      'participant_id'] + '_' + var + '_' + '.'.join(x[key][var])
                                            self.list_files.append(url)
                                            self.g.create_block(blocktemp=self.g.File, id=file_id,
                                                           subject=[{'@id': '%s.json' % element['participant_id']}],
                                                           url=url, name=file_name,
                                                           method=[{'@id': '%s.json' % something}])
                                if type(x[key][var]) == dict:
                                    for y in x[key][var].keys():
                                        if y.startswith('task'):
                                            run = []
                                            if 'nii' in x[key][var][y] or 'tsv' in x[key][var][y]:
                                                for z in x[key][var][y]:
                                                    if type(z) != dict and z.startswith('run'):
                                                        run.append(z)

                                                file_name = element[
                                                                'participant_id'] + '_' + var + '_' + y + '_' + ''.join(
                                                    run)
                                                file_id = element['participant_id'] + '-file-' + y + '_' + ''.join(
                                                    run) + '_' + '.'.join(
                                                    x[key][var][y][1:])
                                                sub_fMRI.append(file_name)
                                                url = self.folderpath + '/' + element[
                                                    'participant_id'] + '/' + var + '/func/' + element[
                                                          'participant_id'] + '_' + var + '_' + y + '_' + ''.join(
                                                    run) + '_' + '.'.join(
                                                    x[key][var][y][1:])
                                                self.list_files.append(url)
                                                self.g.create_block(blocktemp=self.g.File, id=file_id,
                                                               subject=[{'@id': '%s.json' % element['participant_id']}],
                                                               method=[{'@id': 'fMRI-01.json'}],
                                                               url=url, name=file_name)
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
                                                file_name = element[
                                                                'participant_id'] + '_' + var + '_' + y + '_' + ''.join(
                                                    crun) + '_' + '.'.join(filenamelist)
                                                file_id = element[
                                                              'participant_id'] + '_' + var + '_' + y + '_' + ''.join(
                                                    crun) + '_' + '.'.join(filenamelist)
                                                sub_fMRI.append(file_name)
                                                url = self.folderpath + '/' + element[
                                                    'participant_id'] + '/' + var + '/func/' + element[
                                                          'participant_id'] + '_' + var + '_' + y + '_' + ''.join(
                                                    crun) + '_' + '.'.join(filenamelist)
                                                self.list_files.append(url)
                                                self.g.create_block(blocktemp=self.g.File, id=file_id,
                                                               subject=[{'@id': element['participant_id']}],
                                                               method=[{'@id': 'fMRI-01.json'}],
                                                               url=url, name=file_name)


                        elif var.startswith('task'):
                            run = []
                            if 'nii' in x[key][var] or 'tsv' in x[key][var]:
                                for z in x[key][var]:
                                    if type(z) != dict and z.startswith('run'):
                                        run.append(z)
                                file_name = element['participant_id'] + '_' + var + '_' + ''.join(run) + '_' + '.'.join(
                                    x[key][var][1:])
                                file_id = element['participant_id'] + '_' + var + '_' + ''.join(run) + '_' + '.'.join(
                                    x[key][var][1:])
                                sub_fMRI.append(file_name)
                                url = self.folderpath + '/' + element['participant_id'] + '/func/' + element[
                                    'participant_id'] + '_' + var + '_' + ''.join(run) + '_' + '.'.join(
                                    x[key][var][1:])
                                self.list_files.append(url)
                                self.g.create_block(blocktemp=self.g.File, id=file_id,
                                               subject=[{'@id': '%s.json' % element['participant_id']}],
                                               method=[{'@id': 'fMRI-01.json'}],
                                               url=url, name=file_name)
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
                                url = self.folderpath + '/' + element['participant_id'] + '/func/' + element[
                                    'participant_id'] + '_' + var + '_' + ''.join(
                                    crun) + '_' + '.'.join(filenamelist)
                                self.list_files.append(url)
                                self.g.create_block(blocktemp=self.g.File, id=file_id,
                                               subject=[{'@id': '%s.json' % element['participant_id']}],
                                               method=[{'@id': 'fMRI-01.json'}],
                                               url=url, name=file_name)
                        elif not var.startswith('ses') and not var.startswith('task'):
                            if 'nii' in x[key] or 'tsv' in x[key]:
                                if var in ['T1w', 'T2w', 'inplaneT2', 'T1rho', 'T1map', 'T2map',
                                           'T2star', 'FLAIR', 'FLASH', 'PD', 'PDmap',
                                           'PDT2', 'inplaneT2', 'angio']:
                                    file_name = element['participant_id'] + '_' + var
                                    file_id = element['participant_id'] + '_' + '.'.join(x[key])
                                    sub_MRI.append(file_name)
                                    url = self.folderpath + '/' + element['participant_id'] + '/anat/' + element[
                                        'participant_id'] + '_' + '.'.join(x[key])
                                    self.list_files.append(url)
                                    self.g.create_block(blocktemp=self.g.File, id=file_id,
                                                   subject=[{'@id': '%s.json' % element['participant_id']}], url=url,
                                                   name=file_name, method=[{'@id': '%s.json' % var}])

            file_list = []
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
            self.g.create_block(blocktemp=self.g.Subject, id=participant_id)
            self.g.create_block(blocktemp=self.g.Subject, id=participant_id,
                           age=age_unit, sex=[{'@id': '%s.json' % sex}],
                           age_category=[{'@id': '%s.json' % age_category}],
                           handedness=[{'@id': '%s.json' % handedness}], subject=file_list, )
        for element in age_category_list:
            if element == 'juvenile':
                age_category_dict = {'@id': '%s.json' % element, '__block_label': 'Age_category',
                                     '@type': 'https://schema.hbp.eu/uniminds/options/Age_category/v1.0.0',
                                     '__block_id': 'uniminds/options/age_category/v1.0.0', 'Name': element}
                self.g.new_minds_collection['minds_blocks'].append(age_category_dict)
            elif element == 'adult':
                age_category_dict = {'@id': '%s.json' % element, '__block_label': 'Age_category',
                                     '@type': 'https://schema.hbp.eu/uniminds/options/Age_category/v1.0.0',
                                     '__block_id': 'uniminds/options/age_category/v1.0.0', 'Name': element}
                self.g.new_minds_collection['minds_blocks'].append(age_category_dict)
            else:
                continue
        for element in set(sex_list):
            if element == "M":
                sex_dict = {'@id': '%s.json' % element, '@type': 'https://schema.hbp.eu/uniminds/options/Sex/v1.0.0',
                            '__block_label': 'Sex',
                            '__block_id': 'uniminds/options/sex/v1.0.0', 'Name': 'Male',
                            "Description": "sex of the participant"}
                self.g.new_minds_collection['minds_blocks'].append(sex_dict)
            elif element == "F":
                sex_dict = {'@id': '%s.json' % element, '@type': 'https://schema.hbp.eu/uniminds/options/Sex/v1.0.0',
                            '__block_label': 'Sex',
                            '__block_id': 'uniminds/options/sex/v1.0.0', 'Name': 'Female',
                            "Description": "sex of the participant"}
                self.g.new_minds_collection['minds_blocks'].append(sex_dict)
            else:
                continue
        for element in set(handedness_list):
            if element == "L":
                handedness_dict = {'@id': '%s.json' % element,
                                   '@type': 'https://schema.hbp.eu/uniminds/options/Handness/v1.0.0',
                                   '__block_label': 'Handness',
                                   '__block_id': 'uniminds/options/handedness/v1.0.0', 'Name': 'Left',
                                   "Description": "handedness of the participant as reported by the participant"}
                self.g.new_minds_collection['minds_blocks'].append(handedness_dict)
            elif element == "R":
                handedness_dict = {'@id': '%s.json' % element,
                                   '@type': 'https://schema.hbp.eu/uniminds/options/Handness/v1.0.0',
                                   '__block_label': 'Handness',
                                   '__block_id': 'uniminds/options/handedness/v1.0.0', 'Name': 'Right',
                                   "Description": "handedness of the participant as reported by the participant"}
                self.g.new_minds_collection['minds_blocks'].append(handedness_dict)
            else:
                continue
        for element in set(group_list):
            ids = []
            age_cata = []
            selist = []
            handlist = []
            for xelement in self.truelist:
                if xelement['group'] == element:
                    dic = {'@id': xelement['participant_id'] + '.json'}
                    ids.append(dic)
                    if int(xelement['age']) >= 18:
                        age_co = {'@id': 'adult.json'}
                        age_cata.append(age_co)
                    if int(xelement['age']) < 18:
                        age_co = {'@id': 'juvenile.json'}
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
            self.g.create_block(blocktemp=self.g.Subjectgroup, id=element, subjects=ids, age_category=age_cata, sex=selist,
                           handedness=handlist)
        method_id = []
        for element in sub_MRI:
            ext = ['T1w', 'T2w', 'inplaneT2', 'T1rho', 'T1map', 'T2map', 'T2star', 'FLAIR', 'FLASH', 'PD', 'PDmap',
                   'PDT2', 'inplaneT2', 'angio']
            for x in ext:
                if element.endswith(x):
                    method_id.append(x)
        sub_method_id = []
        for element in set(method_id):
            dic = {}
            dic['@id'] = '%s.json' % element
            sub_method_id.append(dic)
            method = []
            for x in sub_MRI:
                if x.endswith(element):
                    dic = {}
                    dic['@id'] = '%s.json' % x
                    method.append(dic)
            self.g.create_block(blocktemp=self.g.Method, id=element, method=method)
        method_fMRI = []
        for element in sub_fMRI:
            dic = {'@id': '%s.json' % element}
            method_fMRI.append(dic)
        for path, dirs, files in os.walk(self.folderpath):
            if 'func' in dirs:
                fmri_id = 'fMRI-01'
                self.g.create_block(blocktemp=self.g.Method, id=fmri_id,
                               description='This the is main MRI method block connected to all other fMRI files',
                               method=method_fMRI)
            if 'anat' in dirs:
                mri_id = 'MRI-01'
                self.g.create_block(blocktemp=self.g.Method, id=mri_id,
                               description='This the is main MRI method block connected to all other MRI files',
                               method=[{'@id': '%s.json' % data_set_name}], sub_method=sub_method_id)
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
                        RepetitionTime = ' RepetitionTime: ' + str(element[key]['RepetitionTime'])
                    else:
                        RepetitionTime = ''
                    if 'CogAtlasID' in element[key].keys():
                        CogAtlasID = element[key]['CogAtlasID']
                    else:
                        CogAtlasID = ''
                    if 'Instructions' in element[key].keys():
                        Instructions = ' Instructions: ' + element[key]['Instructions']
                    else:
                        Instructions = ''
                for element in sub_fMRI:
                    if key in element:
                        fdic = {'@id': '%s.json' % element}
                        flist.append(fdic)
            self.g.create_block(blocktemp=self.g.Method, id=key, identifier=identifier, name=TaskName, method=flist,
                           description=descrip + Instructions + RepetitionTime,
                           publication=[{'@id': '%s-Pub.json' % key}])
            self.g.create_block(blocktemp=self.g.Publication, id=key + '-Pub', identifier=CogAtlasID + ' ' + key, url=CogAtlasID)
        self.g.create_block(blocktemp=self.g.Filebundle, id='main filebundle',
                       description='This filebundle contains all dataset URLs', name='main filebundle',
                       url=str(self.list_files))
        self.graph = self.g.new_minds_collection
    def save_minds(self, graph):
        """
        call the (save_minds_collection) method of the MINDS4PY.MINDS class; save the graph in MINDS
        standard repository structure.
        :param graph: the to be saved graph.
        :type graph: dict
        """
        self.g.save_minds_collection(graph)



#p = BIDS2MINDS(folderpath="C:/Users/Asus T102 H/Desktop/ds001")
#c = p.mindify(data_set_name='ds001', location="C:/Users/Asus T102 H/Desktop/trail")
#p.graph
#p.save_minds(p.graph)

