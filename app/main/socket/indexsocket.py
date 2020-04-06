from flask_socketio import Namespace
from app.main import socketio
from random import random
from threading import Thread, Event
import time


class PocSocketBasedProgramming(Namespace):
    # time Generator Thread
    time_thread = Thread()
    time_stop_event = Event()
    # Random digit generator Thread
    digit_thread = Thread()
    digit_stop_event = Event()

    def on_connect(self):
        """
        Executes when client gets connected
        :return:
        """
        print('Client Connected')
        socketio.emit('status', {'status': 'Active'}, namespace='/index')

    def on_disconnect(self):
        """
        Executes when client gets disconnected
        :return:
        """
        print('Client disconnected')

    def on_time(self):
        """
        To stream time for every 10 seconds
        :return:
        """
        # As it is a streaming data used threading to ensure continuous data streaming

        if not self.time_thread.isAlive():
            print("Starting Thread for time")
            self.time_thread = socketio.start_background_task(self.time_generator)

    def on_random(self):
        """
        To stream random number for every 5seconds
        :return:
        """
        print('Client connected')
        # Start the random number generator thread only if the thread has not been started before.
        if not self.digit_thread.isAlive():
            print("Starting Thread")
            self.digit_thread = socketio.start_background_task(self.str_generator)

    def time_generator(self):
        """
        To emit random number for every 5 seconds
        :return:
        """
        while not self.time_stop_event.isSet():
            socketio.emit('time', {'time': str(time.asctime(time.localtime(time.time())))}, namespace='/index')
            socketio.sleep(10)

    def str_generator(self):
        """
        Streaming time for every 5seconds
        """
        # infinite loop of magical random numbers
        print("Making random numbers")
        while not self.digit_stop_event.isSet():
            number = round(random() * 10, 3)
            print(number)
            socketio.emit('random', {'digit': number}, namespace='/index')
            socketio.sleep(5)