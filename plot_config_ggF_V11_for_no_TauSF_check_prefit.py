# from samples_HHbbmm import *
import varial
import sys
import ROOT as R
import array
import yaml
from Htautau_new_trigger_cut import *
import argparse
import matplotlib.pyplot as plt


plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"


# import wrappers

''' usage:
python run_plotting_with_varial.py plot_config_ggF.py input_path plot_tag & 
'''




####################
# General Settings #
####################



parser = argparse.ArgumentParser(description='Plot btag variables from ROOT files with weights.')
parser.add_argument('dummy_input', type=str, nargs='+', help='Place holder, dummy argument')
parser.add_argument('--input_path', type=str, help='Path to the folder containing ROOT files')
parser.add_argument('--mass',  type=str, help='mass of signal to plot')
parser.add_argument('--era', type=str, default='2022postEE', help='input era, 2022postEE or 2022EE')
parser.add_argument('--channel', type=str, default='mt', help='decay channel, mt, et, tt, em')
parser.add_argument('--region', type=str, default='nob', help='btag selection, nob, btag')
parser.add_argument('--PNN', type=int, default=0, help='run PNN score or not')
parser.add_argument('--signal_type', type=str, default='ggH', help='ggH or bbH or ggH_bbH')
parser.add_argument('--use_LO_DY', type=int, default=0, help='0: use NLO DY, 1: use LO DY')
args = parser.parse_args()

input_path= args.input_path
mass = args.mass
PNN = args.PNN
channel_name = args.channel
era = args.era
signal_type = args.signal_type
region = args.region
# input_path = sys.argv[3]
# mass = int(sys.argv[4])
# PNN = int(sys.argv[5])
# channel_name = str(sys.argv[6])
# era = sys.argv[7]
# run_fakes = int(sys.argv[8])
# region = sys.argv[9]
# run_dy = True




if channel_name == "et":
    channel_index = 1
elif channel_name == "mt":
    channel_index = 2
else:
    channel_index = 1

luminosities = {
    "2016preVFP": 15.1158e3,
    "2016postVFP": 10.0093e3,
    "2017": 41.5e3,
    "2018": 59.8e3,
    "2022EE":8.077009684e3,
    "2022postEE":  26.671609707e3,
    "2023":  18.062659111e3, # B + C
    "2023BPix": 9.693130053e3, # D 
     }
# 2022 golden json
# B         0.096555539
# C 	 	5.010409016
# D 	 	2.970045129
# E 	 	5.806955207
# F 	 	17.781901464     	
# G 	 	3.082753036
# postEE  26.337
if era in luminosities:
        lumi = luminosities[era]
else:
        print("Wrong year provided")
        sys.exit(-10)

print(mass, sys.argv[4],"===================================")

 
samples_name = 'sample_database/datasets_plotting.yaml'
samples_f = open(samples_name, "r") 
samples_list =  yaml.load(samples_f, Loader = yaml.Loader) 

# 'embedding', 
if channel_name != "tt":
    stacking_order = [
    # 'Z->tautau', # 'Z->ll', # 'wjets', # 'Single H',   ###
    'Top', 'DY-Jets-ll','other','fakes' ,'DY-Jets-tt',]
    stacking_order = [
    'DY-Jets', 'fakes',  'Top',     'other',     ]
else:
    stacking_order = [
    'fakes', 'DY-Jets', 'Top',     'other',     ]

if int(mass) > 200:
    scale =10 
elif int(mass) >= 100:
    scale = 200
else:
    scale =10000


if channel_name != 'em':   
                      
    sample_colors = {
    # 'embedding'  :  838,
    # 'electroweak_boson'  :  804,
    # 'electroweak_boson'  :  804,
    # 'dyjets'  :  814,
    'fakes' : 901,
    'DY-Jets' : 864,
    'DY-Jets-ll'  :  814,
    'DY-Jets-#tau#tau'  :  865,
    # "DY-Jets-fakes": 596,
    "Top" : 401,
    # 'wjets'  :  632,
    'Single H': 838,
    'other' : 920, 
    "%s*bbH-%s" %(scale,mass) : 416,
    "%s*ggH-%s" %(scale,mass) : 632,
    # 'Top-genuine-#tau': 401,
    # 'Top-fake-#tau': 501,
    # 'diboson'  :  596,
    # 'ggh_hbb'  :  596,
    # 'ggh_htautau'  :  838,
    # 'singletop'  :  920,
    # 'ttbarFake'  :  596,
    # 'vbf_htautau'  :  814,
    # 'rem_hbb':  615,

    }

elif channel_name == 'em':

    sample_colors = {
    # 'embedding'  :  838,
    # 'electroweak_boson'  :  804,
    # 'electroweak_boson'  :  804,
    # 'dyjets'  :  814,
    'fakes' : 901,
    'DY-Jets' : 864,
    'DY-Jets-ll'  :  814,
    "DY-Jets-#tau#tau"  :  865,
    # 'DY-Jets-tt-em'  :  865,
    "DY-Jets-fakes": 596,
    # 'DY-Jets-tt-other': 838,
    'Top'  :  400,
    # 'wjets'  :  804,
    'Single H': 838,
    'other' : 920, 
    "%s*bbH-%s" %(scale,mass) : 416,
    "%s*ggH-%s" %(scale,mass) : 632,
    "Top-genuine-#tau" : 401,
    "Top-fake-#tau": 617,
    # 'diboson'  :  596,
    # 'ggh_hbb'  :  596,
    # 'ggh_htautau'  :  838,
    # 'singletop'  :  920,
    # 'ttbarFake'  :  596,
    # 'vbf_htautau'  :  814,
    # 'rem_hbb':  615,

}




varial.settings.max_num_processes = 80
varial.settings.rootfile_postfixes += ['.pdf'] #'.pdf'
varial.settings.stacking_order = stacking_order
# try to find output on disk and don't run a step if present
enable_reuse_step = True

#################
# Plot Settings #
#################

name = sys.argv[2]
weight_dict ={"mt" : {}, "et": {}, "tt": {}, "em": {}, "mm":{}}
# weight_dict["mt"] = {
#     "2018": 'Xsec * {0} * genWeight/genEventSumW * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Tight_2 * iso_wgt_mu_1 *  btag_weight * puweight  '.format(lumi),
#     "2017": 'Xsec * {0} * genWeight/genEventSumW * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Tight_2 * iso_wgt_mu_1 *  btag_weight * puweight  '.format(lumi),
#     "2016": 'Xsec * {0} * genWeight/genEventSumW * id_wgt_mu_1 * id_wgt_tau_vsEle_VVLoose_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_Tight_2 * iso_wgt_mu_1 *  btag_weight * puweight  '.format(lumi),
# }
# weight_dict["et"] = {
#     "2018": 'Xsec * {0} * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *   btag_weight * puweight  '.format(lumi),
#     "2017": 'Xsec * {0} * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *   btag_weight * puweight  '.format(lumi),
#     "2016": 'Xsec * {0} * genWeight/genEventSumW *  id_wgt_tau_vsEle_Tight_2 * id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsMu_VLoose_2 *   btag_weight * puweight  '.format(lumi),
# }

weight_dict["mt"]["2022postEE"] = 'Xsec   * {0} * puweight * genWeight/genEventSumW  *  btag_weight * FF_weight  * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 *ZPtMassReweightWeight'.format(lumi) ##    
weight_dict["mt"]["2022EE"] =weight_dict["mt"]["2023"] =weight_dict["mt"]["2023BPix"]= weight_dict["mt"]["2022postEE"]
     

weight_dict["et"]["2022postEE"] =  'Xsec * {0}* puweight * genWeight/genEventSumW     *  btag_weight * FF_weight   * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30 * id_wgt_tau_vsEle_Tight_2 *ZPtMassReweightWeight ' .format(lumi) #  
weight_dict["et"]["2022EE"] =weight_dict["et"]["2023"] =weight_dict["et"]["2023BPix"]= weight_dict["et"]["2022postEE"]

weight_dict["tt"] = {}
weight_dict["tt"]["2022postEE"]  =   'Xsec *  {0}* puweight * genWeight/genEventSumW *    btag_weight    *  FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 *ZPtMassReweightWeight '.format(lumi) # 
weight_dict["tt"]["2022EE"] =weight_dict["tt"]["2023"] =weight_dict["tt"]["2023BPix"]= weight_dict["tt"]["2022postEE"]

weight_dict["em"] = {"2022postEE": '(Xsec * genWeight *  {0} / genEventSumW) * id_wgt_ele_wpTight * id_wgt_mu_2 * btag_weight *  FF_weight * puweight * (( trg_single_mu24 > 0? trg_wgt_single_mu24 : (trg_single_ele30 > 0? trg_wgt_single_ele30 : 1   ) )) * ZPtMassReweightWeight  * iso_wgt_mu_2 '   .format(lumi)} # ( trg_single_ele30 > 0? trg_wgt_single_ele30 :1 )   #remove  trg_wgt_single_ele30  iso_wgt_mu_2 2024/4/2   #add FF_weight 2025/2/12




weight_dict["em"]["2022EE"] =weight_dict["em"]["2023"] =weight_dict["em"]["2023BPix"]= weight_dict["em"]["2022postEE"]

