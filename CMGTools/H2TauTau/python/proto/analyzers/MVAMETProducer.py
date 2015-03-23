import math
import copy

from sklearn.externals import joblib

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer


class MVAMETProducer(Analyzer):
    '''Computes SVfit di-tau mass at the ntuple level.'''

    def __init__(self, *args):
        super(MVAMETProducer, self).__init__(*args)
        self.trainVars = [
            'particleFlow_U', 'particleFlow_SumET', 'particleFlow_UPhi',
            'track_U', 'track_SumET', 'track_UPhi',
            'noPileUp_U', 'noPileUp_SumET', 'noPileUp_UPhi',
            'pileUp_MET', 'pileUp_SumET', 'pileUp_METPhi',
            'pileUpCorrected_U', 'pileUpCorrected_SumET', 'pileUpCorrected_UPhi',
            'jet1_pT', 'jet1_eta', 'jet1_Phi', 
            'jet2_pT', 'jet2_eta', 'jet2_Phi', 
            'nJets', 'numJetsPtGt30', 'nPV'
        ]
        self.clf = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingRegressor_diffu_clf.pkl')
    

    def process(self, event):

        # method override
        met = event.diLepton.met()
        inputs = []
        for var in self.trainVars:
            inputs.append(met.userFloat(var))
        reg = self.clf.predict(inputs)
        rec = reg[0]
        #rec *= met.userFloat('particleFlow_U')
        rec += met.userFloat('particleFlow_U')
        event.diLepton.mvamet_sklearn_u = rec

        p4_leg1 = event.diLepton.leg1().p4()
        p4_leg2 = event.diLepton.leg2().p4()
        p4_met = copy.copy(met.p4())

        phi = met.userFloat('particleFlow_UPhi')

        p4_met.SetPx(rec * math.cos(phi))
        p4_met.SetPy(rec * math.sin(phi))

        p4_met -= p4_leg1
        p4_met -= p4_leg2

        event.diLepton.mvamet_sklearn_pt = p4_met.pt()
