#! ~/anaconda3/bin/python
# python interpreter
'''
Created on 15 Jan 2019

@author: bogdan
'''

import sys, os, re
from collections import defaultdict


class clPyDictSort(object):
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
        
        self.DFieldFrq = defaultdict(int) # frequency dictionary for key field combinations: main data structure
        self.DFieldFrq2D = defaultdict(lambda: defaultdict(int)) # 2D frequency dictionary for value field combinations for each key field combination
        self.fileVRT2dict(IterInput, LKeyColumns, LValueColumns)
        
    
    def fileVRT2dict(self, IterInput, LKeyColumns, LValueColumns):
        """
        LIndexColumns should not be empty, creates tuples which are index of the frq dictionary created from corpus
        for the second dictionary:
        if LValueColumns is empty, then frequency of LIndexColumns tuples is calculated (with an empty tuple as the only value)
        if LValueColumns is not empty, then frequencies of each possible tuples as values for index tuples are given
        """
        for SLine in IterInput:
            SLine = SLine.rstrip()
            if re.match('^<.+>$', SLine): continue
            
            LLine = re.split('\t', SLine)
            # sys.stdout.write('%(LLine)s\n' % locals())
            
            
            TKeyColumns = tuple(LLine[i] for i in range(len(LLine)) if i in LKeyColumns)
            TValueColumns = tuple(LLine[i] for i in range(len(LLine)) if i in LValueColumns)
            
            # sys.stderr.write('TKeyColumns = %(TKeyColumns)s\n' % locals())
            # sys.stderr.write('TValueColumns = %(TValueColumns)s\n\n' % locals())
            
            self.DFieldFrq[TKeyColumns] += 1
            self.DFieldFrq2D[TKeyColumns][TValueColumns] += 1
        
        # sys.stdout.write('done\n')
        return
        
    def printData(self):
        for (key, val) in sorted(self.DFieldFrq.items(), key=lambda k: k[1], reverse=True ):
            sys.stdout.write('%(key)s = %(val)s\n' % locals())
        return
    
    def printData2D(self):
        for (key, DVal) in sorted(self.DFieldFrq2D.items()):
            sys.stdout.write('%(key)s\t' % locals())
            for (TFieldComb, IFrq) in sorted(DVal.items(), key=lambda k: k[1], reverse=True):
                sys.stdout.write('%(TFieldComb)s=%(IFrq)d,' % locals())
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
    
    # sys.stderr.write('LKeyColumns= %(LKeyColumns)s ; LValueColumns= %(LValueColumns)s\n' % locals())
    
    # overriding default values if specified in the shell script
    for el in sys.argv[1:]:
        # sample command line: 
        # python pyDictSort.py "LKeyColumns.extend([0])" "LValueColumns.extend([2,1])" < pyDictSort_in.txt > pyDictSort_out.txt
        eval(el)
    
    sys.stderr.write('LKeyColumns= %(LKeyColumns)s ; LValueColumns= %(LValueColumns)s\n' % locals())
    
    # in case index not initialised
    if len(LKeyColumns) == 0: LKeyColumns.extend([0])
    
    
    OPyDictSort = clPyDictSort(FInput, LKeyColumns, LValueColumns)
    # OPyDictSort.printData()
    OPyDictSort.printData2D()
    
    
    