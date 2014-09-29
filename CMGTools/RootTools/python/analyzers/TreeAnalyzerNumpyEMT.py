from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.statistics.TreeNumpy import TreeNumpy as Tree
from ROOT import TFile

class TreeAnalyzerNumpyEMT( Analyzer ):
    """Base TreeAnalyzerNumpyEMT, to create flat TTrees.

    Check out TestTreeAnalyzer for a concrete example.
    IMPORTANT: FOR NOW, CANNOT RUN SEVERAL TreeAnalyzers AT THE SAME TIME!
    Anyway, you want only one TTree, don't you?"""

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TreeAnalyzerNumpyEMT,self).__init__(cfg_ana, cfg_comp, looperName)
        fileName = '/'.join([self.dirName,
                             self.name+'_tree.root'])
        self.file = TFile( fileName, 'recreate' )
        self.tree = Tree(self.name, self.name)
        self.mtree = Tree(self.name + '_muon', self.name + '_muon')
        self.etree = Tree(self.name + '_electron', self.name + '_electron')
        self.ttree = Tree(self.name + '_tau', self.name + '_tau')
        self.vmtree = Tree(self.name + '_vetomuon', self.name + '_vetomuon')
        self.vetree = Tree(self.name + '_vetoelectron', self.name + '_vetoelectron')
        self.vttree = Tree(self.name + '_vetotau', self.name + '_vetotau')
        self.btree = Tree(self.name + '_bjet', self.name + '_bjet')        
        self.jtree = Tree(self.name + '_jet', self.name + '_jet')
        self.gentree = Tree(self.name + '_gen', self.name + '_gen')
                
        self.declareVariables()
        
    def declareVariables(self):
        print 'TreeAnalyzerNumpyEMT.declareVariables : overload this function.'
        pass

    def write(self):
        super(TreeAnalyzerNumpyEMT, self).write()
        self.file.Write() 

