# -*- coding: utf-8 -*-

import xmlrpc.client
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class OpenERPXMLRPC():
    def __init__(self, protocol, host, port, db, user, password):

        if port and (port != 80 or port != '80'):
            common_url = "%s://%s:%s/xmlrpc/common" % (protocol, host, port)
            object_url = "%s://%s:%s/xmlrpc/object" % (protocol, host, port)
        else:
            common_url = "%s://%s/xmlrpc/common" % (protocol, host)
            object_url = "%s://%s/xmlrpc/object" % (protocol, host)
        com_sock = xmlrpc.client.ServerProxy(common_url)
        uid = com_sock.authenticate(db, user, password, {})
        if uid:
            self.uid = uid
            self.password = password
            self.db = db
        else:
            print ("\n 11111 ERROR IN AUTHENTICATION.")

        self.sock = xmlrpc.client.ServerProxy(object_url)

    def execute(self, model, method, *args):
        res = self.sock.execute(self.db, self.uid, self.password, model,
                                method, *args)
        return res

    def exec_workflow(self, model, method, *args):
        res = self.sock.exec_workflow(
            self.db, self.uid, self.password, model, method, *args)
        return res

# Databse details:
def getSourceConnection(
        protocol='http', host='localhost', port='8017', db='new_test_db2',
        user='admin', password='admin'):
    return OpenERPXMLRPC(
        protocol=protocol, host=host, port=port, db=db, user=user,
        password=password)

def getDestinationConnection(
        protocol='http', host='localhost', port='8019', db='new_test_db3',
        user='admin', password='admin'):
    return OpenERPXMLRPC(
        protocol=protocol, host=host, port=port, db=db, user=user,
        password=password)
