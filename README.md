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
