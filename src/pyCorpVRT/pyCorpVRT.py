#! ~/anaconda3/bin/python
# python interpreter
'''
Created on 17 Jan 2019

@author: bogdan
'''

import sys, os, re
from collections import defaultdict


class clPyCorpVRT(object): # clPyDictSort is the template for this class; extensions include dealing with non-positional features
    '''
    sorting complex Python dictionaries
    '''


    def __init__(self, IterInput, LKeyColumns, LValueColumns, LIndexColumns):
        '''
        tab separated Vertical Text Format (vrt)is input  -- see Corpus Workbench manual for details; 
            creates frequency dictionaries for column tuples:
                a 1d frq dict for keys only;
                a 2d dict for key tuple + different possible value tuple combinations
            takes iterator object (normally file, or -- list of tab separated lines, run functions
            
        
        '''
        FConfig = open('./pyCorpVRT_confstoptags.txt', 'rU')
        for SLine in FConfig:
            SLine = SLine.rstrip()
            (SType, SPatterns) = re.split('\t', SLine, 1)
            sys.stderr.write(SType + ' = ' + SPatterns + '\n')
            if SType == 'STRUCTURAL': self.REStruct = re.compile(SPatterns)
            elif SType == 'LEXICAL': self.RELex = re.compile(SPatterns)
            elif SType == 'POSITIONAL': self.REPosit = re.compile(SPatterns)
            elif SType == 'REPETITION': self.RERepeat = re.compile(SPatterns)
            
        
        self.DFieldFrq = defaultdict(int) # frequency dictionary for key field combinations: main data structure
        self.DFieldFrq2D = defaultdict(lambda: defaultdict(int)) # 2D frequency dictionary for value field combinations for each key field combination
        self.DVrtPoSTemplates2D = defaultdict(lambda: defaultdict(int)) # 2D frq dictionary: PoS patterns mapped from lem+pos configurations
        
        if 'fileVRT2dict' in LFlags:
            self.fileVRT2dict(IterInput, LKeyColumns, LValueColumns)
        
        if 'fileVRT2posTemplates' in LFlags:
            self.fileVRT2posTemplates(IterInput, LKeyColumns, LValueColumns, LIndexColumns)
            
        
    
    def fileVRT2dict(self, IterInput, LKeyColumns, LValueColumns):
        """
        LKeyColumns should not be empty, creates tuples which are index of the frq dictionary created from corpus
        for the second dictionary:
        if LValueColumns is empty, then frequency of LKeyColumns tuples is calculated (with an empty tuple as the only value)
        if LValueColumns is not empty, then frequencies of each possible tuples as values for index tuples are given
        """
        # LPoSPattern = [] # collection of positions between limiting PoS codes (configuration of PoSs)
        for SLine in IterInput:
            SLine = SLine.rstrip()
            # collect pattern until you reach a breaking point;
            # if re.match('pattern', string, flags) # first split the string into fields...
            if re.match('^<.+>$', SLine): continue
            
            LLine = re.split('\t', SLine)
            # sys.stdout.write('%(LLine)s\n' % locals())
            
            
            # TKeyColumns = tuple(LLine[i] for i in range(len(LLine)) if i in LKeyColumns)
            # TValueColumns = tuple(LLine[i] for i in range(len(LLine)) if i in LValueColumns)
            try:
                TKeyColumns = tuple(LLine[i] for i in LKeyColumns)
            except:
                sys.stderr.write('TKeyColumns error: SLine=%(SLine)s\n' % locals())
            try:
                TValueColumns = tuple(LLine[i] for i in LValueColumns) # used as a field for tracking associations (???)
            except:
                sys.stderr.write('TValueColumns error: SLine=%(SLine)s\n' % locals())
            
            # sys.stderr.write('TKeyColumns = %(TKeyColumns)s\n' % locals())
            # sys.stderr.write('TValueColumns = %(TValueColumns)s\n\n' % locals())
            
            self.DFieldFrq[TKeyColumns] += 1
            self.DFieldFrq2D[TKeyColumns][TValueColumns] += 1
        
        # sys.stdout.write('done\n')
        return
    
    def fileVRT2posTemplatesRec(self, LTTemplatesKeys, LTTemplatesVals, LTTemplatesIndx, LTTemplatesKVI):
        """
        loop over one of the list and create representations for the dictionary of templates, keep indices
        - every word in the window receives a representation
        """
        # a prototype template: the value field is collected
        # LTValueTemplate = LTTemplatesVals
        ### sys.stderr.write("LTTemplatesKeys = %(LTTemplatesKeys)s\nLTTemplatesVals = %(LTTemplatesVals)s\nLTTemplatesIndx = %(LTTemplatesIndx)s\n\n" % locals())
        
        for IIndex, TTemplatesKVI in enumerate(LTTemplatesKVI):
            # access  needed information: keys
            TTemplatesKeys = LTTemplatesKeys[IIndex]
            
            
            # - make a clone list for the prototype template
            # a prototype template: the value field is collected
            # LTValueTemplate = LTTemplatesVals
            LTValueTemplate = LTTemplatesVals[:] # quick (shallow) copy
            # sys.stderr.write("LTValueTemplate = %(LTValueTemplate)s\n" % locals())
            
            
            # replace the item in focus with the value of Index fields
            TFocus = LTTemplatesIndx[IIndex]
            # sys.stderr.write("TFocus = %(TFocus)s\n" % locals())
            LFocus = list(TFocus)
            # sys.stderr.write("LFocus = %(LFocus)s\n" % locals())
            SFirstWord = LFocus[0]
            SFirstWord = '!' + SFirstWord
            LFocus[0] = SFirstWord
            LTValueTemplate[IIndex] = tuple(LFocus)
            # sys.stderr.write("LTValueTemplate = %(LTValueTemplate)s\n" % locals())
            
            # now the value template list is ready, we can create a string for the database from it (as will be accepted by the script
            LValueTemplate4String = []
            # sys.stderr.write(":\n" % locals())
            for TEl in LTValueTemplate: # for every tuple in the List
                SEl = '/'.join(TEl)
                # sys.stderr.write("TEl = %(TEl)s ; SEl = %(SEl)s\n" % locals())
                LValueTemplate4String.append(SEl)
            
            SValueTemplate = ' '.join(LValueTemplate4String) # this is value for the current word
            # sys.stderr.write("LValueTemplate4String = %(LValueTemplate4String)s\n" % locals())
            # sys.stderr.write("SValueTemplate = %(SValueTemplate)s\n\n" % locals())
            
            self.DVrtPoSTemplates2D[TTemplatesKeys][SValueTemplate] += 1
            # self.DFieldFrq2D[TTemplatesKeys][SValueTemplate] += 1
            
            # end: for IIndex, TTemplatesKVI in enumerate(LTTemplatesKVI):

        
        
        # this operation is performed for every lemma+pos in the window
        # self.DVrtPoSTemplates2D[TKeyColumns][TValueColumns] += 1
        
        return
    
    
    def fileVRT2posTemplates(self, IterInput, LKeyColumns, LValueColumns, LIndexColumns):
        """
        collect pos templates
        """
        
        # all lists are synchronised, and represent reduplication of information for more convenient processing
        LTTemplatesKeys = [] # main data structure: tuple of lists that will have same length, e.g., PoS and Lemma; allowing any combination
        LTTemplatesVals = []
        LTTemplatesIndx = []
        LTTemplatesKVI = [] # list of tuples: Key, Value, Index (KVI) : this is used for preparing keys frameowrk
        
        # to be destroyed when we reach a boundary;
        # to be extended as we go...
        
        # fixed number of coordinated lists: Key and Value Combination? Need named lists...
        # LPoSPattern = [] # collection of positions between limiting PoS codes (configuration of PoSs)
        for SLine in IterInput:
            SLine = SLine.rstrip()
            # collect pattern until you reach a breaking point;
            # if re.match('^<.+>$', SLine): continue
            
            LLine = re.split('\t', SLine)
            if len(LLine) >= 3:
                SWordForm = LLine[0]
                SPoS = LLine[1]
                SLemma = LLine[2]
            else: # default values
                SWordForm = "~~~"
                SPoS = "~~~"
                SLemma = "~~~"
                

                
            # boundary conditions: fire up recording of the window
            if re.match(self.REStruct, SLine) or re.match(self.RELex, SLemma) or re.match(self.REPosit, SPoS):
                # if any of these conditions for the boundary found, then add values, destroy window, and start the window again
                self.fileVRT2posTemplatesRec(LTTemplatesKeys, LTTemplatesVals, LTTemplatesIndx, LTTemplatesKVI)
                # destroying the window
                LTTemplatesKeys = [] # main data structure: tuple of lists that will have same length, e.g., PoS and Lemma; allowing any combination
                LTTemplatesVals = []
                LTTemplatesIndx = []
                LTTemplatesKVI = []

                continue
                   
            # other conditions: if no boundary detected, then create index + expand the window:
            try:
                # create a tuple for main keys
                TKeyColumns = tuple(LLine[i] for i in LKeyColumns)
                LTTemplatesKeys.append(TKeyColumns)
            except:
                sys.stderr.write('TKeyColumns error: SLine=%(SLine)s\n' % locals())
            try:
                # create a tuple for values (keys of the value dictionary)
                TValueColumns = tuple(LLine[i] for i in LValueColumns) # used as a field for tracking associations (???)
                LTTemplatesVals.append(TValueColumns)
            except:
                sys.stderr.write('TValueColumns error: SLine=%(SLine)s\n' % locals())
            try:
                # create a tuple for index (This is for an item that represents a keyword + its part of speech in a template)
                TIndexColumns = tuple(LLine[i] for i in LIndexColumns)
                LTTemplatesIndx.append(TIndexColumns)
            except:
                sys.stderr.write('TValueColumns error: SLine=%(SLine)s\n' % locals())
            try:
                # create a tuple out of the whole list:
                TTemplatesKVI = tuple(LLine)
                LTTemplatesKVI.append(TTemplatesKVI)
            except:
                sys.stderr.write('TTemplatesKVI error: SLine=%(SLine)s\n' % locals())
                
            # end - for SLine in IterInput (continue: is implicit)
                
            
        
        return
    
        
    def printData(self, BPrintStrFormat=False):
        for (key, val) in sorted(self.DFieldFrq.items(), key=lambda k: k[1], reverse=True ):
            if BPrintStrFormat:
                KeyStr = '~'.join(key)
                sys.stdout.write('%(KeyStr)s\t%(val)s\n' % locals())
            else:
                sys.stdout.write('%(key)s=%(val)s\n' % locals())
        return
    
    def printData2D(self, BPrintStrFormat=False):
        for (key, DVal) in sorted(self.DFieldFrq2D.items()):
            if BPrintStrFormat:
                KeyStr = '/'.join(key)
                sys.stdout.write('%(KeyStr)s\t' % locals())
            else:
                sys.stdout.write('%(key)s\t' % locals())
            for (TFieldComb, IFrq) in sorted(DVal.items(), key=lambda k: k[1], reverse=True):
                if BPrintStrFormat:
                    TFieldCombStr = '/'.join(TFieldComb)
                    sys.stdout.write('%(TFieldCombStr)s=%(IFrq)d|' % locals())
                else:
                    sys.stdout.write('%(TFieldComb)s=%(IFrq)d|' % locals())
            sys.stdout.write('\n')
        return
            
    def printDataTemplates2D(self, BTopOnly=False):
        for (key, DVal) in sorted(self.DVrtPoSTemplates2D.items()):
            KeyStr = '/'.join(key)
            sys.stdout.write('%(KeyStr)s\t' % locals())

            for (TFieldComb, IFrq) in sorted(DVal.items(), key=lambda k: k[1], reverse=True):
                if BTopOnly: 
                    sys.stdout.write('%(TFieldComb)s' % locals())
                    break
                sys.stdout.write('%(TFieldComb)s=%(IFrq)d|' % locals())
                
            sys.stdout.write('\n')
        return
         
            
         


    
        
        
