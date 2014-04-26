import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from sep.commands.sepgen import main

if __name__ == '__main__':
    main()
