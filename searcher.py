#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 19:27:01 2017

@author: bjaus
"""

import os
from sys import exit


def option_handler():
    from optparse import OptionParser
    
    p = OptionParser()
    
    p.add_option(
        '-p', '--path', 
        help='directory to begin search, searches all directories below this.', 
        dest='path', 
        action='store', 
        default=os.getcwd()        
    )
    
    p.add_option(
        '-s', '--search',
        help='word or phrase to search for, this is MANDATORY!',
        dest='term',
        action='store',
        default=None        
    )
    
    p.add_option(
        '-e', '--ext',
        help='specify extension of file to search, defaults to all filtypes',
        dest='ext',
        action='store',
        default=None        
    )
    
    p.add_option(
        '-x', '--exclude',
        help='deactive built-in filetype exclusions when searching all filetypes, only applicable if -e is not specified.',
        dest='excluder',
        action='store_false',
        default=True
    )
    
    opts, args = p.parse_args()
    
    if opts.term is None:
        print '\nA mandatory option is missing\n'
        p.print_help()
        print
        exit(-1)
    
    return opts, args
    

class Searcher(object):
    """
    Starting at the directory provided, search recrusively through all files
    and/or directories below this level for a word in a specific filetype.
    
    Parameters:
        path : string
            Path of directory to begin search
        word : string
            Word to search for within files
        ext : string
            Optional paramter to narrow down the filetype
            If not provided, all files will be considered
            Else only the files that match the specific type

    """
    
    exclude = [
        '.git',
        '.pyc',
        '.pak',
        '.local',
        '.epub',
        '.db',
        '.markers',
        '.prefs',
        '.location',
        '.gdconnection',
        'LICENSE',
        'venv',
        '.md',
        
    ]
    
    
    def __init__(self, path, term, ext, excluder=True):
        self.count = 0
        self.term = term
        self.ext = ext
        self.excluder = excluder
        self.matches = dict()
        
        while not os.path.exists(path):
            print '\nPath does not exist: "{}"\n'.format(path)
            path = raw_input('Enter new path ["q" to Quit]: ')
            
            if path.lower() == 'q': exit(-2)
            
        self.path = path
#        self.matches = self._lookup()


    def _inclusion(self, filename, filepath):
        
        # Does not search in searcher.py itself
        if filename in filepath:
            return False
        
        elif self.excluder:
            
            test = sum([True if i in filepath else False for i in Searcher.exclude])
            
            if test > 0:
                return False

        return True


    def _lookup(self):
        for dpath, dnames, fnames in os.walk(self.path):
            for fn in fnames:
                filepath = os.path.join(dpath, fn)
                if self._inclusion(filename=fn, filepath=filepath):
                    if self.ext:
                        if fn.lower().endswith(self.ext):
                            self._reader(filepath)
                    else:
                        self._reader(filepath)

        return self.matches
                
                
    def _reader(self, filepath):
        with open(filepath, 'r') as f:
            for num, line in enumerate(f.readlines()):
                if self.term in line:
                    if not filepath in self.matches:
                        self.matches[filepath] = []
                        
                    self.matches[filepath].append((num+1, line.strip()))
                    self.count += 1
                        
    
    
    def _match_string(self):
        string = '\n'
        term = string
        for key, values in sorted(self.matches.items()):
            string += '{}{}'.format(key, term)
            for num, line in values:
                string += '  {}) {}{}'.format(num, line, term)
            string += term
            
        return string
    
    
    def _printer(self, path, idx=0):
        print
        if idx == 0:
            print 'Writing file to {}...'.format(path)
        else:
            print 'Neither {} or {} are valid paths. Try again.'.format(
                    path,
                    self.path)
    
    
    def print_matches(self):
        if len(self.matches) > 0:               
            print self._match_string()
            return ''
            
        else:
            return self
    
            

if __name__ == '__main__':    
    opts, args = option_handler()
    
    search = Searcher(
            path=opts.path,
            term=opts.term,
            ext=opts.ext,
            excluder=opts.excluder)
    
    search.print_matches()