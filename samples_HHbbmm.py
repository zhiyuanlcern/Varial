import yaml
import os
import ROOT as R
from Htautau import *
# The name of the TTree in the ntuple.


make_link = False
get_weight = False
input_path = 'fixbtag_nprebtagjets_newgensum_DR_ttbar'
run_fakes = True
pure_MC = True

samples_name = "sample_database/datasets.yaml" 
samples_f = open(samples_name, "r") 
samples_list =  yaml.load(samples_f, Loader = yaml.Loader) 

"""
Xsec: dictionary with key: nick name, value: dictionary of 'xsec', 'era', 'nevents', 'nfiles', 'sample_type'
"""

scope = "mt"
lumi = 59.8e3

treename = 'ntuple'


# default_colors = [632, 814, 596, 870, 800, 840, 902, 797, 891, 401, 434, 838,
#                   872, 420, 403, 893, 881, 804, 599, 615, 831, 403, 593, 810]

input_pattern = [input_path + '/%s*root']
def get_samples(channel, signal_overlay=True, **kwargs):
    sf_lumi = 1.
    sf_zjb = kwargs.get('sf_zjb', 1.)
    ##########################################
    samples = {}
    ## for the first run, set rerun = True
    
    for nick in samples_list:
        xsec = samples_list[nick]['xsec']
        sample_type = samples_list[nick]['sample_type']

        if os.path.exists(input_path):
            if run_fakes:
                pass
                # if  "ttbar" in sample_type:
                #     continue
                # if  "wjets" in sample_type:
                #     continue    
            else:
                if  "fakes" in sample_type:
                    continue    
            if sample_type == 'data':
                continue
            if pure_MC:
                if 'embedding' in sample_type:
                    continue
            else:
                if "DYJets" in nick:
                    continue
            
            # if  "ttbar" in sample_type:
            #     continue
            # if  "wjets" in sample_type:
            #     continue    
            if sample_type == 'embedding':
                samples[nick] = ['1', 1,   sample_type     , [nick] ,  0 ]

            elif sample_type == 'fakes':
                samples[nick] = ['1', 1/59.8e3,   sample_type     , [nick] ,  0 ]
            elif sample_type == 'ttbar':
                samples[nick] = ['1', 0.8,   sample_type     , [nick] ,  0 ]
            else:
                # sumofweight = getnickweight(input_path,nick, rerun = get_weight)  
                # if sumofweight != 0:
                    if "rem" in sample_type or 'electroweak_boson' in sample_type or 'vbf' in sample_type or 'diboson' in sample_type or 'ggh_hbb' in sample_type  or 'singletop' in sample_type  :
                        samples[nick] = ['1', 1,   'other'     , [nick] ,  0 ]
                    else:
                        samples[nick] = ['1', 1,   sample_type     , [nick] ,  0 ]

    #  if signal_overlay:
    #      samples.update({
    #          'HHbbmmC3m05_0':  ["weight>-99", 1.*sf_lumi*0.01, 'HHbbmm(C3m05_0)*0.01',   ['HHbbmmC3m05_0'],1],
    #      })
    
    samples.update({
#             'Data': ["1", 1, 'Data', ['SingleMuon'],0],
            'Data': ["1", 1, 'Data', ['SingleMuon_Run2018'],0],
        })
    
    return samples


def getsampletype(samples_list):
    """
    take samples_list =  yaml.load(samples_f, Loader = yaml.FullLoader)  as input
    return a list of sample type
    """
    sampletype = []
    for nick in samples_list:
        if samples_list[nick]['sample_type'] not in sampletype:
            sampletype.append(samples_list[nick]['sample_type'])
        else:
            continue
    return sampletype


def checknoevents(input_file_name):
    if not os.path.exists(input_path):
        return 0
    f = R.TFile.Open(input_file_name, "READ")
    try:
        tree = f.Get("ntuple")
    except:
        if not tree:
            print(input_file_name)
            return 0
    if tree:
        return 1


# weights_f = open('sample_database/datasets.yaml', "r") 
# samples_list =  yaml.safe_load(weights_f)
# print(getsampletype(samples_list))