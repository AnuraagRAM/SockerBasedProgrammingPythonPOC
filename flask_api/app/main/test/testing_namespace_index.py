import unittest
from flask_api.app.main import socketio, app
import time


class TestSocketIo(unittest.TestCase):

    def verifyconnection(self, received):
        """
        To verify the connection response
        :return:
        """
        self.assertEqual(len(received[0]), 3)
        self.assertEqual(received[0]['name'], 'status')
        self.assertEqual(received[0]['args'][0]['status'], 'Active')
        self.assertEqual(received[0]['namespace'], '/index')

    def verifydisconnect(self, received):
        """
        To verify the disconnection response
        :param received:
        :return:
        """
        self.assertEqual(received[0]['args'], 'Disconnected')

    def testconnection(self):
        """
        To test the connection
        As the default emit has status arg we are verifying it
        :return:
        """
        client = socketio.test_client(app, namespace='/index')
        received = client.get_received('/index')
        self.verifyconnection(received)
        client.disconnect()
        received = client.get_received()
        self.verifydisconnect(received)

    def testeventtime(self):
        """
        To test event time
        There is a possibility of failure for this test case as we are also emitting seconds
        :return:
        """
        client = socketio.test_client(app, namespace='/index')
        received = client.get_received('/index')  # Here we will be receiving the default status event data
        client.emit('time', namespace='/index')
        received = client.get_received('/index')  # Here we will be receiving the custom event time data
        self.assertEqual(received[0]['name'], 'time')
        self.assertEqual(received[0]['args'][0]['time'], str(time.asctime(time.localtime(time.time()))))
        client.disconnect()
        received = client.get_received()
        self.verifydisconnect(received)

    def testmultiplefive(self):
        client = socketio.test_client(app, namespace='/index')
        received = client.get_received('/index')  # Here we will be receiving the default status event data
        client.emit('random', namespace='/index')
        received = client.get_received('/index')  # Here we will be receiving the custom event time data
        self.assertEqual(received[0]['name'], 'random')
        self.assertEqual(received[0]['args'][0]['digit'], 0)
        client.disconnect()
        received = client.get_received()
        self.verifydisconnect(received)


if __name__ == '__main__':
    unittest.main()
