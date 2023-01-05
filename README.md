# FalconScout
FalconScout is a powerful all in one low-code tool for scouting in FRC. The system is configured via 3 JSON and YAML files to setup a low-code scouting and admin app. FalconScout provides two apps, ScoutingApp and FalconScoutCore. 
1. ScoutingApp is a no-code form generation tool which can build PWA forms which generate a qrcode of data. This is then scanned on the FalconScoutCore system.
2. FalconScoutCore is a low-code app for scanning qrcodes, recording data, running data validation, and posting data to GitHub. 
    - Core contains a Data Validation tool which provides general and year specific tests on data you could collect. This system protects against common errors like scouting matches multiple times.
3. Posted data can be easily integrated into tools like **Tableau** or **Excel/Google Sheets** or [FalconVis](https://www.github.com/Team4099/FalconVis.git), 4099's low-code, online, data visualization tool.

![ui_visual](/docs/ui_visual.png)


## Docs
- [What is FalconScout](/docs/WHAT_IS_FALCONSCOUT.md)
- [Tool Setup Guide](/docs/TOOL_SETUP_GUIDE.md)
- [Quick Start](/docs/QUICK_START.md)
- [Configuring Datavalidation](/docs/CONFIGURING_DATAVALIDATION.md)
- [Example Forms](/docs/EXAMPLE_FORMS.md)
