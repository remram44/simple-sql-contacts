try:
    from contacts.main import main
except ImportError:
    import os
    import sys

    sys.path.insert(0, os.path.realpath('.'))

    from contacts.main import main


main()
