/************************** Yenista Optics ************************************/
/* Header file for CT400_lib.dll                                              */
/*                                                                            */
/******************************************************************************/

#ifndef CT400_LIB_H
#define CT400_LIB_H
#   if defined (CT400_LIB_EXPORT)
#       define _DECLSPEC __declspec(dllexport)
#   else
#       define _DECLSPEC __declspec(dllimport)
#   endif

// Definition of the integer types
#include "CT400_Types.h"

#ifdef __cplusplus
extern "C"
{
#endif

  typedef enum
  {
    LS_TunicsPlus = 0,
    LS_TunicsPurity,
    LS_TunicsReference,
	LS_TunicsT100s_HP,
    LS_TunicsT100r,
    LS_JdsuSws,
    LS_Agilent,
	NB_SOURCE
  } rLaserSource;

  typedef enum
  {
	LI_1 = 1,
    LI_2,
	LI_3,
    LI_4
  } rLaserInput;

  typedef enum
  {
	DE_1 = 1,
	DE_2,
	DE_3,
	DE_4,
	DE_5
  } rDetector;

  typedef enum
  {
    DISABLE = 0,
    ENABLE
  } rEnable;

  typedef enum
  {
    Unit_mW = 0, Unit_dBm
  } rUnit;


//------------------------------ CT400_Init ------------------------------------
// Function CT400_Init
//
//  Purpose: Initialises the CT400 Dll
//
//  Parameters: IN/OUT iError : pointer over a variable
//
//  Returns:  uiHandle for use in subsequent functions
//            uiHandle = 0 indicate that init() failed
//			  iError = -1001, DSP firmware version not compatible
//------------------------------------------------------------------------------
_DECLSPEC uint64_t __stdcall CT400_Init(int32_t *iError);

//------------------------------ CT400_CheckConnected---------------------------
// Function CT400_CheckConnected
//
//  Purpose: Checks if CT400 is connected
//
//  Parameters: IN uiHandle: from CT400_Init
//
//  Returns:  1 if CT400 is connected, 0 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_CheckConnected(uint64_t uiHandle);

//------------------------------ CT400_GetNbInputs------------------------------
// Function CT400_GetNbInputs
//
//  Purpose: Returns the number of available inputs
//
//  Parameters: IN uiHandle: from CT400_Init
//
//  Returns:  number of inputs if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_GetNbInputs(uint64_t uiHandle);

//------------------------------ CT400_GetNbDetectors---------------------------
// Function CT400_GetNbDetectors
//
//  Purpose: Returns the number of available detectors
//
//  Parameters: IN: uiHandle: from CT400_Init
//
//  Returns:  number of detectors if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_GetNbDetectors(uint64_t uiHandle);

//------------------------------ CT400_GetCT400Type  ---------------------------
// Function CT400_GetCT400Type
//
//  Purpose: Returns the CT400 type
//  0: SMF
//  1: PM13
//  2: PM15
//
//  Parameters: IN uiHandle: from CT400_Init
//
//  Returns:  CT400 Type if success(0, 1, 2), -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_GetCT400Type(uint64_t uiHandle);


//------------------------------ CT400_SetLaser --------------------------------
// Function CT400_SetLaser
//
//  Purpose: Configures lasers connected to the CT400
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eLaser: Laser # defined as enum
//              IN eEnable: Enables /Disables the laser output
//              IN iGPIBAdress: Laser GPIB address
//              IN eLaserType: Laser type defined as enum
//              IN dMinWavelength: Laser min wavelength
//              IN dMaxWavelength: Laser max wavelength
//              IN Speed: Laser speed
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SetLaser(uint64_t uiHandle,
rLaserInput eLaser, rEnable eEnable, int32_t iGPIBAdress,
rLaserSource eLaserType, double dMinWavelength,
double dMaxWavelength, int32_t Speed);

//------------------------------ CT400_SetSamplingResolution -------------------
// Function CT400_SetSamplingResolution
//
//  Purpose: Configures CT400 sampling resolution
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eResolution: sampling resolution defined as enum
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SetSamplingResolution(uint64_t uiHandle,
uint32_t uiResolution);

//------------------------------ CT400_SetScan ---------------------------------
// Function CT400_SetScan
//
//  Purpose: Configures CT400 scan properties
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN dLaserPower: Laser power in mW
//              IN dMinWavelength: scan min wavelength
//              IN dMaxWavelength: scan max wavelength
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SetScan(uint64_t uiHandle, double dLaserPower,
double dMinWavelength, double dMaxWavelength);

//------------------------------ CT400_SetDetectorArray ------------------------
// Function CT400_SetDetectorArray
//
//  Purpose: Configures CT400 active detectors
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eDect2: Enables/Disables detector 2
//              IN eDect3: Enables/Disables detector 3
//              IN eDect4: Enables/Disables detector 4
//              IN eExt: Enables/Disables BNC C connector
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SetDetectorArray(uint64_t uiHandle,
rEnable eDect2, rEnable eDect3, rEnable eDect4, rEnable eExt);

//------------------------------ CT400_SetBNC ----------------------------------
// Function CT400_SetBNC
//
//  Purpose: Configures CT400 external BNC detector
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eEnable: if 1 (BNC C input is converted to optical power)
//                          if 0 (BNC C input is read as voltage)
//              IN dAlpha: Alpha param (out = Ax + B)
//              IN dBeta: Beta param (out = Ax + B)
//              IN eUnit: Units defined as enum
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SetBNC(uint64_t uiHandle, rEnable eEnable,
double dAlpha, double dBeta, rUnit eUnit);

//------------------------------ CT400_SetExternalSynchronization --------------
// Function CT400_SetExternalSynchronization
//
//  Purpose: Configures CT400 external synchronization output
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eEnable: Enables/disables external sync
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SetExternalSynchronization(uint64_t uiHandle,
rEnable eEnable);

//------------------------------ CT400_SetExternalSynchronizationIN ------------
// Function CT400_SetExternalSynchronizationIN
//
//  Purpose: Configures CT400 external synchronization input
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eEnable: Enables/disables external sync-in
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_SetExternalSynchronizationIN(uint64_t uiHandle, rEnable eEnable);

//------------------------------ CT400_ScanStart -------------------------------
// Function CT400_ScanStart
//
//  Purpose: Starts CT400 scan
//
//  Parameters: IN uiHandle: from CT400_Init
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanStart(uint64_t uiHandle);

//------------------------------ CT400_ScanStop --------------------------------
// Function CT400_ScanStop
//
//  Purpose: Stops CT400 scan
//
//  Parameters: IN uiHandle: from CT400_Init
//  Returns:  0 if success, -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanStop(uint64_t uiHandle);

//------------------------------ CT400_ScanWaitEnd -----------------------------
// Function CT400_ScanWaitEnd
//
//  Purpose: Waits for scan to end and returns errors
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT tcError[1024]: Initialized array that stores the
//									  description of the error
//  Returns:  error number and error description (0 = no error) if success.
//			  -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanWaitEnd(uint64_t uiHandle,
char tcError[1024]);

