# SSDC 2026 Ground Control Station 
This is the repository for the University of Florida's Space System Design Club Ground Control Station 2025-2026.

# User WARNINGS
- This repo is only intended for use with Linux and Unix Systems. Some of the features used by Tkinter for this app are not supported on Windows systems.
- Note that this repo relies on Tkinter already being bundled with your version of python. If you don't have Tkinter included, please install it before proceeding, or install it alongside the other packages in step 4.

# Installation
The following steps highlight how to start the code:
1. Ensure python3 is installed on your computer.
2. Clone the repository. 
3. After you enter the Ground-Control-Station directory create a python virtual environment to install your packages with the following command:
```bash
python3 -m venv .venv
```
4. Use the following command to activate the virtual environment to be ready to install the python packages:
```bash
source .venv/bin/activate
```
5. Inside of requirements.txt is a list of all the required packages. You may automatically install them all to the virtual environment using the following command:
```bash
python3 -m pip install -r requirements.txt
```
6. Finally just run ```make``` to start the GCS application!

# Notes:

The main.py file contains the file directories, and IP addresses for the different components of the GCS. If you want to change those, you can make the appropriate modifications in main.py

# Resources

[Cansat Competition Guide 2026](https://cansatcompetition.com/docs/CanSat_Mission_Guide_2026e.pdf)
