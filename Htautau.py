import ROOT as R
import os
import yaml
from math import *
import numpy as np






def combinecut(*args):
    return '(' + '&&'.join(args) + ')'
class Htautau_selections:
    nob = "( nbtag == 0 ) "
    btag = "( nbtag >= 1 ) "
    tight_mT = " ( mt_1 < 40.0) "
    loose_mT = " ( mt_1 > 40.0 && mt_1 < 70.0 ) "
    mt_tau_selections ={
        "2018": "(id_tau_vsMu_Tight_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) ",
        "2022EE": "(id_tau_vsMu_Loose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) ",
        "2022postEE": "(id_tau_vsMu_Loose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_VVLoose_2 > 0 && pt_2 > 30 ) ",
    } 
    et_tau_selections = {
        "2018": " (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 ) ",
        "2022EE": " (id_tau_vsMu_VLoose_2 > 0 && id_tau_vsJet_Medium_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 && pt_2 > 30 ) ",
        "2022postEE":" (id_tau_vsMu_VLoose_2 > 0  &&  id_tau_vsEle_Tight_2 > 0 && id_tau_vsJet_Medium_2 > 0 && pt_2 > 30 ) ", #
    } 
    DR_deeptau_selections = {}
    DR_deeptau_selections["mt"] = " (id_tau_vsMu_Tight_2 > 0 &&   id_tau_vsEle_VVLoose_2 > 0  ) "
    DR_deeptau_selections["et"] = " (id_tau_vsMu_VLoose_2 > 0 &&  id_tau_vsEle_Tight_2 > 0 ) "
    DR_deeptau_selections["tt"] = " (id_tau_vsMu_VLoose_1 > 0 &&  id_tau_vsEle_VVLoose_1 > 0 && id_tau_vsMu_VLoose_1 > 0 ) "
    DR_deeptau_selections["em"] = " 1 > 0" ## TODO: add em selections
    
    # tt_triggers_selections = " (trg_double_tau40_mediumiso_tightid == 1 ||  trg_double_tau35_mediumiso_hps == 1 || trg_double_tau35_tightiso_tightid == 1 || trg_double_tau40_tightiso == 1  || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)" 
    # tt_triggers_selections = " (  trg_double_tau35_mediumiso_hps == 1   || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1)" 

    lowDzeta = '-35 <= pzetamissvis && pzetamissvis < -10'
    mediumDzeta = '-10 <= pzetamissvis && pzetamissvis < 30'
    highDzeta = '30 <= pzetamissvis'






    
    tt_secondtau_selections = " (id_tau_vsJet_Medium_2 > 0  && dz_2 < 0.2 &&   pt_2 > 40 && eta_2 < 2.1 && eta_2 > -2.1 && id_tau_vsEle_VVLoose_2 > 0   &&id_tau_vsMu_VLoose_2 > 0         && deltaR_ditaupair > 0.5 ) "
    tt_leadingtau_selections = "(id_tau_vsJet_Medium_1 > 0 && dz_1 < 0.2 && pt_1 > 40 && eta_1 < 2.1 && eta_1 > -2.1 && id_tau_vsEle_VVLoose_1 > 0   &&id_tau_vsMu_VLoose_1 > 0  )"
    # et_triggers_selections = " (trg_cross_ele24tau30 == 1  || trg_single_ele27 == 1 || trg_single_ele32 == 1 || trg_single_ele35 == 1 )" #|| trg_cross_ele24tau30_hps == 1
    lepton_veto = "extramuon_veto == 0  && extraelec_veto == 0 " 

    et_triggers_selections = {}
    mt_triggers_selections = {}
    em_triggers_selections = {}
    tt_triggers_selections = {}
    et_triggers_selections["2016preVFP"]="(trg_cross_ele24tau20==1||trg_cross_ele24tau20_crossL1==1||trg_cross_ele24tau30==1||trg_single_ele25==1||trg_single_tau120_2==1||trg_single_tau140_2==1)"
    mt_triggers_selections["2016preVFP"]="(trg_cross_mu20tau27==1||trg_cross_mu19tau20==1||trg_single_mu22==1||trg_single_mu22_tk==1||trg_single_tau120_2==1||trg_single_tau140_2==1)"
    et_triggers_selections["2016postVFP"] = et_triggers_selections["2016preVFP"]
    mt_triggers_selections["2016postVFP"] = mt_triggers_selections["2016preVFP"]
    et_triggers_selections["2017"]="(trg_cross_ele24tau30==1||trg_single_ele27==1||trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)"
    mt_triggers_selections["2017"]="(trg_cross_mu20tau27==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)"
    em_triggers_selections["2017"] = "(trg_cross_mu23ele12 == 1 || trg_cross_mu8ele23 == 1 || trg_single_ele27 == 1 || trg_single_ele32 == 1 || trg_single_ele35 == 1 || trg_single_mu24 == 1 || trg_single_mu27 == 1)"

    mt_triggers_selections["2018"]="(trg_cross_mu20tau27==1||trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)"
    et_triggers_selections["2018"]= "(trg_cross_ele24tau30==1||trg_cross_ele24tau30_hps==1||trg_single_ele27==1||trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)"
    
    mt_triggers_selections["2022EE"]="(trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)"
    # et_triggers_selections["2022EE"]= "(trg_cross_ele24tau30_hps==1||trg_single_ele27==1||trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)"
    mt_triggers_selections["2022postEE"]="(trg_cross_mu20tau27_hps==1||trg_single_mu24==1||trg_single_mu27==1||trg_single_tau180_2==1)"
    # et_triggers_selections["2022postEE"]= "(trg_cross_ele24tau30_hps==1||trg_single_ele27==1||trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)"
    et_triggers_selections["2022EE"]= "(trg_single_ele30 ==1|| trg_single_ele32==1||trg_single_ele35==1||trg_single_tau180_2==1)" # trg_cross_ele24tau30_hps==1||
    et_triggers_selections["2022postEE"]= "( (trg_single_ele30 ==1|| trg_single_ele32==1)||(trg_single_ele35==1)||trg_single_tau180_2==1)" #trg_cross_ele24tau30_hps==1||
    # et_triggers_selections["2022postEE"]= "( trg_cross_ele24tau30_hps==1)" #trg_cross_ele24tau30_hps==1||
    
    tt_triggers_selections["2022EE"] = " (trg_double_tau35_mediumiso_hps == 1 || trg_double_tau40_mediumiso_tightid == 1 || trg_double_tau40_tightiso == 1 || trg_single_tau180_1 == 1 || trg_single_tau180_2 == 1 || trg_double_tau30_plusPFjet60 == 1 || trg_double_tau30_plusPFjet75 == 1 )" 
    tt_triggers_selections["2022postEE"] = tt_triggers_selections["2022EE"] 

    em_triggers_selections["2022EE"] = "(trg_cross_mu23ele12 == 1 || trg_cross_mu8ele23 == 1 || (trg_single_ele30 == 1) ||(trg_single_ele32 == 1)|| (trg_single_ele35 == 1) || (trg_single_mu24 == 1)|| (trg_single_mu27 == 1))"
    em_triggers_selections["2022postEE"] = em_triggers_selections["2022EE"]



