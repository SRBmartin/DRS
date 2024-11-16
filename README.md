# SURVEY PROJECT

### Setting up the applications and environments

1. Clone the repository:
  * Open the folder you want to clone repository to and open **Git Bash**.
  * Take the HTTPS link in top right corner of repository and go back to Git bash and run ``` git clone [link] ```
    
2. Start up Docker
  * Open the command prompt in the base folder of your newly cloned repository.
  * Navigate to docker folder ``` cd .\docker\ ```
  * Pull and run the containers by running command ``` docker-compose -p survey-project up -d --build ```
  * This should create two containers (postgres_container & pgadmin_container), verify this.
  * After this, the containers will be started and you can manage them easily by using **Docker desktop**
    
3. Setting up database server
  * Log into pgAdmin @ ``` https://localhost:5050 ``` with credentials user@email.com & admin.
  * Click on ``` Servers -> Register -> Server ```
  * In **General** tab, enter the name you like, for example survey-db.
  * In **Connection** tab**:
    * In **Host name/address**: postgres_container (this is the name of the container defined in docker-compose.yml)
    * In **Port**: Put the port 5432
    * In **Maintenance database**: survey
    * In **Username**: dev (check from docker-compose.yml)
    * In **Password**: Drs1312! (check from docker-compose.yml)
  * Click Save and you should be able to browse to the database 'survey'
4. Setting up Python
 * If you don't have, you should install python 3.9 by running ``` winget install --id=Python.Python.3.9 --source=winget ```
 * After installing Python, verify that you have it bu running ``` python --version ``` and you should get something like ``` Python 3.9.13 ```
 * Now, from the **root** folder, navigate to ``` cd .\backend\api\ ``` and run the following ``` python -m venv venv ```.
 * After this, you will type ``` .\venv\Scripts\Activate ``` and will install dependencies ``` pip install -r requirements.txt ```.
 * After this, you should be able to run Flask application ``` python app.py ```

5. Setting up Angular
 * If you don't have, install Node.js by running ``` winget install --id=OpenJS.NodeJS -e  ``` and check if it's properly install by running ``` npm --version ```
 * Install Angular CLI by running ``` npm install -g @angular/cli ``` and verify the installation by running ``` ng version ```
 * From the **root** repo folder, navigate to ``` cd .\frontend\survey-project\ ``` and run ``` npm i ```.
 * You can start Angular application by running ``` npm start ``` or ``` ng serve ``` for development purposes.
