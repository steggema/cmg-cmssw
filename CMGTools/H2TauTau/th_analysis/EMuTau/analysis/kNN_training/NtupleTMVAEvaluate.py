
import datetime

from array import array

from ROOT import *
gROOT.SetBatch()

class NtupleTMVAEvaluate(object):
    def __init__(self, rootFilename):
        self._ntupleNames = []
        self._mvaMethodDicts = []
        self._variables = []
        self._spectatorVariables = []

        self._rootFilename = rootFilename
        self._rootFile = None

        self._compsiteVariableHandler = None

    def addMVAMethod(self, methodName, branchName, weightFilename):
        self._mvaMethodDicts.append({"methodName": methodName, "branchName": branchName, "weightFilename": weightFilename})

    def setVariables(self, variables):
        self._variables = variables

    def setSpectator(self, variables):
        self._spectatorVariables = variables

    def collectListOfNtuples(self):
        if not self._rootFile:
            print "%s.collectListOfNtuples() - ERROR: Input root file not opened for reading. Aborting..." % (self.__class__.__name__)
            return

        for entry in self._rootFile.GetListOfKeys():
            if not (entry.GetName() in self._ntupleNames):
                self._ntupleNames.append(entry.GetName())

    def open(self):
        if not self._rootFile:
            print "%s: Opening file '%s'..." % (self.__class__.__name__, self._rootFilename)
            self._rootFile = TFile(self._rootFilename, "UPDATE")

    def close(self):
        print "%s: Closing file '%s'..." % (self.__class__.__name__, self._rootFilename)
        self._rootFile.Write()
        self._rootFile.Close()
        self._rootFile = None

    def setCompositeVariableHandler(self, compositeVariableHandler):
        """ The handler is a function invoked during TMVA evaluation.

            The purpose is to translate ROOT cut string parser expressions into expressions on the variable values.
            The handler receives two arguments during evaluate: a list of composite variable expressions,
            and a dictionary containing all variable values of the current ntuple entry.
            The dictionary is of the type: {"variableName": array('f', [0.])}

            The handler should modify the entry in the dictionary in place and
            return a list of all compositeVariable it handled. This is used to provide meaningful error messages.
        """

        self._compsiteVariableHandler = compositeVariableHandler

    def identifiyCompositeVariables(self, existingBranchNames):
        """ composite variables are equations for the ROOT cut string parser
            e.g. mass/pT, abs(varName) - 15.4

            This function returns the list of original variables comprising composite variables
            if they are not already included in the input variables list (setVariables()).
        """

        inputVariables = self._variables + self._spectatorVariables
        compositeOriginalVariables = []
        for variable in inputVariables:
            if variable in existingBranchNames:
                # non-composite variable, nothing to do
                continue
            # strip special characters
            charactersToReplace = ["+", "-", "*", "/", "(", ")", ":", ","]
            for character in charactersToReplace:
                variable = variable.replace(character, " ")

            compositeCandidates = variable.split(" ")

            for candidate in compositeCandidates:
                if candidate in existingBranchNames and candidate not in inputVariables + compositeOriginalVariables:
                    compositeOriginalVariables.append(candidate)

        return compositeOriginalVariables

    def process(self, ntupleNames=[]):
        startTime = datetime.datetime.now()
        self.open()

        if not ntupleNames:
            self.collectListOfNtuples()
            ntupleNames = self._ntupleNames

            print "%s: The following directories have been found and will be processed:" % (self.__class__.__name__)
            for entry in self._ntupleNames:
                print entry

        for processName in ntupleNames:
            print "________________________________________\n"
            self.processSample(processName)

        runTime = datetime.datetime.now() - startTime
        print "%s: Total processing time for all directories: %s (%d sec)." % (self.__class__.__name__, runTime, runTime.seconds)
        self.close()

    def processSample(self, processName):
        print "%s:   Processing sample '%s'..." % (self.__class__.__name__, processName)
        ntuple = self._rootFile.Get(processName)
        print "%s    ntuple =" % self.__class__.__name__, ntuple

        if not ntuple:
            print "%s:   Did not find ntuple for sample '%s'. Skipping..." % (self.__class__.__name__, processName)
            return

        existingBranchNames = [branch.GetName() for branch in ntuple.GetListOfBranches()]

        reader = TMVA.Reader("!Color:!Silent")

        #
        # deal with composite variables
        #
        compositeVariables = []
        compositeOriginalVariables = self.identifiyCompositeVariables(existingBranchNames)
        print "\ncompositeOriginalVariables                =", compositeOriginalVariables, "\n"
        #print "\nself._variables + self._spectatorVariables =", self._variables + self._spectatorVariables, "\n"
        

        # set variable addresses for TMVA.Reader and ntuple
        # need to store references to variable array()s --> readerVarDict
        # otherwise python will free the memory of the arrays
        readerVarDict = {}
        for variable in self._variables + self._spectatorVariables + compositeOriginalVariables:
            if type(variable) == tuple:
                #variableLabel = variable[1]
                variable = variable[0]
            var = array('f', [0.])
            readerVarDict[variable] = var
            if variable in existingBranchNames:
                print "%s:     Adding variable '%s'" % (self.__class__.__name__, variable)
                ntuple.SetBranchAddress(variable, var)
            else:
                compositeVariables.append(variable)
                #print "\n%s:     ERROR: Unknown branch '%s'. Skipping... \n" % (self.__class__.__name__, variable)
                print "\n%s:     Found composite variable '%s'.\n" % (self.__class__.__name__, variable)

        for variable in self._variables:
            if type(variable) == tuple:
                variable = variable[0]
            reader.AddVariable(variable, readerVarDict[variable])

        for variable in self._spectatorVariables:
            print "%s:     Adding spectator variable '%s'" % (self.__class__.__name__, variable)
            if type(variable) == tuple:
                variable = variable[0]
            reader.AddSpectator(variable, readerVarDict[variable])

        #
        # Book the TMVA Reader instances
        #
        for mvaMethodDict in self._mvaMethodDicts:
            methodName = mvaMethodDict["methodName"]
            weightFilename = mvaMethodDict["weightFilename"]
            print "%s:     Booking mva method '%s'..." % (self.__class__.__name__, methodName)
            reader.BookMVA(methodName, weightFilename)

        #
        # create branches
        #
        branchVariablesDict = {}
        branchesDict = {}

        for mvaMethodDict in self._mvaMethodDicts:
            methodName = mvaMethodDict["methodName"]
            branchName = mvaMethodDict["branchName"]
            weightFilename = mvaMethodDict["weightFilename"]

            #oldBdtBranch = ntuple.GetBranch(branchName)
            if branchName in existingBranchNames:
                print "%s:       Branch already exists. Skipping..." % (self.__class__.__name__)
                continue

            # create branch for BDT discriminator
            print "%s:     Adding branch '%s' for method '%s'..." % (self.__class__.__name__, branchName, methodName)
            branchVariablesDict[methodName] = array('f', [0.])
            branchesDict[methodName] = ntuple.Branch(branchName, branchVariablesDict[methodName], branchName + "/F")  # third parameter: use same name for discriminant leave name (of type float) as for branchName
            #print "%s:       oldBdtBranch =" % self.__class__.__name__, oldBdtBranch
            #print "%s:       branch       =" % self.__class__.__name__, branchesDict[methodName]

        #
        # evaluate 
        #
        successFlag = True
        ntupleEntriesCount = ntuple.GetEntries()
        for i in range(ntupleEntriesCount):
            ntuple.GetEntry(i)

            # handle composite variables
            if self._compsiteVariableHandler:
                handledCompositeVariables = self._compsiteVariableHandler(compositeVariables, readerVarDict)

                # make sure it breaks if something is wrong
                if i == 0:
                    if type(handledCompositeVariables) == list:
                        for compositeVariable in compositeVariables:
                            if  not compositeVariable in handledCompositeVariables:
                                successFlag = False
                                print "\n%s:     ERROR: Composite variable '%s' is not handled. Aborting evaluation..." % (self.__class__.__name__, compositeVariable)
                    else:
                        successFlag = False
                        print "\n%s:     ERROR: Composite handler did not return a list of handled options. Cannot check whether all composite variables are handled. Aborting evaluation... \n" % (self.__class__.__name__)
            elif i == 0 and len(compositeVariables) > 0:
                print "\n%s:     ERROR: Found composite variables. However, no handler provided, see setCompositeVariableHandler(). Aborting evaluation...\n" % (self.__class__.__name__)
                successFlag = False

            if not successFlag:
                break

            # insert hook here
            for mvaMethodDict in self._mvaMethodDicts:
                methodName = mvaMethodDict["methodName"]
                if methodName in branchVariablesDict and methodName in branchesDict:
                    branchVariablesDict[methodName][0] = reader.EvaluateMVA(methodName)
                    branchesDict[methodName].Fill()
                #print i, methodName, reader.EvaluateMVA(methodName)
            #print "branchArray[0] =", branchArray[0]

        if successFlag:
            for mvaMethodDict in self._mvaMethodDicts:
                methodName = mvaMethodDict["methodName"]
                print "%s:     Processed %d events for mva method '%s'..." % (self.__class__.__name__, ntupleEntriesCount, methodName)

        reader.Delete()
        reader = None



if __name__ == "__main__":

    def convertCompositeVariables(compositeVariables, readerVarDict):
        """ Example immplementation of compositeHandler.
            This function converts ROOT cut string parser expressions for the NtupleTMVAEvaluate class.
        """
        handledCompositeVariables = compositeVariables[:]

        # finish convert statement with 'continue'. Otherwise 
        for variableExpression in compositeVariables:
            if False:
                pass
            elif variableExpression == "Reconstructed_sumJetPt/Reconstructed_sumJetE":
                readerVarDict[variableExpression][0] = readerVarDict["Reconstructed_sumJetPt"][0] / readerVarDict["Reconstructed_sumJetE"][0]
                continue
            elif variableExpression == "abs(Reconstructed_min_higgs_mass - 119.75)":
                readerVarDict[variableExpression][0] = abs(readerVarDict["Reconstructed_min_higgs_mass"][0] - 119.75)
                continue
            elif variableExpression == "abs(Reconstructed_deltaEtaTlepHiggs)":
                readerVarDict[variableExpression][0] = abs(readerVarDict["Reconstructed_deltaEtaTlepHiggs"][0])
                continue

            handledCompositeVariables = [v for v in handledCompositeVariables if v != variableExpression]

        return handledCompositeVariables
