#!/usr/bin/env python

"""
@package ion_functions.test.generic_functions
@file ion_functions/test/generic_functions.py
@author Christopher Mueller
@brief Unit tests for generic_functions module
"""

from nose.plugins.attrib import attr
from ion_functions.test.base_test import BaseUnitTestCase

import numpy as np
from ion_functions.data import generic_functions as gfunc


@attr('UNIT', group='func')
class TestGenericFunctionsUnit(BaseUnitTestCase):

    def test_magnetic_declination(self):
        """
        Test magnetic_declination function.

        Some values based on those defined in the WMM document,
        WMM2010testvalues.pdf which accompanies the software.  Others
        were created and checked using online calculators.

        Implemented by Stuart Pearce, April 2013
        """

        lat = np.array([45.0, 45.0, 80.0, 0.0, -80.0, 80.0, 0.0, -80.0])
        lon = np.array([-128.0, -128.0, 0.0, 120.0,
                        240.0, 0.0, 120.0, 240.0])
        z = np.array([0.0, 1000.0, 0.0, 0.0,
                      0.0, 100000.0, 100000.0, 100000.0])
        timestamp = np.array([3575053740.7382507,  # 2013-04-15 22:29:00
                              3575053740.7382507,  # UTC
                              3471292800.0,        # 2010-01-01 UTC
                              3471292800.0,
                              3471292800.0,
                              3471292800.0,
                              3471292800.0,
                              3471292800.0])

        decln = np.array([16.46093044096720, 16.46376239313584, -6.13, 0.97,
                          70.21, -6.57, 0.94, 69.62])

        out = gfunc.magnetic_declination(lat, lon, timestamp, z, -1)

        self.assertTrue(np.allclose(out, decln, rtol=0, atol=1e-2))

    def test_magnetic_correction(self):
        """
        Test magentic_correction function.

        Input values based on those defined in DPS; output values calculated to
            more significant figures using matlab code specified in the DPS.

        OOI (2012). Data Product Specification for Velocity Profile and Echo
            Intensity. Document Control Number 1341-00750.
            https://alfresco.oceanobservatories.org/ (See: Company Home >> OOI
            >> Controlled >> 1000 System Level >>
            1341-00750_Data_Product_SPEC_VELPROF_OOI.pdf)

        Implemented by Christopher Wingard, April 2013
        Modified by Russell Desiderio, April 07, 2014. Changed the rtol values
            from 1e4 to 1e-4 to get a fair test. Changed the output values by
            adding more significant figures.
        """
        # apply the magnetic declination correction.
        uu_cor, vv_cor = gfunc.magnetic_correction(16.9604, np.array([0.4413]),
                                                   np.array([0.1719]))

        # test the transform
        self.assertTrue(np.allclose(uu_cor, 0.472251, rtol=1e-4, atol=0))
        self.assertTrue(np.allclose(vv_cor, 0.035692, rtol=1e-4, atol=0))

    def test_ntp_to_unix_time(self):
        """
        Test ntp_to_unix_time function.

        Timestamp Values gathered from various internet sources
        including the NTP FAQ and HOWTO.

        Implemented by Stuart Pearce, April 2013
        """
        ntp_timestamps = np.array([3176736750.7358608,
                                   3359763506.2082224,
                                   3575049755.4380851])

        output = gfunc.ntp_to_unix_time(ntp_timestamps)

        check_values = np.array([967747950.735861,
                                 1150774706.2082224,
                                 1366060955.438085])
        self.assertTrue(np.allclose(output, check_values,
                                    rtol=0, atol=1e-6))

    def test_extract_parameters(self):
        """
        Test extract_parameter function.

        Array values created by author.

        Implemented by Christopher Wingard, April 2013
        """
        in_array = np.array([34, 67, 12, 15, 89, 100, 54, 36])
        self.assertTrue(np.equal(34, gfunc.extract_parameter(in_array, 0)))
        self.assertTrue(np.equal(67, gfunc.extract_parameter(in_array, 1)))
        self.assertTrue(np.equal(12, gfunc.extract_parameter(in_array, 2)))
        self.assertTrue(np.equal(15, gfunc.extract_parameter(in_array, 3)))
        self.assertTrue(np.equal(89, gfunc.extract_parameter(in_array, 4)))
        self.assertTrue(np.equal(100, gfunc.extract_parameter(in_array, 5)))
        self.assertTrue(np.equal(54, gfunc.extract_parameter(in_array, 6)))
        self.assertTrue(np.equal(36, gfunc.extract_parameter(in_array, 7)))