####    

###





    em_electron_selection = "pt_1 > 15 && eta_1 < 2.4 && dz_1 < 0.2 && dxy_1 < 0.045 && iso_1 < 0.15 && deltaR_ditaupair > 0.3"
    #em_electron_selection = "(dz_1 < 0.2 && dxy_1 < 0.045 && iso_1 < 0.15 && deltaR_ditaupair > 0.3 && pt_1 > 15)"


    em_muon_selection = "pt_2 > 15 && eta_2 < 2.4 && dz_2 < 0.2 && dxy_2 < 0.045 && iso_2 < 0.2"
    #em_muon_selection = "(dz_2 < 0.2 && dxy_2 < 0.045 && iso_2 < 0.2 && pt_2 > 15)"
    electron_selections = 'pt_1 > 30 '
    muon_selections = " pt_1> 25.0 "
    
    W_true_only =     "(  ( gen_match_2 != 6 && is_wjets>0 ) || (is_wjets <1)  ) " # for w-jets, only consider the true tau components
    # W_true_only =     "(  1 > 0 ) " # for w-jets, only consider the true tau components
    ttbar_true_only = "(  ( gen_match_2 != 6 && is_ttbar>0 ) || (is_ttbar <1)  )" # for ttbar, only consider the true tau components 
    opposite_sign = ' ((q_1 * q_2) < 0) '
    same_sign = ' ((q_1 * q_2) > 0) '
    DR_QCD_lt = '( (  (q_1 * q_2) > 0)  && (iso_1 > 0.05) )'## SS + iso cut
    DR_QCD_tt = ' (  (q_1 * q_2) > 0) '## SS + iso cut
    DR_W = " (q_1 * q_2) < 0 && ( mt_1 > 70.0 ) && nbtag == 0"
    DR_ttbar = " (q_1 * q_2) < 0 && ( mt_1 > 70.0 ) && nbtag >= 2"
    DR_ttbar_test = " ( mt_1 > 70.0 ) && nbtag >= 1"
    ID_lt = " (id_tau_vsJet_Medium_2 > 0) "
    Anti_ID_lt = " (id_tau_vsJet_Medium_2 == 0) "
    ID_tt = " (id_tau_vsJet_Medium_1 > 0) "
    Anti_ID_tt = " (id_tau_vsJet_Medium_1 == 0) "

    true_tau = "(gen_match_2 != 6 )"
    pt_tt_1 = "(pt_tt < 50) "
    pt_tt_2 = "(pt_tt > 50 && pt_tt < 100) "
    pt_tt_3 = "(pt_tt > 100 && pt_tt < 200) "
    pt_tt_4 = "(pt_tt > 200) "

    # et_selections = combinecut(opposite_sign, et_triggers_selections,electron_selections,lepton_veto,et_tau_selections)
    # mt_selections = combinecut(opposite_sign, mt_triggers_selections,muon_selections,lepton_veto,mt_tau_selections)



