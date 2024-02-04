import os
import sys

sys.path.append("/share/scratch0/czheng/offlineAnalysisFix/offlinetooldebug/")

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

filelist =['/home/czheng/scratch0/upROOT_SIM/FlatSimSampleFile/output_99.root:t']

branches = ['pmt_nPE','pmt_layer']

mycuts = milliqanCuts()

myplotter = milliqanPlotter()

#create root histogram 
h_NPE = r.TH1F("nPE", "nPE", 500, 0, 1000)

#add root histogram to plotter
myplotter.addHistograms(h_NPE, 'pmt_nPE', 'eventCuts')

def LayerCut(self, cutName=None, cut=False, branches=None):
    self.events['layer1'] = self.events['pmt_layer'] == 1

    if cut:
        branches.append('layer1')
        for branch in branches:
            self.events[branch] = self.events[branch][LayerCuts]

setattr(milliqanCuts, 'LayerCut', LayerCut)

eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['layer1'])


#print(myplotter.dict)
#things inside dict are the name of histogram not the the histogram variable. eg here the name of histogram is nPE


cutflow = [mycuts.LayerCut,eventCuts,myplotter.dict['nPE']]


myschedule = milliQanScheduler(cutflow, mycuts, myplotter)


myschedule.printSchedule()


#in the demo mycuts, myplotter arguements are useless now
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

myiterator.run()

output_file = r.TFile("run99_NPEL1.root", "RECREATE")
h_NPE.Write()
output_file.Close()
