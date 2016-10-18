from __future__ import unicode_literals

import os
import sqlite3

import numpy

__all__ = ["FieldsDatabase"]

class FieldsDatabase(object):

    FIELDS_DB = "Fields.db"
    """Internal file containing the standard 3.5 degree FOV survey field information."""

    def __init__(self):
        """Initialize the class.
        """
        self.db_name = self.FIELDS_DB
        self.connect = sqlite3.connect(os.path.join(os.path.dirname(__file__), self.db_name))

    def __del__(self):
        """Delete the class.
        """
        self.connect.close()

    def get_opsim3_userregions(self, query, precision=2):
        """Get a formatted string of OpSim3 user regions.

        This function gets a formatted string of OpSim3 user regions suitable for an OpSim3
        configuration file. The format looks like (RA,Dec,Width):

        userRegion = XXX.XX,YYY.YY,0.03
        ...

        The last column is unused in OpSim3. The precision argument can be used to control
        the formatting, but OpSIm3 configuration files use 2 digits as standard.

        Parameters
        ----------
        query : str
            The query for field retrieval.
        precision : int, optional
            The precision used for the RA and Dec columns. Default is 2.

        Returns
        -------
        str
            The OpSim3 user regions formatted string.
        """
        format_str = "userRegion = {{:.{0}f}},{{:.{0}f}},0.03".format(precision)
        cursor = self.connect.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(format_str.format(row[2], row[3]))
        return str(os.linesep.join(result))

    def get_ra_dec_arrays(self, query):
        """Retrieve lists of RA and Dec.

        Parameters
        ----------
        query : str
            The query for field retrieval.

        Returns
        -------
        numpy.array, numpy.array
            The arrays of RA and Dec.
        """
        cursor = self.connect.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        ra = []
        dec = []
        for row in rows:
            ra.append(row[2])
            dec.append(row[3])

        return numpy.array(ra), numpy.array(dec)
