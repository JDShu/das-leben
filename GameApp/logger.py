#!/usr/env python

import logging

# create logger
logger = logging.getLogger("application log")
logger.setLevel( logging.DEBUG )

# create console handler and set level to debug
ch = logging.FileHandler( "logging.log" )
ch.setLevel( logging.DEBUG )

# create formatter
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# "application" code
def LOG_DBG( instance, message ):
    logger.debug( "%s - %s " % ( instance, message ) )

def LOG_INFO( instance, message ):
    logger.info( "%s - %s " % ( instance, message ) )

def LOG_WARN( instance, message ):
    logger.warn( "%s - %s " % ( instance, message ) )

def LOG_ERROR( instance, message ):
    logger.error( "%s - %s " % ( instance, message ) )

def LOG_CRITICAL( instance, message ):
    logger.critical( "%s - %s " % ( instance, message ) )


if __name__ == "__main__":
    LOG_CRITICAL( None, "cheese" )
    LOG_ERROR( None, "cheese" )
    LOG_WARN( None, "cheese" )
    LOG_INFO( None, "cheese" )
    LOG_DBG( None, "cheese" )

