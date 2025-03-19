# from samples_HHbbmm import *
import varial
import sys
import ROOT as R
import array
import yaml
from Htautau import *
import argparse

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
    'DY-Jets',     'fakes',     'Top',     'other',     ]
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
    'fakes' : 617,
    'DY-Jets' : 864,
    'DY-Jets-ll'  :  814,
    'DY-Jets-tt'  :  864,
    "DY-Jets-fakes": 596,
    'Top'  :  400,
    # 'wjets'  :  632,
    'Single H': 838,
    'other' : 920, 
    "%s*bbH-%s" %(scale,mass) : 416,
    "%s*ggH-%s" %(scale,mass) : 632,
    'Top: genuine tau': 401,
    'Top: fake tau': 501,
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
    'QCD_fakes' : 901,
    'DY-Jets' : 864,
    'DY-Jets-ll'  :  814,
    'DY-Jets-tt'  :  864,
    'DY-Jets-tt-em'  :  865,
    "DY-Jets-fakes": 596,
    'DY-Jets-tt-other': 838,
    'Top'  :  400,
    'wjets'  :  804,
    'Single H': 838,
    'other' : 920, 
    "%s*bbH-%s" %(scale,mass) : 416,
    "%s*ggH-%s" %(scale,mass) : 632,
    'Top-genuine_tau': 401,
    'Top-fake_tau': 617,
    # 'diboson'  :  596,
    # 'ggh_hbb'  :  596,
    # 'ggh_htautau'  :  838,
    # 'singletop'  :  920,
    # 'ttbarFake'  :  596,
    # 'vbf_htautau'  :  814,
    # 'rem_hbb':  615,

}




varial.settings.max_num_processes = 80
varial.settings.rootfile_postfixes += [ '.png', '.pdf'] #'.pdf'
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

weight_dict["mt"]["2022postEE"] = 'Xsec   * {0} * puweight * genWeight/genEventSumW *  btag_weight  * FF_weight * id_wgt_tau_vsJet_Medium_2 * iso_wgt_mu_1  *trg_wgt_ditau_crosstau_2 *  id_wgt_tau_vsMu_Tight_2 * id_wgt_mu_1 *ZPtMassReweightWeight'.format(lumi) ##  
weight_dict["mt"]["2022EE"] =weight_dict["mt"]["2023"] =weight_dict["mt"]["2023BPix"]= weight_dict["mt"]["2022postEE"]
     

weight_dict["et"]["2022postEE"] =  'Xsec * {0}* puweight * genWeight/genEventSumW     *  btag_weight * FF_weight * id_wgt_tau_vsJet_Medium_2  * id_wgt_ele_wpTight * trg_wgt_ditau_crosstau_2  * trg_wgt_single_ele30 * id_wgt_tau_vsEle_Tight_2 *ZPtMassReweightWeight ' .format(lumi) #  
weight_dict["et"]["2022EE"] =weight_dict["et"]["2023"] =weight_dict["et"]["2023BPix"]= weight_dict["et"]["2022postEE"]

weight_dict["tt"] = {}
weight_dict["tt"]["2022postEE"]  =   'Xsec *  {0}* puweight * genWeight/genEventSumW *    btag_weight   *id_wgt_tau_vsJet_Medium_2 * id_wgt_tau_vsJet_Medium_1 *  FF_weight * trg_wgt_ditau_crosstau_1 *trg_wgt_ditau_crosstau_2 *ZPtMassReweightWeight '.format(lumi) # 
weight_dict["tt"]["2022EE"] =weight_dict["tt"]["2023"] =weight_dict["tt"]["2023BPix"]= weight_dict["tt"]["2022postEE"]

