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
 
# Auxiliar Functions =====================================================================

import os, sys

HookingManager = None

class HookingMgr:
	spyManager = None
	applist = []
	functionModuleAndNameList = ["Ole32.dll!CoCreateInstance", "Winmm.dll!waveInMessage"]
	hookEnum = None

	def __init__(self, spyMgr):
		self.spyManager = spyMgr
		# Here we create the hooks for each function.
		self.InitializeHooks()
	
	def OpenApp(self):
		print ("Starting Chrome...")
		# We assume the Chrome executable path to be in "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
		appPath = os.path.join(os.environ['ProgramFiles(x86)'],"Google\\Chrome\\Application\\chrome.exe")
		# appPath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
		# CreateProcess takes a path and a boolean. If true is passed to it, it will suspend the process upon creation and return a cookie to resume the process later on.
		# It has two return values: the first is an INktProcess object and the second is the aforementioned cookie.
		app = self.spyManager.CreateProcess(appPath, False)
		if app is None:
			print ("Cannot launch Chrome.")
			sys.exit(0)

	def HookFunctionsForProcess(self, pid):
		for functionModuleAndName in self.functionModuleAndNameList:
			print ("Hooking function " + functionModuleAndName + " for PID " + str(pid))
		# We attach the INktHooks to the process. If true is passed as the second argument, the return from the call implies operation completion.
		self.hookEnum.Attach(pid, True)
		print ("Process " + str(pid) + " successfully hooked")
		
	def InitializeHooks(self):
		self.hookEnum = self.spyManager.CreateHooksCollection()
		for functionModuleAndName in self.functionModuleAndNameList:
			# CreateHook takes a function string (whose format is functionModule!functionName) and flags to customize the hook.
			# PostCall only hook flag = 0x0020, PreCall only hook flag = 0x0010, AutoHookChildProcess flag = 0x0001
			hook = self.spyManager.CreateHook(functionModuleAndName, 0x0010)
			self.hookEnum.Add(hook)
		# We activate the hooks in all processes.
		self.hookEnum.Hook(True)
	


