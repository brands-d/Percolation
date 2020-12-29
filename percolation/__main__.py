import sys
import signal

from percolation.percolation import Percolation

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    app = Percolation(sys.argv)
    sys.exit(app.run())
