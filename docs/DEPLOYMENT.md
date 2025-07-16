# FalconScout and FalconScoutCore Deployment


## FalconScout


**Deployment**


Every comp we send out a link that our members can use to scout with. We need to deploy our falconscout app before the competition starts to send out new updates to the scouting app. Scouters need to also add this new deployment as a PWA to enable scouting without a stable internet connection.


**steps**
1. Clone the repository and navigate to the app directory:
  ```bash
  git clone <repo_url>
  cd scoutingapp
  ```


2. Install dependencies and build the app:
  ```bash
  npm install
  npm run build
  ```
  This creates a `dist/` folder containing static files for deployment.  This is what you will use to paste into netlify   
- Open netlify: [https://app.netlify.com]
- Press deploy manually and paste in dist folder


![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdgPi5lVeUqFj4PASBbE2F4lotlNc4HL93lzrn2twJLXGXo5MZrNyRI0bojiEmn8HJ1xtVfnaw5vhAZqxO8YqWHcI-lCMVBkze-55Decl1tuz3FyJRWCJAUo8-BYOWuC4cmJLc?key=J0V1m3z5KovbrEM4V1CYsA)


- Change scouting app link to make it match our naming scheme. 




## FalconScoutCore




For FalconScoutCore, it’s not recommended to use a deployment to run it during competitions. It’s easier and recommended to just run the application locally with `python -m streamlit run app.py.` Visit the Quick Start documentation for more information.




There is more stuff to setup with GitHub, however


-  To add your personal github access token, make a file called .env in the `/falconscoutcore/` folder and add this line
   ```
     GITHUB\_KEY=<your key here>
   ```
-  Go into config/structure.json and change the last few lines to match the current event code.
-  Go to our other repo, team4099/ScoutingAppData and create the files that you just updated the names of.



