# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:40:28 2020

@author: rober
"""

from copy import deepcopy

class SaveTrigger(object):
    def __init__(self):
        super(SaveTrigger, self).__init__()
        
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
        if name in self._vals:
            self._vals[name].append(value)
            return
        else:
            self._vals[name] = [value]
    
    def __getattr__(self, name):
        
        
        return self._vals[name][-1]
    
    def _get_prev(self, name, prev_level=1):
        return self._vals[name][-1-prev_level]
    
    #This will probably get really expensive eventually
    #so I'll have to make it better sometime
    def _make_save(self):
        save = Save()
        
        save._auto_keys = deepcopy(self._auto_keys)
        save._vals = deepcopy(self._vals)
        save._states_from_times = deepcopy(self._states_from_times)
        
        return save
    
    def prev(self, prev_level=1):
        return PrevWrapper(self, prev_level=prev_level)
    
    def at(self, key):
        save = self._states_from_times[key]
        
        result = SaveTrigger()
        
        result._auto_keys = save._auto_keys
        result._vals = save._vals
        result._states_from_times = save._states_from_times
        
        return result
    
    def save(self, key=None):
        """
        Save the current state under the given key.
        
        Parameters:
            key: The key to save the current state under.
        
        Return:
            key
        """
        if key == None:
            key = object()
            self._auto_keys.append(key)
            
        self._states_from_times[key] = self._make_save()
        return key

class Save(object):
    pass

class PrevWrapper(object):
    def __init__(self, wrapped, prev_level=1):
        super(PrevWrapper, self).__init__()
        
        self._wrapped = wrapped
        self._prev_level = prev_level
    
    def __getattr__(self, name):
        return self._wrapped._get_prev(name, prev_level=self._prev_level)
    