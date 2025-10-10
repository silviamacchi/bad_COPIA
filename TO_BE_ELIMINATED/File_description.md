This file contains a description for each file present in the main folder
# files that CAN/SHOULD BE MODIFIED

## txt files
- metadata.txt: file containing the text that will be shown in the "Manage and install plugin" section in QGIS


## py files

- __init__.py: is the file that inizialises the plugin, so that QGIS knows that this is a plugin 

- BAD.py: this file contains the main plugin implementation, in particular: 
    1. How to add a toolbar icon to the toolbar and how to add the icon in the general QGIS interface
    2. Implementation of restore buttons that are present inside the plug-in to go back to the defaul visualization of the parameters
    3. Implementation of the code to save the outputs at the various steps
    4. Reading of the input and feature computation
    5. Membership Degree computation
    6. OWA computation
    7. Region Growing Algorithm 
    8. Severity computation 
    9. RG Severity computation and validity map
    10. run method that actually allow the buttons to function

- DoMagic.py: file that contains the implementation of the actual functions to do computations on data, for example: RegionGrowing function, membership function...

- Message.py: file containing the implementation of a message to the user

- Preview_window.py: file containing the implementation of of the preview window
## ui files, they can be modified opening them in Qt Designer
- BAD_dialog_base.ui: file containing the design of the main interface of the plugin
- preview window.ui: file containin the design of the preview window for validation
- Message.ui: file containing the design of a message to the user

# Files to upload in the official qgis plugin repo 
- plugin_upload.py

# Files that CANNOT BE MODIFIED
- BAD_dialog.py: This connects the implementation of the plugin with the designer of the interface
- icon.png: contains the fire icon
- resources.py: file needed to run the plugin
- resources.qrc: allow the icon image to be included in the binary of the application
- pylintrc: defines how Pylint should check the code(which rules to enable or disable, naming conventions, import paths, formatting standards...)
- pb_tool.cfg: file containing the configuration for the plug in builder
- Makefile: other file connected to the plugin builder

# Other, not useful for the actual pluging functioning
- both README files were automatically generated with the pluing builder and they contain few information on how to build a plugin
- LICENSE
- appoggio.txt: probabily a useless file that contains an older version for a certain function
