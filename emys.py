import xmlrpc.client
import time
import numpy as np
import ctypes


class TimeoutTransport(xmlrpc.client.Transport):
    timeout = 500.0
    def set_timeout(self, timeout):
        self.timeout = timeout

# Assuming thalamusAddress and clientPort are defined somewhere else in your code
thalamusAddress = "localhost"  # Example address
clientPort = 2002         # Example 
t = TimeoutTransport()
t.set_timeout(1000)

eventPublisher = xmlrpc.client.ServerProxy('http://{0}:{1}'.format(thalamusAddress, clientPort), transport=t, verbose=False)

s = eventPublisher.Connect("SERA","python", 2011, 2010, 1)
print(s)
e = eventPublisher.PongSync("python", 1)
print(e)
eventPublisher.Disconnect("python")