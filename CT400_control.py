# Class for controlling the Yenista CT400.
# Code based on the 'CT400_testwrap.py' test file provided by Yenista with the
# installation, and A.A.G.'s code from October 2017.
# Tested with Python version 3.4.5 and Anaconda 4.3.1
# E.D. December 2022

'''
To to - 06/12/22
- check functions again
'''

from ctypes import *
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import compress

# Definition of various constants to use the same names as the C interface
(LS_TunicsPlus, LS_TunicsPurity, LS_TunicsReference, LS_TunicsT100s_HP, 
	LS_TunicsT100r, LS_JdsuSws, LS_Agilent, NB_SOURCE) = (0,1,2,3,4,5,6,7)
(LI_1, LI_2, LI_3, LI_4) = (1,2,3,4)
(DE_out, DE_1, DE_2, DE_3, DE_4, DE_5) = (0,1,2,3,4,5)
(DISABLE, ENABLE) = (0,1)
(Unit_mW, Unit_dBm) = (0,1)

class Yenista_CT400:

	uiHandle = None
	laser_model = LS_TunicsT100s_HP
	GPIB_addr = 10
	las_input = LI_1
	las_min_wav = 1500.0
	las_max_wav = 1630.0
	iErrorID = 0
	tcError = None
	strRet = None

	def __init__(self, def_pow = 6):
		'''
		Initialise the CT400 and establish number of inputs and detectors

		Parameters
		----------
		def_pow : float
			default power for the laser in mW
			laser reverts to this power after a wavelength sweep
		'''
		print("Initialising CT400...")
		# string to return error message
		tcError = create_string_buffer(1024)
		strRet = create_string_buffer(1024)
		# initialise CT400
		iErrorSize = c_int * 1
		(iError)=(iErrorSize())
		uiHandle = c_longlong(windll.CT400_lib.CT400_Init(byref(iError)))
		print("{}{}".format("Error/Warning: ",iError[0]))
		if uiHandle:
			print("Initialisation complete\n")
			print("Default laser power: {}mW".format(def_pow))
			print("{}{}".format("Number of Inputs: ", windll.CT400_lib.CT400_GetNbInputs(uiHandle)))
			print("{}{}".format("Number of Detectors: ", windll.CT400_lib.CT400_GetNbDetectors(uiHandle)))
			# print("{}{}".format("CT400 Option: ", windll.CT400_lib.CT400_GetCT400Type(uiHandle)))
		else:
			print("Initialising failed. Error/Warning: {}".format(iError[0]))

		self.uiHandle = uiHandle
		self.tcError = tcError
		self.strRet = strRet
		self.def_pow = def_pow


	def close_conn(self):
		'''
		closes the connection to the CT400 and releases all memory allocated by CT400_Init
		'''
		windll.CT400_lib.CT400_Close(self.uiHandle)


	def __del__(self):
		self.close_conn()


	def las_on(self, wav, power = None):
		'''
		turn on the laser and set it to a wavelength and power

		Parameters
		----------
		wav : float
			wavelength in nm
		power : float
			laser power in mW
			set to default power if not stated
		'''
		if self.uiHandle is None:
			print("Error: the CT400 has not been initialised")
		elif windll.CT400_lib.CT400_CheckConnected(self.uiHandle):
			if power == None: power = self.def_pow
			windll.CT400_lib.CT400_SetLaser(self.uiHandle, self.las_input, ENABLE, self.GPIB_addr, self.laser_model, c_double(self.las_min_wav), c_double(self.las_max_wav), 100)
			windll.CT400_lib.CT400_CmdLaser(self.uiHandle, self.las_input, ENABLE, c_double(wav), c_double(power))
			print("Laser on and set to {}nm and {}mW".format(wav, power))
		else:
			strRet = 'Error: could not connect to the CT400'
			return strRet


	def las_off(self):
		'''
		turn off the laser (and set it to 1550nm and 1mW)
		'''
		if self.uiHandle is None:
			print("Error: the CT400 has not been initialised")
		elif windll.CT400_lib.CT400_CheckConnected(self.uiHandle):
			windll.CT400_lib.CT400_CmdLaser(self.uiHandle, self.las_input, DISABLE, c_double(1550.0), c_double(self.def_pow))
			print("Laser switched off")
		else:
			strRet = 'Error: could not connect to the CT400'
			return strRet	


	def print_det_pows(self, det_list = [0, 1]):
		'''
		prints the power being detected at the output and detectors specified by the bool list

		Parameters
		----------
		det_list : list[int]
			list of detectors to be printed
			(DE_out, DE_1, DE_2, DE_3, DE_4, DE_5) = (0,1,2,3,4,5)
		'''
		PowerArraySize = c_double * 1
		(Pout, P1, P2, P3, P4, Vext) = (PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize())
		windll.CT400_lib.CT400_ReadPowerDetectors(self.uiHandle, byref(Pout), byref(P1), byref(P2), byref(P3), byref(P4), byref(Vext))
		all_powers = [Pout[0], P1[0], P2[0], P3[0], P4[0], Vext[0]]
		det_names = ['Pout', 'P1', 'P2', 'P3', 'P4', 'Vext']
		[print("{}: {:.3f} dBm".format(det_names[i], all_powers[i])) for i in det_list]


	def return_det_pows(self, det_list = [0, 1]):
		'''
		returns the power being detected at the output and detectors specified by the bool list
		
		Parameters
		----------
		det_list : list[int]
			list of detectors to have their powers returned
			(DE_out, DE_1, DE_2, DE_3, DE_4, DE_5) = (0,1,2,3,4,5)
		
		Returns
		--------
		powers : list[float]
			a list of lists containing the powers measured for each detector specified
		'''
		PowerArraySize = c_double * 1
		(Pout, P1, P2, P3, P4, Vext) = (PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize())
		windll.CT400_lib.CT400_ReadPowerDetectors(self.uiHandle, byref(Pout), byref(P1), byref(P2), byref(P3), byref(P4), byref(Vext))
		all_powers = [Pout[0], P1[0], P2[0], P3[0], P4[0], Vext[0]]
		powers = [all_powers[i] for i in det_list]
		return powers

	def plot_powers(self, det = None, array_Live = 50):
		'''
		function that live plots the power (dBm) of one of the detectors specified
		title includes the current power reading the the max power read so far

		Parameters
		----------
		det : int
			(DE_1, DE_2, DE_3, DE_4, DE_5) = (1,2,3,4,5)
		array_Live : int
			the size of the array of data points displayed in the live plot
		'''

		if det is None:
			print("No power meter specified")

		else:
			try:
				get_ipython().magic('matplotlib notebook')
				counter = 0
				n_sample = []
				powers = []
				fig, ax = plt.subplots(figsize=(8,4))
				ax.set_xlabel("Time flies")
				ax.set_ylabel("Power (dBm)")
				ax.grid()
				ax.plot([],[])

				while True:
					powers.append(self.return_det_pows([det])[0])
					n_sample.append(counter)
					ax.lines[0].set_data(n_sample[-min(array_Live,len(n_sample)):],powers[-min(array_Live,len(n_sample)):])
					ax.set_title("Detector: {}\nCurrent power: {:.3f} dBm | Max power: {:.3f} dBm".format(det, powers[-1], max(powers)))
					ax.relim()
					ax.autoscale_view()
					fig.tight_layout()
					fig.canvas.draw()
					counter += 1

			except KeyboardInterrupt:
				get_ipython().magic('matplotlib inline')
				print("Plotting stopped")



	def scan_config(self, min_wav = 1500.0, max_wav = 1630.0, las_pow = None, 
		res = 1, det_list = [DISABLE, DISABLE, DISABLE, DISABLE], speed = 100):
		'''
		Configures the CT400 for a wavelength scan with the given parameters.
		By default, the first detector is enabled.

		Parameters
		----------
		min_wav : float
			starting wavelength for scan
		max_wav : float
			final wavelength for scan
		las_pow : float
			laser power in mW
			set to the 'self.def_pow' (default power) by default
		res : float
			scan resolution in pm
			possible values: 1-250pm
		det_list : list[bool]
			enable/disable additional detectors
			list corresponds to: [Dect2, Dect3, Dect4, eExt]
			enable/disable with ENABLE or DISABLE
		speed : int
			speed of laser scan in nm/s
			possible values: from 10 to 100
		'''

		if self.uiHandle is None:
			print("Error: the CT400 has not been initialised")

		# checking the CT400 is connected to the computer
		elif windll.CT400_lib.CT400_CheckConnected(self.uiHandle):
			print("Configuring laser for scan")
			# configure laser input
			if las_pow == None: las_pow = float(self.def_pow)
			windll.CT400_lib.CT400_SetLaser(self.uiHandle, self.las_input, ENABLE, self.GPIB_addr, 
				self.laser_model, c_double(self.las_min_wav), c_double(self.las_max_wav), speed)
			# configure laser sweep
			windll.CT400_lib.CT400_SetScan(self.uiHandle, c_double(las_pow), c_double(min_wav), c_double(max_wav))
			windll.CT400_lib.CT400_SetSamplingResolution(self.uiHandle, res)
			windll.CT400_lib.CT400_SetDetectorArray(self.uiHandle, det_list[0], det_list[1], det_list[2], det_list[3])
			windll.CT400_lib.CT400_SetBNC(self.uiHandle, DISABLE, c_double(0.0), c_double(0.0), Unit_mW)
			print("Scan configuration complete")
			print("Configuration settings:")
			print("Wavelength range: {}-{}nm, Power: {}mW, Resolution: {}pm, Speed: {}nm/s, Detectors enabled: D1:1 D2:{} D3:{} D4:{} BNC:{}"
				.format(min_wav, max_wav, las_pow, res, speed, det_list[0], det_list[1], det_list[2], det_list[3]))
		else:
			strRet = 'Error: could not connect to the CT400'
			return strRet


	def perform_scan(self, dets_used = [DE_1], set_laser = False, heterodyne = False):
		'''
		Performs a wavelength scan with the preconfigured range, speed, laser power and resolution

		Parameters
		----------
		dets_used : list
			list of detectors used in the measurement
			e.g. if all four detectors were used: dets_used = [1, 2, 3, 4]
		set_laser : bool
			if true, set the laser to 1550nm and def_pow
		heterodyne : bool
			bool deciding whether to perform heterodyne detection (HD) measurements of spectral lines
			if true, will print spectral lines detected with HD

		Returns
		-------
		wavs : np.array[float]
			array of the resampled wavelengths scanned
		det_pows : np.array[list[float]]
			array with lists of resampled powers for each of the detectors used
		'''

		print("Beginning scan...")
		start_time = time.clock()
		windll.CT400_lib.CT400_ScanStart(self.uiHandle)
		self.iErrorID = windll.CT400_lib.CT400_ScanWaitEnd(self.uiHandle, self.tcError)
		if self.iErrorID == 0:

			# prepare arrays for storing measurement data
			DataPointSize = c_int * 1
			(iDataPoints, iDiscardPoints) =(DataPointSize(), DataPointSize())
			windll.CT400_lib.CT400_GetNbDataPoints(self.uiHandle,byref(iDataPoints),byref(iDiscardPoints))
			iPointsNumber = iDataPoints[0]
			iPointsNumberResampled = windll.CT400_lib.CT400_GetNbDataPointsResampled(self.uiHandle)
			det_pows = np.empty([len(dets_used), iPointsNumberResampled])
			# DataArraySize = c_double * iPointsNumber
			DataArraySizeResampled = c_double * iPointsNumberResampled

			for i, det in enumerate(dets_used):

				# (dWavelengthSync, dDetector1Sync) = (DataArraySize(), DataArraySize())
				(dWavelengthResampled, dDetectorResampled) = (DataArraySizeResampled(), DataArraySizeResampled())

				# call functions for scanning
				# windll.CT400_lib.CT400_ScanGetWavelengthSyncArray(uiHandle, byref(dWavelengthSync), iPointsNumber)
				windll.CT400_lib.CT400_ScanGetWavelengthResampledArray(self.uiHandle, byref(dWavelengthResampled), iPointsNumberResampled)

				# windll.CT400_lib.CT400_ScanGetDetectorArray(uiHandle, det, byref(dDetector1Sync), iPointsNumber)
				windll.CT400_lib.CT400_ScanGetDetectorResampledArray(self.uiHandle, det, byref(dDetectorResampled), iPointsNumberResampled)

				det_pows[i, :] = dDetectorResampled

			wavs = np.array(dWavelengthResampled)

			# display the number of points for standard and resampled measurements
			print("Scan executed in {:.2f}s".format(time.clock()-start_time))
			print("Total number of points, discarded points, resampled points: {}, {}, {}\n".format(iPointsNumber,iDiscardPoints[0],iPointsNumberResampled))

			if heterodyne:
				# returns the number of spectral lines detected with heterodyne detection (HD)
				iLinesDetected = windll.CT400_lib.CT400_GetNbLinesDetected(uiHandle)
				LinesArraySize = c_double * iLinesDetected
				dLinesValues = LinesArraySize()
				# returns the values of spectral lines detected by HD
				windll.CT400_lib.CT400_ScanGetLinesDetectionArray(uiHandle, byref(dLinesValues) ,iLinesDetected)
				# print lines detected by HD
				for i in range (iLinesDetected):
						print ("Spectral line #{i+1}:{:.4f}".format(dLinesValues[i]))

			if set_laser == True:
				# turn laser on and set to 1550nm once sweep complete
				windll.CT400_lib.CT400_CmdLaser(self.uiHandle, self.las_input, ENABLE, c_double(1550.0), c_double(self.def_pow))
				print("Laser set to 1550nm and {}mW\n".format(self.def_pow))

			return wavs, det_pows

		else:
			print('Error: ' + repr(self.tcError.value))

	
	def update_det_calib(self, det = None):
		'''
		Calibrates one of the detectors - effectively sets where 0dBm is to account for input losses,
		such that when you perform sweeps you get the transfer function of anything after the input fibre.
		It must be called after a scan has been performed on the same detector.
		
		Setup: the optical output of the CT400 should be connected directly to the detector in question.

		Parameters
		----------
		det : int
			The detector in question: DE_1, DE_2, DE_3, DE_4 = 1, 2, 3, 4
		'''
		if self.uiHandle is None:
			print("Error: the CT400 has not been initialised")
		
		if det == None:
			print('No detector specified')
		else:
			windll.CT400_lib.CT400_UpdateCalibration(self.uiHandle, det)
			print("Calibration for detector {} updated".format(det))

	def reset_dets_calib(self):
		'''
		Reset all of the detector calibrations.
		'''

		if self.uiHandle is None:
			print("Error: the CT400 has not been initialised")
		else:
			windll.CT400_lib.CT400_ResetCalibration(self.uiHandle)
			print("Calibration for detector {} reset".format(det))