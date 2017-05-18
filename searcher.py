#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 19:27:01 2017

@author: bjaus
"""

import os


def option_handler():
    from optparse import OptionParser
    
    p = OptionParser()
    
    p.add_option(
        '-p', '--path', 
        help='search path', 
        dest='path', 
        action='store', 
        defaul=os.getcwd()        
    )
    
    p.add_option(
        '-i', '--item',
        help='word or phrase to search',
        dest='item',
        action='store',
        default=None        
    )
    
    p.add_option(
        '-e', '--ext',
        help='specify extension of file to search. defaults to all filtypes',
        dest='ext',
        action='store',
        default=None        
    )
    
    return p.parse_args()
    

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
    
    ext_exclude = [
        'git',
        'pyc',
        'pak',
        'local',
        'epub',
        'db',
        'markers',
        'prefs',
        'location',
        'gdconnection',
        
    ]
    
    def __init__(self, path=os.getcwd(), word=None, ext=None):
        self.word = word
        self.ext = ext
        self.count = 0
        self.matches = dict()
        
        if os.path.exists(path):
            self.path = path
        else:
            self.path = os.getcwd()  
            
        if self.word:
            self.matches = self._lookup()
            
        self.write_path = self.path
            

    def __repr__(self):        
        return """There were {:,} matches for:
    Path: {}/*
    Word: {}
    Ext: {}""".format(
        self.count if self.matches else 0,
        self.path,
        self.word,
        self.ext if self.ext else 'All Files'
    )
                
        
    def _file_reader(self, filepath):
        with open(filepath, 'r') as f:
            for num, line in enumerate(f.readlines()):
                if self.word.lower() in line.lower():
                    if not filepath in self.matches:
                        self.count += 1
                        self.matches[filepath] = []
                        
                    self.matches[filepath].append(
                        (
                            num+1,
                            line.strip()
                        )        
                    )
                        
    
    def _ext_excluder(self, filename):
        
        if '.' in filename:
            ext = filename.split('.')[-1]
        else:
            ext = filename
            
        return ext in Searcher.ext_exclude
                        
    
    def _lookup(self):
        for dpath, dnames, fnames in os.walk(self.path):
#            if 'venv' not in dpath:
            for fn in fnames:
                ex = fn.split('.')[-1]
                if not (
                        fn in __file__ 
                        or ex in Searcher.ext_exclude
                        or 'venv' in dpath):
                    filepath = os.path.join(dpath, fn)
                    if self.ext:
                        if fn.endswith(self.ext):
                            self._file_reader(filepath)
                    else:
                        self._file_reader(filepath)
                        
        return self.matches
    
    
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
            
            
    def _write(self, filepath=os.path.join(os.getcwd(), 'searcher')):
        
        if len(self.matches) > 0:
            
            with open(filepath + '.txt', 'w') as f:
                f.write(self._match_string())

        else:
            print '\nNothing to write because:'
            print self
    
    
    def print_matches(self):
        if len(self.matches) > 0:               
            print self._match_string()
            return ''
            
        else:
            return self
    
    
    def writer(self, path=os.getcwd(), filename='searcher'):
        
        if os.path.exists(path):
            self._printer(idx=0, path=path) 
            self._write(filepath=os.path.join(path, filename))
        elif os.path.exists(self.path):
            self._printer(idx=0, path=self.path)
            self._write(filepath=os.path.join(self.path, filename))
        else:
            self._printer(idx=1, path=path)
            


if __name__ == '__main__':
    
    search = Searcher(
        path='/Users/bjaus/Desktop',
        word='affiliate',
        ext='.py'        
    )
    
    search.print_matches()
#    search.print_matches()
#    search.writer(path='/Users/bjaus/Desktop/SearcherTesting', filename=search.word)