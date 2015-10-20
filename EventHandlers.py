#
# Copyright (C) 2010-2015 Nektra S.A., Buenos Aires, Argentina.
# All rights reserved. Contact: http://www.nektra.com
#
#
# This file is part of Deviare
#
#
# Commercial License Usage
# ------------------------
# Licensees holding valid commercial Deviare licenses may use this file
# in accordance with the commercial license agreement provided with the
# Software or, alternatively, in accordance with the terms contained in
# a written agreement between you and Nektra.  For licensing terms and
# conditions see http://www.nektra.com/licensing/. Use the contact form
# at http://www.nektra.com/contact/ for further information.
#
#
# GNU General Public License Usage
# --------------------------------
# Alternatively, this file may be used under the terms of the GNU General
# Public License version 3.0 as published by the Free Software Foundation
# and appearing in the file LICENSE.GPL included in the packaging of this
# file.  Please visit http://www.gnu.org/copyleft/gpl.html and review the
# information to ensure the GNU General Public License version 3.0
# requirements will be met.
#
#

# Module imports ======================================================================
import win32com.client
import HookingModule
 
# Event Handlers ======================================================================

class NktSpyMgrEvents:
	
	def OnAgentLoad(self, proc, errorCode):
		# A few processes will fail due to restricted privileges.
		if not errorCode == 0:
			print ("OnAgentLoad error code: %d" % (errorCode,))

	def OnProcessStarted(self, nktProcessAsPyIDispatch):
		nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
		# This will hook all chrome processes except for a few that have restricted privileges.
		if (nktProcess.Name == "chrome.exe"):
			print ("A Chrome process was started. (" + str(nktProcess.Id) + ")")
		elif (nktProcess.Name == "nacl64.exe"):
			print ("A Native Client process was started. (" + str(nktProcess.Id) + ")")
		else:
			return None
		HookingModule.HookingManager.HookFunctionsForProcess(nktProcess.Id)
		HookingModule.HookingManager.applist.append(nktProcess.Id)

	def OnProcessTerminated(self, nktProcessAsPyIDispatch):
		nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
		if (nktProcess.Name == "chrome.exe"):
			print ("A Chrome process was terminated. (" + str(nktProcess.Id) + ")")
		elif (nktProcess.Name == "nacl64.exe"):
			print ("A Native Client process was terminated. (" + str(nktProcess.Id) + ")")
		else:
			return None
		HookingModule.HookingManager.applist.remove(nktProcess.Id)

	def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):
		# We instantiate INktHookCallInfo and INktProcess objects. It's easy to get the hook through the call information object.
		nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
		nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
		if (nktHookCallInfo.Hook().FunctionName != "Ole32.dll!CoCreateInstance"):
			# For hooking experimentation.
			print (nktHookCallInfo.Hook().FunctionName + " was called.")
		elif (nktHookCallInfo.Params().First().GuidString == "{BCDE0395-E52F-467C-8E3D-C4579291692E}"):
			print ("MMDeviceEnumerator instantiated.")
			# Chrome instantiates an MMDeviceEnumerator object to select the recording device.
			# It is possible to hook more specific functionality: it involves hooking the interface of the COM object.
			# In this case in particular MMDeviceEnumerator is used to instantiate AudioClient and AudioCaptureClient objects later on.
			# This is done through the Activate() method. Hooking that method can be done to obtain more fine-grained control over the execution flow.
			# Skipping the call is enough for demonstration purposes.
			nktHookCallInfo.SkipCall()
			print ("Call skipped. No MMDeviceEnumerator for you!")
			# We set the return value of the function to an error code which should be handled appropriately to avoid crashing the application.
			# In this case we chose HRESULT E_POINTER (0x80004003). In the majority of cases any error should suffice though.
			nktHookCallInfo.Result().ULongVal = 0x80004003

		
			


