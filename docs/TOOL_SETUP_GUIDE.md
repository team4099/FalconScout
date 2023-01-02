# FalconScout Tool Setup Guide
Team 4099's scouting system to generate, ingest, and visualize match data for competition.

# Installation

## Installing Python

A Quick Guide for Installing Python on Common Operating Systems

1. [Install on Windows](#windows-)
2. [Install on MacOS](#macos-)
3. [Install on Linux](#linux-)

## **Windows** 
1. If you have not yet installed Python on your Windows OS, then download and install the **latest Python3** installer from [Python Downloads Page](https://www.python.org/downloads/)
   - Make sure to check the box during installation which adds Python to PATH. Labeled something like **Add Python 3.X to PATH**

2. Once Python is installed, you should be able to open a command window, type `python`, hit ENTER, and see a Python prompt opened. Type `quit()` to exit it. You should also be able to run the command `pip` and see its options. If both of these work, then you are ready to go.

  - If you cannot run `python` or `pip` from a command prompt, you may need to add the Python installation directory path to the Windows PATH variable
    - The easiest way to do this is to find the new shortcut for Python in your start menu, right-click on the shortcut, and find the folder path for the `python.exe` file
      - For Python2, this will likely be something like `C:\Python27`
      - For Python3, this will likely be something like `C:\Users\<USERNAME>\AppData\Local\Programs\Python\Python37`
    - Open your Advanced System Settings window, navigate to the "Advanced" tab, and click the "Environment Variables" button
    - Create a new system variable:
      - Variable name: `PYTHON_HOME`
      - Variable value: <your_python_installation_directory>
    - Now modify the PATH system variable by appending the text `;%PYTHON_HOME%\;%PYTHON_HOME%;%PYTHON_HOME%\Scripts\` to the end of it.
    - Close out your windows, open a command window and make sure you can run the commands `python` and `pip`

## **MacOS**
MacOS comes with a native version of Python. As of this writing, it comes with a version of Python2, which has been deprecated. In order to use most modern Python applications, you need to install Python3. Python2 and Python3 can coexist on the same machine without problems, and for MacOS it is in fact necessary for this to happen, since MacOS continues to rely on Python2 for some functionality.

There are a couple of ways we can install Python3 on your MacOS operating system:

### Option 1: Install the official Python release
1. Browse to the [Python Downloads Page](https://www.python.org/downloads/)
2. Click on the "Download Python 3.x.x" button on the page
3. Walk through the steps of the installer wizard to install Python3
4. Once installed, the wizard will open a Finder window with some `.command` files in it
    - Double-click the `Install Certificates.command` file and the `Update Shell Profile.command` file to run each of them
    - Close the windows once they are finished
6. Open your **Terminal** application and run the command `python3` to enter the Python interactive command line. Issue the command `quit()` to exit. Also make sure PIP (the Python package manager) is installed by issuing the command `pip3 -V`. It should display the current version of PIP as well as Python (which should be some release of Python3).
7. You're all done. Python is installed and ready to use.

### Option 2: Install with Homebrew
[Homebrew](https://brew.sh/) is a MacOS Linux-like package manager. Walk through the below steps to install Homebrew and an updated Python interpreter along with it.

1. Open your **Terminal** application and run: `xcode-select --install`. This will open a window. Click **'Get Xcode'** and install it from the app store.
2. Install Homebrew. Run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - You can also find this command on the [Homebrew website](https://brew.sh/)
3. Install latest Python3 with `brew install python`
4. Once Python is installed, you should be able to open your **Terminal** application, type `python3`, hit ENTER, and see a Python 3.X.X prompt opened. Type `quit()` to exit it. You should also be able to run the command `pip3` and see its options. If both of these work, then you are ready to go.
  - Here are some additional resources on [Installing Python 3 on Mac OS X](https://docs.python-guide.org/starting/install3/osx/)

## **Linux**
- **Raspberry Pi OS** may need Python and PIP
  - Install them: `sudo apt install -y python3-pip`
- **Debian (Ubuntu)** distributions may need Python and PIP
  - Update the list of available APT repos with `sudo apt update`
  - Install Python and PIP: `sudo apt install -y python3-pip`
- **RHEL (CentOS)** distributions usually need PIP
  - Install the EPEL package: `sudo yum install -y epel-release`
  - Install PIP: `sudo yum install -y python3-pip`

# PyCharm

In order to run the application you are going to need an IDE that does a lot of stuff for you. Install PyCharm.
- [Windows PyCharm Installation](https://www.jetbrains.com/help/pycharm/installation-guide.html#standalone)
- [macOS PyCharm Instalation](https://www.jetbrains.com/help/pycharm/installation-guide.html#c272f695)

# Github

## Windows

### Step 1 - Installing Git

1. **Download** *Git* from [Git for Windows](https://gitforwindows.org) and **install it**.

### Step 2 - Cloning the repository

1. Create a folder somewhere accessible, this will be the folder you download the Tableau file into.
2. [Copy the file path of your newly made folder](https://www.youtube.com/watch?v=MVoQhYWJuvw)

Open a command prompt window and run the following commands. If a command uses <> then don't actually put the <> when you run the command.
- Ex: `cd C:\Documents\Newsletters\Summer2018.pdf`

```
cd <YOUR_COPIED_FILE_PATH>
git clone https://github.com/team4099/falconscout.git
```

## Mac OS

Open a new terminal window

### Step 1 – Install [*Homebrew*](http://brew.sh/)

> *Homebrew* […] simplifies the installation of software on the Mac OS X operating system.

– [Homebrew – Wikipedia](http://en.wikipedia.org/wiki/Homebrew_%28package_management_software%29)

**Copy & paste the following** into the terminal window and **hit `Return`**.

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew doctor
```

You will be offered to install the *Command Line Developer Tools* from *Apple*. **Confirm by clicking *Install***. After the installation finished, continue installing *Homebrew* by **hitting `Return`** again.

### Step 2 – Install *Git*

**Copy & paste the following** into the terminal window and **hit `Return`**.

```shell
brew install git
```

### Step 3 - Cloning the repository

1. Create a folder somewhere accessible, this will be the folder you put stuff into.
2. [Copy the file path of your newly made folder](https://osxdaily.com/2015/11/05/copy-file-path-name-text-mac-os-x-finder/)

Open a command prompt window and run the following commands. If a command uses <> then don't actually put the <> when you run the command.
- Ex: `cd /Users/ballen/github`

```
cd <YOUR_COPIED_FILE_PATH>
git clone https://github.com/team4099/falconscout.git
```

## Linux
If you're maining Linux, you'll probably already know how to install git onto your machine.

Clone this repo using this command

```
git clone https://github.com/team4099/falconscout.git
```

# Javascript Installation
This is very long to do so [here](https://github.com/npm/cli) is info on how to install npm and the bundled version of node. 

# Conclusion
Once you can verify that you have installed the following, move onto the [Quick Start](./QUICK_START.md)
 - Python
 - Node / Npm
 - Git
 - IDE (PyCharm, VSCode)