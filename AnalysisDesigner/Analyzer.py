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
        
        # Define aliases for mass and isolation
        self.tree.SetAlias("MuonPair_mass", "((Muon_energy[0]+Muon_energy[1])**2 - (Muon_px[0]+Muon_px[1])**2 - (Muon_py[0]+Muon_py[1])**2 - (Muon_pz[0]+Muon_pz[1])**2)**(0.5)") 
        self.tree.SetAlias("Muon_relIso", "(Muon_isolation_hadEt + Muon_isolation_emEt + Muon_isolation_sumPt)/Muon_pt")
        
        # Get the number of entries(events) of the TTree (file.root)
        self.numEntries=self.tree.GetEntries()
        # Initialize all datamembers (taken from the tree)
        self.Setup()

    def beginJob(self):
        '''Executed before the first object comes in'''

        print('*** Begin job')
        self.DefineHistograms()
        #self.h_efficiency=ROOT.TH1F('h_efficiency','efficiency',11,1,12)

    def process(self, event):
        '''Executed on every event'''
        pass

    def endJob(self, name):
        ''' 
        Executed after the analysis to write the histograms in the root file
        '''
        self.rootfile= ROOT.TFile("datafiles/"+name, "RECREATE") 
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

        self.h_MuonType=ROOT.TH1F('h_type', 'Number of Muons;Muon type;Number of muons', 4, 1, 5)
        self.h_MuonType1=ROOT.TH1F( 'h_type1', 'Tracker muons', 4, 1, 5)
        self.h_MuonType2=ROOT.TH1F( 'h_type2', 'StandAlone muons', 4, 1, 5)
        self.h_MuonType3=ROOT.TH1F( 'h_type3', 'Global muons', 4, 1, 5)
        self.h_MuonType4=ROOT.TH1F( 'h_type4', 'Tracker or global muons', 4, 1, 5)
        self.h_pt=ROOT.TH1F( 'h_pt', 'Muons Transverse Momentun; Muon transverse momentum p_{T} (GeV); Number of muons', 50, 0, 200 )
        self.h_px=ROOT.TH1F( 'h_px', 'Muons x- Momentun; Muon momentum p_{x} (GeV); Number of muons', 50, -300, 300 )
        self.h_py=ROOT.TH1F( 'h_py', 'Muons y- Momentun; Muon momentum p_{y} (GeV); Number of muons', 50, -300, 300 )
        self.h_pz=ROOT.TH1F( 'h_pz', 'Muons z- Momentun; Muon momentum p_{z} (GeV); Number of muons', 50, -300, 300 )
        self.h_eta=ROOT.TH1F( 'h_eta', 'Pseudorapidity; Muon pseudorapidity #eta; Number of muons', 50, -5 , 5 )
        self.h_energy=ROOT.TH1F('h_energy','Muons Energy; Muon energy E (GeV); Number of muons', 50, -300,300)
        self.h_dz=ROOT.TH1F('h_dz','Distance from Primary vertex Z; Muon distance d_{z} (cm); Number of muons', 50, -3,3)
        self.h_charge=ROOT.TH1F('h_charge','Muons Charge; Muon charge q; Number of muons', 4,-2,2)
        self.h_normChi2=ROOT.TH1F('h_normChi2', 'Muons Chi2/ndof; Muon track #chi^{2}/ndof; Number of muons', 50, 0,100)
        self.h_numberOfValidHits=ROOT.TH1F('h_numberOfValidHits', 'Number of Valid Hits; Number of valid hits; Number of muons', 50, 0,50)
        self.h_numOfMatches=ROOT.TH1F('h_numOfMatches', 'Number of muon chambers matched; Number of matched muon chambers; Number of muons',10, 0, 10)
        self.h_NValidHitsSATk=ROOT.TH1F('h_NValidHitsSATk', 'Number of hits in the muon chambers; Number of hits in the muon chambers; Number of muons', 60, 0, 60)
        self.h_dB=ROOT.TH1F('h_dB','Impact Parameter; Muon transverse impact parameter |d_{xy}| (cm); Number of muons',50,0,2)
        self.h_isolation_sumPt=ROOT.TH1F('h_isolation_sumPt','Muon tracker Isolation; Number of muons',50, 0,300)
        self.h_isolation_emEt=ROOT.TH1F('h_isolation_emEt','Muon ECAL Isolation; Number of muons',50, 0,300)
        self.h_isolation_hadEt=ROOT.TH1F('h_isolation_hadEt','Muon HCAL Isolation; Number of muons',50, 0,300)
        self.h_isolation=ROOT.TH1F('h_isolation','Muon relative Isolation; Number of muons',50, 0,300)
        self.h_mass=ROOT.TH1F('h_mass', 'Invariant mass; Invariant mass m_{#mu#mu} (GeV); Events', 150, 0, 300)

        
        
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
        
    def FillHistogramsFromTree(self, cuts = False):
        
        if cuts:
            selection_all = cuts.fullSelection()     # selection applied in all muons
            selection_0   = cuts.fullSelection("0")  # selection applied in leading muon
            selection_1   = cuts.fullSelection("1")  # selection applied in subleading muon
        else:
            selection_all = "1"
            selection_0   = "1"
            selection_1   = "1"
        
        selection_pair = selection_0 + " && " + selection_1 + " && (Muon_charge[0]*Muon_charge[1] < 0)"
        
        self.tree.Project("h_type1", "1*(Muon_isTrackerMuon)", selection_all)
        self.tree.Project("h_type2", "2*(Muon_isStandAloneMuon)", selection_all)
        self.tree.Project("h_type3", "3*(Muon_isGlobalMuon)", selection_all)
        self.tree.Project("h_type4", "4*(Muon_isTrackerMuon && Muon_isGlobalMuon)", selection_all)
        print("> h_type filled (1/19)")
        self.tree.Project("h_pt", "Muon_pt", selection_all)
        print("> h_pt filled (2/19)")
        self.tree.Project("h_px", "Muon_px", selection_all)
        print("> h_px filled (3/19)")
        self.tree.Project("h_py", "Muon_py", selection_all)
        print("> h_py filled (4/19)")
        self.tree.Project("h_pz", "Muon_pz", selection_all)
        print("> h_pz filled (5/19)")
        self.tree.Project("h_eta", "Muon_eta", selection_all)
        print("> h_eta filled (6/19)")
        self.tree.Project("h_energy", "Muon_energy", selection_all)
        print("> h_energy filled (7/19)")
        self.tree.Project("h_dz", "Muon_distance", selection_all)
        print("> h_dz filled (8/19)")
        self.tree.Project("h_charge", "Muon_charge", selection_all)
        print("> h_charge filled (9/19)")
        self.tree.Project("h_normChi2", "Muon_normChi2", selection_all)
        print("> h_normChi2 filled (10/19)")
        self.tree.Project("h_numberOfValidHits", "Muon_numberOfValidHits", selection_all)
        print("> h_numberOfValidHits filled (11/19)")
        self.tree.Project("h_numOfMatches", "Muon_numOfMatches", selection_all)
        print("> h_numOfMatches filled (12/19)")
        self.tree.Project("h_NValidHitsSATk", "Muon_NValidHitsSATk", selection_all)
        print("> h_NValidHitsSATk filled (13/19)")
        self.tree.Project("h_dB", "Muon_dB", selection_all)
        print("> h_dB filled (14/19)")
        self.tree.Project("h_isolation_sumPt", "Muon_isolation_sumPt", selection_all)
        print("> h_isolation_sumPt (15/19)")
        self.tree.Project("h_isolation_emEt", "Muon_isolation_emEt", selection_all)
        print("> h_isolation_emEt filled (16/19)")
        self.tree.Project("h_isolation_hadEt", "Muon_isolation_hadEt", selection_all)
        print("> h_isolation_hadEt filled (17/19)")
        self.tree.Project("h_isolation", "(Muon_isolation_hadEt + Muon_isolation_emEt + Muon_isolation_sumPt)/Muon_pt", selection_all)
        print("> h_isolation filled (18/19)")
        self.tree.Project("h_mass", "MuonPair_mass", selection_pair)
        print("> h_mass filled (19/19)")
       
            
    def FillEfficiency(self, efficiency, sequence):
        self.h_aux=ROOT.TH1F('h_aux', 'Auxiliar', 1, 0, 1000)
        for c,cut in enumerate(sequence):
            self.tree.Draw("Muon_pt>>h_aux", cut)
            efficiency.SetBinContent(c+1, self.h_aux.GetEntries())

                                   
    def WriteHistograms(self):
        '''Function to write Histograms: Neither mass nor efficiency
        Add here the histograms to print'''
        self.h_MuonType.Add(self.h_MuonType1)
        self.h_MuonType.Add(self.h_MuonType2)
        self.h_MuonType.Add(self.h_MuonType3)
        self.h_MuonType.Add(self.h_MuonType4)
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
        self.h_mass.Write()
