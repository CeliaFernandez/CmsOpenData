import os
import logging
import ROOT

from Analyzer import Analyzer
#import Selec

class AnalyzerSel(Analyzer):
    """Selection Analyzer class. 
    The custom analyzers should inherit from this class
    """
    def DefineHistograms(self):
        Analyzer.DefineHistograms(self)
        #Add histograms for the mass and efficiency
        self.h_efficiency=ROOT.TH1F('h_efficiency','efficiency',11,1,12)
        print("efficiency defined")

    def process(self, event,selector):
        '''Executed on every event'''
        self.tree.GetEntry(event)
        
        #selec = Selector()
        for particle in range(0,self.Muon_pt.size()):
            # Fill the histogram for each variable
            self.h_efficiency.Fill(1)
            # Get the mass. ONLY if the events has more than 1 muon
            if (self.Muon_pt.size()) > 1:
                for j in range (particle+1,self.Muon_pt.size()):
                    if (self.Muon_charge[particle]*self.Muon_charge[j])<0:
                        # get the Lorentz vector for the both muons through a ROOT function 
                        tlv1=ROOT.TLorentzVector()
                        tlv1.SetPxPyPzE(self.Muon_px[particle], self.Muon_py[particle], self.Muon_pz[particle],self.Muon_energy[particle])
                        
                        tlv2=ROOT.TLorentzVector()
                        tlv2.SetPxPyPzE(self.Muon_px[j], self.Muon_py[j], self.Muon_pz[j],self.Muon_energy[j])
                        
                        # Get the mass = (TLV Muon1 + TLV Muon2).M()
                        mass=(tlv1+tlv2).M()
                        #print mass
                        
                        # If the both muons are selected between the cuts fill the histogram 
                        if selector.selector(self,particle) and selector.selector(self, j):
                            self.h_mass.Fill(mass)
                            
            # Apply the selection over all particles in the event calling the selector function and fill the histograms for each variable
            if selector.selector(self, particle):
                    self.FillHistograms(particle)


    def endJob(self):
        self.h_efficiency.Write()
        Analyzer.endJob(self)
