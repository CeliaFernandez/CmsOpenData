import os
import logging
import ROOT

class Analyzer(object):
    """Base Analyzer class. 

    The custom analyzers should inherit from this class
    """
    def __init__(self):
        """Create an analyzer.
        Parameters (also stored as attributes for later use):
        cfg_ana: configuration parameters for this analyzer (e.g. a pt cut)
        cfg_comp: configuration parameters for the data or MC component (e.g. DYJets)
        looperName: name of the Looper which runs this analyzer.
        Attributes:
        dirName : analyzer directory, where you can write anything you want
        """
        self.file = ROOT.gROOT.GetListOfFiles().FindObject("mytree.root")
        if not self.file or not self.file.IsOpen():
            self.file = ROOT.TFile("datafiles/mytree.root", "read")
        self.tree = self.file.Get("muons")
        
        # Get the number of entries(events) of the TTree (file.root)
        self.numEntries=self.tree.GetEntries()
        # Initialize all datamembers (taken from the tree)
        self.Setup()

    def beginJob(self, name):
        '''Executed before the first object comes in'''

        print('*** Begin job')
        self.DefineHistograms()
        self.rootfile= ROOT.TFile("datafiles/"+name, "RECREATE") 

    def process(self, event):
        '''Executed on every event'''
        pass

    def endJob(self):
        ''' 
        Executed after the analysis to write the histograms in the root file
        '''
        print("*** writing file", self.rootfile)
        self.WriteHistograms()
        self.rootfile.Close()
        print("*** done")

    def Setup(self):
        '''
        Setup, init the variables for the particle and set 
        branch addresses
   
        '''
        self.relIso = -999. 

        self.tree.GetEntry(0)

        # Extract all branches and use it as datamembers of this class
        for br in self.tree.GetListOfBranches():
            setattr(self,br.GetName(),getattr(self.tree,br.GetName()))
        
    ### DEFINE AND FILL HISTOGRAMS ### 

    def DefineHistograms(self):
        '''Function that define the histograms for all and selected analyzers'''
        # Define and init the histograms for each branch as a TH1F object from ROOT

        self.h_MuonType=ROOT.TH1F('h_type', 'Number of Muons', 4, 1, 5)
        self.h_pt=ROOT.TH1F( 'h_pt', 'Muons Transverse Momentun', 50, 0, 200 )
        self.h_px=ROOT.TH1F( 'h_px', 'Muons x- Momentun', 50, -300, 300 )
        self.h_py=ROOT.TH1F( 'h_py', 'Muons y- Momentun', 50, -300, 300 )
        self.h_pz=ROOT.TH1F( 'h_pz', 'Muons z- Momentun', 50, -300, 300 )
        self.h_eta=ROOT.TH1F( 'h_eta', 'Angle Transvese', 50, -5 , 5 )
        self.h_energy=ROOT.TH1F('h_energy','Muons Energy', 50, -300,300)
        self.h_dz=ROOT.TH1F('h_dz','Distance from Primary vertex Z ', 50, -3,3)
        self.h_charge=ROOT.TH1F('h_charge','Muons Charge', 4,-2,2)
        self.h_normChi2=ROOT.TH1F('h_normChi2', 'Muons Chi2/ndof', 50, 0,100)
        self.h_numberOfValidHits=ROOT.TH1F('h_numberOfValidHits', 'Number of Valid Hits', 50, 0,50)
        self.h_numOfMatches=ROOT.TH1F('h_numOfMatches', 'Number of muon chambers matched',10, 0, 10)
        self.h_NValidHitsSATk=ROOT.TH1F('h_NValidHitsSATk', 'Number of hits in the muon chambers', 60, 0, 60)
        self.h_dB=ROOT.TH1F('h_dB','Impact Parameter',50,0,2)
        #self.h_edB=ROOT.TH1F('h_edB','Impact Parameter Error',50,-1,200) >> Pintar como barras de error en el histograma?
        self.h_isolation_sumPt=ROOT.TH1F('h_isolation_sumPt','Tracker Isolation',50, 0,300)
        self.h_isolation_emEt=ROOT.TH1F('h_isolation_emEt','ECAL Isolation',50, 0,300)
        self.h_isolation_hadEt=ROOT.TH1F('h_isolation_hadEt','HCAL Isolation',50, 0,300)
        self.h_isolation=ROOT.TH1F('h_isolation','Relative Isolation',50, 0,300)
        self.h_mass=ROOT.TH1F('h_mass', 'MassInv', 150, 0, 300)
     #   self.h_numOfMatches=ROOT.TH1F('h_numOfMatches', 'Number of matches in the Muon chambers', 8, 0, 8)

        
        
    def FillHistograms(self, particle):
       
        #self.relIso = self.Muon_isolation_hadEt[particle] + self.Muon_isolation_hadEt[particle] + self.Muon_isolation_sumPt[particle]/self.Muon_pt[particle]
        self.h_isolation.Fill((self.Muon_isolation_hadEt[particle] + self.Muon_isolation_hadEt[particle] + self.Muon_isolation_sumPt[particle])/self.Muon_pt[particle])
        '''Function that fill the histograms for each variable and particle in the event'''
        
        if self.Muon_isTrackerMuon[particle] == 1:
            self.h_MuonType.Fill(1)
            
        if self.Muon_isStandAloneMuon[particle] == 1:
            self.h_MuonType.Fill(2)

        if self.Muon_isGlobalMuon[particle] == 1: 
            self.h_MuonType.Fill(3)
        
        if self.Muon_isGlobalMuon[particle] == 1 and self.Muon_isTrackerMuon[particle] == 1: 
            self.h_MuonType.Fill(4)
        
        
        self.h_pt.Fill(self.Muon_pt[particle])
        self.h_px.Fill(self.Muon_px[particle])
        self.h_py.Fill(self.Muon_py[particle])
        self.h_pz.Fill(self.Muon_pz[particle])
        self.h_eta.Fill(self.Muon_eta[particle])
        self.h_energy.Fill(self.Muon_energy[particle])
        self.h_dz.Fill(self.Muon_distance[particle])
        self.h_charge.Fill(self.Muon_charge[particle])
        self.h_normChi2.Fill(self.Muon_normChi2[particle])
        self.h_numberOfValidHits.Fill(self.Muon_numberOfValidHits[particle])
        self.h_numOfMatches.Fill(self.Muon_numOfMatches[particle])
       	self.h_dB.Fill(self.Muon_dB[particle])
        self.h_isolation_sumPt.Fill(self.Muon_isolation_sumPt[particle])
       	self.h_isolation_emEt.Fill(self.Muon_isolation_emEt[particle])
        self.h_isolation_hadEt.Fill(self.Muon_isolation_hadEt[particle])
        self.h_NValidHitsSATk.Fill(self.Muon_NValidHitsSATk[particle])

                                   
    def WriteHistograms(self):
        '''Function to write Histograms: Neither mass nor efficiency
        Add here the histograms to print'''
        self.h_MuonType.Write()
        self.h_pt.Write()
        self.h_px.Write()
        self.h_py.Write()
        self.h_pz.Write()
        self.h_eta.Write()
        self.h_energy.Write()
        self.h_dz.Write()
        self.h_charge.Write()
        self.h_normChi2.Write()
        self.h_numberOfValidHits.Write()
        self.h_numOfMatches.Write()
        self.h_NValidHitsSATk.Write()
        self.h_dB.Write()
        self.h_isolation_sumPt.Write()
        self.h_isolation_emEt.Write()
        self.h_isolation_hadEt.Write()
        self.h_isolation.Write()
        #self_h_numOfMatches.Write()
        self.h_mass.Write()
