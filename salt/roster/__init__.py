# -*- coding: utf-8 -*-
'''
Generate roster data, this data is used by non-minion devices which need to be
hit from the master rather than acting as an independent entity. This covers
hitting minions without zeromq in place via an ssh agent, and connecting to
systems that cannot or should not host a minion agent.
'''

# Import salt libs
import salt.loader


class Roster(object):
    '''
    Used to manage a roster of minions allowing the master to become outwardly
    minion aware
    '''
    def __init__(self, opts, backends=None):
        self.opts = opts
        self.backends = backends
        self.rosters = salt.loader.roster(opts)

    def _gen_back(self):
        '''
        Return a list of loaded roster backends
        '''
        back = set()
        if self.backends:
            for backend in self.backends:
                fun = '{0}.targets'.format(backend)
                if fun in self.rosters:
                    back.add(backend)
            return back
        for roster in self.rosters:
            back.add(roster.split('.')[0])
        return sorted(back)

    def targets(self, tgt, tgt_type):
        '''
        Return a dict of {'id': {'ipv4': <ipaddr>}} data sets to be used as
        targets given the passed tgt and tgt_type
        '''
        targets = {}
        for back in self._gen_back():
            f_str = '{0}.targets'.format(back)
            if f_str not in self.rosters:
                continue
            targets.update(self.rosters[f_str](tgt, tgt_type))
        return targets
