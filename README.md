# FalconScout
An all-in-one tool for building scouting apps for FRC


## Backend
- [Quick Start](/docs/QUICK_START.md)
- [Full Installation Guide](/docs/FULL_INSTALLATION_GUIDE.md)
- [Data Pipeline Explination](/docs/DATA_PIPIELINE_EXPLINATION.md)
- [Configuring Datavalidation](/docs/CONFIGURING_DATAVALIDATION.md)
- [Example Forms](/docs/EXAMPLE_FORMS.md)

### Installing dependencies
- Create virtual env.
    ```sh
    $ python3 -m venv venv
    ```
- Activate virtual env.
    ```sh
    $ # Linux/macOS
    $ source venv/bin/activate  
    $ # Windows
    $ venv\Scripts\activate    
    ```
- Install packages in the virtual env.
    ```sh
    (venv) $ pip install package-name
    (venv) $ pip install -r requirements.txt
    
### Pre-Commit
Whenever you attempt to commit files, a pre-commit hook will run to lint your code. You should fix all issues before pushing.