def makelink(input_path,*args):
    os.system('mkdir -p ' + input_path)
    os.chdir(input_path)
    for arg in args:
        os.system('ln -s ' + arg + ' .')
    os.chdir('..')
def checknoevents(input_file_name):
    # if not os.path.exists(input_path):
    #     return 0
    try:
        f = R.TFile.Open(input_file_name, "READ")
    except:
        print('warning!! could not open file '+ input_file_name )
        return input_file_name
    tree = None
    try:
        tree = f.Get("ntuple")
    except:
        pass
    if not tree:
        print(input_file_name)
        return input_file_name
    else:
        f.Close()
        return ''
    if tree:
        f.Close()
        
def check_and_remove(input_path):
    no_events = []

    for i in os.listdir(input_path):
        no_events_f = checknoevents(input_path + '/' + i)
        if no_events_f:
            no_events.append(no_events_f)
    for i in no_events:
        os.system("mkdir -p  noevents_files")
        os.system('mv '+ i + ' '  + 'noevents_files/')
    print(no_events)

def getnickweight(input_path, nick, rerun = False):
    """
    take input_path and nick as input,
    return the sum of weights given nick
    set rerun as true also removes files with no events
    """
    sumofweight = 0.0
    
    
    veto = ['Embedding','DoubleMuon_Run2018','EGamma_Run2018','EGamma_Run2018','SingleMuon_Run2018','SingleMuon_Run2018','Tau_Run2018']
    ## return 1 for data, embedding samples
    for v in veto:
        if v in nick:
            return 1
    ## input_pattern example: 2018/ZZ_TuneCP5_13TeV-pythia8_RunIISummer20UL18NanoAODv9-106X/mt/*%s*'
    if not os.path.exists(input_path):
        return 1
    yaml_name =  'SumOfWeights_{0}.yaml'.format(input_path)
    if not os.path.exists(yaml_name) or rerun: 
        if not os.path.exists(yaml_name):
            weights_f = open(yaml_name, "w") 
        for i in os.listdir(input_path):
            if nick in i:
                fname = '/'.join([input_path, i])
                f = R.TFile.Open(fname, "READ")
                # print(f)
                weight_tree = f.Get("conditions")
                for entry in weight_tree:
                    sumw = entry.genEventSumw
                    # print(sumw)
                    if sumw == 0:
                        if not "Run2018" in nick:
                            print("Warning!!!  getting 0 sumofweight!!! Nick: " + nick)
                    sumofweight += sumw
                f.Close()
        weight_dict = {nick: sumofweight}
        Firstdict = False
        ## check if yaml file was created 
        with open(yaml_name , 'r') as file:
            dict_tmp = yaml.safe_load(file) 
            if not dict_tmp:
                Firstdict = True
        if Firstdict:
            with open(yaml_name , 'w') as file:
                yaml.safe_dump(weight_dict, file) 
        else:
            dict_tmp.update(weight_dict)
            with open(yaml_name , 'w') as file:
                yaml.safe_dump(dict_tmp, file) 
        return sumofweight
    else:
        weights_f = open(yaml_name, "r") 
        weight_list =  yaml.load(weights_f, Loader = yaml.Loader) 
        return weight_list[nick]

