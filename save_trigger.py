# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:40:28 2020

@author: rober
"""


class SaveTrigger(object):
    def __init__(self):
        self._auto_keys = list()
        
        #Store these separately.
        #That way I can make sure I only save them, and not the other vars.
        self._vals = dict()
        
        self._states_from_times = dict()
    
    def __setattr__(self, name, value):
        #These are internal vars, which should function normally
        if name[0] == '_':
            super(SaveTrigger, self).__setattr__(name, value)
            return
        
        #These are external vars, which we put in _vals
        #and store history for
        self._vals.get(name, list()).append(value)
    
    def __getattribute__(self, name):
        #These are internal vars, which should function normally
        if name[0] == '_':
            return super(SaveTrigger, self).__getattribute__(name)
        
        #There are external vars, which we store in _vals
        #By default, use the most recent value
        return self._vals[name][-1]
    
    #This will probably get really expensive eventually
    #so I'll have to make it better sometime
    def _make_copy(self):
        copy = SaveTrigger()
        
        copy._auto_keys = self._auto_keys.copy()
        copy._vals = self._vals.copy()
        copy._states_from_times = self._states_from_times.copy()
        
        return copy
    
    def save(self, key):
        """
        Save the current state under the given key.
        
        Parameters:
            key: The key to save the current state under.
        
        Return:
            key
        """
        pass
        #self._state
    
    #This is a separate method so that None will be a valid key.
    def save(self):
        """
        Save the current state under an auto-generated key.
        
        Return:
            The auto-generated key.
        """
        pass