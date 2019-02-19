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


    def __init__(self, IterInput, LKeyColumns, LValueColumns):
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
        
        if 'wf2lemPosFrq' in LFlags:
            self.fileVRT2dict(IterInput, LKeyColumns, LValueColumns)
        
        if 'kwLemPos2posTemplatesFrq' in LFlags:
            pass
        
    
    def fileVRT2dict(self, IterInput, LKeyColumns, LValueColumns):
        """
        LIndexColumns should not be empty, creates tuples which are index of the frq dictionary created from corpus
        for the second dictionary:
        if LValueColumns is empty, then frequency of LIndexColumns tuples is calculated (with an empty tuple as the only value)
        if LValueColumns is not empty, then frequencies of each possible tuples as values for index tuples are given
        """
        LPoSPattern = [] # collection of positions between limiting PoS codes (configuration of PoSs)
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
            
        
            
         


    
        
        
if __name__ == '__main__':
    """
    object should be able to handle any iterable over strings (e.g., list, tuple, etc); in this case we open a file as an iterable
    write file argment names; prepare the values of the list to be injected
    """
    for el in sys.argv: sys.stderr.write('Argument: %(el)s\n' % locals()) # debug: are arguments correctly specified?
    # injecting variables from the command line string (what is expected by default -- in case run not from shell script 
    # + eval() statement to override the default value)
    
    FInput=sys.stdin
    LKeyColumns=[] 
    LValueColumns=[]
    LFlags = []
    
    # sys.stderr.write('LKeyColumns= %(LKeyColumns)s ; LValueColumns= %(LValueColumns)s\n' % locals())
    
    # overriding default values if specified in the shell script
    for el in sys.argv[1:]:
        # sample command line: 
        # python pyDictSort.py "LKeyColumns.extend([0])" "LValueColumns.extend([2,1])" < pyDictSort_in.txt > pyDictSort_out.txt
        eval(el)
    
    sys.stderr.write('LKeyColumns= %(LKeyColumns)s ;\n LValueColumns= %(LValueColumns)s ;\n LFlags = %(LFlags)s ;\n' % locals())
    
    # in case index not initialised
    if len(LKeyColumns) == 0: LKeyColumns.extend([0])
    
    
    OPyCorpVRT = clPyCorpVRT(FInput, LKeyColumns, LValueColumns)
    if 'dict1d' in LFlags:
        OPyCorpVRT.printData()
    if 'dict2d' in LFlags:
        OPyCorpVRT.printData2D()
    if 'dict1dstr' in LFlags:
        OPyCorpVRT.printData(BPrintStrFormat=True)
    if 'dict2dstr' in LFlags:
        OPyCorpVRT.printData2D(BPrintStrFormat=True)


    
    
    