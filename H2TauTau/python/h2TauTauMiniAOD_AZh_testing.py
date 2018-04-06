import FWCore.ParameterSet.Config as cms
# from CMGTools.Production.datasetToSource import datasetToSource
# from CMGTools.H2TauTau.tools.setupRecoilCorrection import setupRecoilCorrection
# from CMGTools.H2TauTau.tools.setupEmbedding import setupEmbedding
# from CMGTools.H2TauTau.objects.jetreco_cff import addAK4Jets
from CMGTools.H2TauTau.tools.setupOutput import addTauMuOutput, addTauEleOutput, addDiTauOutput, addMuEleOutput, addDiMuOutput
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *


from CMGTools.H2TauTau.eventContent.tauMu_cff import tauMu as tauMuEventContent
from CMGTools.H2TauTau.eventContent.tauEle_cff import tauEle as tauEleEventContent
from CMGTools.H2TauTau.eventContent.muEle_cff import muEle as muEleEventContent
from CMGTools.H2TauTau.eventContent.diTau_cff import diTau as diTauEventContent



def addMETFilters(process):
    process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
    process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
    process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
    process.BadPFMuonFilter.taggingMode = cms.bool(True)

    process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
    process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
    process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
    process.BadChargedCandidateFilter.taggingMode = cms.bool(True)

def addNewTauID(process):
    process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
    
    process.rerunDiscriminationByIsolationMVArun2v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
        PATTauProducer = cms.InputTag('slimmedTaus'),
        Prediscriminants = noPrediscriminants,
        loadMVAfromDB = cms.bool(True),
        mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1"),
        mvaOpt = cms.string("DBoldDMwLT"),
        requireDecayMode = cms.bool(True),
        verbosity = cms.int32(0)
    )

    process.rerunDiscriminationByIsolationMVArun2v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
        PATTauProducer = cms.InputTag('slimmedTaus'),    
        Prediscriminants = noPrediscriminants,
        toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw'),
        key = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw:category'),
        loadMVAfromDB = cms.bool(True),
        mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_mvaOutput_normalization"),
        mapping = cms.VPSet(
                cms.PSet(
                        category = cms.uint32(0),
                        cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff90"),
                        variable = cms.string("pt"),
                )
        )
    )

    process.rerunDiscriminationByIsolationMVArun2v1Loose = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
    process.rerunDiscriminationByIsolationMVArun2v1Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff80")
    process.rerunDiscriminationByIsolationMVArun2v1Medium = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
    process.rerunDiscriminationByIsolationMVArun2v1Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff70")
    process.rerunDiscriminationByIsolationMVArun2v1Tight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
    process.rerunDiscriminationByIsolationMVArun2v1Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff60")
    process.rerunDiscriminationByIsolationMVArun2v1VTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
    process.rerunDiscriminationByIsolationMVArun2v1VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff50")
    process.rerunDiscriminationByIsolationMVArun2v1VVTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
    process.rerunDiscriminationByIsolationMVArun2v1VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff40")

    process.slimmedTausExtraIDs = cms.EDProducer("PATTauIDEmbedder",
        src = cms.InputTag('slimmedTaus'),
        tauIDSources = cms.PSet(
          byIsolationMVArun2v1DBoldDMwLTrawNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw'),
          byVLooseIsolationMVArun2v1DBoldDMwLTNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VLoose'),
          byLooseIsolationMVArun2v1DBoldDMwLTNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1Loose'),
          byMediumIsolationMVArun2v1DBoldDMwLTNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1Medium'),
          byTightIsolationMVArun2v1DBoldDMwLTNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1Tight'),
          byVTightIsolationMVArun2v1DBoldDMwLTNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VTight'),
          byVVTightIsolationMVArun2v1DBoldDMwLTNew = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1VVTight')
          )
    )

