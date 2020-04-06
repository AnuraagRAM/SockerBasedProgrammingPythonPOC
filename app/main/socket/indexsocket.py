from flask_socketio import Namespace
from threading import Thread, Event
from app.main import socketio
import time
from app.main.utils.logging import root_log


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
        root_log.info('Client Connected')
        socketio.emit('status', {'status': 'Active'}, namespace='/index')

    def on_disconnect(self):
        """
        Executes when client gets disconnected
        :return:
        """
        root_log.error('Client disconnected')

    def on_time(self):
        """
        To stream time for every 10 seconds
        :return:
        """
        # As it is a streaming data used threading to ensure continuous data streaming

        if not self.time_thread.isAlive():
            root_log.info("Starting Thread for time")
            self.time_thread = socketio.start_background_task(self.time_generator)

    def on_random(self):
        """
        To stream random number for every 5seconds
        :return:
        """
        root_log.info('Client connected')
        # Start the random number generator thread only if the thread has not been started before.
        if not self.digit_thread.isAlive():
            root_log.info("Starting Thread")
            self.digit_thread = socketio.start_background_task(self.str_generator)

    def time_generator(self):
        """
        Streaming time for every 5seconds
        :return:
        """
        while not self.time_stop_event.isSet():
            socketio.emit('time', {'time': str(time.asctime(time.localtime(time.time())))}, namespace='/index')
            socketio.sleep(10)

    def str_generator(self):
        """
        Displaying multiples of 5.
        """
        root_log.info("Making random numbers")
        number = 0
        while not self.digit_stop_event.isSet():
            socketio.emit('random', {'digit': number}, namespace='/index')
            socketio.sleep(5)
            number = number + 5