weight_dict["mm"] = {"2022postEE": '(Xsec * genWeight *  {0} / genEventSumW) * puweight *  id_wgt_mu_1*iso_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_2* trg_wgt_single_mu24 '.format(lumi)} # * ZPtMassReweightWeight
weight_dict["mm"]["2022EE"] =weight_dict["mm"]["2023"] =weight_dict["mm"]["2023BPix"]= weight_dict["mm"]["2022postEE"]

weight = weight_dict[channel_name][era]


# weight = "Train_weight"
plot_vars = {}
nob_tight_mT = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,5000.0]
nob_loose_mT = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,5000.0]
btag_tight_mT = [0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,250.0,300.0,350.0,400.0,500.0,600.0,700.0,5000.0] # remove two bin
mt_tot_b = [30, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500]
m_fastmtt = [0,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,240,260,300]
met = [0,10,20,30,40,50,60,70,80,90,120,140,200,400]
pt = [30,40,50,60,70,80,90,100,120,140,200,350,500, 700, 1000]


plot_vars.update({ 

    #PNN_input :     mass: 5     pt: 4    Angle: 6 advanece: 10
    
       
    # 'btag_weight': ('btag_weight', ';btag_weight;NEvents', 30, 0, 3),
    # 'btag_weight__btagUncCFerr1Down': ('btag_weight__btagUncCFerr1Down', ';btag_weight__btagUncCFerr1Down;NEvents', 30, 0, 3),
    # 'btag_weight__btagUncCFerr1Up': ('btag_weight__btagUncCFerr1Up', ';btag_weight__btagUncCFerr1Up;NEvents', 30, 0, 3),



    # 'mt_tot': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents', 30, 0, 300),


    'm_vis'       :    ('m_vis', '; m^{vis}[GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs1prong0pizeroDown': ('m_vis__tauEs1prong0pizeroDown', ';m^{vis}__tauEs1prong0pizeroDown [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs1prong0pizeroUp'  : ('m_vis__tauEs1prong0pizeroUp',   ';m^{vis}__tauEs1prong0pizeroUp [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs1prong1pizeroDown': ('m_vis__tauEs1prong1pizeroDown', ';m^{vis}__tauEs1prong1pizeroDown [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs1prong1pizeroUp'  : ('m_vis__tauEs1prong1pizeroUp',   ';m^{vis}__tauEs1prong1pizeroUp [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs3prong0pizeroDown': ('m_vis__tauEs3prong0pizeroDown', ';m^{vis}__tauEs3prong0pizeroDown [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs3prong0pizeroUp'  : ('m_vis__tauEs3prong0pizeroUp',   ';m^{vis}__tauEs3prong0pizeroUp [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs3prong1pizeroDown': ('m_vis__tauEs3prong1pizeroDown', ';m^{vis}__tauEs3prong1pizeroDown [GeV];NEvents', 40, 0, 200),
    'm_vis__tauEs3prong1pizeroUp'  : ('m_vis__tauEs3prong1pizeroUp',   ';m^{vis}__tauEs3prong1pizeroUp [GeV];NEvents', 40, 0, 200),



    # 'mt_1' : ('mt_1',';m_{T}^{l_{1}}[GeV];NEvents',50,0,200),
    # 'mt_2' : ('mt_2',';m_{T}^{l_{2}}[GeV];NEvents',50,0,200),
    # 'met' : ('met',';met[GeV];NEvents',30,0,150), 

    # 'pt_1' : ('pt_1',';pt_{1}[GeV];NEvents',31,25,180),
    # 'pt_2' : ('pt_2',';pt_{2}[GeV];NEvents',30,30,180),
    # 'pt_tt'   :    ('pt_tt', ';pt_{tt}[GeV];NEvents', 40, 0, 200),
    # 'pt_vis'   :    ('pt_vis', ';pt_{vis}[GeV];NEvents', 40, 0, 200),

    # 'deta_12' : ('eta_1-eta_2', ';#Delta#eta_{12};NEvents',30 ,-3.5, 3.5),
    # 'deltaR_ditaupair' :  ('deltaR_ditaupair', ';#DeltaR ;NEvents',25 , 0, 5), 
    # 'dphi_12': ('dphi_12', ';#Delta#phi(l_{1},l_{2});NEvents', 30, 0, 3.2),
    # 'metphi' : ('metphi',';#Delta#phi_{#scale[0.8]{MET}};NEvents',80,-4,4),
    # 'dphi_H1' : ('dphi_H1', ';#Delta#phi(#scale[0.8]{ditau},l_{1});NEvents',30 ,0, 3.2),
    # 'dphi_H2' : ('dphi_H2', ';#Delta#phi(#scale[0.8]{ditau},l_{2});NEvents',30 ,0, 3.2),
    
    # 'njets' : ('njets',';Njets;NEvents',10,0,10),

    'm_fastmtt'       :    ('m_fastmtt', '; m^{#tau#tau};NEvents',  27, 30, 300),
    
    'm_fastmtt__jerUncDown': ('m_fastmtt__jerUncDown', ';m^{#tau#tau}__jerUncDown;NEvents', 27, 30, 300),
    'm_fastmtt__jerUncUp': ('m_fastmtt__jerUncUp', ';m^{#tau#tau}__jerUncUp;NEvents', 27, 30, 300),
    
    'm_fastmtt__jesUncAbsoluteDown': ('m_fastmtt__jesUncAbsoluteDown', ';m^{#tau#tau}__jesUncAbsoluteDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncAbsoluteUp':   ('m_fastmtt__jesUncAbsoluteUp',   ';m^{#tau#tau}__jesUncAbsoluteUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncAbsoluteYearDown': ('m_fastmtt__jesUncAbsoluteYearDown', ';m^{#tau#tau}__jesUncAbsoluteYearDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncAbsoluteYearUp':   ('m_fastmtt__jesUncAbsoluteYearUp',   ';m^{#tau#tau}__jesUncAbsoluteYearUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncBBEC1Down': ('m_fastmtt__jesUncBBEC1Down', ';m^{#tau#tau}__jesUncBBEC1Down;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncBBEC1Up':   ('m_fastmtt__jesUncBBEC1Up',   ';m^{#tau#tau}__jesUncBBEC1Up;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncBBEC1YearDown': ('m_fastmtt__jesUncBBEC1YearDown', ';m^{#tau#tau}__jesUncBBEC1YearDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncBBEC1YearUp':   ('m_fastmtt__jesUncBBEC1YearUp',   ';m^{#tau#tau}__jesUncBBEC1YearUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncEC2Down': ('m_fastmtt__jesUncEC2Down', ';m^{#tau#tau}__jesUncEC2Down;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncEC2Up':   ('m_fastmtt__jesUncEC2Up',   ';m^{#tau#tau}__jesUncEC2Up;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncEC2YearDown': ('m_fastmtt__jesUncEC2YearDown', ';m^{#tau#tau}__jesUncEC2YearDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncEC2YearUp':   ('m_fastmtt__jesUncEC2YearUp',   ';m^{#tau#tau}__jesUncEC2YearUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncFlavorQCDDown': ('m_fastmtt__jesUncFlavorQCDDown', ';m^{#tau#tau}__jesUncFlavorQCDDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncFlavorQCDUp':   ('m_fastmtt__jesUncFlavorQCDUp',   ';m^{#tau#tau}__jesUncFlavorQCDUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncHFDown': ('m_fastmtt__jesUncHFDown', ';m^{#tau#tau}__jesUncHFDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncHFUp':   ('m_fastmtt__jesUncHFUp',   ';m^{#tau#tau}__jesUncHFUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncHFYearDown': ('m_fastmtt__jesUncHFYearDown', ';m^{#tau#tau}__jesUncHFYearDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncHFYearUp':   ('m_fastmtt__jesUncHFYearUp',   ';m^{#tau#tau}__jesUncHFYearUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncRelativeBalDown': ('m_fastmtt__jesUncRelativeBalDown', ';m^{#tau#tau}__jesUncRelativeBalDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncRelativeBalUp':   ('m_fastmtt__jesUncRelativeBalUp',   ';m^{#tau#tau}__jesUncRelativeBalUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncRelativeSampleYearDown': ('m_fastmtt__jesUncRelativeSampleYearDown', ';m^{#tau#tau}__jesUncRelativeSampleYearDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncRelativeSampleYearUp':   ('m_fastmtt__jesUncRelativeSampleYearUp',   ';m^{#tau#tau}__jesUncRelativeSampleYearUp;NEvents',   27, 30, 300),

    'm_fastmtt__jesUncTotalDown': ('m_fastmtt__jesUncTotalDown', ';m^{#tau#tau}__jesUncTotalDown;NEvents', 27, 30, 300),
    'm_fastmtt__jesUncTotalUp':   ('m_fastmtt__jesUncTotalUp',   ';m^{#tau#tau}__jesUncTotalUp;NEvents',   27, 30, 300),

    'm_fastmtt__tauEs1prong0pizeroDown': ('m_fastmtt__tauEs1prong0pizeroDown', ';m^{#tau#tau}__tauEs1prong0pizeroDown;NEvents', 27, 30, 300),
    'm_fastmtt__tauEs1prong0pizeroUp':   ('m_fastmtt__tauEs1prong0pizeroUp',   ';m^{#tau#tau}__tauEs1prong0pizeroUp;NEvents',   27, 30, 300),

    'm_fastmtt__tauEs1prong1pizeroDown': ('m_fastmtt__tauEs1prong1pizeroDown', ';m^{#tau#tau}__tauEs1prong1pizeroDown;NEvents', 27, 30, 300),
    'm_fastmtt__tauEs1prong1pizeroUp':   ('m_fastmtt__tauEs1prong1pizeroUp',   ';m^{#tau#tau}__tauEs1prong1pizeroUp;NEvents',   27, 30, 300),

    'm_fastmtt__tauEs3prong0pizeroDown': ('m_fastmtt__tauEs3prong0pizeroDown', ';m^{#tau#tau}__tauEs3prong0pizeroDown;NEvents', 27, 30, 300),
    'm_fastmtt__tauEs3prong0pizeroUp':   ('m_fastmtt__tauEs3prong0pizeroUp',   ';m^{#tau#tau}__tauEs3prong0pizeroUp;NEvents',   27, 30, 300),

    'm_fastmtt__tauEs3prong1pizeroDown': ('m_fastmtt__tauEs3prong1pizeroDown', ';m^{#tau#tau}__tauEs3prong1pizeroDown;NEvents', 27, 30, 300),
    'm_fastmtt__tauEs3prong1pizeroUp':   ('m_fastmtt__tauEs3prong1pizeroUp',   ';m^{#tau#tau}__tauEs3prong1pizeroUp;NEvents',   27, 30, 300),


    # 'mTdileptonMET' : ('mTdileptonMET',';m_{T}^{#scale[0.8]{dileptonMET}};NEvents',20,0,200),
    # 'pt_fastmtt'   :    ('pt_fastmtt', ';p_{T}^{#tau#tau} ;NEvents', 40, 0, 200),
    # 'eta_fastmtt' : ('eta_fastmtt',';eta_{#tau#tau};NEvents',30,-2.3,2.3),

    # 'nbtag' : ('nbtag',';Nbtag;NEvents',5,0,5),
    # 'kT' : ('kT',   ';kT;NEvents',     40,0,400       ),
    # 'antikT' : ('antikT',   ';antikT;NEvents',     40,0,0.2       ),
    # 'pt1_LT_to_ptH' : ('pt1_LT_to_ptH', ';p_{T}^{l_{1}} / p_{T}^{#tau#tau};NEvents', 40, 0, 3),
    # 'pt2_LT_to_ptH' : ('pt2_LT_to_ptH',   ';p_{T}^{l_{2}} / p_{T}^{#tau#tau};NEvents', 40, 0, 3),

    # 'mass_tt'       :    ('mass_tt', '; mass_tt;NEvents', 30, 0, 300),
    # 'pt_tt'       :    ('pt_tt', '; pt_tt;NEvents', 30, 0, 300),

    # 'eta_1' : ('eta_1',';eta_{1};NEvents',30,-2.4,2.4),
    # 'eta_2' : ('eta_2',';eta_{2};NEvents',30,-2.4,2.4),
    # 'eta_1_morebins' : ('eta_1',';eta_{1};NEvents',50,-2.5,2.5),
    # 'eta_2_morebins' : ('eta_2',';eta_{2};NEvents',50,-2.5,2.5),
    # 'jeta_1' : ('jeta_1',';jeta_{1};NEvents',60,-6.3,6.3),
    # 'jeta_2' : ('jeta_2',';jeta_{2};NEvents',60,-6.3,6.3),


    


# extra
    # 'C_W'   : ('C_W', ';C_W ;NEvents', 20, -5, 6),
    # 'C_QCD'   : ('C_QCD', ';C_QCD ;NEvents', 20, -5, 5),
    # 'phi_1' : ('phi_1',';phi_{1};NEvents',20,-3.14,3.14),
    # 'phi_2' : ('phi_2',';phi_{2};NEvents',20,-3.14,3.14),
    # 'phi_fastmtt': ('phi_fastmtt',';phi_{#tau#tau};NEvents',20,-3.14,3.14),
    # 'nprebjets' : ('nprebjets',';N_{prebjets};NEvents',10,0,10),
    # # 'taujet_pt_1:' : ('taujet_pt_1',';taujet_{pt_{1}}[GeV];NEvents',30,30,180),
    # # 'taujet_pt_2:' : ('taujet_pt_2',';taujet_{pt_{2}}[GeV];NEvents',30,30,180),


    # 'mass_tt'       :    ('mass_tt', '; mass_tt;NEvents', 30, 0, 300),
    # 'mass_ll'       :    ('mass_ll', '; mass_ll;NEvents', 30, 0, 300),

    # 'metSumEt' : ('metSumEt',';metSumEt;NEvents',40,0,400),
    # 'pzetamissvis' : ('pzetamissvis',';D_{#zeta};NEvents',25,-150,100),  
    
    
    # 'mt_tot': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents', 50, 0, 500),
    # 'mt_tot_rebinned': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents',5000, 0, 5000),
    


    #'mt_tot_rebinned_nob': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents',5000, 0, 5000),
    # 'mt_tot_rebinned_btag': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents',5000, 0, 5000),
    # 'mt_tot_rebinned_nob_loose_mT': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents',5000, 0, 5000),



    # 'phi_1' : ('phi_1',';phi_{1};NEvents',20,-3.14,3.14),
    # 'phi_2' : ('phi_2',';phi_{2};NEvents',20,-3.14,3.14),


  
    
    




#     # 'C_W'   : ('C_W', ';C_W ;NEvents', 20, -5, 6),
#     # 'C_QCD'   : ('C_QCD', ';C_QCD ;NEvents', 20, -2, 2),

#     # 'dphi_H1_LT' : ('dphi_H1_LT', ';#dphi_H1_LT;NEvents',30 ,0, 3.1415),
#     # 'dphi_H2_LT' : ('dphi_H2_LT', ';#dphi_H2_LT;NEvents',30 ,0, 3.1415),    
#     # 'dphi_HMET' : ('dphi_HMET', ';#dphi_HMET;NEvents',30 ,0, 3.1415),
#     # 'dphi_MET_1' : ('dphi_MET_1', ';#dphi_MET_1;NEvents',30 ,0, 3.1415),
#     # 'dphi_MET_2' : ('dphi_MET_2', ';#dphi_MET_2;NEvents',30 ,0, 3.1415),
#     # 'dphi_HMET_LT' : ('dphi_HMET_LT', ';#dphi_HMET_LT;NEvents',30 ,0, 3.1415),
#     # 'dphi_MET_1_LT' : ('dphi_MET_1_LT', ';#dphi_MET_1_LT;NEvents',30 ,0, 3.1415),
#     # 'dphi_MET_2_LT' : ('dphi_MET_2_LT', ';#dphi_MET_2_LT;NEvents',30 ,0, 3.1415),
#     # 'cos_dphi_H1' : ('cos_dphi_H1', ';#cos_dphi_H1;NEvents',40 ,-1, 1),
#     # 'cos_dphi_H2' : ('cos_dphi_H2', ';#cos_dphi_H2;NEvents',40 ,-1, 1),
#     # 'cos_dphi_H1_LT' : ('cos_dphi_H1_LT', ';#cos_dphi_H1_LT;NEvents',40 ,-1, 1),
#     # 'cos_dphi_H2_LT' : ('cos_dphi_H2_LT', ';#cos_dphi_H2_LT;NEvents',40 ,-1, 1),    
#     # 'cos_dphi_HMET' : ('cos_dphi_HMET', ';#cos_dphi_HMET;NEvents',40 ,-1, 1),
#     # 'cos_dphi_MET_1' : ('cos_dphi_MET_1', ';#cos_dphi_MET_1;NEvents',40 ,-1, 1),
#     # 'cos_dphi_MET_2' : ('cos_dphi_MET_2', ';#cos_dphi_MET_2;NEvents',40 ,-1, 1),
#     # 'cos_dphi_HMET_LT' : ('cos_dphi_HMET_LT', ';#cos_dphi_HMET_LT;NEvents',40 ,-1, 1),
#     # 'cos_dphi_MET_1_LT' : ('cos_dphi_MET_1_LT', ';#cos_dphi_MET_1_LT;NEvents',40 ,-1, 1),
#     # 'cos_dphi_MET_2_LT' : ('cos_dphi_MET_2_LT', ';#cos_dphi_MET_2_LT;NEvents',40 ,-1, 1),
#     # 'costhstar_1_LT' : ('costhstar_1_LT', ';costhstar_1_LT;NEvents', 40, -1, 1),
#     # 'costhstar_2_LT' : ('costhstar_2_LT', ';costhstar_2_LT;NEvents', 40, -1, 1),
#     # 'costheta_1_LT' : ('costheta_1_LT', ';costheta_1_LT;NEvents', 40, -1, 1),
#     # 'costheta_2_LT' : ('costheta_2_LT', ';costheta_2_LT;NEvents', 40, -1, 1),
#     # 'pt_1_LT' : ('pt_1_LT',   ';pt_1_LT;NEvents',   50,0,100         ),
#     # 'pt_2_LT' : ('pt_2_LT',   ';pt_2_LT;NEvents',   50,0,100         ),
#     # 'eta_1_LT' : ('eta_1_LT',   ';eta_1_LT;NEvents',   30,-3,3         ),
#     # 'eta_2_LT' : ('eta_2_LT',   ';eta_2_LT;NEvents',   30,-3,3         ),
#     # 'phi_1_LT' : ('phi_1_LT',   ';phi_1_LT;NEvents',   20,-3.14,3.14         ),
#     # 'phi_2_LT' : ('phi_2_LT',   ';phi_2_LT;NEvents',   20,-3.14,3.14         ),
#     # 'deltaR_LT' : ('deltaR_LT',   ';deltaR_LT;NEvents',25 , 0, 5            ),
#     # 'kT_LT' : ('kT_LT',   ';kT_LT;NEvents',     40,0,400       ),
#     # 'antikT_LT' : ('antikT_LT',   ';antikT_LT;NEvents',     40,0,0.2       ),
#     # 'Z_NN_LT' : ('Z_NN_LT',   ';Z_NN_LT;NEvents',    30,0,0.6        ),
#     # 'm_vis_square' : ('m_vis_square',   ';m_vis_square;NEvents',    40, 0, 30e3        ),
#     # 'pt1_to_ptH' : ('pt1_to_ptH',   ';pt1_to_ptH;NEvents',  40, 0, 3         ),
#     # 'pt2_to_ptH' : ('pt2_to_ptH',   ';pt2_to_ptH;NEvents',  40, 0, 3          ),

#     # 'dtheta_12' : ('dtheta_12', ';#dtheta_12;NEvents',30 ,-3.5, 3.5),
#     # 'dphi_12_LT' : ('dphi_12_LT', ';#dphi_12_LT;NEvents', 30 ,0, 3.5 ),
#     # 'deta_12_LT' : ('deta_12_LT', ';#deta_12_LT;NEvents',30 ,-3.5, 3.5 ),
#     # 'dtheta_12' : ('dtheta_12', ';#cos(dtheta_12);NEvents', 30 ,-3.5, 3.5),
#     # 'cos_dtheta_12' : ('cos_dtheta_12', ';#cos(dtheta_12);NEvents', 40 ,-1, 1 ),
#     # 'pt1_to_mH' : ('pt1_to_mH', ';#pt1_to_mH;NEvents', 40, 0, 1),
#     # 'pt2_to_mH' : ('pt2_to_mH', ';#pt2_to_mH;NEvents', 40, 0, 1),
#     # 'pt1_LT_to_mH' : ('pt1_LT_to_mH', ';#pt1_LT_to_mH;NEvents', 40, 0, 0.5),
#     # 'pt2_LT_to_mH' : ('pt2_LT_to_mH', ';#pt2_LT_to_mH;NEvents', 40, 0, 0.5),
#     # 'pt_ttmet_to_mH' : ('pt_ttmet_to_mH', ';#pt_ttmet_to_mH;NEvents', 40, 0, 1),
#     # 'pt_fastmtt_to_mH' : ('pt_fastmtt_to_mH', ';#pt_fastmtt_to_mH;NEvents', 40, 0, 1),
#     # 'pt_vis_to_mH' : ('pt_vis_to_mH', ';#pt_vis_to_mH;NEvents', 40, 0, 1),
#     # 'pt1_LT_to_pt2_LT' : ('pt1_LT_to_pt2_LT', ';#pt1_LT_to_pt2_LT;NEvents', 40, 0, 2),
#     # 'eta_vis' :  ('eta_vis',';eta_vis;NEvents',30,-2.3,2.3),
#     # 'phi_vis' : ('phi_vis',';phi_vis;NEvents',30,-3.5,3.5),
})
if channel_name == "em":
    plot_vars.update({
    'pt_1' : ('pt_1',';pt_{1};NEvents',24,0,120),
    'pt_2' : ('pt_2',';pt_{2};NEvents',24,0,120),
    # 'eta_1' : ('eta_1',';eta_{1};NEvents',30,-3,3),
    # 'eta_2' : ('eta_2',';eta_{2};NEvents',30,-3,3),
    'm_vis'       :    ('m_vis', '; m^{vis};NEvents', 13, 50, 310),
    }
    )
if channel_name == "mm":
     plot_vars.update({       
            'mass_ll'       :    ('mass_ll', '; mass_ll;NEvents', 30, 0, 300),
            'pt_ll'       :    ('pt_ll', '; pt_ll;NEvents', 75, 0, 150),
            'iso_1' : ('iso_1',';iso_{1};NEvents',50,0,0.3),
            'iso_2' : ('iso_2',';iso_{2};NEvents',50,0,0.3),
            'met' : ('met',';met;NEvents',50,0,150),
            })
else:
    print("1")
    # plot_vars.update({
    #     'm_fastmtt'       :    ('m_fastmtt', '; m^{#tau#tau};NEvents',  27, 30, 300),
        
    #     # 'eta_fastmtt' : ('eta_fastmtt',';eta_{#tau#tau};NEvents',30,-2.3,2.3),
    #     # 'pt_fastmtt'   :    ('pt_fastmtt', ';p_{T}^{#tau#tau} ;NEvents', 40, 0, 200),
    #     # 'phi_fastmtt' : ('phi_fastmtt',';phi_{#tau#tau};NEvents',30,-3.5,3.5),
    #     # 'iso_1' : ('iso_1',';iso_{1};NEvents',50,0,1),
    #     # 'iso_2' : ('iso_2',';iso_{2};NEvents',50,0,1),
    # })
if PNN:
    plot_vars = {
        'eta_1' : ('eta_1',';eta_{1};NEvents',30,-2.4,2.4),
        'eta_2' : ('eta_2',';eta_{2};NEvents',30,-2.4,2.4),

        'm_vis'       :    ('m_vis', '; m^{vis};NEvents', 40, 0, 200),

        'pt_1' : ('pt_1',';pt_{1};NEvents',30,30,180),
        'pt_2' : ('pt_2',';pt_{2};NEvents',30,30,180),

        'met' : ('met',';met;NEvents',20,0,100),         
        'mt_tot': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents', 50, 0, 500),
        'm_fastmtt'       :    ('m_fastmtt', '; m^{#tau#tau};NEvents', 27, 30, 300),
        'pt_1' : ('pt_1',';pt_{1};NEvents',20,20,220),
        'pt_2' : ('pt_2',';pt_{2};NEvents',20,20,220),
        'mt_1' : ('mt_1',';mt_{1};NEvents',50,0,200),
        'mt_2' : ('mt_2',';mt_{2};NEvents',50,0,200),
    }
    if int(mass) < 250:
        plot_vars.update({       
            'PNN_%s_nob' %mass : ('PNN_%s' %mass,     ';PNN %s [GeV];NEvents' %mass,  20,0,1),
            'PNN_%s_btag' %mass : ('PNN_%s' %mass,     ';PNN %s [GeV];NEvents' %mass,  15,0,1),
                 }
            
            
            )
else:
    print("1")
    # plot_vars.update({
    # # 'dxy_1' : ('dxy_1',';dxy_{1};NEvents',25,-0.02,0.02),
    # # 'dxy_2' : ('dxy_2',';dxy_{2};NEvents',25,-0.02,0.02),
    # # 'dz_1' : ('dz_1',';dz_{1};NEvents',25,-0.02,0.02),
    # # 'dz_2' : ('dz_2',';dz_{2};NEvents',25,-0.02,0.02),

    # # 'mass_1' : ('mass_1',';mass_{1};NEvents',30,0,0.1),
    # # 'mass_2' : ('mass_2',';mass_{2};NEvents',30,0,3),    
    # 'njets' : ('njets',';njets;NEvents',10,0,10),
    
    # })

# plot_vars.update({  
#     'm_vis'       :    ('m_vis', '; m^{vis};NEvents', 40, 0, 200),
#     'eta_1' : ('eta_1',';eta_{1};NEvents',30,-2.3,2.3),
#     'eta_2' : ('eta_2',';eta_{2};NEvents',30,-2.3,2.3),
#     'pt_1' : ('pt_1',';pt_{1};NEvents',50,0,100),
#     'pt_2' : ('pt_2',';pt_{2};NEvents',50,0,100),
    
#         'met' : ('met',';met;NEvents',30,0,150), 
#             'iso_1' : ('iso_1',';iso_{1};NEvents',30,0,0.3),
#     'iso_2' : ('iso_2',';iso_{2};NEvents',50,0,1),
#   })

#######################################
# Samples, Selections, and Categories #
#######################################

"""
Xsec: dictionary with key: nick name, value: dictionary of 'xsec', 'era', 'nevents', 'nfiles', 'sample_type'
"""

y_bounds = (100,10e6)
treename = 'ntuple'


input_pattern = [input_path + '/%s*root']
def get_samples(channel, signal_overlay=True, **kwargs):
    sf_lumi = 1.
    
    sf_zjb = kwargs.get('sf_zjb', 1.)
    ##########################################
    samples = {}
    
    #         if sample_type == 'fakes':
    #             if region == "SR":
    #                 samples["FF_Combined"] = ['1', 1,   sample_type     , ["FF_Combined"] ,  0 ]
    #             elif region == "DR_QCD":
    #                 samples["FF_QCD"] = ['1', 1,   sample_type     , ["FF_QCD"] ,  0 ]
    #             elif region == "DR_W":
    #                 samples["FF_W"] = ['1', 1,   sample_type     , ["FF_W"] ,  0 ]
    #             elif region == "DR_ttbar":
    #                 samples["FF_ttbar"] = ['1', 1,   sample_type     , ["FF_ttbar"] ,  0 ]

    # ttbar_list=[]
    # for i in range(0, 11):
    #     for v in ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q']:
    #         ttbar_list.append('{0}_{1}'.format(i, v),)
            
        
    samples.update({
            # 'Single-Top':['1', 1, 'Single-Top', ["TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"], 0],
            'Data': ["jpt_1 > -999", 1, 'Data', [ "Muon_*_withsyst", "Tau", "EGamma", "DoubleMuon", "SingleMuon" ],0],
            #'Data': ["jpt_1 > -999", 1, 'Data', ["TTtoLNu2Q"],0], ## "MuonEG" will be identified by Muon so don't double count
            # "DY-Jets": ["1", 1, 'DY-Jets', DY_list, 0],
            'Top': ['1', 1 ,   'Top'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            "DY-Jets-tt": ["(gen_match_1 == 4 && gen_match_2 ==5)", 1, 'DY-Jets-#tau#tau', ["DYto2L-2Jets",], 0],
            "other": ["1", 1, 'other', ["WtoLNu" , "WZto", "ZZto", "WWto", "GluGluHto2Tau_M-125_TuneCP5_13p6TeV_amcatnloFXFX", "GluGluHToTauTau_M-125_TuneCP5_13p6TeV_powheg", "VBFH"],0],
            # "Wjets" : ["1", 1, 'W-Jets', ["WtoLNu"], 0], 
            "fakes": ["1", 1, 'fakes', ["FF_Combined_withsyst"],0],
                
            })
    if "ggH" in signal_type and "bbH" in signal_type:
        samples.update({

            "%s*%s-%s" %(scale,"ggH",mass) : ["abs(Train_weight )<10", scale, "%s*%s-%s" %(scale,"ggH",mass), ["GluGluHto2Tau_M-%s_2HDM"%(mass)], 0 ]    ,
            "%s*%s-%s" %(scale,"bbH",mass) : ["abs(Train_weight )<10", scale, "%s*%s-%s" %(scale,"bbH",mass), ["bbHto2Tau_M-%s_"%(mass) ,"BBHto2Tau_M-%s_"%(mass)], 0 ]    ,

            # "ggH-60"  : ["1", 1, "ggH-60" , ["GluGluHto2Tau_M-60_2HDM"], 0 ]    ,
            # "bbH-60"  : ["1", 1, "bbH-60" , ["bbHto2Tau_M-60_" ,"BBHto2Tau_M-60_"], 0 ]  ,   

            # "ggH-100"  : ["1", 1, "ggH-100" , ["GluGluHto2Tau_M-100_2HDM"], 0 ]    ,
            # "bbH-100"  : ["1", 1, "bbH-100" , ["bbHto2Tau_M-100_" ,"BBHto2Tau_M-100_"], 0 ]  ,             


            # "ggH-130"  : ["1", 1, "ggH-130" , ["GluGluHto2Tau_M-130_2HDM"], 0 ]    ,
            # "bbH-130"  : ["1", 1, "bbH-130" , ["bbHto2Tau_M-130_" ,"BBHto2Tau_M-130_"], 0 ]  ,   

            # "ggH-160"  : ["1", 1, "ggH-160" , ["GluGluHto2Tau_M-160_2HDM"], 0 ]    ,
            # "bbH-160"  : ["1", 1, "bbH-160" , ["bbHto2Tau_M-160_" ,"BBHto2Tau_M-160_"], 0 ]  ,    
 

            # "ggH-250"  : ["1", 1, "ggH-250" , ["GluGluHto2Tau_M-250_2HDM"], 0 ]    ,
            # "bbH-250"  : ["1", 1, "bbH-250" , ["bbHto2Tau_M-250_" ,"BBHto2Tau_M-250_"], 0 ]  , 


            # "ggH-500"  : ["1", 1, "ggH-500" , ["GluGluHto2Tau_M-500_2HDM"], 0 ]    ,
            # "bbH-500"  : ["1", 1, "bbH-500" , ["bbHto2Tau_M-500_" ,"BBHto2Tau_M-500_"], 0 ]  , 

            # # "ggH-800"  : ["1", 1, "ggH-800" , ["GluGluHto2Tau_M-800_2HDM"], 0 ]    ,
            # # "bbH-800"  : ["1", 1, "bbH-800" , ["bbHto2Tau_M-800_" ,"BBHto2Tau_M-800_"], 0 ]  , 

            # "ggH-1000"  : ["1", 1, "ggH-1000" , ["GluGluHto2Tau_M-1000_2HDM"], 0 ]    ,
            # "bbH-1000"  : ["1", 1, "bbH-1000" , ["bbHto2Tau_M-1000_" ,"BBHto2Tau_M-1000_"], 0 ]  ,        


            # "ggH-1400"  : ["1", 1, "ggH-1400" , ["GluGluHto2Tau_M-1400_2HDM"], 0 ]    ,
            # "bbH-1400"  : ["1", 1, "bbH-1400" , ["bbHto2Tau_M-1400_" ,"BBHto2Tau_M-1400_"], 0 ]  , 

            # # "ggH-1800"  : ["1", 1, "ggH-1800" , ["GluGluHto2Tau_M-1800_2HDM"], 0 ]    ,
            # # "bbH-1800"  : ["1", 1, "bbH-1800" , ["bbHto2Tau_M-1800_" ,"BBHto2Tau_M-1800_"], 0 ]  ,        

            # "ggH-2000"  : ["1", 1, "ggH-2000" , ["GluGluHto2Tau_M-2000_2HDM"], 0 ]    ,
            # "bbH-2000"  : ["1", 1, "bbH-2000" , ["bbHto2Tau_M-2000_" ,"BBHto2Tau_M-2000_"], 0 ]  ,        
      
            # "ggH-2600"  : ["1", 1, "ggH-2600" , ["GluGluHto2Tau_M-2600_2HDM"], 0 ]    ,
            # "bbH-2600"  : ["1", 1, "bbH-2600" , ["bbHto2Tau_M-2600_" ,"BBHto2Tau_M-2600_"], 0 ]  , 

            # # "ggH-3000"  : ["1", 1, "ggH-3000" , ["GluGluHto2Tau_M-3000_2HDM"], 0 ]    ,
            # # "bbH-3000"  : ["1", 1, "bbH-3000" , ["bbHto2Tau_M-3000_" ,"BBHto2Tau_M-3000_"], 0 ]  ,        

            # "ggH-3500"  : ["1", 1, "ggH-3500" , ["GluGluHto2Tau_M-3500_2HDM"], 0 ]    ,
            # "bbH-3500"  : ["1", 1, "bbH-3500" , ["bbHto2Tau_M-3500_" ,"BBHto2Tau_M-3500_"], 0 ]  ,                          
       
        })
    elif "ggH" in signal_type:
        samples.update({
            "%s*%s-%s" %(scale,"ggH",mass) : ["abs(Train_weight )<10", scale, "%s*%s-%s" %(scale,"ggH",mass), ["GluGluHto2Tau_M-%s_2HDM"%(mass)], 0 ]    ,
        })
    elif "bbH" in signal_type:
        samples.update({
            "%s*%s-%s" %(scale,"bbH",mass) : ["abs(Train_weight )<10", scale, "%s*%s-%s" %(scale,"bbH",mass), ["bbHto2Tau_M-%s_"%(mass), "BBHto2Tau_M-%s_"%(mass)], 0 ]    ,
        })
    # if channel_name != 'em':
    #     samples.update({
    #         'Top': ['1', 1 ,   'Top'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
    #     })


    else:
        samples.update({
            # 'Top-true': ['((gen_match_1 ==1 && gen_match_2 ==2) ||(gen_match_1 ==3 && gen_match_2 ==4) || (gen_match_1 ==1 && gen_match_2 ==4) || (gen_match_1 ==3 && gen_match_2 ==2))', 1 ,   'Top-true'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            # 'Top-fake': ['(!((gen_match_1 ==1 && gen_match_2 ==2) ||(gen_match_1 ==3 && gen_match_2 ==4) || (gen_match_1 ==1 && gen_match_2 ==4) || (gen_match_1 ==3 && gen_match_2 ==2)))', 1 ,   'Top-fake'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            "Top-genuine-tau": ['(gen_match_1 ==1 && gen_match_2 ==2)', 1 ,   "Top-genuine-#tau"     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            "Top-fake-tau": ['!(gen_match_1 ==1 && gen_match_2 ==2)', 1 ,   "Top-fake-#tau"     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
        })
    print(samples)


    if args.use_LO_DY:
        
        if channel_name == 'em':


            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
                "DY-Jets-tautau": ["! ( (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2) )", 1, "DY-Jets-#tau#tau", ["DYto2L-2Jets",], 0]
            })



#####       old  SF
            # if era == '2022EE':
            #     samples.update({
            #         "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.82 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            #     })
            #     samples.update({
            #         "DY-Jets-tautau": ["! ( (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2) )", 0.82, "DY-Jets-#tau#tau", ["DYto2L-2Jets",], 0],
            #         # "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.82 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
            #     })
                

            # elif era == '2022postEE':
            #     samples.update({
            #         "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.783 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            #     })   
            #     samples.update({
            #         "DY-Jets-tautau": ["! ( (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2) )", 0.783, "DY-Jets-#tau#tau", ["DYto2L-2Jets",], 0],
            #         # "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.783 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
            #     })

            # elif era == '2023':
            #     samples.update({
            #         "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.903 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            #     })                     
            #     samples.update({
            #         "DY-Jets-tautau": ["! ( (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2) )", 0.903, "DY-Jets-#tau#tau", ["DYto2L-2Jets",], 0],
            #         # "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.903 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
            #     })   

            # elif era == '2023BPix':
            #     samples.update({
            #         "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.897 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            #     })
            #     samples.update({
            #         "DY-Jets-tautau": [" ! ( (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2) )", 0.897, "DY-Jets-#tau#tau", ["DYto2L-2Jets",], 0],
            #         # "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.897 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
            #     })  


        elif channel_name =='et':
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 3 && gen_match_2 ==5)", 1, 'DY-Jets-#tau#tau', ["DYto2L-2Jets",], 0],        
                # "DY-Jets-fakes": ["(gen_match_1 == 3 &&  gen_match_2 !=5)", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],
            })
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
        # elif channel_name =='mt':
        #     samples.update({
        #         "DY-Jets-tt": ["(gen_match_1 == 4 && gen_match_2 ==5)", 1, 'DY-Jets-#tau#tau', ["DYto2L-2Jets",], 0],    
        #         # "DY-Jets-fakes": ["(gen_match_1 == 4 &&  gen_match_2 !=5)", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],    
        #     })
        #     samples.update({
        #         "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
        #     })                
        elif channel_name =='tt':
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 5)", 1, 'DY-Jets-#tau#tau', ["DYto2L-2Jets",], 0],  #2025/06/03 new tt fakes                
                #"DY-Jets-tt": ["(gen_match_1 == 5 && gen_match_2 ==5)", 1, 'DY-Jets-#tau#tau', ["DYto2L-2Jets",], 0],  # old
                #"DY-Jets-fakes": ["(gen_match_1 == 5 &&  gen_match_2 !=5) || (gen_match_1 != 5 &&  gen_match_2 ==5) ", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],   
            })
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
        elif channel_name =='mm':
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 5 && gen_match_2 ==5)", 1, 'DY-Jets-#tau#tau', ["DYto2L-2Jets",], 0],     
                "DY-Jets-fakes": ["(gen_match_1 == 5 &&  gen_match_2 !=5) || (gen_match_1 != 5 &&  gen_match_2 ==5) ", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],   
            })
        
        # ///   1 = prompt electron,
        # ///   2 = prompt muon,
        # ///   3 = tau->e decay,
        # ///   4 = tau->mu decay,
        # ///   5 = hadronic tau decay,
        # ///   0 = unknown or unmatched
    else:
        samples.update({
            "DY-Jets-tautau": ["1", 1, 'DY-Jets-tautau', ["DYto2Tau",], 0],
            "DY-Jets-ll": ["1", 1, 'DY-Jets-ll', ["DYto2Mu_MLL", "DYto2E_MLL"]  , 0],
        })
    if region == "SR":
        print("1")
    #     if channel_name != 'em' :
        
    #         samples.update({"fakes": ["1", 1, 'fakes', ["FF_Combined_withsyst"],0],})
        
    #     elif channel_name == 'em' : 

    #         samples.update({"fakes": ["1", 1, 'fakes', ["FF_Combined"],0],})


    elif region == "DR_QCD":
        samples.update({"fakes": ["1", 1, 'fakes', ["FF_QCD"],0],})
    elif region == "DR_W":
        samples.update({"fakes": ["1", 1, 'fakes', ["FF_W"],0],})
    elif region == "DR_ttbar":
        samples.update({"fakes": ["1", 1, 'fakes', ["FF_ttbar"],0],})
    
    return samples

Htautau = Htautau_selections()
if channel_name == "mt":
    lepton_selection = combinecut( Htautau.mt_triggers_selections[era],Htautau.muon_selections,Htautau.lepton_veto,Htautau.mt_tau_selections[era])
    anti_selection = combinecut( Htautau.mt_triggers_selections[era],Htautau.muon_selections,Htautau.lepton_veto,"(id_tau_vsMu_Tight_2 > 0 && id_tau_vsJet_Medium_2 < 1 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) ")
elif channel_name == "et":
    lepton_selection = combinecut( Htautau.et_triggers_selections[era],Htautau.electron_selections,Htautau.lepton_veto,Htautau.et_tau_selections[era])
    anti_selection = combinecut( Htautau.et_triggers_selections[era],Htautau.electron_selections,Htautau.lepton_veto, "(id_tau_vsMu_VLoose_2 > 0  &&  id_tau_vsEle_Tight_2 > 0 && id_tau_vsJet_Medium_2  <1  && pt_2 > 30 )")
elif channel_name == "tt":
    lepton_selection = combinecut( Htautau.tt_triggers_selections[era],Htautau.lepton_veto, Htautau.tt_leadingtau_selections, Htautau.tt_secondtau_selections)
    anti_selection =  combinecut( Htautau.tt_triggers_selections[era],Htautau.lepton_veto, Htautau.tt_secondtau_selections, "(id_tau_vsJet_Medium_1 <1 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )")
elif channel_name == "em":

    if region == "SR":
         lepton_selection = combinecut(Htautau.em_electron_selection, Htautau.em_muon_selection, Htautau.lepton_veto, Htautau.em_triggers_selections[era])
    if region == "DR":
         lepton_selection = combinecut(Htautau.em_electron_selection, Htautau.em_muon_selection_DR, Htautau.lepton_veto, Htautau.em_triggers_selections[era])

elif channel_name == "mm":
    lepton_selection = "pt_1 > 25 && iso_1 < 0.15 && iso_2 < 0.15 && abs(dxy_1) < 0.045 && abs(dxy_2)  < 0.045 && abs(dz_1) < 0.2 && abs(dz_2) < 0.2 &&  met > 0 && nmuons==2 && (q_1 * q_2 ) < 0 && mass_ll > 50 && HLT_IsoMu24 > 0  "
the_samples_dict = get_samples(
    channel='Htt',
    
    signal_overlay=True,
    
    sf_zjb = 1.0,
)

print(the_samples_dict)
regions = {
# 'nob': '1> 0 '
# 'all' : '1>0',

# 'nob' : Htautau.nob,


'nob' : combinecut( Htautau.nob),
# 'nob_mt_morethan50' : combinecut( Htautau.nob, "mt_1 > 50" ),

# 'nob1' : combinecut( Htautau.nob, "pt_tt > 0" , "pt_tt < 50"),
# 'nob2' : combinecut( Htautau.nob, "pt_tt > 50" , "pt_tt < 100"),
# 'nob3' : combinecut( Htautau.nob, "pt_tt > 100" , "pt_tt < 200"),
# 'nob4' : combinecut( Htautau.nob, "pt_tt > 200" ),


# 'nob1_mt_less50' : combinecut( Htautau.nob, "pt_tt > 0" , "pt_tt < 50", "mt_1 < 50"),
# 'nob2_mt_less50' : combinecut( Htautau.nob, "pt_tt > 50" , "pt_tt < 100", "mt_1 < 50"),
# 'nob3_mt_less50' : combinecut( Htautau.nob, "pt_tt > 100" , "pt_tt < 200", "mt_1 < 50"),
# 'nob4_mt_less50' : combinecut( Htautau.nob, "pt_tt > 200", "mt_1 < 50" ),


# 'nob1_mt_morethan50' : combinecut( Htautau.nob, "pt_tt > 0" , "pt_tt < 50" , "mt_1 > 50"),
# 'nob2_mt_morethan50' : combinecut( Htautau.nob, "pt_tt > 50" , "pt_tt < 100", "mt_1 > 50"),
# 'nob3_mt_morethan50' : combinecut( Htautau.nob, "pt_tt > 100" , "pt_tt < 200", "mt_1 > 50"),
# 'nob4_mt_morethan50' : combinecut( Htautau.nob, "pt_tt > 200" , "mt_1 > 50" ),


# "nob" : combinecut( Htautau.nob, Htautau.ttbar_true_only),
# "nob_mt_2_50" : combinecut( Htautau.nob, Htautau.ttbar_true_only, "mt_2 < 50"),
# "btag" : Htautau.btag,

'btag' : combinecut( Htautau.btag),
# 'btag_mt_morethan50' : combinecut( Htautau.btag, "mt_1 > 50" ),


# # "nob_tight_mT" : combinecut(Htautau.nob, Htautau.tight_mT,lepton_selection, Htautau.W_true_only, Htautau.opposite_sign,"mt_1 < 40"),
# "nob_AntiID" : combinecut( Htautau.nob,   anti_selection, Htautau.W_true_only, Htautau.ttbar_true_only,Htautau.opposite_sign, "mt_1 < 70") if (channel_name != 'tt' and channel_name != 'em') else combinecut( Htautau.nob,   anti_selection,  Htautau.W_true_only, Htautau.opposite_sign),
# "btag_AntiID" : combinecut( Htautau.btag,   anti_selection,  Htautau.W_true_only,Htautau.ttbar_true_only, Htautau.opposite_sign, "mt_1 < 70") if (channel_name != 'tt' and channel_name != 'em') else combinecut( Htautau.btag,   anti_selection,  Htautau.W_true_only, Htautau.opposite_sign),
}

if PNN:
    regions["nob_PNN0p8"] = combinecut( "PNN_100 > 0.8", Htautau.nob)
    regions["btag_PNN0p8"] = combinecut("PNN_100 > 0.8", Htautau.btag)

selections = [ "mt_1 > 0  "] #, Htautau.W_true_only????


# if (channel_name == 'tt') :
#      for i in regions:
#         print(regions[i])
#         print("hi  tt channel====================== ")
#         regions[i] = combinecut(regions[i],  "(  (  ( gen_match_2 != 6 && is_ttbar > 0 ) || (is_ttbar < 1)  ) && (  ( gen_match_2 != 6 && is_wjets > 0 ) || (is_wjets < 1)  )    )" ) #


if (channel_name == 'mt') or (channel_name =='et'):
     for i in regions:
        print(regions[i])
        print("hi ====================== ")
        regions[i] = combinecut(regions[i],  "mt_1 < 50" ) #
if channel_name == 'em':
     for i in regions:
         print(regions[i])
         print("combinecut(regions[i],   (pzetamissvis > -35)  ):" ,regions[i] , " (pzetamissvis > -35 ) " )
         #regions[i] = combinecut(regions[i],  " (pzetamissvis > -3000 ) " ) #
         regions[i] = combinecut(regions[i],  "pzetamissvis > -35" )

# if channel_name == 'et' and era =="2022postEE":
#     for i in regions:
#         regions[i] = combinecut(regions[i], '( ! (phi_2>1.8 && phi_2< 2.7 && eta_2 > 1.5  && eta_2<2.2)  )')
# if channel_name == 'et':
    
# ## apply to all reigions    
# for i in regions:
    # regions[i] = combinecut(regions[i], '&& abs(jeta_1) > 2.5 &&abs(jeta_1) < 3 && is_data==0) ) ', '&& abs(jeta_2) > 2.5 &&abs(jeta_2) < 3 && is_data==0) ) ')
    # regions[i] = combinecut(regions[i], '&& abs(jeta_1) > 2.5 &&abs(jeta_1) < 3 ) ) ', '&& abs(jeta_2) > 2.5 &&abs(jeta_2) < 3 ) ) ')




if region == "SR":
    if channel_name != 'em':
        selections += [ Htautau.opposite_sign , Htautau.W_true_only,  lepton_selection, Htautau.true_MC_only ]
    else:
        selections += [ Htautau.opposite_sign,  lepton_selection ]
        # selections += [ Htautau.same_sign,  lepton_selection ]


        
elif region == "DR_QCD":
    regions["DR_QCD"] = combinecut(Htautau.DR_QCD_tt, lepton_selection)
    regions["AntiDR_QCD"] = combinecut(Htautau.DR_QCD_tt, anti_selection)
    regions["DR_QCD_btag"] = combinecut(Htautau.btag, Htautau.DR_QCD_tt, lepton_selection)
elif region == "DR_W":
    regions["DR_W"] = combinecut(Htautau.DR_W, lepton_selection, Htautau.W_true_only)
    regions["AntiDR_W"] = combinecut(Htautau.DR_W, anti_selection, Htautau.W_true_only)
    regions['nob'] = combinecut(regions['nob'], Htautau.W_true_only ) 
    regions['btag'] = combinecut(regions['btag'], Htautau.W_true_only ) 
    #regions["DR_W_btag"] = combinecut(Htautau.btag, Htautau.DR_W_tt ,anti_selection)
elif region == "DR_ttbar":
    regions["DR_ttbar"] = combinecut(Htautau.DR_ttbar, lepton_selection,Htautau.ttbar_true_only)
    regions["AntiDR_ttbar"] = combinecut(Htautau.DR_ttbar, anti_selection,Htautau.ttbar_true_only)
    #regions["DR_ttbar_btag"] = combinecut(Htautau.btag, Htautau.DR_ttbar_tt ,anti_selection) 
elif region == "AR":
    selections += [ Htautau.opposite_sign , Htautau.W_true_only, anti_selection]
else:
    print("wrong region provided!! region supported: SR, DR_QCD,DR_ttbar, DR_W ")
    sys.exit(0)
# print( "printing cuts applied:   ",regions['nob_PNN0p8'] , "for channels: ", channel_name )



the_category_dict = {
    'Htautau': [regions, selections, plot_vars],
}

print("regions",regions)
print("selections",selections)
# yields_f_tmp = open('sample_database/datayields.yaml', 'r')
# yields = yaml.safe_load(yields_f_tmp)
# bins = yields['bins']







# Blinding the Signal Region
def additional_input_hook(wrps):

    @varial.history.track_history


    #

    def add_syst(w, all_wrps):
        print(">>> Processing:", w.name, "| Sample:", w.sample,"| bin:", w.in_file_path )
        
        if '__' in w.name:
            return w  # skip syst variation histograms themselves

        base_name = w.name
        syst_histos = []

        # collect all variation histos for this base
        for other in all_wrps:
            if other.name.startswith(base_name + '__') and other.sample == w.sample:
                print("[Find] syst variation for {}: {} (sample={})".format(base_name, other.name, other.sample))
                syst_histos.append(other.histo)

        print("[DEBUG] syst_histos for {}: {}".format(base_name, [h.GetName() for h in syst_histos]))

        if syst_histos:
            h_nom = w.histo
            h_sys = h_nom.Clone(h_nom.GetName() + "__sys_combined")
            h_sys.Reset("ICES")

            for i in range(h_sys.GetNbinsX()):
                nom = h_nom.GetBinContent(i)
                stat_err =   h_nom.GetBinError(i)  or 1e-10
               

                if w.sample not in ['Data', 'fakes']:
                    print("bin {}:".format(i))
                    print("self.sample: {}".format(w.sample))
                    print("config stat err: {}".format(stat_err))

                    errs = [(h.GetBinContent(i) - nom)**2 for h in syst_histos]
                    rms = (sum(errs) if errs else 1e-10) ** 0.5
                    print("config syst err: {}".format(rms))
                else:
                    print("bin {}:".format(i))
                    print("self.sample: {}".format(w.sample))
                    print("config stat err: {}".format(stat_err))
                    rms =  1e-10
                    print("config syst err: {}".format(rms))
                
                stat_err_new =   ( stat_err**2 + rms**2 ) **.5
                h_nom.SetBinError(i,stat_err_new)

                print("after adjust:")
                print("bin {}:".format(i))
                print("self.sample: {}".format(w.sample))
                print("config stat err: {}".format(stat_err))
                print("config syst err: {}".format(rms))
                print("config tot err: {}".format(stat_err_new))

                h_sys.SetBinContent(i, nom)
                h_sys.SetBinError(i, rms)

            w.histo_sys_err = h_sys
            print("[Set] histo_sys_err set for {} using {} variations".format(w.name, len(syst_histos)))

        # Now accumulate other backgrounds into DY-Jets-tt AFTER all histo_sys_err are built
        # if w.sample == 'DY-Jets-tt':
        #     # define what samples to accumulate from
        #     accepted_samples = ['DY-Jets-ll', 'fakes', 'other', 'Top']

        #     other_bkgs = []
        #     for other in all_wrps:
        #         if '__' in other.name:
        #             continue
        #         if other.sample not in accepted_samples:
        #             continue
        #         if not hasattr(other, "histo_sys_err") or other.histo_sys_err is None:
        #             continue
        #         if other.name != w.name:
        #             continue
        #         other_bkgs.append(other)

        #     if other_bkgs:
        #         print("[INFO] Accumulating syst error from the following background samples into DY-Jets-tt:")
        #         for o in other_bkgs:
        #             print(" - {:<20} | histo_sys_err: {}".format(o.sample, o.histo_sys_err.GetName()))

        #         for i in range(w.histo_sys_err.GetNbinsX()):
        #             err0 = w.histo_sys_err.GetBinError(i)
        #             add_err2 = sum(h.histo_sys_err.GetBinError(i)**2 for h in other_bkgs)
        #             new_err = (err0**2 + add_err2) ** 0.5
        #             w.histo_sys_err.SetBinError(i, 2*new_err)

        #         print("[INFO] Added {} background samples' syst errors into DY-Jets-#tau#tau.".format(len(other_bkgs)))

        return w

    # Logic
    # wrapper
    wrps = list(wrps)


    print("\n===== PHASE 1: Processing non-DY samples =====")
    non_dytt_wrps = [w for w in wrps if w.sample != '111']
    for w in non_dytt_wrps:
        w = add_syst(w, wrps)
        #check 
        print("[Post-Process] Sample {}: histo_sys_err={}".format(
            w.sample, 
            "Set" if hasattr(w, 'histo_sys_err') else "Not Set"
        ))

    print("\n===== PHASE 2: Processing DY-Jets-tt samples =====")
    # dytt_wrps = [w for w in wrps if w.sample == 'DY-Jets-tt']
    # for w in dytt_wrps:
    #     w = add_syst(w, wrps)




    def PPrint(w):
        print("w_items after syst_add:")
        for k, v in vars(w).items():
            print("{}: {}".format(k, v))
        return w 
        
    # wrps = (PPrint(w) for w in wrps) 


    def blind_in_HmmWin(w):
        if w.legend == 'Data': # and w.in_file_path.startswith('Hmm_win'):
            if "PNN_%s_rebinned"%args.mass in w.name:
                print('BLINDING Data in %s' % w.in_file_path)
                for i in xrange(w.histo.GetNbinsX() -int( w.histo.GetNbinsX() /2), w.histo.GetNbinsX() + 5001):
                    w.histo.SetBinContent(i, 0.)
                    w.histo.SetBinError(i, 0.)
            if "mt_tot_rebinned" in w.name:
                if args.mass >= 200:
                    for i in xrange(7, w.histo.GetNbinsX() + 15001):
                        w.histo.SetBinContent(i, 0.)
                        w.histo.SetBinError(i, 0.)
                else:
                    for i in xrange(3, w.histo.GetNbinsX() + 15001):
                        w.histo.SetBinContent(i, 0.)
                        w.histo.SetBinError(i, 0.)
        return w
    def getyields(w):
        region = ["nob_loose","nob_tight","btag_tight","btag_loose"]
        if "mt_tot" in w.name and ("ALL" not in w.in_file_path):
            for r in region:
                yields_l = []
                if r in w.in_file_path:
                    os.system('rm ' + r+'datayields.yaml')
                    w_copy = w.histo.Rebin(len(bins[r])-1,  'w_copy'+r, array.array('d', bins[r]))
                    for i in xrange(1,w_copy.GetNbinsX() + 1):
                        # print('    'combinecut(i, w_copy.GetBinContent(i), w_copy.GetXaxis().GetBinLowEdge(i), w.in_file_path))
                        yields_l.append(w_copy.GetBinContent(i))
                    a = {}
                    a[r] = yields_l
                    os.system('echo ' + r + ': ' + str(a[r]) + ' >> ' + r+'datayields.yaml')                      
                    # with open(r+'datayields.yaml' , 'w') as file:
                    #     yaml.safe_dump(yields, file) 
        return w
    def rebin(w):
        # PNN_100 = [0, 0.1,0.2,0.3, 0.4,0.5, 0.525,0.55,0.575, 0.6, 0.625,0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8, 
        # 0.81, 0.82, 0.83,0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1] ## complete to 1        # Array of decimal values from 0.81 to 0.85 with 0.01 increments, representing a sequence approaching 1.0
        pt_2_rebin = [30,35,40,45,50,55,60,70,80,100,120,140,200]
        met_rebin = [0,5,10, 15, 20, 25, 30,35,40,45,50,60,70,80,100,120,150,200]
        # btag_PNN_100 = [0.0,0.37866893344667235,0.6017550877543877,0.7466623331166559,0.771513575678784,0.7967898394919746,0.8243662183109155,0.8341167058352917,0.8485174258712935,0.8646682334116705,0.8745437271863593,0.8809940497024851,0.8866193309665483,0.8942447122356117,0.9010200510025501,0.9111955597779889,0.9173458672933646,0.9289714485724286,0.9379968998449922,0.9522726136306815,0.9632981649082454,0.972073603680184,0.9776488824441222,1.01,]
        # nob1_PNN_100 = [0.0,0.8158657932896645,0.8434671733586679,0.8588179408970449,0.8702935146757338,0.8789689484474223,0.8863193159657983,0.8924946247312365,0.8973948697434871,0.9025451272563628,0.9070953547677384,0.9111455572778638,0.9151957597879894,0.9183209160458022,0.9217460873043652,0.9252962648132407,0.9283964198209911,0.9315965798289915,0.9347967398369919,0.9378718935946797,0.9407970398519926,0.9441722086104305,0.947922396119806,0.9526476323816191,0.9576478823941197,1.01,]
        # nob2_PNN_100 = [0.0,0.7125606280314015,0.8221911095554778,0.8515425771288564,0.872193609680484,0.8852192609630481,0.8928696434821741,0.8968698434921746,0.903445172258613,0.9092454622731136,0.9132956647832392,0.9166458322916146,0.919845992299615,0.9230461523076153,0.9256962848142407,0.9287214360718036,0.9311965598279914,0.9343717185859293,0.9363968198409921,0.9391719585979299,0.9418970948547427,0.9444722236111806,0.9473223661183059,0.9504475223761188,0.9548977448872443,1.01,]
        # nob3_PNN_100 = [0.0,0.7776638831941597,0.8663183159157958,0.8932946647332367,0.9099204960248013,0.9230461523076153,0.928296414820741,0.932671633581679,0.9363718185909295,0.9403470173508676,0.9426971348567429,0.9448222411120556,0.9470723536176808,0.9490224511225561,0.9513225661283065,0.9530226511325566,0.9551477573878694,0.9569478473923696,0.9593479673983699,0.9606730336516826,0.9628981449072453,0.9641982099104955,0.9668233411670584,0.9699734986749338,0.972273613680684,1.01,]
        # nob4_PNN_100 = [0.0,0.11868093404670234,0.9252212610630531,0.9382469123456173,0.9482474123706185,0.9524226211310566,0.9565478273913696,0.9587729386469324,0.9621481074053703,0.9649732486624332,0.967598379918996,0.9693734686734337,0.9707985399269964,0.9723736186809341,0.9741237061853093,0.975298764938247,0.975948797439872,0.9768238411920596,0.9780739036951848,0.9792739636981849,0.98012400620031,0.9810740537026852,0.9825491274563728,0.984199209960498,0.9862243112155608,1.01,]
        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(len(mt_tot_b)-1, 'rebinned_mt_tot', array.array('d', mt_tot_b))
        # if "mt_" in w.name or "mT" in w.name:
        #         w.histo = w.histo.Rebin(len(mt)-1, 'rebinned_mt', array.array('d', mt))
        if "met_rebinned" in w.name:
            w.histo = w.histo.Rebin(len(met_rebin)-1, 'rebinned_met{0}'.format(w.name), array.array('d', met_rebin))
        if "pt_2_rebinned"  in w.name:
            w.histo = w.histo.Rebin(len(pt_2_rebin)-1, 'rebinned_{0}'.format(w.name), array.array('d', pt_2_rebin))  
        # if "pt_2"  in w.name or "pt_1" in w.name:
        #     w.histo = w.histo.Rebin(len(pt)-1, 'rebinned_{0}'.format(w.name), array.array('d', pt))            
        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(2)
        # if "m_fastmtt" in w.name and "zoom" not in w.name: 
        #     w.histo = w.histo.Rebin(len(m_fastmtt)-1, 'rebinned_m_fastmtt', array.array('d', m_fastmtt))





        if "mt_tot_rebinned_nob" in w.name:
            w.histo = w.histo.Rebin(len(nob_tight_mT)-1, 'rebinned_mt_tot', array.array('d', nob_tight_mT))
        if "mt_tot_rebinned_btag" in w.name:
            w.histo = w.histo.Rebin(len(btag_tight_mT)-1, 'rebinned_mt_tot', array.array('d', btag_tight_mT))
        # if "mt_tot_rebinned_nob_loose_mT" in w.name:
        #     w.histo = w.histo.Rebin(len(nob_loose_mT)-1, 'rebinned_mt_tot', array.array('d', nob_loose_mT))
        

        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(len(nob_tight_mT)-1, 'mt_tot', array.array('d', nob_tight_mT))    
        
        # print("printing w name:  ===================      ", w.name)
        # print("printing w title:  ===================      ", w.title)
        if "PNN_500_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_500) -1, 'rebinned_mt_tot', array.array('d', PNN_500))   
            # h_PNN_500 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_500))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        if "PNN_1000_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_1000) -1, 'rebinned_mt_tot', array.array('d', PNN_1000))   
            # h_PNN_1000 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_1000))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        if "PNN_%s_rebinned"%args.mass in w.name:
            rebinned_h = w.histo.Clone()
            rebinned_h = rebinned_h.Rebin(len(PNN_100) -1, 'rebinned_PNN_%s'%args.mass, array.array('d', PNN_100)) 
            original_bin = []
            for i in range(rebinned_h.GetNbinsX() + 2):
                original_bin.append((float(i)/(rebinned_h.GetNbinsX() +1)))
            # h_PNN_100 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(len(PNN_100) -1, 'rebinned_PNN_100_original',array.array('d', original_bin))
            for i in xrange(w.histo.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        # if "PNN_200_rebinned" in w.name:
        #     rebinned_h = w.histo.Rebin(len(PNN_200) -1, 'rebinned_mt_tot', array.array('d', PNN_200))   
        #     # h_PNN_200 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
        #     w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_200))   
        #     for i in xrange(rebinned_h.GetNbinsX() + 1):
        #         w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
        #         w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        return w

            
    
    def scale_by_binwidth(w):
        for i in xrange(w.histo.GetNbinsX() + 1):
            w.histo.SetBinContent(i, w.histo.GetBinContent(i)/w.histo.GetBinWidth(i) )
            w.histo.SetBinError(i, w.histo.GetBinError(i)/w.histo.GetBinWidth(i))
        # w.histo.GetYaxis().SetTitle("")
        return w
    def setylimit(w):
        for i in xrange(w.histo.GetNbinsX() + 1):
            # w.histo.GetYaxis().SetRangeUser(0.1,10e5 )
            w.histo.SetMinimum(10)
        return w
            # print('+++++++++++++++++ ' , yields , '+++++++++++++++++ ')
    # wrps = (getyields(w) for w in wrps)
    # if not use_all_signal:
    wrps = (rebin(w) for w in wrps)
    
    wrps = (blind_in_HmmWin(w) for w in wrps)
    # wrps = (setylimit(w) for w in wrps)
    # wrps = (scale_by_binwidth(w) for w in wrps)
    # for w in wrps:
    #     w.y_bounds = (1, 10e5)
    return wrps



