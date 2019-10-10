import os
import array

#from array import array
from ROOT import TMatrixD, std, TFile, TH1

from TauAnalysis.ClassicSVfit.MeasuredTauLepton import MeasuredTauLepton
from TauAnalysis.ClassicSVfit.ClassicSVfit import ClassicSVfit as SVfitAlgo

#from TauAnalysis.ClassicSVfit.svFitHistogramAdapter import svFitHistogramAdapter

#../../../TauAnalysis/ClassicSVfit/python/
#../../../SVfitStandalone/python/
##from CMGTools.TauAnalysis.ClassicSVfit.SVfitStandaloneAlgorithm import SVfitAlgoOld
#from CMGTools.SVfitStandalone.MeasuredTauLepton import measuredTauLepton


#import needed stuff

#TH1.AddDirectory(False)

#import os
#import array

from CMGTools.TTHAnalysis.treeReAnalyzer import *

class svFit_classic:
    def __init__(self, channel):
        self.branches = [ "A_vis", "A_Hscaled", "A_svFit", "A_svFit_scaled", "A_svFit_constrained",
                          "H_vis", "H_scaled", "H_svFit", "H_svFit_scaled" , "H_svFit_constrained" ]

        self.channel = channel
    def listBranches(self):
        return self.branches[:]

    def scaleMassPT(self, pt1, eta1, phi1, m1, pt2, eta2, phi2, m2, Mass2scale, scalePT=True ) :
        lorentz1 = ROOT.TLorentzVector( 0.,0.,0.,0. )
        lorentz1.SetPtEtaPhiM( pt1, eta1, phi1, m1 )
        lorentz2 = ROOT.TLorentzVector( 0.,0.,0.,0. )
        lorentz2.SetPtEtaPhiM( pt2, eta2, phi2, m2 )

        lorentz3 = ROOT.TLorentzVector( 0.,0.,0.,0. )

        if Mass2scale==91:
            scale = 91.2/(lorentz1 + lorentz2).M()
        else:
            scale = 125.06/(lorentz1 + lorentz2).M()
        phi = (lorentz1 + lorentz2).Phi()
        eta = (lorentz1 + lorentz2).Eta()
        pt = (lorentz1 + lorentz2).Pt()
        mass = (lorentz1 + lorentz2).M()

        if scalePT:
            lorentz3.SetPtEtaPhiM( scale*pt, eta, phi, scale*mass )
        else:
            lorentz3.SetPtEtaPhiM( pt, eta, phi, scale*mass )

        return lorentz3

    def __call__(self,event):
        #(met, metphi)  = event.met, event.met_phi
        # prepare output
        ret = dict([(name,0.0) for name in self.branches])

        ##Get Z boson
        ptZ = event.Z_Pt
        etaZ = event.Z_Eta
        phiZ = event.Z_Phi
        mZ = event.m_vis

        Zunscaled = ROOT.TLorentzVector( 0.,0.,0.,0. )
        Zunscaled.SetPtEtaPhiM( ptZ, etaZ, phiZ, mZ )

        ptZ2 = ptZ + 100

       	ZTESTI = ROOT.TLorentzVector( 0.,0.,0.,0. )
        ZTESTI.SetPtEtaPhiM( ptZ2, etaZ, phiZ, mZ )


        print "Testing: mZ and Zunscaled", mZ, Zunscaled.M(), ptZ, ptZ2, ZTESTI.M()


        #Fetch Higgs legs 
        pt3 = event.pt_3
        eta3 = event.eta_3
        phi3 = event.phi_3
        m3 = event.m_3
        

        pt4 = event.pt_4
        eta4 = event.eta_4
        phi4 = event.phi_4
        m4 = event.m_4

        DM3 = -1
        DM4 = -1

        if self.channel=="EETT" or self.channel=="MMTT":
            DM3 = int(event.decayMode_3)
            DM4 = int(event.decayMode_4)  
        elif self.channel=="EEET" or self.channel=="MMET" or self.channel=="EEMT" or self.channel=="MMMT":
            DM3 = -1                    
            DM4 = int(event.decayMode_4)

        #Add here the final state if sentences... for types
        if self.channel=="EETT" or self.channel=="MMTT":
            l1type = 1
            l2type = 1
        if self.channel=="EEET" or self.channel=="MMET":
            l1type = 2
            l2type = 1
       	    m3 = 0.51100e-3  # PDG mass [GeV]
        if self.channel=="EEMT" or self.channel=="MMMT":
            l1type = 3
            l2type = 1
       	    m3 = 0.10566 # PDG mass [GeV]        
        if self.channel=="EEEM" or self.channel=="MMEM":
            l1type = 2
            l2type = 3
            m3 = 0.51100e-3  # PDG mass [GeV]
       	    m4 = 0.10566    # PDG mass [GeV]
	
        

        ptH = event.H_Pt
        etaH = event.H_Eta
        phiH = event.H_Phi

        #unscaled values
        mH = event.H_vis
        mA = event.Mass
        ##print "Okayokay"
        ret["H_vis"] = mH
        ret["A_vis"] = mA

        #Get 4-vectors and fill output
        scalePT = True
        Hscaledpt = self.scaleMassPT( pt3, eta3, phi3, m3, pt4, eta4, phi4, m4, 125, scalePT )
       
        #print "juhu"
        ret["H_scaled"] = Hscaledpt.M()
        #print "moi"
        ret["A_Hscaled"] = (Zunscaled+Hscaledpt).M()

        #H legs
        #print "OKOK"
        #catch types

 
        #print "JEP"
        leg1 = MeasuredTauLepton(l1type, pt3, eta3, phi3, m3, DM3)
        leg2 = MeasuredTauLepton(l2type, pt4, eta4, phi4, m4, DM4)

        measuredLeptons = std.vector('classic_svFit::MeasuredTauLepton')()

        ## RIC: not really needed since SVfit internally sorts the inputs
        #if hasattr(self.cfg_ana, 'order') and self.cfg_ana.order == '12':
        #    measuredLeptons.push_back(leg1)
        #    measuredLeptons.push_back(leg2)
        #else:
        measuredLeptons.push_back(leg2)
        measuredLeptons.push_back(leg1)

        #      print measuredLeptons        

        #Here you take the covariance matrix   
        cov00 = event.metcov00
        cov01 = event.metcov01
        cov11 = event.metcov11


        metcov = TMatrixD(2, 2)
    
        a_metcov = array('d', [cov00, cov01, cov01, cov11])
        
        #print "matrix toimi"
        metcov.SetMatrixArray(a_metcov)

        mex = event.met_px
        mey = event.met_py

        svfit = SVfitAlgo(0)

        if self.channel=="EETT" or self.channel=="MMTT":      
            svfit.addLogM_fixed(True, 5.)
        elif self.channel=="EEMT" or self.channel=="MMMT" or self.channel=="EEET" or self.channel=="MMET":
            svfit.addLogM_fixed(True, 4.)
        elif self.channel=="EEEM" or self.channel=="MMEM":
            svfit.addLogM_fixed(True, 3.)

        svfit.integrate(measuredLeptons, mex, mey, metcov)

        #elif self.cfg_ana.integration == 'MarkovChain':
        #    svfit.integrateMarkovChain()
        #else:
        #    print 'The integration method must be defined in the cfg as "integration".'
        #    print 'Options: [VEGAS, MarkovChain]'
        #    raise

        # debug
        #if self.cfg_ana.verbose:
        #    if abs(event.diLepton.svfitMass()-svfit.mass()) > 0.01:
        #        print 'WARNING: run {RUN}, lumi {LUMI}, event {EVT}'.format(RUN=str(event.run),
        #                                                                    LUMI=str(event.lumi),
        #                                                                    EVT=str(event.eventId))
        #        print 'precomputed svfit mass   ', event.diLepton.svfitMass()
        #        print 'svfit mass computed here ', svfit.mass()

        # method override
        ##print "uuusi"
        m_sV = svfit.getHistogramAdapter().getMass()
        pt_sV = svfit.getHistogramAdapter().getPt()
        eta_sV = svfit.getHistogramAdapter().getEta()
        phi_sV =  svfit.getHistogramAdapter().getPhi()

        HsvFit = ROOT.TLorentzVector( 0.,0.,0.,0. )
        HsvFit.SetPtEtaPhiM( pt_sV, eta_sV, phi_sV, m_sV )
      
        ##print "m_SV and HsFIT:", m_sV, HsvFit.M()

        ret["H_svFit"] = HsvFit.M()
        ret["A_svFit"] = (Zunscaled+HsvFit).M()


        #scale mass here
        if m_sV!=0.0:
            scale = 125.06/m_sV
        else:
            scale = 0.0
        HsvFit_scaled = ROOT.TLorentzVector( 0.,0.,0.,0. )
        HsvFit_scaled.SetPtEtaPhiM( scale*pt_sV, eta_sV, phi_sV, scale*m_sV )
         
        ret["H_svFit_scaled"] = HsvFit_scaled.M()
        ret["A_svFit_scaled"] = (Zunscaled+HsvFit_scaled).M()


        massConstraint = 125.06
        svfit.setDiTauMassConstraint(massConstraint);
        svfit.integrate(measuredLeptons, mex, mey, metcov)

        H_constrained = svfit.getHistogramAdapter().getMass()
        pt_sV_constrained = svfit.getHistogramAdapter().getPt()
        eta_sV_constrained = svfit.getHistogramAdapter().getEta()
        phi_sV_constrained =  svfit.getHistogramAdapter().getPhi()
        
        HsvFit_constrained = ROOT.TLorentzVector( 0.,0.,0.,0. )
        HsvFit_constrained.SetPtEtaPhiM( pt_sV_constrained, eta_sV_constrained, phi_sV_constrained, H_constrained )

        ret["H_svFit_constrained"] = HsvFit_constrained.M()
        ret["A_svFit_constrained"] = (Zunscaled+HsvFit_constrained).M()


        return ret


###MODULES = [ ( 'svFit_classicEETT', lambda : svFit_classic("EETT") ), ]
MODULES = [
 ( 'svFit_classicEETT', lambda : svFit_classic("EETT") ),
 ( 'svFit_classicEEET', lambda : svFit_classic("EEET") ),
 ( 'svFit_classicEEEM', lambda : svFit_classic("EEEM") ),
 ( 'svFit_classicEEMT', lambda : svFit_classic("EEMT") ),
 ( 'svFit_classicMMTT', lambda : svFit_classic("MMTT") ),
 ( 'svFit_classicMMET', lambda : svFit_classic("MMET") ),
 ( 'svFit_classicMMEM', lambda : svFit_classic("MMEM") ),
 ( 'svFit_classicMMMT', lambda : svFit_classic("MMMT") ) ]


if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = svFit_classic()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d" % (ev.run, ev.lumi, ev.evt)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)


