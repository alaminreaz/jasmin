# Copyright 2012 Fourat Zouari <fourat@gmail.com>
# See LICENSE for details.

import pickle
from twisted.spread import pb
from twisted.internet import reactor

def ConnectedPB(fn):
    'Check connection to PB before passing to session handler'
    def check_cnx_and_call(self, *args, **kwargs):
        if self.isConnected == False:
            raise Exception("PB proxy is not connected !")
        
        return fn(self, *args, **kwargs)
    return check_cnx_and_call

class RouterPBProxy:
    pb = None
    isConnected = False
    pickleProtocol = 2
    
    def connect(self, host, port):
        # Launch a client
        self.pbClientFactory = pb.PBClientFactory()
        reactor.connectTCP(host, port, self.pbClientFactory)
        
        return self.pbClientFactory.getRootObject( ).addCallback(self._connected)
    
    def disconnect(self):
        self.isConnected = False
        return self.pbClientFactory.disconnect()
    
    def _connected(self, rootObj):
        self.isConnected = True
        self.pb = rootObj
        
    def pickle(self, obj):
        return pickle.dumps(obj, self.pickleProtocol)
    
    def unpickle(self, obj):
        return pickle.loads(obj)
    
    @ConnectedPB
    def persist(self, profile = "jcli-prod", scope = 'all'):
        return self.pb.callRemote('persist', profile, scope)
    
    @ConnectedPB
    def load(self, profile = "jcli-prod", scope = 'all'):
        return self.pb.callRemote('load', profile, scope)
    
    @ConnectedPB
    def user_add(self, user):
        return self.pb.callRemote('user_add', self.pickle(user))
    
    @ConnectedPB
    def user_authenticate(self, username, password):
        return self.pb.callRemote('user_authenticate', username, password)
    
    @ConnectedPB
    def user_remove(self, uid):
        return self.pb.callRemote('user_remove', uid)

    @ConnectedPB
    def user_remove_all(self):
        return self.pb.callRemote('user_remove_all')

    @ConnectedPB
    def user_get_all(self, gid = None):
        return self.pb.callRemote('user_get_all', gid)

    @ConnectedPB
    def group_add(self, group):
        return self.pb.callRemote('group_add', self.pickle(group))
    
    @ConnectedPB
    def group_remove(self, gid):
        return self.pb.callRemote('group_remove', gid)

    @ConnectedPB
    def group_remove_all(self):
        return self.pb.callRemote('group_remove_all')

    @ConnectedPB
    def group_get_all(self):
        return self.pb.callRemote('group_get_all')

    @ConnectedPB
    def mtroute_add(self, route, order):
        return self.pb.callRemote('mtroute_add', self.pickle(route), order)
    
    @ConnectedPB
    def moroute_add(self, route, order):
        return self.pb.callRemote('moroute_add', self.pickle(route), order)
    
    @ConnectedPB
    def mtroute_flush(self):
        return self.pb.callRemote('mtroute_flush')
    
    @ConnectedPB
    def moroute_flush(self):
        return self.pb.callRemote('moroute_flush')
    
    @ConnectedPB
    def mtroute_get_all(self):
        return self.pb.callRemote('mtroute_get_all')
    
    @ConnectedPB
    def moroute_get_all(self):
        return self.pb.callRemote('moroute_get_all')    