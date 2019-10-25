import os
import logging
import ROOT

from Analyzer import Analyzer

class AnalyzerAll(Analyzer):
    """Analyzer class for all muons. 

    """
    # Get the number of entries(events) of the TTree (file.root)
    # numEntries= tree.GetEntries()

    def process(self, event):
        '''Executed on every event'''
        self.tree.GetEntry(event)
        # Get the particles in the event
        for particle in range(self.Muon_pt.size()):
            # Fill histograms for each particle variable
            self.FillHistograms(particle)
            # Get the mass. ONLY if the events has more than 1 muon
            if self.Muon_pt.size()>1:
                for j in range(particle+1,self.Muon_pt.size()):
                    if (self.Muon_charge[particle]*self.Muon_charge[j])<0:
                        # get the Lorentz vector for the both muons through a ROOT function 
                        tlv1=ROOT.TLorentzVector()
                        tlv1.SetPxPyPzE(self.Muon_px[particle], self.Muon_py[particle], self.Muon_pz[particle],self.Muon_energy[particle])
                        
                        tlv2=ROOT.TLorentzVector()
                        tlv2.SetPxPyPzE(self.Muon_px[j], self.Muon_py[j], self.Muon_pz[j],self.Muon_energy[j])
                        
                        # Get the mass = (TLV Muon1 + TLV Muon2).M()
                        mass=(tlv1+tlv2).M()
                        # Fill the histogram for the mass
                        self.h_mass.Fill(mass)