weight_dict["em"] = {"2022postEE": '(Xsec * genWeight *  {0} / genEventSumW) * id_wgt_ele_wpTight * id_wgt_mu_2 * btag_weight *  FF_weight * puweight * (trg_wgt_single_mu24 )'   .format(lumi)}   #add FF_weight 2025/2/12
weight_dict["em"]["2022EE"] =weight_dict["em"]["2023"] =weight_dict["em"]["2023BPix"]= weight_dict["em"]["2022postEE"]

weight_dict["mm"] = {"2022postEE": '(Xsec * genWeight *  {0} / genEventSumW) * puweight *  id_wgt_mu_1*iso_wgt_mu_1*id_wgt_mu_2*iso_wgt_mu_2* trg_wgt_single_mu24 '.format(lumi)} # * ZPtMassReweightWeight
weight_dict["mm"]["2022EE"] =weight_dict["mm"]["2023"] =weight_dict["mm"]["2023BPix"]= weight_dict["mm"]["2022postEE"]

weight = weight_dict[channel_name][era]


# weight = "Train_weight"
plot_vars = {}

mt_tot_b = [30, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500]
nob_tight_mT = [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,2100.0,5000.0]
m_fastmtt = [0,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,240,260,300]
met = [0,10,20,30,40,50,60,70,80,90,120,140,200,400]
pt = [30,40,50,60,70,80,90,100,120,140,200,350,500, 700, 1000]


