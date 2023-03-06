#-*- coding: utf8 -*-
# sample Python control program for Yenista Optics' CT400
# version 1.4.0 
# tested successfully with Python 2.7.7 and Python 3.4.2
# please refer to CT400_lib.h for the documentation of the full set of interface functions

from ctypes import *

# Definition of various constants to use the same names as the C interface
(LS_TunicsPlus, LS_TunicsPurity, LS_TunicsReference, LS_TunicsT100s_HP, LS_TunicsT100r, LS_JdsuSws, LS_Agilent, NB_SOURCE) = (0,1,2,3,4,5,6,7)
(LI_1, LI_2, LI_3, LI_4) = (1,2,3,4)
(DE_1, DE_2, DE_3, DE_4, DE_5) = (1,2,3,4,5)
(DISABLE, ENABLE) = (0,1)
(Unit_mW, Unit_dBm) = (0,1)

def main():	 
	# string to return error message
	tcError = create_string_buffer(1024)
	strRet  = create_string_buffer(1024)
	# initialize CT400
	iErrorSize = c_int * 1
	(iError)=(iErrorSize())
	uiHandle = c_longlong(windll.CT400_lib.CT400_Init(byref(iError)))
	print("{}{}".format("Error/Warning: ",iError[0]))
	if uiHandle:
		print("{}{}".format("Number of Inputs : ", windll.CT400_lib.CT400_GetNbInputs(uiHandle)))
		print("{}{}".format("Number of Detectors : ",windll.CT400_lib.CT400_GetNbDetectors(uiHandle)))
		print("{}{}".format("CT400 Option : ",windll.CT400_lib.CT400_GetCT400Type(uiHandle)))
		if windll.CT400_lib.CT400_CheckConnected(uiHandle):
			# configure laser inputs
			windll.CT400_lib.CT400_SetLaser(uiHandle, LI_2, ENABLE, 10, LS_TunicsT100s_HP, c_double(1500.0), c_double(1600.0), 50)
			# configure laser sweep
			windll.CT400_lib.CT400_SetScan(uiHandle, c_double(5.0), c_double(1550.0), c_double(1560.0))
			windll.CT400_lib.CT400_SetSamplingResolution(uiHandle, 250)
			windll.CT400_lib.CT400_SetDetectorArray(uiHandle, DISABLE, DISABLE, DISABLE, DISABLE)
			windll.CT400_lib.CT400_SetBNC(uiHandle, DISABLE, c_double(0.0), c_double(0.0), Unit_mW)
			# start sweep
			print('Sweep starting')
			windll.CT400_lib.CT400_ScanStart(uiHandle)
			iErrorID = windll.CT400_lib.CT400_ScanWaitEnd(uiHandle, tcError)
			if iErrorID == 0:				
				# arrays for storing measurement data
				DataPointSize = c_int * 1
				(iDataPoints, iDiscardPoints) =(DataPointSize(), DataPointSize())
				windll.CT400_lib.CT400_GetNbDataPoints(uiHandle,byref(iDataPoints),byref(iDiscardPoints))
				iPointsNumber = iDataPoints[0]
				iPointsNumberResampled = windll.CT400_lib.CT400_GetNbDataPointsResampled(uiHandle)
				DataArraySize = c_double * iPointsNumber
				DataArraySizeResampled = c_double * iPointsNumberResampled
				(dWavelengthSync, dDetector1Sync) = (DataArraySize(), DataArraySize())
				(dWavelengthResampled, dDetector1Resampled) = (DataArraySizeResampled(), DataArraySizeResampled())
								
				windll.CT400_lib.CT400_ScanGetWavelengthSyncArray(uiHandle, byref(dWavelengthSync), iPointsNumber)				
				windll.CT400_lib.CT400_ScanGetDetectorArray(uiHandle, DE_1, byref(dDetector1Sync), iPointsNumber)
				windll.CT400_lib.CT400_ScanGetWavelengthResampledArray(uiHandle, byref(dWavelengthResampled), iPointsNumberResampled)
				windll.CT400_lib.CT400_ScanGetDetectorResampledArray(uiHandle, DE_1, byref(dDetector1Resampled), iPointsNumberResampled)

				windll.CT400_lib.CT400_ScanSaveWavelengthResampledFile(uiHandle, c_char_p(b"Lambda_Resampled.txt"))
				windll.CT400_lib.CT400_ScanSaveWavelengthSyncFile(uiHandle, c_char_p(b"Lambda_Sync.txt"))
				windll.CT400_lib.CT400_ScanSaveDetectorFile(uiHandle, DE_1, c_char_p(b"Output_Detector5_Sync.txt"))
				windll.CT400_lib.CT400_ScanSaveDetectorResampledFile(uiHandle,  DE_1, c_char_p(b"Output_Detector5_Resampled.txt"))
				windll.CT400_lib.CT400_ScanSavePowerSyncFile(uiHandle, c_char_p(b"Output_Sync.txt"))
				windll.CT400_lib.CT400_ScanSavePowerResampledFile(uiHandle, c_char_p(b"Output_Resampled.txt"))
				iLinesDetected = windll.CT400_lib.CT400_GetNbLinesDetected(uiHandle)
				LinesArraySize = c_double * iLinesDetected
				dLinesValues = LinesArraySize()
				windll.CT400_lib.CT400_ScanGetLinesDetectionArray(uiHandle, byref(dLinesValues) ,iLinesDetected)
				PowerArraySize = c_double * 1
				(Pout, P1, P2, P3, P4, Vext) = (PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize(), PowerArraySize())
				windll.CT400_lib.CT400_ReadPowerDetectors(uiHandle, byref(Pout), byref(P1), byref(P2), byref(P3), byref(P4), byref(Vext))
				
				#---------------------------------------------------
				# do here whatever you need with your data

				for i in range(iPointsNumber):					
					print("{}{:.4f}{}{:.2f}".format("Lambda : ", dWavelengthSync[i]," ; DE_1: ", dDetector1Sync[i]))

				for i in range(iPointsNumberResampled):
					print("{}{:.3f}{}{:.2f}".format("Lambda : ", dWavelengthResampled[i]," ; DE_1: ", dDetector1Resampled[i]))

				#Display spectral lines detected, in case a light source is connected in port 2 and 4

				for i in range (iLinesDetected):
					print ("{}{}{}{:.4f}".format("Spectral line #", i+1, ": ", dLinesValues[i]))

				#---------------------------------------------------
				# Display the number of points for standard and resampled measurements
				print("{}{}".format("Total number of points: ", iPointsNumber))
				print("{}{}".format("Total of discarded points: ", iDiscardPoints[0]))
				print("{}{}".format("Total number of resampled points: ",iPointsNumberResampled))
				#---------------------------------------------------
				# Power on detectors is read and displayed
				print("{}".format("Power on Detectors"))
				print("{}{:.2f}".format("Pout = ", Pout[0]))
				print("{}{:.2f}".format("P1 = ", P1[0]))
				print("{}{:.2f}".format("P2 = ", P2[0]))
				print("{}{:.2f}".format("P3 = ", P3[0]))
				print("{}{:.2f}".format("P4 = ", P4[0]))
				print("{}{:.4f}".format("Vext = ", Vext[0]))
				#---------------------------------------------------
				# Laser in port 1 is disabled
				windll.CT400_lib.CT400_CmdLaser(uiHandle, LI_2, ENABLE, c_double(1550.0), c_double(5.0))
				
				strRet = 'OK'
			else: # the sweep failed: show error message from CT400
				strRet = 'Error: '+repr(tcError.value)
		else:
			strRet = 'Error: could not connect to CT400'
				
		# cleanup
		windll.CT400_lib.CT400_Close(uiHandle)
	else:  strRet = 'Error: could not connect to CT400' 	
	return strRet

if __name__ == '__main__': 
	try: # Python 2.x
		print (main())
	except: # Python 3.x
		print(main())
