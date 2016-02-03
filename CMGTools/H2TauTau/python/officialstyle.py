from ROOT import kBlack, TLatex, TCanvas, TPad, gStyle

def officialStyle(style):
    style.SetCanvasColor (0)
    style.SetCanvasBorderSize(10)
    style.SetCanvasBorderMode(0)
    style.SetCanvasDefH (700)
    style.SetCanvasDefW (700)
    style.SetCanvasDefX (100)
    style.SetCanvasDefY (100)
    # color palette for 2D temperature plots
    # style.SetPalette(1,0)
    # Pads
    style.SetPadColor (0)
    style.SetPadBorderSize (10)
    style.SetPadBorderMode (0)
    
    style.SetPadBottomMargin(0.15)
    style.SetPadTopMargin (0.05)
    style.SetPadLeftMargin (0.17)
    # style.SetPadRightMargin (0.03566265)
    style.SetPadRightMargin (0.065)
    style.SetPadGridX (0)
    style.SetPadGridY (0)
    style.SetPadTickX (1)
    style.SetPadTickY (1)
    # Frames
    style.SetLineWidth(3)
    style.SetFrameFillStyle ( 0)
    style.SetFrameFillColor ( 0)
    style.SetFrameLineColor ( 1)
    style.SetFrameLineStyle ( 0)
    style.SetFrameLineWidth ( 2)
    style.SetFrameBorderSize(10)
    style.SetFrameBorderMode( 0)
    # Histograms
    style.SetHistFillColor(2)
    style.SetHistFillStyle(0)
    style.SetHistLineColor(1)
    style.SetHistLineStyle(0)
    style.SetHistLineWidth(3)
    style.SetNdivisions(505)
    # Functions
    style.SetFuncColor(1)
    style.SetFuncStyle(0)
    style.SetFuncWidth(2)
    # Various
    style.SetMarkerStyle(20)
    style.SetMarkerColor(kBlack)
    style.SetMarkerSize (1.4)
    style.SetTitleBorderSize(0)
    style.SetTitleFillColor (0)
    style.SetTitleX (0.2)
    style.SetTitleSize (0.055,"X")
    style.SetTitleOffset(1.100,"X")
    style.SetLabelOffset(0.005,"X")
    style.SetLabelSize (0.050,"X")
    style.SetLabelFont (42 ,"X")
    style.SetStripDecimals(False)
    style.SetLineStyleString(11,"20 10")
    style.SetTitleSize (0.055,"Y")
    style.SetTitleOffset(1.55,"Y")
    style.SetLabelOffset(0.010,"Y")
    style.SetLabelSize (0.050,"Y")
    style.SetLabelFont (42 ,"Y")
    style.SetTextSize (0.055)
    style.SetTextFont (42)
    style.SetStatFont (42)
    style.SetTitleFont (42)
    style.SetTitleFont (42,"X")
    style.SetTitleFont (42,"Y")
    style.SetOptStat (0)

def cmsPrel(lumi,  energy,  simOnly,  onLeft=True,  sp=0):
    latex = TLatex()
  
    t = gStyle.GetPadTopMargin()/(1-sp)
    tmpTextSize=0.75*t
    latex.SetTextSize(tmpTextSize)
    latex.SetNDC()
    textSize=latex.GetTextSize()

    latex.SetName("lumiText")
    latex.SetTextFont(42)

    lumyloc = 0.965
    cmsyloc = 0.893
    simyloc = 0.858
    if sp!=0:
        lumyloc = 0.945
        cmsyloc = 0.85
        simyloc = 0.8
    cmsalign = 31
    cmsxloc = 0.924
    if onLeft:
        cmsalign = 11
        cmsxloc = 0.204
    if (lumi > 0.):
        latex.SetTextAlign(31) # align left, right=31
        latex.SetTextSize(textSize*0.6/0.75)
        if(lumi > 1000. ):
            latex.DrawLatex(0.93,lumyloc,
                            " {lumi} fb^{{-1}} ({energy} TeV)".format(
                                lumi=lumi/1000.,
                                energy=energy
                            ))
        else:
            latex.DrawLatex(0.93,lumyloc,
                            " {lumi} pb^{{-1}} ({energy} TeV)".format(
                                lumi=lumi,
                                energy=energy
                            ))
  
    else:
        latex.SetTextAlign(31) # align right=31
        latex.SetTextSize(textSize*0.6/0.75)
        latex.DrawLatex(0.93,lumyloc," {energy} TeV".format(energy=energy))
  
 
    latex.SetTextAlign(cmsalign) # align left / right
    latex.SetTextFont(61)
    latex.SetTextSize(textSize)
    latex.DrawLatex(cmsxloc, cmsyloc,"CMS")
  
    latex.SetTextFont(52)
    latex.SetTextSize(textSize*0.76)
    
    if(simOnly):
        print cmsxloc, simyloc
        latex.DrawLatex(cmsxloc, simyloc,"Simulation")
    
        
class HistStyle:
    def __init__(self,
                 markerStyle = 8,
                 markerColor = 1,
                 markerSize = 1,
                 lineStyle = 1,
                 lineColor = None,
                 lineWidth = 2,
                 fillColor = None,
                 fillStyle = 0 ):
        self.markerStyle = markerStyle
        self.markerColor = markerColor
        self.markerSize = markerSize
        self.lineStyle = lineStyle
        if lineColor is None:
            self.lineColor = markerColor
        else:
            self.lineColor = lineColor
        self.lineWidth = lineWidth
        self.fillColor = fillColor
        self.fillStyle = fillStyle

    def format( self, hist):
        hist.SetMarkerStyle( self.markerStyle )
        hist.SetMarkerColor( self.markerColor )
        hist.SetMarkerSize( self.markerSize )
        hist.SetLineStyle( self.lineStyle )
        hist.SetLineColor( self.lineColor )
        hist.SetLineWidth( self.lineWidth )
        if self.fillColor is not None:
            hist.SetFillColor( self.fillColor )
        hist.SetFillStyle( self.fillStyle )

