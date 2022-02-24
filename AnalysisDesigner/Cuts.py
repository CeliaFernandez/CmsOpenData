class Cuts(object):
    
    def __init__(self, isGlobal = 1, pt_min = 5, eta_max = 2.4, normChi2 = 10, numValidHitsSTATk = 10, numValidHits = 10, numOfMatches = 1, dz_max = 0.2, dB_max = 0.02, relIsolation = 0.15, mass_min = 0):

        self.isGlobal    = isGlobal
        self.isGlobalCut = "({0}*(Muon_isGlobalMuon[i] || Muon_isTrackerMuon[i]) + (1 - {0}))".format(isGlobal)
                
        self.pt_min = pt_min
        self.ptCut  = "(Muon_pt[i] > {0})".format(pt_min)
                
        self.eta_max = eta_max
        self.etaCut  = "(fabs(Muon_eta[i]) < {0})".format(eta_max)
                
        self.normChi2    = normChi2
        self.normChi2Cut = "(Muon_normChi2[i] < {0})".format(normChi2)
                
        self.numValidHitsSTATk    =  numValidHitsSTATk
        self.numValidHitsSTATkCut = "(Muon_NValidHitsSATk[i] > {0})".format(numValidHitsSTATk)
                
        self.numValidHits = numValidHits
        self.numValidHitsCut = "(Muon_numberOfValidHits[i] > {0})".format(numValidHits)
                
        self.numOfMatches = numOfMatches
        self.numOfMatchesCut = "(Muon_numOfMatches[i] > {0})".format(numOfMatches)
                
        self.dz_max = dz_max
        self.dzCut = "(fabs(Muon_distance[i]) < {0})".format(dz_max)
                
        self.dB_max = dB_max # cm. dB=impact parameter
        self.dBCut = "(fabs(Muon_dB[i]) < {0})".format(dB_max)
                
        self.relIsolation = relIsolation
        self.relIsolationCut = "((Muon_isolation_hadEt[i] + Muon_isolation_emEt[i] + Muon_isolation_sumPt[i])/Muon_pt[i] < {0})".format(relIsolation)
                
        self.mass_min = mass_min
        
        self.selection = ""
                
                
    def fullSelection(self, muon = False):
         
        selection = "1"
        selection += " && " + self.isGlobalCut
        selection += " && " + self.ptCut
        selection += " && " + self.etaCut
        selection += " && " + self.normChi2Cut
        selection += " && " + self.numValidHitsSTATkCut
        selection += " && " + self.numValidHitsCut
        selection += " && " + self.numOfMatchesCut
        selection += " && " + self.dzCut
        selection += " && " + self.dBCut
        selection += " && " + self.relIsolationCut
                
        if not muon:
            return selection.replace("[i]", "")
        else:
            return selection.replace("[i]", "[" + muon + "]")
        
    def sequentialSelection(self):
        
        sequence = []
        sequence.append("1")
        sequence.append( sequence[-1] + " && " + self.isGlobalCut )
        sequence.append( sequence[-1] + " && " + self.ptCut) 
        sequence.append( sequence[-1] + " && " + self.etaCut) 
        sequence.append( sequence[-1] + " && " + self.normChi2Cut) 
        sequence.append( sequence[-1] + " && " + self.numValidHitsSTATkCut) 
        sequence.append( sequence[-1] + " && " + self.numValidHitsCut) 
        sequence.append( sequence[-1] + " && " + self.numOfMatchesCut) 
        sequence.append( sequence[-1] + " && " + self.dzCut) 
        sequence.append( sequence[-1] + " && " + self.dBCut)
        sequence.append( sequence[-1] + " && " + self.relIsolationCut)
        
        for i in range(0, len(sequence)):
            sequence[i] = sequence[i].replace("[i]", "")
                  
        return sequence
                
                
                
                
                
                
                