plot_vars.update({    
    'eta_1' : ('eta_1',';eta_{1};NEvents',30,-2.4,2.4),
    'eta_2' : ('eta_2',';eta_{2};NEvents',30,-2.4,2.4),
    # 'eta_1_morebins' : ('eta_1',';eta_{1};NEvents',50,-2.5,2.5),
    # 'eta_2_morebins' : ('eta_2',';eta_{2};NEvents',50,-2.5,2.5),
    # 'jeta_1' : ('jeta_1',';jeta_{1};NEvents',60,-6.3,6.3),
    # 'jeta_2' : ('jeta_2',';jeta_{2};NEvents',60,-6.3,6.3),
    # 'mTdileptonMET' : ('mTdileptonMET',';mTdileptonMET;NEvents',20,0,200),
    # 'mass_tt'       :    ('mass_tt', '; mass_tt;NEvents', 30, 0, 300),
    # 'pt_tt'       :    ('pt_tt', '; pt_tt;NEvents', 30, 0, 300),
    'm_vis'       :    ('m_vis', '; m^{vis};NEvents', 40, 0, 200),
    'met' : ('met',';met;NEvents',30,0,150), 
    'metSumEt' : ('metSumEt',';metSumEt;NEvents',40,0,400),
    'metphi' : ('metphi',';metphi;NEvents',80,-4,4),
    'mt_tot': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents', 50, 0, 500),
    'mt_1' : ('mt_1',';mt_{1};NEvents',50,0,200),
    'mt_2' : ('mt_2',';mt_{2};NEvents',50,0,200),
    'phi_1' : ('phi_1',';phi_{1};NEvents',20,-3.14,3.14),
    'phi_2' : ('phi_2',';phi_{2};NEvents',20,-3.14,3.14),
    'pt_1' : ('pt_1',';pt_{1};NEvents',50,0,100),
    'pt_2' : ('pt_2',';pt_{2};NEvents',50,0,100),
    'pt_tt'   :    ('pt_tt', ';pt_{tt} ;NEvents', 40, 0, 200),
    'pt_vis'   :    ('pt_vis', ';pt_{vis} ;NEvents', 40, 0, 200),
    'pzetamissvis' : ('pzetamissvis',';D_{#zeta};NEvents',25,-150,100),    
    'deltaR_ditaupair' :  ('deltaR_ditaupair', ';#deltaR [GeV];NEvents',25 , 0, 5),
    
    'dphi_12' : ('dphi_12', ';#dphi_12;NEvents',30 ,0, 3.1415),
    'dphi_H1' : ('dphi_H1', ';#dphi_H1;NEvents',30 ,0, 3.1415),
    'dphi_H2' : ('dphi_H2', ';#dphi_H2;NEvents',30 ,0, 3.1415),
    'kT' : ('kT',   ';kT;NEvents',     40,0,400       ),
    'antikT' : ('antikT',   ';antikT;NEvents',     40,0,0.2       ),
    'pt1_LT_to_ptH' : ('pt1_LT_to_ptH',   ';pt1_LT_to_ptH;NEvents',  40, 0, 3         ),
    'pt2_LT_to_ptH' : ('pt2_LT_to_ptH',   ';pt2_LT_to_ptH;NEvents',  40, 0, 3          ),

#     # 'C_W'   : ('C_W', ';C_W ;NEvents', 20, -5, 6),
#     # 'C_QCD'   : ('C_QCD', ';C_QCD ;NEvents', 20, -2, 2),
#     # 'deta_12' : ('deta_12', ';#deta_12;NEvents',30 ,-3.5, 3.5),
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
    'eta_1' : ('eta_1',';eta_{1};NEvents',30,-3,3),
    'eta_2' : ('eta_2',';eta_{2};NEvents',30,-3,3),
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
    plot_vars.update({
        'm_fastmtt'       :    ('m_fastmtt', '; m^{#tau#tau};NEvents',  27, 30, 300),
        
        'eta_fastmtt' : ('eta_fastmtt',';eta_{#tau#tau};NEvents',30,-2.3,2.3),
        'pt_fastmtt'   :    ('pt_fastmtt', ';p_{T}^{#tau#tau} ;NEvents', 40, 0, 200),
        'phi_fastmtt' : ('phi_fastmtt',';phi_{#tau#tau};NEvents',30,-3.5,3.5),
        'iso_1' : ('iso_1',';iso_{1};NEvents',50,0,1),
        'iso_2' : ('iso_2',';iso_{2};NEvents',50,0,1),
    })
if PNN:
    plot_vars = {
        
        'mt_tot': ('mt_tot', ';m_{T}^{tot} [GeV];NEvents', 50, 0, 500),
        'm_fastmtt'       :    ('m_fastmtt', '; m^{#tau#tau};NEvents', 27, 30, 300),
        'pt_1' : ('pt_1',';pt_{1};NEvents',20,20,220),
        'pt_2' : ('pt_2',';pt_{2};NEvents',20,20,220),
        'mt_1' : ('mt_1',';mt_{1};NEvents',50,0,200),
        'mt_2' : ('mt_2',';mt_{2};NEvents',50,0,200),
    }
    if int(mass) < 250:
        plot_vars.update({       
            'PNN_%s' %mass : ('PNN_%s' %mass,     ';PNN %s [GeV];NEvents' %mass,  20,0,1),     })
else:
    plot_vars.update({
    # 'dxy_1' : ('dxy_1',';dxy_{1};NEvents',25,-0.02,0.02),
    # 'dxy_2' : ('dxy_2',';dxy_{2};NEvents',25,-0.02,0.02),
    # 'dz_1' : ('dz_1',';dz_{1};NEvents',25,-0.02,0.02),
    # 'dz_2' : ('dz_2',';dz_{2};NEvents',25,-0.02,0.02),

    # 'mass_1' : ('mass_1',';mass_{1};NEvents',30,0,0.1),
    # 'mass_2' : ('mass_2',';mass_{2};NEvents',30,0,3),    
    'njets' : ('njets',';njets;NEvents',10,0,10),
    
    })

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
            'Data': ["1", 1, 'Data', [ "Muon", "Tau", "EGamma", "DoubleMuon", "SingleMuon" ],0], ## "MuonEG" will be identified by Muon so don't double count
            # "DY-Jets": ["1", 1, 'DY-Jets', DY_list, 0],
            "other": ["1", 1, 'other', [ "WZto", "ZZto", "WWto", "GluGluHto2Tau_M-125_TuneCP5_13p6TeV_amcatnloFXFX", "GluGluHToTauTau_M-125_TuneCP5_13p6TeV_powheg", "VBFH"],0],
            "Wjets" : ["1", 1, 'W-Jets', ["WtoLNu"], 0], 
            # "fakes": ["1", 1, 'fakes', ["FF_Combined"],0],
                
            })
    if "ggH" in signal_type and "bbH" in signal_type:
        samples.update({
            "%s*%s-%s" %(scale,"ggH",mass) : ["1", scale, "%s*%s-%s" %(scale,"ggH",mass), ["GluGluHto2Tau_M-%s_2HDM"%(mass)], 0 ]    ,
            "%s*%s-%s" %(scale,"bbH",mass) : ["1", scale, "%s*%s-%s" %(scale,"bbH",mass), ["bbHto2Tau_M-%s_"%(mass) ,"BBHto2Tau_M-%s_"%(mass)], 0 ]    ,
        })
    elif "ggH" in signal_type:
        samples.update({
            "%s*%s-%s" %(scale,"ggH",mass) : ["1", scale, "%s*%s-%s" %(scale,"ggH",mass), ["GluGluHto2Tau_M-%s_2HDM"%(mass)], 0 ]    ,
        })
    elif "bbH" in signal_type:
        samples.update({
            "%s*%s-%s" %(scale,"bbH",mass) : ["1", scale, "%s*%s-%s" %(scale,"bbH",mass), ["bbHto2Tau_M-%s_"%(mass), "BBHto2Tau_M-%s_"%(mass)], 0 ]    ,
        })
    if channel_name != 'em':
        samples.update({
            'Top': ['1', 1 ,   'Top'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
        })


    else:
        samples.update({
            # 'Top-true': ['((gen_match_1 ==1 && gen_match_2 ==2) ||(gen_match_1 ==3 && gen_match_2 ==4) || (gen_match_1 ==1 && gen_match_2 ==4) || (gen_match_1 ==3 && gen_match_2 ==2))', 1 ,   'Top-true'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            # 'Top-fake': ['(!((gen_match_1 ==1 && gen_match_2 ==2) ||(gen_match_1 ==3 && gen_match_2 ==4) || (gen_match_1 ==1 && gen_match_2 ==4) || (gen_match_1 ==3 && gen_match_2 ==2)))', 1 ,   'Top-fake'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            'Top-genuine_tau': ['(gen_match_1 ==1 && gen_match_2 ==2)', 1 ,   'Top-genuine_tau'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
            'Top-fake_tau': ['!(gen_match_1 ==1 && gen_match_2 ==2)', 1 ,   'Top-fake_tau'     , ['TTtoLNu2Q', 'TTto2L2Nu', 'TTto4Q', "TBbarQ_t", "TbarBQ_t", "TbarWplus", "TWminus"] ,  0 ], # + ttbar_list 
        })
    print(samples)


    if args.use_LO_DY:
        
        if channel_name == 'em':

            if era == '2022EE':
                samples.update({
                    "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.82 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
                })
                samples.update({
                    "DY-Jets-tt-em": ["(gen_match_1 == 3 && gen_match_2 ==4)", 0.82, 'DY-Jets-tt-em', ["DYto2L-2Jets",], 0],
                    "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.82 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
                })
                

            elif era == '2022postEE':
                samples.update({
                    "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.783 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
                })   
                samples.update({
                    "DY-Jets-tt-em": ["(gen_match_1 == 3 && gen_match_2 ==4)", 0.783, 'DY-Jets-tt-em', ["DYto2L-2Jets",], 0],
                    "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.783 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
                })

            elif era == '2023':
                samples.update({
                    "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.903 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
                })                     
                samples.update({
                    "DY-Jets-tt-em": ["(gen_match_1 == 3 && gen_match_2 ==4)", 0.903, 'DY-Jets-tt-em', ["DYto2L-2Jets",], 0],
                    "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.903 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
                })   

            elif era == '2023BPix':
                samples.update({
                    "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 0.897 , 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
                })
                samples.update({
                    "DY-Jets-tt-em": ["(gen_match_1 == 3 && gen_match_2 ==4)", 0.897, 'DY-Jets-tt-em', ["DYto2L-2Jets",], 0],
                    "DY-Jets-tt-other": ["  !(       (gen_match_1 == 3 && gen_match_2 ==4) || (gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)   ) ", 0.897 , 'DY-Jets-tt-other', ["DYto2L-2Jets",], 0],    ###    
                })  


        elif channel_name =='et':
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 3 && gen_match_2 ==5)", 1, 'DY-Jets-tt', ["DYto2L-2Jets",], 0],        
                "DY-Jets-fakes": ["(gen_match_1 == 3 &&  gen_match_2 !=5)", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],
            })
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
        elif channel_name =='mt':
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 4 && gen_match_2 ==5)", 1, 'DY-Jets-tt', ["DYto2L-2Jets",], 0],    
                "DY-Jets-fakes": ["(gen_match_1 == 4 &&  gen_match_2 !=5)", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],    
            })
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
        elif channel_name =='tt':
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 5 && gen_match_2 ==5)", 1, 'DY-Jets-tt', ["DYto2L-2Jets",], 0],     
                "DY-Jets-fakes": ["(gen_match_1 == 5 &&  gen_match_2 !=5) || (gen_match_1 != 5 &&  gen_match_2 ==5) ", 1, 'DY-Jets-fakes', ["DYto2L-2Jets",], 0],   
            })
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
        elif channel_name =='mm':
            samples.update({
                "DY-Jets-ll": ["(gen_match_1 == 1 && gen_match_2 ==1) || (gen_match_1 == 2 && gen_match_2 ==2)", 1, 'DY-Jets-ll', ["DYto2L-2Jets",], 0],
            })                
            samples.update({
                "DY-Jets-tt": ["(gen_match_1 == 5 && gen_match_2 ==5)", 1, 'DY-Jets-tt', ["DYto2L-2Jets",], 0],     
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
        
        if channel_name != 'em' :
        
            samples.update({"fakes": ["1", 1, 'fakes', ["FF_Combined"],0],})
        
        elif channel_name == 'em' : 

            samples.update({"QCD_fakes": ["1", 1, 'QCD_fakes', ["FF_Combined"],0],})


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
'all' : '1>0',
'nob' : Htautau.nob,
# 'nob1' : combinecut( Htautau.nob, "pt_tt > 0" , "pt_tt < 50"),
# 'nob2' : combinecut( Htautau.nob, "pt_tt > 50" , "pt_tt < 100"),
# 'nob3' : combinecut( Htautau.nob, "pt_tt > 100" , "pt_tt < 200"),
# 'nob4' : combinecut( Htautau.nob, "pt_tt > 200" ),

# "nob" : combinecut( Htautau.nob, Htautau.ttbar_true_only),
# "nob_mt_2_50" : combinecut( Htautau.nob, Htautau.ttbar_true_only, "mt_2 < 50"),
"btag" : Htautau.btag,


# # "nob_tight_mT" : combinecut(Htautau.nob, Htautau.tight_mT,lepton_selection, Htautau.W_true_only, Htautau.opposite_sign,"mt_1 < 40"),
# "nob_AntiID" : combinecut( Htautau.nob,   anti_selection, Htautau.W_true_only, Htautau.ttbar_true_only,Htautau.opposite_sign, "mt_1 < 70") if (channel_name != 'tt' and channel_name != 'em') else combinecut( Htautau.nob,   anti_selection,  Htautau.W_true_only, Htautau.opposite_sign),
# "btag_AntiID" : combinecut( Htautau.btag,   anti_selection,  Htautau.W_true_only,Htautau.ttbar_true_only, Htautau.opposite_sign, "mt_1 < 70") if (channel_name != 'tt' and channel_name != 'em') else combinecut( Htautau.btag,   anti_selection,  Htautau.W_true_only, Htautau.opposite_sign),
}

if PNN:
    regions["nob_PNN0p8"] = combinecut( "PNN_100 > 0.8", Htautau.nob)
    regions["btag_PNN0p8"] = combinecut("PNN_100 > 0.8", Htautau.btag)

selections = [ "mt_1 > 0  "] #, Htautau.W_true_only????

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
        selections += [ Htautau.opposite_sign , Htautau.W_true_only,  lepton_selection ]
    else:
        selections += [ Htautau.opposite_sign,  lepton_selection ]


        
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

    def blind_in_HmmWin(w):
        if w.legend == 'Data': # and w.in_file_path.startswith('Hmm_win'):
            if  'PNN' in w.name:  #'m_fastmtt'  in w.name or
                print('BLINDING Data in %s' % w.in_file_path)
                for i in xrange(w.histo.GetNbinsX() -9, w.histo.GetNbinsX() + 1):
                    w.histo.SetBinContent(i, 0.)
                    w.histo.SetBinError(i, 0.)
            if 'mt_tot' in w.name:  #
                if args.mass >= 200:
                    for i in xrange(6, w.histo.GetNbinsX() + 1):
                        w.histo.SetBinContent(i, 0.)
                        w.histo.SetBinError(i, 0.)
                else:
                    for i in xrange(3, 11):
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
        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(len(mt_tot_b)-1, 'rebinned_mt_tot', array.array('d', mt_tot_b))
        # if "mt_" in w.name or "mT" in w.name:
        #         w.histo = w.histo.Rebin(len(mt)-1, 'rebinned_mt', array.array('d', mt))
        # if "met" in w.name:
        #     w.histo = w.histo.Rebin(len(met)-1, 'rebinned_met{0}'.format(w.name), array.array('d', met))
        # if "pt_2"  in w.name or "pt_1" in w.name:
        #     w.histo = w.histo.Rebin(len(pt)-1, 'rebinned_{0}'.format(w.name), array.array('d', pt))            
        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(2)
        # if "m_fastmtt" in w.name and "zoom" not in w.name: 
        #     w.histo = w.histo.Rebin(len(m_fastmtt)-1, 'rebinned_m_fastmtt', array.array('d', m_fastmtt))
        # if "mt_tot_rebinned" in w.name:
        #     w.histo = w.histo.Rebin(len(nob_tight_mT)-1, 'rebinned_mt_tot', array.array('d', nob_tight_mT))

        # if "mt_tot" in w.name:
        #     w.histo = w.histo.Rebin(len(nob_tight_mT)-1, 'mt_tot', array.array('d', nob_tight_mT))    
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
        if "PNN_100_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_100) -1, 'rebinned_mt_tot', array.array('d', PNN_100))   
            # h_PNN_100 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_100))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
        if "PNN_200_rebinned" in w.name:
            rebinned_h = w.histo.Rebin(len(PNN_200) -1, 'rebinned_mt_tot', array.array('d', PNN_200))   
            # h_PNN_200 = R.TH1F("h1", "Original Histogram", w.histo.GetNbinsX(), 0, w.histo.GetNbinsX()) 
            w.histo =w.histo.Rebin(w.histo.GetNbinsX()/ len(PNN_200))   
            for i in xrange(rebinned_h.GetNbinsX() + 1):
                w.histo.SetBinContent(i, rebinned_h.GetBinContent(i))
                w.histo.SetBinError(i, rebinned_h.GetBinError(i))
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
    if PNN:
        wrps = (blind_in_HmmWin(w) for w in wrps)
    # wrps = (setylimit(w) for w in wrps)
    # wrps = (scale_by_binwidth(w) for w in wrps)
    # for w in wrps:
    #     w.y_bounds = (1, 10e5)
    return wrps