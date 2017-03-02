import ROOT

import math

from itertools import product
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2
from PhysicsTools.Heppy.physicsobjects.Particle import Particle

import pprint
import itertools


mass = {23: 91., 25: 125.}

class Resonance(Particle):
    '''Resonance decaying into 2 particles.
    The interface of this class mimics the interface of the CMS Candidate class.
    In this way Resonance objects or CMS Candidate objects can be processed
    transparently.
    '''

    def __init__(self, leg1, leg2, met, pdgid, status=3):
        '''
	Parameters (stored as attributes):
        leg1,2 : first and second leg.
        pdgid  : pdg code of the resonance
        status : status code of the resonance
        '''
	self._leg1 = leg1
        self._leg2 = leg2
        self._p4 = leg1.p4() + leg2.p4() #+ met.p4()
        if met!=None:             
            self._met = met
        else:
            print 'Z selvasti, met none'
        self._charge = leg1.charge() + leg2.charge()
        self._pdgid = pdgid
        self._status = status

    def p4(self):
        return self._p4

    def leg1(self):
        return self._leg1

    def leg2(self):
        return self._leg2

    def pt(self):
        return self._p4.pt()

    def energy(self):
        return self._p4.energy()

    def eta(self):
        return self._p4.eta()

    def phi(self):
        return self._p4.phi()

    def mass(self):
        return self._p4.mass()

    def charge(self):
        return self._charge

    def pdgId(self):
        return self._pdgid

    def met(self):
        return self._met

    def svfitMass(self):
        return -999.

    def svfitTransverseMass(self):
        return -999.

    def svfitMassError(self):
        return -999.

    def svfitPt(self):
        return -999.

    def svfitPtError(self):
        return -999.

    def svfitEta(self):
        return -999.

    def svfitPhi(self):
        return -999.

    def __getattr__(self, name):
        '''Redefine getattr to original version.'''
        raise AttributeError


