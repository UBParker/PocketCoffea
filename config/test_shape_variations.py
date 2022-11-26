from pocket_coffea.parameters.cuts.preselection_cuts import *
from pocket_coffea.workflows.tthbb_base_processor import ttHbbBaseProcessor
from pocket_coffea.lib.cut_functions import get_nObj_min, get_nObj_eq, get_nBtag, get_HLTsel
from pocket_coffea.parameters.histograms import *
from pocket_coffea.parameters.btag import btag_variations
from pocket_coffea.lib.weights_manager import WeightCustom
import numpy as np


cfg =  {
    "dataset" : {
        "jsons": ["datasets/signal_ttHTobb_local.json",
                  "datasets/backgrounds_MC_TTbb_local.json",
                  "datasets/backgrounds_MC_ttbar_local.json",
                  "datasets/DATA_SingleMuon_local.json",
                  "datasets/DATA_SingleEle.json"],
        "filter" : {
            "samples": [
                # "TTToSemiLeptonic","TTbbSemiLeptonic",
                "ttHTobb",
                # "DATA_SingleMu", "DATA_SingleEle"
            ],
            "samples_exclude" : [],
            "year": ['2018']
        },
    },
    

    # Input and output files
    "workflow" : ttHbbBaseProcessor,
    "output"   : "output/test_shape_variations",
    "workflow_options" : {},

    "run_options" : {
        "executor"       : "dask/slurm",
        "workers"        : 1,
        "scaleout"       : 100,
        "queue"          : "short",
        "walltime"       : "00:40:00",
        "mem_per_worker" : "4GB", # GB
        "exclusive"      : False,
        "chunk"          : 400000,
        "retries"        : 50,
        "treereduction"  : 10,
        "max"            : None,
        "skipbadfiles"   : None,
        "voms"           : None,
        "limit"          : None,
        "adapt"          : False,
        "env"            : "conda"
    },

    # Cuts and plots settings
    "finalstate" : "semileptonic",
    "skim": [get_nObj_min(4, 15., "Jet"),
             get_HLTsel("semileptonic")],
    "preselections" : [semileptonic_presel],
    "categories": {
        "baseline": [passthrough],
    },

    

    "weights": {
        "common": {
            "inclusive": ["genWeight","lumi","XS",
                          "pileup",
                          "sf_ele_reco", "sf_ele_id",
                          "sf_mu_id","sf_mu_iso",
                          "sf_btag", "sf_jet_puId", 
                          ],
            "bycategory" : {
            }
        },
        "bysample": {
        }
    },

    "variations": {
        "weights": {
            "common": {
                "inclusive": [  "pileup",
                                "sf_ele_reco", "sf_ele_id",
                                "sf_mu_id", "sf_mu_iso", "sf_jet_puId",
                                *[ f"sf_btag_{b}" for b in btag_variations["2018"]]                               
                              ],
                "bycategory" : {
                }
            },
            "bysample": {
            }    
        },
        "shape": {
            "common":{
                "inclusive": ["JES_jes"]
            }
        }
    },

   "variables":
    {

        **ele_hists(coll="ElectronGood", pos=0),
        **muon_hists(coll="MuonGood", pos=0),
        **count_hist(name="nElectronGood", coll="ElectronGood",bins=3, start=0, stop=3),
        **count_hist(name="nMuonGood", coll="MuonGood",bins=3, start=0, stop=3),
        **count_hist(name="nJets", coll="JetGood",bins=10, start=4, stop=14),
        **count_hist(name="nBJets", coll="BJetGood",bins=12, start=2, stop=14),
        **jet_hists(coll="JetGood", pos=0),
        **jet_hists(coll="JetGood", pos=1),
        **jet_hists(coll="JetGood", pos=2),
        **jet_hists(coll="JetGood", pos=3),
        **jet_hists(coll="JetGood", pos=4),
        **jet_hists(name="bjet",coll="BJetGood", pos=0),
        **jet_hists(name="bjet",coll="BJetGood", pos=1),
        **jet_hists(name="bjet",coll="BJetGood", pos=2),

        # 2D plots
        "jet_eta_pt_leading": HistConf(
            [
                Axis(coll="JetGood", field="pt", pos=0, bins=40, start=0, stop=1000,
                     label="Leading jet $p_T$"),
                Axis(coll="JetGood", field="eta", pos=0, bins=40, start=-2.4, stop=2.4,
                     label="Leading jet $\eta$"),
            ]
        ),
        "jet_eta_pt_all": HistConf(
            [
                Axis(coll="JetGood", field="pt", bins=40, start=0, stop=1000,
                     label="Leading jet $p_T$"),
                Axis(coll="JetGood", field="eta", bins=40, start=-2.4, stop=2.4,
                     label="Leading jet $\eta$")
            ]
        ),

        # Metadata of the processing
        "events_per_chunk" : HistConf(
               axes=[
                   Axis(name='nEvents_initial', field=None,
                        bins=100, start=0, stop=500000,                       
                        label="Number of events in the chunk",
                        ), 
                   Axis(name='nEvents_after_skim', field=None,
                        bins=100, start=0, stop=500000,                       
                        label="Number of events after skim per chunk",
                        ), 
                   Axis(name='nEvents_after_presel',field=None,
                        bins=100, start=0, stop=500000,
                        label="Number of events after preselection per chunk",
                        )
               ],
            storage="int64",
            autofill=False,
            metadata_hist = True,
            no_weights=True,
            only_categories=["baseline"],
            variations=False,),
    }
}