def createProcess(runOnMC=True, channel='tau-mu', runSVFit=False, runMVAETmiss=False,
                  # Christians's default. If not touched, it would default to this anyways
                  p4TransferFunctionFile='CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root',
                  integrateOverP4=False, scaleTau=0., recorrectJets=True,
                  verbose=False):
    '''Set up CMSSW process to run MVA MET and SVFit.

    Args:
        runOnMC (bool): run on MC (access to gen-level products) or data
        channel (string): choose from 'tau-mu' 'di-tau' 'tau-ele' 'mu-ele' 
                          'all-separate' 'all'
        runSVFit (bool): enables the svfit mass reconstruction used for the 
                         H->tau tau analysis.
    '''

    sep_line = '-'*70

    process = cms.Process("H2TAUTAU")

    addNewTauID(process)
    addMETFilters(process)

    if recorrectJets:
        # Adding jet collection
        process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

        # Global tags from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC 07 Feb 2017
        process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
        if not runOnMC:
            process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v7'

        process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
        process.load('Configuration.StandardSequences.MagneticField_38T_cff')

        ##this one?  
        from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
        process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
            src=cms.InputTag("slimmedJets"),
            levels=['L1FastJet',
                    'L2Relative',
                    'L3Absolute'],
            payload='AK4PFchs'
        )  # Make sure to choose the appropriate levels and payload here!

        if not runOnMC:
            process.patJetCorrFactorsReapplyJEC.levels += ['L2L3Residual']

        from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
        process.patJetsReapplyJEC = updatedPatJets.clone(
            jetSource=cms.InputTag("slimmedJets"),
            jetCorrFactorsSource=cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
        )

    if runMVAETmiss:
        if recorrectJets:
            runMVAMET(process, jetCollectionPF="patJetsReapplyJEC")
        else:
            runMVAMET(process)

    # We always need this
    runMetCorAndUncFromMiniAOD(process, isData=not runOnMC)

    process.selectedVerticesForPFMEtCorrType0.src = cms.InputTag("offlineSlimmedPrimaryVertices")

    # loadLocalSqlite(process, 'Spring16_25nsV3_DATA.db') #os.environ['CMSSW_BASE'] + '/src/CMGTools/RootTools/data/jec/'

    process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

    numberOfFilesToProcess = -1
    numberOfFilesToProcess = 1
    debugEventContent = False

    # increase to 1000 before running on the batch, to reduce size of log files
    # on your account
    reportInterval = 100

    print sep_line
    print 'channel', channel
    print 'runSVFit', runSVFit

    # Input & JSON             -------------------------------------------------

    # dataset_user = 'htautau_group'
    # dataset_name = '/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Spring14dr-PU20bx25_POSTLS170_V5-v1/AODSIM/SS14/'
    # dataset_files = 'miniAOD-prod_PAT_.*root'

    if runOnMC:
        from CMGTools.H2TauTau.proto.samples.spring16.higgs_susy import HiggsAZH300 as azh300 
        ### from CMGTools.H2TauTau.proto.samples.summer16.higgs_susy import HiggsSUSYGG160 as ggh160
        process.source = cms.Source(
            "PoolSource",
            noEventSort=cms.untracked.bool(True),
            duplicateCheckMode=cms.untracked.string("noDuplicateCheck"),
            fileNames=cms.untracked.vstring(azh300.files)
        )
    else:
        # from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_Promptv4
        from CMGTools.H2TauTau.proto.samples.summer16.htt_common import data_single_muon
        process.source = cms.Source(
            "PoolSource",
            noEventSort=cms.untracked.bool(True),
            duplicateCheckMode=cms.untracked.string("noDuplicateCheck"),
            fileNames=cms.untracked.vstring(data_single_muon[1].files)  # mu-tau
        )

    if runOnMC:
        process.genEvtWeightsCounter = cms.EDProducer(
            'GenEvtWeightCounter',
            verbose=cms.untracked.bool(False)
        )

    if numberOfFilesToProcess > 0:
        process.source.fileNames = process.source.fileNames[:numberOfFilesToProcess]

    print 'Run on MC?', runOnMC #, process.source.fileNames[0]

    # if not runOnMC:
    #     from CMGTools.H2TauTau.proto.samples.spring16.htt_common import json
    #     # print 'Running on data, setting up JSON file'
    #     # json = setupJSON(process)

    # Message logger setup.
    process.load("FWCore.MessageLogger.MessageLogger_cfi")
    process.MessageLogger.cerr.FwkReport.reportEvery = reportInterval
    process.MessageLogger.suppressWarning = cms.untracked.vstring('cmgDiTau')
    process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

    process.options = cms.untracked.PSet(
        allowUnscheduled=cms.untracked.bool(True)
    )



    # load the channel paths -------------------------------------------

    if runMVAETmiss:
        process.MVAMET.requireOS = cms.bool(False)
        process.MVAMET.srcMETs = cms.VInputTag(cms.InputTag("slimmedMETs", "", "PAT" if runOnMC else "RECO"),
                                               cms.InputTag("patpfMET"),
                                               cms.InputTag("patpfMETT1"),
                                               cms.InputTag("patpfTrackMET"),
                                               cms.InputTag("patpfNoPUMET"),
                                               cms.InputTag("patpfPUCorrectedMET"),
                                               cms.InputTag("patpfPUMET"),
                                               cms.InputTag("slimmedMETsPuppi", "", "PAT" if runOnMC else "RECO"))

    if channel == 'tau-mu':
        process.load('CMGTools.H2TauTau.objects.tauMuObjectsMVAMET_cff')

        if runMVAETmiss:
            process.mvaMETTauMu = process.MVAMET.clone()
            process.mvaMETTauMu.srcLeptons = cms.VInputTag("tauPreSelectionTauMu", "muonPreSelectionTauMu")
            process.mvaMETTauMu.MVAMETLabel = cms.string('mvaMETTauMu')
            process.cmgTauMu.metCollection = cms.InputTag('mvaMETTauMu', 'mvaMETTauMu')
        else:
            process.cmgTauMu.metCollection = cms.InputTag('slimmedMETs')
        if not runSVFit:
            process.cmgTauMuCorSVFitPreSel.SVFitVersion = 0
        if integrateOverP4:
            process.cmgTauMuCorSVFitPreSel.integrateOverP4 = integrateOverP4
        if p4TransferFunctionFile:
            process.cmgTauMuCorSVFitPreSel.p4TransferFunctionFile = p4TransferFunctionFile
        if scaleTau:
            process.cmgTauMuCor.nSigma = scaleTau


    # OUTPUT definition ----------------------------------------------------------
    #process.outpath = cms.EndPath()

    if runOnMC:
        #        pass
        process.genEvtWeightsCounterPath = cms.Path(process.genEvtWeightsCounter)
#        process.schedule.insert(0, process.genEvtWeightsCounterPath)

    # Enable printouts like this:
    # process.cmgTauMuCorSVFitPreSel.verbose = True

    #oneFile = (channel == 'all')

    #if channel == 'tau-mu' or 'all' in channel:
    #    addTauMuOutput(process, debugEventContent, addPreSel=False, oneFile=oneFile)

    process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("test3.root"),
    outputCommands=cms.untracked.vstring('drop *')
    )

    eventContent = set(tauMuEventContent +
                           tauEleEventContent +
                           diTauEventContent +
                           muEleEventContent)

    process.out.outputCommands.extend(eventContent)
    process.outpath = cms.EndPath(process.out)

    if verbose:
        print sep_line
        print 'INPUT:'
        print sep_line
        print process.source.fileNames
        print
        # if not runOnMC:
        #     print 'json:', json
        print
        print sep_line
        print 'PROCESSING'
        print sep_line
        print 'runOnMC:', runOnMC
        print

    return process

if __name__ == '__main__':
    process = createProcess()

# process = createProcess()