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
 
# Main ==================================================================

import win32com.client
import ctypes, sys
import warnings
import HookingModule

from EventHandlers import NktSpyMgrEvents

if sys.version_info.major < 3:
	warnings.warn("Python 3.0 is needed for this program to run", RuntimeWarning)
	sys.exit(0)

# We initialize a SpyMgr COM object with NktSpyMgrEvents callbacks.
win32com.client.pythoncom.CoInitialize()
spyManager = win32com.client.DispatchWithEvents("DeviareCOM.NktSpyMgr", NktSpyMgrEvents)
result = spyManager.Initialize()

if not result == 0:
	print ("ERROR: Could not initialize the SpyManager. Error code: %d" % (result))
	sys.exit(0)

# We'll let the HookingMgr class defined in HookingModule handle the hooking for us.
HookingModule.HookingManager = HookingModule.HookingMgr(spyManager)

if len(sys.argv) == 1:
	# We launch the Chrome process ourselves.
	HookingModule.HookingManager.OpenApp()
else:
	for i in range(1, len(sys.argv)):
		# We attach and hook the process identified in the argument.
		print ("PID attach request for " + sys.argv[i])
		pid = int(sys.argv[i])
		HookingModule.HookingManager.HookFunctionsForProcess(pid)
		HookingModule.HookingManager.applist.append(pid)

# UI
MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox(None, "Press OK to end the demo.", "Deviare Python Demo", 0)

for pid in HookingModule.HookingManager.applist:
	print ("Process " + str(pid) + " terminated.")
	# We obtain the INktProcess COM object from the spy manager.
	app = spyManager.ProcessFromPID(pid)
	app.Terminate(0)