//------------------------------ CT400_GetNbDataPoints -------------------------
// Function CT400_GetNbDataPoints
//
//  Purpose: Returns the number of valid data points
//
//  Parameters: IN uiHandle: from CT400_Init
//				IN/OUT iDataPoints: pointer over a variable
//									(number of valid data points)
//              IN/OUT iDiscardPoints: pointer over a variable
//									   (index value associated to the
//									   first-valid top-pulse)
//  Returns:  number of valid data points and index value of the first-valid
// 			  top pulse associated to the first measured data point(if success).
//			  -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_GetNbDataPoints (uint64_t uiHandle,
int32_t *iDataPoints, int32_t *iDiscardPoints);

//------------------------------ CT400_GetNbDataPointsResampled ----------------
// Function CT400_GetNbDataPointsResampled
//
//  Purpose: Returns the number of available resampled data points
//
//  Parameters: IN uiHandle: from CT400_Init
//
//  Returns:  the number of resampled available data in the array.
//			  -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_GetNbDataPointsResampled (uint64_t uiHandle);

//------------------------------ CT400_GetNbLinesDetected ----------------------
// Function CT400_GetNbLinesDetected
//
//  Purpose: Returns the number of lines detected with hetedodyne detection
//
//  Parameters: IN uiHandle: from CT400_Init
//
//  Returns:  the number of lines detected.
//			  -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_GetNbLinesDetected (uint64_t uiHandle);