class AZhAnalyzer(Analyzer):

    def declareHandles(self):
        super(AZhAnalyzer, self).declareHandles()
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


    def testDeltaR(self, leg1, leg2, dR_value):
        '''returns True if the two diLepton.leg1() and .leg2() have a delta R larger than the dR_min parameter.'''
        dR = deltaR(leg1.eta(), leg1.phi(),
                    leg2.eta(), leg2.phi())
        return dR > dR_value

    def constructZboson(self, collection, deltaR_min, event):
        '''Constructs all possible Z bosons using the given collection, and returns the candidate that has the mass the closest to the Z mass.'''

        Z_bosons=[]
        resonances=[]
        event.goodVertices = event.vertices

        for leg1, leg2 in itertools.combinations(collection,2):
            if leg1.pt()>20 or leg2.pt()>20:
                if leg2.pt()>leg1.pt():
                    print 'moi, kato taa'
                    print leg1
                    print leg2
                    leg_dummy=leg1
                    leg1=leg2
                    leg2=leg_dummy
                    print leg_dummy
                    print leg1
                    print leg2
                leg1.associatedVertex = event.goodVertices[0]
                leg2.associatedVertex = event.goodVertices[0]
                if (leg1.charge()+leg2.charge())==0 and abs(leg1.dxy()) < 0.045 and abs(leg1.dz()) < 0.2 and abs(leg2.dxy()) < 0.045 and abs(leg2.dz()) < 0.2 and self.testDeltaR(leg1, leg2, deltaR_min):
                    resonances.append( Resonance(leg1, leg2, None, 23, 3) )
    
        nominal_mass = mass[23]
        resonances.sort(key=lambda x: abs(x.mass()-nominal_mass))

        print 'massat:'
        for bosoni in resonances:
            print bosoni.mass()

        if resonances:
            if 60 <= resonances[0].mass() <= 120:
                Z_bosons.append(resonances[0])
        
        return Z_bosons

    def constructHbosonLepTau(self, leptons, taus, deltaR_min, event):
        '''Constructs all possible H bosons using the given collections for leptons and taus, and returns the candidate that has the mass the closest to the H mass.'''

        H_bosons=[]
        print 'NYT LEPTAU'
        event.goodVertices = event.vertices
        Zleg1=event.Zboson[0].leg1()
        Zleg2=event.Zboson[0].leg2()
        met=event.met

        for lepton in leptons:
            print 'leptoni:'
            print lepton
            if lepton==Zleg1 or lepton==Zleg2:
                print 'OLI KAYTETTY'
                print Zleg1
                print Zleg2
                print '----'
                continue 
            for tau in taus:
                if tau.pt()>21:
                    lepton.associatedVertex = event.goodVertices[0]
                    tau.associatedVertex = event.goodVertices[0]
                    if abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2:
                        di_tau = Resonance(lepton, tau, met, 25, 3)
                        di_tau.mvaMetSig = None
                        if di_tau.charge()==0 and self.testDeltaR(lepton, tau, deltaR_min):
                           print 'VARAUS OK TAULLA'
                           H_bosons.append(di_tau)
                                  
        nominal_mass = mass[25]
        H_bosons.sort(key=lambda x: abs(x.mass()-nominal_mass))

        print 'massat:'
        for bosoni in H_bosons:
            print bosoni.mass()

        return H_bosons

    def constructHbosondiTau(self, collection, deltaR_min, event):
        '''Constructs all possible H bosons using the given tau collections, and returns the candidate that has the mass the closest to the H mass.'''

        H_bosons=[]
        print 'NYT TAUTAU'
        event.goodVertices = event.vertices
        #Zleg1=event.Zboson[0].leg1()
        #Zleg2=event.Zboson[0].leg2()
        met=event.met
 
        for leg1, leg2 in itertools.combinations(collection,2):
            if leg1.pt()>21 and leg2.pt()>21:
                if leg2.pt()>leg1.pt():
                    print 'moi, kato taa'
                    print leg1
                    print leg2
                    leg_dummy=leg1
                    leg1=leg2
                    leg2=leg_dummy
                    print leg_dummy
                    print leg1
                    print leg2
                    print '------'
                leg1.associatedVertex = event.goodVertices[0]
                leg2.associatedVertex = event.goodVertices[0]
                di_tau = Resonance(leg1, leg2, met, 25, 3)
                di_tau.mvaMetSig = None
                if di_tau.charge()==0 and self.testDeltaR(leg1, leg2, deltaR_min):
                    print 'VARAUS OK TAULLA'
                    H_bosons.append(di_tau)

        nominal_mass = mass[25]
        H_bosons.sort(key=lambda x: abs(x.mass()-nominal_mass))

        print 'massat:'
        for bosoni in H_bosons:
            print bosoni.mass()

        return H_bosons

    def constructHbosonEleMu(self, electrons, muons, deltaR_min, event):
        '''Constructs all possible H bosons using the given collections for muons and electrons, and returns the candidate that has the mass the closest to the H mass.'''

        H_bosons=[]
        print 'NYT ELEMU'
        event.goodVertices = event.vertices
	Zleg1=event.Zboson[0].leg1()
        Zleg2=event.Zboson[0].leg2()
        met=event.met

        for electron in electrons:
            print 'electron:'
            print electron
            if electron==Zleg1 or electron==Zleg2:
                print 'ELECTRON OLI KAYTETTY'
                print Zleg1
                print Zleg2
                print '----'
                continue
            for muon in muons:
                if muon==Zleg1 or muon==Zleg2:
                    print 'MUON OLI KAYTETTY'
                    print Zleg1
                    print Zleg2
                    print '----'
                    continue
                electron.associatedVertex = event.goodVertices[0]
                muon.associatedVertex = event.goodVertices[0]
                if abs(electron.dxy()) < 0.045 and abs(electron.dz()) < 0.2 and abs(muon.dxy()) < 0.045 and abs(muon.dz()) < 0.2 and self.testDeltaR(electron, muon, deltaR_min):
                        di_tau = Resonance(electron, muon, met, 25, 3)
                        di_tau.mvaMetSig = None
                        if di_tau.charge()==0:
                           print 'VARAUS OK TAULLA'
                           H_bosons.append(di_tau)

        nominal_mass = mass[25]
        H_bosons.sort(key=lambda x: abs(x.mass()-nominal_mass))

        print 'massat:'
        for bosoni in H_bosons:
            print bosoni.mass()

        return H_bosons


    def process(self, event):

        #read collection and map necessary objects

        super(AZhAnalyzer, self).readCollections(event.input)

        event.goodVertices = event.vertices

        muons = map(Muon, self.handles['muons'].product())  
        electrons = map(Electron, self.handles['electrons'].product())
        taus = map(Tau, self.handles['taus'].product())
        met = self.handles['met'].product()[0]

        setattr(event, 'nMuonsBEFORE', len(muons))
        setattr(event, 'nElectronsBEFORE', len(electrons))
        setattr(event, 'nTausBEFORE', len(taus))

        event.isSignal = True

        #maybe not needed?
        setattr(event, 'muons', muons)
        setattr(event, 'electrons', electrons)
        setattr(event, 'taus', taus) 
        setattr(event, 'met', met)

        #make pt and eta cuts
        muons = [ muon for muon in muons if muon.pt()>10 and abs(muon.eta())<2.4]
        electrons = [ electron for electron in electrons if electron.pt()>10 and abs(electron.eta())<2.5]
        taus = [ tau for tau in taus if tau.pt()>10 and abs(tau.eta())<2.3]

        setattr(event, 'nMuonsPtEta', len(muons))
        setattr(event, 'nElectronsPtEta', len(electrons))
        setattr(event, 'nTausPtEta', len(taus))

        #event.goodVertices = event.vertices

        #make iso cut

        muons = [ muon for muon in muons if muon.pt()>10 and abs(muon.eta())<2.4 and muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < 0.15]
        electrons = [ electron for electron in electrons if electron.pt()>10 and abs(electron.eta())<2.5 and electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.1]
        taus = [ tau for tau in taus if tau.pt()>10 and abs(tau.eta())<2.3 and tau.tauID('byTightIsolationMVArun2v1DBoldDMwLT') > 0.5]

        setattr(event, 'nMuonsPtEtaIso', len(muons))
        setattr(event, 'nElectronsPtEtaIso', len(electrons))
       	setattr(event, 'nTausPtEtaIso', len(taus))

        #make the final cuts cuts
        muons = [ muon for muon in muons if muon.pt()>10 and abs(muon.eta())<2.4 and muon.muonID('POG_ID_Medium_ICHEP') and muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < 0.15] 
        electrons = [ electron for electron in electrons if electron.pt()>10 and abs(electron.eta())<2.5 and electron.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90') and electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.1]
 #electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and electron.passConversionVeto() and electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.1]
        taus = [ tau for tau in taus if tau.pt()>10 and abs(tau.eta())<2.3 and tau.tauID('byTightIsolationMVArun2v1DBoldDMwLT') > 0.5 and tau.tauID('againstElectronVLooseMVA6') > 0.5 and tau.tauID('againstMuonTight3') > 0.5]

        print 'LENGTHS:'
        print len(muons)
        print len(electrons)
        print len(taus)

        setattr(event, 'nMuons', len(muons))
        setattr(event, 'nElectrons', len(electrons))
        setattr(event, 'nTaus', len(taus))
        
        #construct the Z boson here

        Z_muons = self.constructZboson(muons, 0.3, event)
        Z_electrons = self.constructZboson(electrons, 0.5, event)

        Z_resonance = []

        if Z_muons and Z_electrons:
            print 'There is two muons and two electrons, empty them to reject this!'
            Z_muons = []
            Z_electrons = []
        elif Z_muons and not Z_electrons:
            print 'Nyt muoneista!'
            Z_resonance.append(Z_muons[0])
        elif not Z_muons and Z_electrons:
            print 'Nyt elektroneista!'
            Z_resonance.append(Z_electrons[0])
        else:
            print 'No Z bosons!'     

        setattr(event, 'Zboson_mm', Z_muons)
        setattr(event, 'Zboson_ee', Z_electrons) 
        setattr(event, 'Zboson', Z_resonance)
            
        #construct the H boson here if there is a good Z candidate:

        H_resonance=[]      
        H_muTau = []
        H_eleTau = []
        H_diTau = []
        H_eleMu = []

        if Z_muons and Z_electrons:
            print 'There is two muons and two electrons, empty them to reject this!'
            Z_muons = []
            Z_electrons = []
            Z_resonance= []

        if Z_resonance:
            print 'paino olo'
            print Z_resonance[0].mass()
            Zleg1=Z_resonance[0].leg1()
            Zleg2=Z_resonance[0].leg2() 
            print Zleg1
            print Zleg2      
            print '--------END------'
            print 'MENNAAN RAKENTAMAAN BOSONI'
            if Z_muons:
                if len(muons)==3 and len(electrons)==0 and len(taus)==1:
                    H_muTau = self.constructHbosonLepTau(muons, taus, 0.5, event)
                    if H_muTau:
                        for i in range (0,len(H_muTau)):
                            H_resonance.append(H_muTau[i])
                if len(muons)==2 and len(electrons)==1 and len(taus)==1:
                    H_eleTau = self.constructHbosonLepTau(electrons, taus, 0.5, event)
                    if H_eleTau:
                        for i in range (0,len(H_eleTau)):
                            H_resonance.append(H_eleTau[i])
                if len(muons)==2 and len(electrons)==0 and len(taus)==2:
                    H_diTau = self.constructHbosondiTau(taus, 0.5, event)
                    if H_diTau:
                        for i in range (0,len(H_diTau)):
                            H_resonance.append(H_diTau[i])
                if len(muons)==3 and len(electrons)==1 and len(taus)==0:
                    H_eleMu = self.constructHbosonEleMu(electrons, muons, 0.5, event)
                    if H_eleMu:
                        for i in range (0,len(H_eleMu)):
                            H_resonance.append(H_eleMu[i])
            if Z_electrons:
                if len(muons)==1 and len(electrons)==2 and len(taus)==1:
                    H_muTau = self.constructHbosonLepTau(muons, taus, 0.5, event)
                    if H_muTau:
                        for i in range (0,len(H_muTau)):
                            H_resonance.append(H_muTau[i])
                if len(muons)==0 and len(electrons)==3 and len(taus)==1:
                    H_eleTau = self.constructHbosonLepTau(electrons, taus, 0.5, event)
                    if H_eleTau:
                        for i in range (0,len(H_eleTau)):
                            H_resonance.append(H_eleTau[i])
                if len(muons)==0 and len(electrons)==2 and len(taus)==2:
                    H_diTau = self.constructHbosondiTau(taus, 0.5, event)
                    if H_diTau:
                        for i in range (0,len(H_diTau)):
                            H_resonance.append(H_diTau[i])
                if len(muons)==1 and len(electrons)==3 and len(taus)==0:
                    H_eleMu = self.constructHbosonEleMu(electrons, muons, 0.5, event)
                    if H_eleMu:
                        for i in range (0,len(H_eleMu)):
                            H_resonance.append(H_eleMu[i])

        if H_resonance:
            print 'NYT ON HIGGS MYOS'
            pituus = len(H_resonance)
            print 'pituus: %d' %pituus
            for i in range (0,len(H_resonance)):
                print H_resonance[i].mass()
 
        setattr(event, 'Hboson', H_resonance)
        setattr(event, 'Hboson_mt', H_muTau)
        setattr(event, 'Hboson_et', H_eleTau)
        setattr(event, 'Hboson_tt', H_diTau)
        setattr(event, 'Hboson_em', H_eleMu)

        #construct the A boson here

        A_resonance=[]

        if Z_resonance and H_resonance:
            print 'contstruct A'
            Aboson = Resonance(H_resonance[0], Z_resonance[0], met, 36, 3)
            if 220<=Aboson.mass()<=350:
                print 'OK, AN MASSA'
                print Aboson.mass()
                A_resonance.append(Aboson)
        
        setattr(event, 'Aboson', A_resonance)