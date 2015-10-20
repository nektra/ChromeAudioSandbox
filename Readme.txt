Requisites: 
  1. Python 3 (tested with Python 3.4.3) with its pywin32 bindings.
  2. Deviare COM registration.
  3. Chrome (tested with Chrome 43.0.2357.130).

First of all, a Python 3 interpreter should be installed.
Corresponding pywin32 extension modules should be installed too. They can be obtained from http://sourceforge.net/projects/pywin32/files/

  To register the Deviare COM interfaces, visit http://www.nektra.com/products/deviare-api-hook-windows/ and download the package.
Alternatively you can clone the github repository and even build the binaries yourself.
Whichever you choose, to register the interfaces it is necessary to run a command line with administrator privileges and do the following:
    - Navigate to the bin directory of Deviare2.
		- Execute "regsvr32 DeviareCOM.dll"
		- If using a 64 bit operating system, execute "regsvr32 DeviareCOM64.dll"

  Furthermore, it is necessary to correctly configure Chrome to enable the hotword "Ok Google" extension. To do so, go to chrome://settings 
and set the default search engine to Google. A checkbox should appear just below. "Enable "Ok Google" to start a voice search."
After you check it, the hotword NaCl extension module should load automatically whenever you visit Google's homepage or open a new tab, 
provided that your country is supported. If this isn't the case (you won't see "Say "Ok Google"" within the search textbox, 
or any equivalent in your language), you'll have to use www.google.com.

  After testing it out, you're ready to try hooking Chrome to intercept the microphone. There are two ways to invoke the demonstration script.

  The first one is without arguments. In this case, it will try to guess the path to the executable of Chrome and launch it.
Immediately after that, the hooks are created and attached to the process.

The second way is to invoke it with a list of PIDs in this fashion:
  python3 ChromeAudioCaptureSandbox.py pid1 pid2 pid3 ... pidn
In this case, it will attach the created hooks to the specified PIDs.



Possible caveat:
  This script wasn't tested in Windows XP, and presumably it won't work since it is hooking APIs available in Windows Vista or later.
However, it shouldn't be difficult to find what API is used instead and hook the pertinent functions.

Known Issues:
  -Hooking the Chrome processes when the hotword NaCl module is running may crash Chrome.
We think it is normal for this to happen because at that point Chrome assumes the existence of a recording device.
The fact that we attach to it and trick it into thinking there is no such device is outside the possible normal execution flows.
Normally, the unavailability of a device would be notified through an unplug event.
  -These hooks will disable all sound. There is no fine-grained control over the interaction with the sound devices.