import os, sys
from datetime import datetime
#sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)))

import javaLoggingHelper.main

if __name__ == '__main__':
    print 'Started at %s' % str(datetime.now())
    javaLoggingHelper.main.main()
    print 'Ended at %s' % str(datetime.now())