# checknoevents("samples_Htautau/VBFHToBB_M-125_TuneCP5_13TeV-powheg-pythia8_RunIISummer20UL18NanoAODv9-106X_5.R")
#check_and_remove('Fakefactor')







def plot(sig, bkg, data, x_label, filename):
    """
    Plot invariant mass for signal and background processes from simulated
    events overlay the measured data.
    """
    # Canvas and general style options
    R.gStyle.SetOptStat(0)
    R.gStyle.SetTextFont(42)
    d = R.TCanvas("", "", 800, 700)
    # Make sure the canvas stays in the list of canvases after the macro execution
    R.SetOwnership(d, False)
    d.SetLeftMargin(0.15)

    # Get signal and background histograms and stack them to show Higgs signal
    # on top of the background process
    h_bkg = bkg
    h_cmb = sig.Clone()

    h_cmb.Add(h_bkg)
    h_cmb.SetTitle("")
    h_cmb.GetXaxis().SetTitle(x_label)
    h_cmb.GetXaxis().SetTitleSize(0.04)
    h_cmb.GetYaxis().SetTitle("N_{Events}")
    h_cmb.GetYaxis().SetTitleSize(0.04)
    h_cmb.SetLineColor(R.kRed)
    h_cmb.SetLineWidth(2)
    h_cmb.SetMaximum(18)
    h_bkg.SetLineWidth(2)
    h_bkg.SetFillStyle(1001)
    h_bkg.SetLineColor(R.kBlack)
    h_bkg.SetFillColor(R.kAzure - 9)

    # Get histogram of data points
    h_data = data
    h_data.SetLineWidth(1)
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.0)
    h_data.SetMarkerColor(R.kBlack)
    h_data.SetLineColor(R.kBlack)

    # Draw histograms
    h_cmb.DrawCopy("HIST")
    h_bkg.DrawCopy("HIST SAME")
    h_data.DrawCopy("PE1 SAME")

    # Add legend
    legend = R.TLegend(0.62, 0.70, 0.82, 0.88)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.AddEntry(h_data, "Data", "PE1")
    legend.AddEntry(h_bkg, "ZZ", "f")
    legend.AddEntry(h_cmb, "m_{H} = 125 GeV", "f")
    legend.Draw()

    # Add header
    cms_label = R.TLatex()
    cms_label.SetTextSize(0.04)
    cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS Open Data}")
    header = R.TLatex()
    header.SetTextSize(0.03)
    header.DrawLatexNDC(0.63, 0.92, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")

    # Save plot
    d.SaveAs(filename)



def make_logbinning(xmin, xmax, nbins):
    r = [] 
    xlogmin = log(xmin, 10);
    xlogmax = log(xmax,10);
    dlogx   = (xlogmax-xlogmin)/(nbins)
    for i in range(0,nbins+1):
        xlog = xlogmin+ i*dlogx
        a = exp( log(10) * xlog ) 
        r.append(round(a,1))
    return r


# true_only = "(gen_match_2 != 6)"
Htautau = Htautau_selections()
# regions = {
#     # "ALL"                  : combinecut(Htautau.opposite_sign, Htautau.tau_selections,true_only),
#     "nob_loose_mT" : combinecut(Htautau.nob, Htautau.loose_mT,Htautau.opposite_sign, Htautau.tau_selections,true_only),
#     "nob_tight_mT" : combinecut(Htautau.nob, Htautau.tight_mT,Htautau.opposite_sign, Htautau.tau_selections,true_only),
#     "btag_loose_mT"      : combinecut(Htautau.btag, Htautau.loose_mT,Htautau.opposite_sign, Htautau.tau_selections, true_only),
#     "btag_tight_mT"      : combinecut(Htautau.btag, Htautau.tight_mT,Htautau.opposite_sign, Htautau.tau_selections, true_only), }

regions_PNN = {
    # "ALL"                  : 'mt_1 < 70',
    "nob_loose_mT" : combinecut(Htautau.nob, Htautau.loose_mT ),
    "nob_tight_mT" : combinecut(Htautau.nob, Htautau.tight_mT ),
    "btag_loose_mT"      : combinecut(Htautau.btag, Htautau.loose_mT),
    "btag_tight_mT"      : combinecut(Htautau.btag, Htautau.tight_mT),}


def custom_bins(bin_count_fine=20, bin_count_coarse=10, division = 0.9):
    fine_bins = np.linspace(division, 1.05, bin_count_fine + 1)
    coarse_bins = np.linspace(0, division, bin_count_coarse + 1)
    bin_edges = np.unique(np.concatenate((fine_bins, coarse_bins)))
    return bin_edges

def make_binning_by_error(h,xmin, xmax):
    '''
    algo to rebin by fractional error in data
    default minimum data required: 1
    
    '''
    
    binning = []
    binning_abs = []
    for i in range(0, h.GetNbinsX()+1):
       
        if not binning:
            binning.append(xmin)
        if i < binning[-1] or i in binning:
            continue
        j = i 
        print(j)
        herror = h.GetBinError(i)
        hvalue = h.GetBinContent(i)
        while hvalue <= 1 and j < xmax/h.GetBinWidth(1):
            herror = h.GetBinError(j)**2 + herror**2
            herror = sqrt(herror)
            hvalue += h.GetBinContent(j)
            j+=1
        while herror / hvalue  > 0.15 and j < xmax/h.GetBinWidth(1):
            herror = h.GetBinError(j)**2 + herror**2
            herror = sqrt(herror)
            hvalue += h.GetBinContent(j)
            j+=1
        
        if j > xmax/h.GetBinWidth(1):
            binning.append(int(xmax/h.GetBinWidth(1)))
            break
        else:
            binning.append(j)   
    for i in binning:
        binning_abs.append(i*h.GetBinWidth(1))
    if binning_abs[-1] < xmax:
        binning_abs.append(xmax)
    return binning_abs

 
AN_Result = {
    "bins" : {
      "nob_loose_mT" : [0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,5000.0],
      "btag_tight_mT" : [0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,250.0,300.0,350.0,400.0,500.0,600.0,700.0,800.0,900.0,1100.0,1300.0,5000.0],
      "nob_tight_mT" : [50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,225.0,250.0,275.0,300.0,325.0,350.0,400.0,450.0,500.0,600.0,700.0,800.0,900.0,1100.0,1700.0,2100.0,5000.0],
      "btag_loose_mT" : [0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,250.0,300.0,350.0,400.0,500.0,600.0,700.0,800.0,900.0,5000.0],},
    "values" : {
        "nob_loose_mT" : [41,612,2172,7579,14674,19620,21205,17566,11151,7022,4455,2991,2089,1578,1103,841,1339,723,406,263,150,99,128,64,41,40,20,11,5,0,2,1],
        "btag_tight_mT" : [5104,6355,7925,5139,3316,2120,1509,959,1260,551,216,110,110,41,8,1,1,1,0,0],
        "nob_tight_mT" : [9720,7180,26879,63984,77472,60919,36169,19465,10579,6329,4049,2924,2133,1681,1220,986,1594,1051,581,425,247,202,243,139,103,92,46,16,6,10,1,1,0],
        "btag_loose_mT": [441,2958,6174,5838,4083,2657,1655,1086,1361,497,199,95,86,18,7,3,3,1],}
}