traditional_style = HistStyle(
    markerColor=4,
    markerStyle=21,
    lineColor=4,
)
pf_style = HistStyle(
    markerColor=2,
    markerStyle=8,
    lineColor=2
)


class CanvasRatio( TCanvas ):
    '''Produces a canvas with a ratio pad.
    
    The main pad is accessible through self.main
    The ratio pad through self.ratio
    '''
    def __init__(self, name, title, lumi, energy, simOnly):
        super(CanvasRatio, self).__init__(name, title)

        self.lumi = lumi
        self.energy = energy
        self.simOnly = simOnly

        bm_ = gStyle.GetPadBottomMargin()  
        tm_ = gStyle.GetPadTopMargin()
        lm_ = gStyle.GetPadLeftMargin()
        rm_ = gStyle.GetPadRightMargin()
  
        self.splitPad = 0.34
        self.cd()
        self.main = TPad("pMain","pMain",
                         0., self.splitPad ,1.,1.)
        
        self.ratio  = TPad("pRatio","pRatio",
                           0., 0. ,1.,self.splitPad)

        self.main.SetLeftMargin(lm_)
        self.main.SetRightMargin(rm_)
        self.main.SetTopMargin(tm_/(1-self.splitPad) )
        self.main.SetBottomMargin(0.02/(1-self.splitPad) )
        
        self.ratio.SetLeftMargin(lm_)
        self.ratio.SetRightMargin(rm_)
        self.ratio.SetTopMargin(0.01/self.splitPad)
        self.ratio.SetBottomMargin(bm_/self.splitPad)
        self.main.Draw()
        # cmsPrel(25000., 8., True, self.splitPad)
        self.ratio.Draw()

    def draw(self, hist, on_main, *args, **kwargs):
        yaxis = hist.GetYaxis()
        xaxis = hist.GetXaxis()
        if on_main:
            self.main.cd()
            yaxis.SetLabelSize( gStyle.GetLabelSize("Y")/(1-self.splitPad) )
            yaxis.SetTitleSize( gStyle.GetTitleSize("Y")/(1-self.splitPad) )
            yaxis.SetTitleOffset( gStyle.GetTitleOffset("Y")*(1-self.splitPad) )
            xaxis.SetLabelSize( 0 )
            xaxis.SetTitleSize( 0 )
            cmsPrel(self.lumi, self.energy, self.simOnly, True, self.splitPad)
            self.main.Update()
            
        else:
            self.ratio.cd()
            yaxis.SetLabelSize( gStyle.GetLabelSize("Y")/self.splitPad )
            yaxis.SetTitleSize( gStyle.GetTitleSize("Y")/self.splitPad )
            xaxis.SetLabelSize( gStyle.GetLabelSize("Y")/self.splitPad )
            xaxis.SetTitleSize( gStyle.GetTitleSize("Y")/self.splitPad )
            yaxis.SetTitleOffset( gStyle.GetTitleOffset("Y")*self.splitPad )
            yaxis.SetNdivisions(5,5,0)
            yaxis.SetRangeUser(0.71, 1.29)
        hist.Draw(*args, **kwargs)
        self.Update()
            


if __name__ == "__main__":

    from ROOT import gStyle, TH1F, gPad, TLegend, TF1

    officialStyle(gStyle)

    c1 = TCanvas("c1", "c1") 
    
    h = TH1F("h", "; p_{T} (GeV); stuff_{index}^{Power}", 50, -40000, 40000)
    h.Sumw2()
    gaus1 = TF1('gaus1', 'gaus')
    gaus1.SetParameters(1, 0, 5000)
    h.FillRandom("gaus1", 5000)
    h.Draw()
    pf_style.format(h)

    gPad.Update()

    h2 = TH1F("h2", "; p_{T} (GeV); stuff_{Index}^{Power}", 50, -40000, 40000)
    h2.Sumw2()
    gaus1.SetParameters(1, 0, 10000)
    h2.FillRandom("gaus1", 5000)
    h2.Draw("same")
    traditional_style.format(h2)

    legend = TLegend(0.65, 0.76, 0.9, 0.91)
    legend.AddEntry(h, "PF", "p")
    legend.AddEntry(h2, "Traditional", "p")
    legend.Draw()
     
    cmsPrel(25000., 8., True)

    c2 = TCanvas("c2", "c2")
    h.Draw()
    h2.Draw('same')
    cmsPrel(-1, 8., True)    

    gPad.Update()

    cr  = CanvasRatio('cr', 'canvas with ratio', 25000, 8., True)
    h3 = h.Clone('h3')
    h4 = h2.Clone('h4')
    cr.draw(h3, True)
    cr.draw(h4, True, 'same')
    
    hratio = h3.Clone('hratio')
    hratio.Divide(h4)
    hratio.SetYTitle('ratio')
    cr.draw(hratio, False)

    gPad.Update()
    
    
    c1.SaveAs('c1.pdf')
    c2.SaveAs('c2.pdf')
    cr.SaveAs('cr.pdf')
