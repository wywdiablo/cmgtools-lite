import ROOT

import math

from itertools import product
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

#import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.Heppy.physicsutils.ElectronCalibrator import Run2ElectronCalibrator

import pprint
import itertools


mass = {23: 91.2, 25: 125.}

class LeptonSelector(Analyzer):

    def declareHandles(self):
        super(LeptonSelector, self).declareHandles()
        self.handles['muons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
            )

        self.handles['electrons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
            )

        self.handles['taus'] = AutoHandle(
                'slimmedTaus',
                'std::vector<pat::Tau>'
            )

     	self.handles['met'] = AutoHandle(
                'slimmedMETs',
                'std::vector<pat::MET>'
            )

        self.handles['metCov'] = AutoHandle(
                'METSignificance:METCovariance:H2TAUTAU',
                'ROOT::Math::SMatrix<double,2,2,ROOT::Math::MatRepSym<double,2>>'
            )


    def process(self, event):

        #read collection and map necessary objects

        super(LeptonSelector, self).readCollections(event.input)

        event.goodVertices = event.vertices

        muons = map(Muon, self.handles['muons'].product())  
        electrons = map(Electron, self.handles['electrons'].product())
        taus = map(Tau, self.handles['taus'].product())
        met = self.handles['met'].product()[0] 
        METSignificance = self.handles['metCov'].product()

        fillMatrix = False
        #if hasattr(met, 'getSignificanceMatrix'):
            #mvaMetSig = met.getSignificanceMatrix()
            #
        metcov00 = METSignificance[0][0]#mvaMetSig(0,0)
        metcov01 = METSignificance[0][1]#mvaMetSig(0,1)
        metcov10 = METSignificance[0][1] #met.getSignificanceMatrix[1][0]#mvaMetSig(1,0)
        metcov11 = METSignificance[1][1] #met.getSignificanceMatrix[1][1] #mvaMetSig(1,1)
        fillMatrix=True
 
        #set vertex for each candidate
        setVertex = []
        setVertex += muons
        setVertex += electrons
        setVertex += taus

        for leptoni in setVertex:
            leptoni.associatedVertex = event.goodVertices[0]

        if self.cfg_ana.doElectronScaleCorrections:
            conf = self.cfg_ana.doElectronScaleCorrections
            print conf['isSync']
            print conf['isMC']
            self.electronEnergyCalibrator = Run2ElectronCalibrator(
                conf['data'],
                conf['GBRForest'],
                conf['isMC'],
                conf['isSync'] if 'isSync' in conf else False,
            )

        for lep in electrons:
            lep.event = event.input.object()
        
        if self.cfg_ana.doElectronScaleCorrections:
            for lep in electrons:
                self.electronEnergyCalibrator.correct(lep, event.run)          

        setattr(event, 'nMuonsBEFORE', len(muons))
        setattr(event, 'nElectronsBEFORE', len(electrons))
        setattr(event, 'nTausBEFORE', len(taus))

        #ADD LATER ON: electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1

        #define good leptons, remove iso
        muonsGOOD = [ muon for muon in muons if muon.pt()>10 and abs(muon.eta())<2.4 and  abs(muon.dxy()) < 0.045 and abs(muon.dz()) < 0.2 and muon.muonID('POG_ID_Loose') and muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < 0.25]
        electronsGOOD = [ electron for electron in electrons if electron.pt()>10 and abs(electron.eta())<2.5 and abs(electron.dxy()) < 0.045 and abs(electron.dz()) < 0.2 and electron.mvaIDRun2('Spring16', 'POG90') and electron.passConversionVeto() and electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1]
        tausGOOD = [ tau for tau in taus if tau.pt()>18 and abs(tau.eta())<2.3 and tau.tauID('decayModeFinding') > 0.5 and abs(tau.leadChargedHadrCand().dz()) < 0.2 and tau.tauID('byMediumIsolationMVArun2v1DBoldDMwLT') > 0.5 and tau.tauID('againstElectronVLooseMVA6') > 0.5 and tau.tauID('againstMuonLoose3') > 0.5]

        if self.cfg_ana.applyIDISO:
            muons = [ muon for muon in muonsGOOD]
            electrons = [ electron for electron in electronsGOOD] # if electron.pt()>9 and abs(electron.eta())<2.5 and abs(electron.dxy()) < 0.045 and abs(electron.dz()) < 0.2 and electron.mvaIDRun2('Spring16', 'POG90') and electron.passConversionVeto() and electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3 and electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1]
            taus = [ tau for tau in tausGOOD] #if tau.pt()>20 and abs(tau.eta())<2.3 and tau.tauID('decayModeFinding') > 0.5 and abs(tau.leadChargedHadrCand().dz()) < 0.2 and tau.tauID('byMediumIsolationMVArun2v1DBoldDMwLT') > 0.5 and tau.tauID('againstElectronVLooseMVA6') > 0.5 and tau.tauID('againstMuonLoose3') > 0.5]     
        else:
            muons = [ muon for muon in muons if muon.pt()>9 and abs(muon.eta())<2.4 and abs(muon.dxy()) < 0.045 and abs(muon.dz()) < 0.2 and ( muon.isGlobalMuon() or muon.isTrackerMuon() )]
            electrons = [ electron for electron in electrons if electron.pt()>9 and abs(electron.eta())<2.5 and abs(electron.dxy()) < 0.045 and abs(electron.dz()) < 0.2 and electron.passConversionVeto() and electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1]
            taus = [ tau for tau in taus if tau.pt()>18 and abs(tau.eta())<2.3 and abs(tau.leadChargedHadrCand().dz()) < 0.2 and tau.tauID('decayModeFinding') > 0.5 and tau.tauID('againstElectronVLooseMVA6') > 0.5 and tau.tauID('againstMuonLoose3') > 0.5]

        leptons_me = []
        leptons_me += muons
        leptons_me += electrons
 
        setattr(event, 'nMuons', len(muons))
        setattr(event, 'nElectrons', len(electrons))
        setattr(event, 'nTaus', len(taus))

        setattr(event, 'muons', muons)
        setattr(event, 'electrons', electrons)
        setattr(event, 'taus', taus)
        setattr(event, 'met', met)

        if fillMatrix:
            setattr(event, 'metcov00', metcov00)
            setattr(event, 'metcov01', metcov01)
            setattr(event, 'metcov10', metcov10)
            setattr(event, 'metcov11', metcov11)
        #setattr(event, 'mvaMetSig', mvaMetSig)

        setattr(event, 'muonsGOOD', muonsGOOD)
        setattr(event, 'electronsGOOD', electronsGOOD)
        setattr(event, 'tausGOOD', tausGOOD)


        setattr(event, 'nMuonsGOOD', len(muonsGOOD))
        setattr(event, 'nElectronsGOOD', len(electronsGOOD))
        setattr(event, 'nTausGOOD', len(tausGOOD))

        #EXTRA LEPTON VETO

        #check how many electrons and muons we have 
        if ( len(muonsGOOD)+len(electronsGOOD) )<2 or ( len(muonsGOOD)+len(electronsGOOD) )>4:
            return False

        #we cannot have more than 3 electrons or 3 muons at this point anymore
        if ( len(muonsGOOD) > 3 ) or ( len(electronsGOOD) > 3):
            return False


        event.isSignal = True

        allLeptons = []
        allLeptons += muons
        allLeptons += electrons
        allLeptons += taus

        goodLeptons = []
        goodLeptons += muonsGOOD
        goodLeptons += electronsGOOD
        goodLeptons += tausGOOD

        setattr(event, 'allLeptons', len(allLeptons))
        setattr(event, 'selectedLeptons', allLeptons)
        setattr(event, 'goodLeptons', goodLeptons)

        #if len(allLeptons)!=3:
        #    fourLeptons = True
        #else:
        #    return False
           
	