//------------------------------ CT400_ScanGetLinesDetectionArray --------------
// Function CT400_ScanGetLineDetectionArray
//
//  Purpose: Returns the line detection array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns:  value of corresponding data points in the array.
//			  -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanGetLinesDetectionArray (uint64_t uiHandle,
double dArray[], int32_t iArraySize);

//------------------------------ CT400_ScanGetWavelengthSyncArray --------------
// Function CT400_ScanGetWavelengthSyncArray
//
//  Purpose: Returns the Wavelength sync array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns:    available data points in the array and the corresponding
//				data values.
//			   -1 otherwise
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanGetWavelengthSyncArray(uint64_t uiHandle,
double dArray[], int32_t iArraySize);

//---------------------- CT400_ScanGetWavelengthResampledArrayResampled --------
// Function CT400_ScanGetWavelengthResampledArray
//
//  Purpose: Returns the Resampled wavelength sync array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns: available data points in the array and the corresponding
//			 data values, -1 otherwise.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanGetWavelengthResampledArray(uint64_t uiHandle,
double dArray[], int32_t iArraySize);


//------------------------------ CT400_ScanGetPowerSyncArray -------------------
// Function CT400_ScanGetPowerSyncArray
//
//  Purpose: Returns the Power out array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns:  available data points in the array and the corresponding
//			  data values, -1 otherwise.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanGetPowerSyncArray(uint64_t uiHandle,
double dArray[], int32_t iArraySize);

//------------------------------ CT400_ScanGetPowerResampledArray --------------
// Function CT400_ScanGetPowerResampledArray
//
//  Purpose: Returns the Resampledolated Power out array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns:  available data points in the array and the corresponding
//			  data values, -1 otherwise.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanGetPowerResampledArray(uint64_t uiHandle,
double dArray[], int32_t iArraySize);

//------------------------------ CT400_ScanGetDetectorArray --------------------
// Function CT400_ScanGetDetectorArray
//
//  Purpose: Returns the Detector X out array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eDetector: number defined as enum
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns:  available data points in the array and the corresponding
//			  data values, -1 otherwise.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ScanGetDetectorArray(uint64_t uiHandle,
rDetector eDetector, double dArray[], int32_t iArraySize);

//--------------------------- CT400_ScanGetDetectorResampledArray---------------
// Function CT400_ScanGetDetectorResampledArray
//
//  Purpose: Returns the resampled detector X out array
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eDetector: number defined as enum
//              IN/OUT dArray: pointer over an initialized array
//              IN iArraySize: size of the array
//  Returns:  available data points in the array and the corresponding
//			  data values, -1 otherwise.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanGetDetectorResampledArray(uint64_t uiHandle, rDetector eDetector,
double dArray[], int32_t iArraySize);

//------------------------------ CT400_ScanSaveWavelengthSyncFile --------------
// Function CT400_ScanSaveWavelengthSyncFile
//
//  Purpose: Returns the wavelength sync as a .txt file
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT pcPath: String path to the file to write
//  Returns:  0 if sucess and the corresponding file path, -1 otherwise.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanSaveWavelengthSyncFile(uint64_t uiHandle, char *pcPath);

//---------------------------- CT400_ScanSaveWavelengthResampledFile -----------
// Function CT400_ScanSaveWavelengthResampledFile
//
//  Purpose: Returns the resampled wavelength sync as a .txt file
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT pcPath: String path to the file to write
//  Returns:  0 if success and the corresponding file path, otherwise -1.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanSaveWavelengthResampledFile(uint64_t uiHandle, char *pcPath);

//------------------------------ CT400_ScanSavePowerSyncFile -------------------
// Function CT400_ScanSavePowerSyncFile
//
//  Purpose: Returns the power out as a .txt file
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT pcPath: String path to the file to write
//  Returns:  0 if success and the corresponding file path, otherwise -1.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanSavePowerSyncFile(uint64_t uiHandle, char *pcPath);

