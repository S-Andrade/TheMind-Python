
import xmlrpc.client


port = 2002

proxy = xmlrpc.client.ServerProxy(f"http://localhost:{port}/")


try:
    proxy.ISpeakActions.Speak("player0", "Olá do python")
except xmlrpc.client.Fault as err:
    print("A fault occurred")
    print("Fault code: %d" % err.faultCode)
    print("Fault string: %s" % err.faultString)