if __name__ == '__main__':
    """
    object should be able to handle any iterable over strings (e.g., list, tuple, etc); in this case we open a file as an iterable
    write file argment names; prepare the values of the list to be injected
    """
    for el in sys.argv: sys.stderr.write('Argument: %(el)s\n' % locals()) # debug: are arguments correctly specified?
    # injecting variables from the command line string (what is expected by default -- in case run not from shell script 
    # + eval() statement to override the default value)
    
    FInput=sys.stdin
    LKeyColumns=[] # key columns from VRT
    LValueColumns=[] # value columns from VRT
    LIndexColumns=[] # index columns (this is for collection of templates: one of the items will be a keyword, which is used as an "index" (e.g., pos1, *lem/pos2, pos3...) - e.g., 'deal'
    LFlags = []
    
    # sys.stderr.write('LKeyColumns= %(LKeyColumns)s ; LValueColumns= %(LValueColumns)s\n' % locals())
    
    # overriding default values if specified in the shell script
    for el in sys.argv[1:]:
        # sample command line: 
        # python pyDictSort.py "LKeyColumns.extend([0])" "LValueColumns.extend([2,1])" < pyDictSort_in.txt > pyDictSort_out.txt
        eval(el)
    
    sys.stderr.write('LKeyColumns= %(LKeyColumns)s ;\n LValueColumns= %(LValueColumns)s LIndexColumns = %(LIndexColumns)s;\n LFlags = %(LFlags)s ;\n' % locals())
    
    # in case index not initialised
    if len(LKeyColumns) == 0: LKeyColumns.extend([0])
    
    
    OPyCorpVRT = clPyCorpVRT(FInput, LKeyColumns, LValueColumns, LIndexColumns)
    if 'dict1d' in LFlags:
        OPyCorpVRT.printData()
    if 'dict2d' in LFlags:
        OPyCorpVRT.printData2D()
    if 'dict1dstr' in LFlags:
        OPyCorpVRT.printData(BPrintStrFormat=True)
    if 'dict2dstr' in LFlags:
        OPyCorpVRT.printData2D(BPrintStrFormat=True)
    if 'templates2d' in LFlags:
        OPyCorpVRT.printDataTemplates2D()
    if 'templates2dtoponly' in LFlags:
        OPyCorpVRT.printDataTemplates2D(BTopOnly=True)




    
    
    