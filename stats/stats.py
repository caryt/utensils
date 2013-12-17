"""Stats - Graphite Interface
=============================
"""
import socket
import time


class Stats(object):
    """Stats objects send messages to a Graphite server and 
    retrieve graphs.
    """
    def __init__(self, app, name=None):
        self.app = app
        self.name = name

    @property
    def stats_server(self):
        return (self.app.config.GRAPH_HOST, self.app.config.STATS_PORT)

    def unix_time(self, datetime):
        """Convert a `datetime` to Unix time."""
        return time.mktime(datetime.timetuple())

    @property
    def now(self):
        """Return the current time (in Unix time)."""
        return int(time.time())

    def message(self, name, value, datetime=None):
        """Contruct a Graphite message from `name`, `value` and `time`
        If `time` is omitted, the current time will be used.
        """
        return '%s %s %d\n' % (name, value, 
            self.unix_time(datetime) if datetime else self.now)

    def _send(self, message):
        """Send the `message` to the Graphite port."""
        sock = socket.socket()
        try:
            sock.connect(self.stats_server)
            sock.sendall(message)
        finally:
            sock.close()

    def __call__(self, value, datetime=None):
        """Publish a stat `value` to Graphite at `time`.
        If `time` is omitted, the current time will be used.
        """
        self._send(self.message(self.name, value, datetime))

    def publish(self, iterator):
        """Publish all stats in `iterator` that returns (value, datetime) tuples."""
        [self(value, datetime) for (value, datetime) in iterator]

    def __getattr__(self, attr):
        """Implements dot-notation usage, e.g. `Stats(app).A.dotted.Graphite.name(value)`."""
        return Stats(self.app, '.'.join((self.name, attr)) if self.name else attr)


