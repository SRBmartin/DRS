# SURVEY PROJECT

### Setting up the applications and environments

1. Clone the repository:
  * Open the folder you want to clone repository to and open **Git Bash**.
  * Take the HTTPS link in top right corner of repository and go back to Git bash and run ``` git clone [link] ```
    
2. Start up Docker
  * Open the command prompt in the base folder of your newly cloned repository.
  * Navigate to docker folder ``` cd .\docker\ ```
  * Pull and run the containers by running command ``` docker-compose up -d ```
  * This should create two containers (postgres_ & pgadmin_), verify this.
  * After this, the containers will be started and you can manage them easily by using **Docker desktop**
