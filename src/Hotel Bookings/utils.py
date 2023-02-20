#this is a file that stores functions that will commonly need to be accessed

import logging    
import constants    
def setup_logging():
    logging.basicConfig(filename= constants.LOG_FILE_PATH,
                filemode='a+',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=logging.INFO)