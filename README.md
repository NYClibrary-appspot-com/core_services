# DistributedSystem-And-CloudComputing
# git commands:
1. create you own branch
    - git checkout -b tusharBranch

2. switch to your branch from master to tusharBranch
    - git checkout tusharBranch
    
    - or: use force to checkout
        git checkout -f tusharBranch

3. git pull , eg: if you are behind
    - git pull

4. If you want to pull a branch and you edited your branch

    - stash the your branch   
         - git stash
         
    - then pull
        - pull master

5. if you want to rebase your branch with master
    - git rebase master


6. do not merge with master without conversation
    - eg: if you want to merge your local branch with - - - -    - tusharBranch
        - git merge tusharBranch
# Stop giving username and password for every commit:
- git config --global user.name "example@gmail.com"
- git config --global user.password "password"
# Create virtul environemnt to run python code
- install virtual environment:
- python -m pip  install --user  virtualenv

    - create an instance of virtual environment:
        - linux:
        - python -m virtualenv venv
        - window:
        - python -m venv venv
        
     - activate your virtual environment:
        - linux:
            - . venv/bin/activate
    - window:
          - .\venv\Scripts\activate

# Install "requirements.txt"
- pip install -r requirements.txt
    - or
        - pip3 install --user requirements.txt

# Expose mongodb PORT
 - # gcloud compute firewall-rules create allow-mongodb --allow tcp:27017


# Docker CMD
1. create an image from cmd
- docker build -t snowlibrary:latest .
2. confirm the build images
- docker images
3. run the image ("PORT-FORWORDING")
- docker run -it -d -p 5000:5000 snowlibrary
4. check if the image is running or not
- docker ps
5. stop the image (two steps):
    - docker ps (to get the running image id)
    - docker stop <imges-id>

# Deploy in google Kubernetes using google-console
- docker build -t gcr.io/pyback/snowlibrary:v1 .
- docker push gcr.io/pyback/snowlibrary:v1
# go inside cluster and click connect to get the link
- gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project pyback
- kubectl get pods
- kubectl expose deployment pyback --type=LoadBalancer --port 80 --target-port 5000
- kubectl get service
- kubectl scale deployment pyback --replicas=3
- kubectl get deployment pyback
# update version
- kubectl set image pyback=gcr.io/pyback/snowlibrary:v2