//---------------------------- CT400_ScanSavePowerResampledFile ----------------
// Function CT400_ScanSavePowerResampledFile
//
//  Purpose: Returns the resampled power out as a .txt file
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT pcPath: String path to the file to write
//  Returns:  0 if success and the corresponding file path, otherwise -1.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanSavePowerResampledFile(uint64_t uiHandle, char *pcPath);

//------------------------------ CT400_ScanSaveDetectorFile --------------------
// Function CT400_ScanSaveDetectorFile
//
//  Purpose: Returns the Detector X out as a .txt file
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eDetector number define as enum
//              IN/OUT pcPath: String path to the file to write
//  Returns:  0 if success and the corresponding file path, otherwise -1.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanSaveDetectorFile(uint64_t uiHandle, rDetector eDetector, char *pcPath);

//------------------------------ CT400_ScanSaveDetectorResampledFile -----------
// Function CT400_ScanSaveDetectorResampledFile
//
//  Purpose: Returns the resmpled detector X out as a .txt file
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eDetector number define as enum
//              IN/OUT pcPath: String path to the file to write
//  Returns:  0 if success and the corresponding file path, otherwise -1.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ScanSaveDetectorResampledFile(uint64_t uiHandle, rDetector eDetector,
char *pcPath);

//------------------------------ CT400_UpdateCalibration -----------------------
// Function CT400_UpdateCalibration
//
//  Purpose: Calibrates internal detectors to cancel loss from a previous scan
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eDetector number define as enum
//  Returns:  0 if success, otherwise -1.
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_UpdateCalibration(uint64_t uiHandle,
rDetector eDetector);

//------------------------------ CT400_ResetCalibration ------------------------
// Function CT400_ResetCalibration
//
//  Purpose: Resets all calibration done by CT400_UpdateCalibration
//
//  Parameters: IN uiHandle: from CT400_Init
//  Returns:  0 if success, otherwise -1
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_ResetCalibration(uint64_t uiHandle);

//------------------------------ CT400_SwitchInput -----------------------------
// Function CT400_SwitchInput
//
//  Purpose: Selects the input laser switch
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eLaser: LI_1 to LI_4
//  Returns:  0 if success, otherwise -1
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_SwitchInput(uint64_t uiHandle,
rLaserInput eLaser);

//------------------------------ CT400_ReadPowerDetectors-----------------------
// Function CT400_ReadPowerDetectors
//
//  Purpose: Reads power on detectors
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN/OUT Pout: Pointer over a variable (Power on output)
//              IN/OUT P1: Pointer over a variable (Power on Dectector 1)
//              IN/OUT P2: Pointer over a variable (Power on Dectector 2)
//              IN/OUT P3: Pointer over a variable (Power on Dectector 3)
//              IN/OUT P4: Pointer over a variable (Power on Dectector 4)
//              IN/OUT Vext: Pointer over a variable (Voltage on Ext)
//  Returns:  0 if success, otherwise -1
//------------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall
CT400_ReadPowerDetectors(uint64_t uiHandle, double *Pout, double *P1,
double *P2, double *P3, double *P4, double *Vext);

//------------------------------ CT400_CmdLaser---------------------------------
// Function CT400_CmdLaser
//
//  Purpose: Pilots a laser
//
//  Parameters: IN uiHandle: from CT400_Init
//              IN eLaser: Laser # define as enum
//              IN eEnable: Enables/Disables the laser output
//              IN dWavelength: Wavelength to move to
//              IN dPower: Power to set
//  Returns:  0 if success, otherwise -1
//----------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_CmdLaser(uint64_t uiHandle, rLaserInput eLaser, rEnable eEnable, double dWavelength, double dPower);

//------------------------------ CT400_Close ---------------------------------
// Function CT400_Close
//
//  Purpose: Releases memory allocated by the CT400 DLL
//
//  Parameters: IN uiHandle: from CT400_Init
//  Returns:  0 if success, otherwise -1
//----------------------------------------------------------------------------
_DECLSPEC int32_t __stdcall CT400_Close(uint64_t uiHandle);

#ifdef __cplusplus
}
#endif


#endif


