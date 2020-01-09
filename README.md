# Big Code : What it is ?
  - It is prototype pipeline to apply machine learning on source code. It has five main programs:

      > A program to find repositories on Github on the basis of some criteria and dump the
        results in a csv file.

      > A program to process (get AST also using Babelfish) a git repo and write the output file
        in a csv file which can be feed to a neural network models.

      > A program to train a set of Neural Network Models (LSTM) on the basis of the data 
        created in the last step.

      > A program to get inference on the basis of the trained model.

      > A set of examples to demonstrate how to build neural network models. 
 
# Requirements:

- Babelfish - Universal Code Parser 
    > (1) Get Babelfish Docker container with the command: ref ->  https://hub.docker.com/r/bblfsh/bblfshd
    
    > `docker pull bblfsh/bblfshd`
    
    >  (2) Install the required driver with the command (make sure docker/babelfish is up and running)
    
    > `docker exec -it bblfshd bblfshctl driver install --all`
    
    >  Install Python client : ref ->  https://github.com/bblfsh/python-client 
    
    > `pip3 install bblfsh` 

- Machine Learning Tools :
    > `conda  create --name  bigcode_env python=3.6 `
    
    > `$ conda activate bigcode_env`
    
    > `$ pip install -r requirements.txt`
    
    
# Running the code :

    -  Review the input parameter files (data_input.ini and ml_input.ini) in 'config' directory.  

    - (1) Get a list of repos by running the following [This is optional]
    
     `$ python github_data_crawler.py --help`
    
    - (2) Process the giit data :
    
     `$ python driver_data.py -c config/input_data.ini `
    
    - (3) Launch the ML Pipeline 
    
    > `$ python driver_ml.py -c config/input_ml.ini`
    
#  References :

   >  https://doc.bblf.sh/
  
   > https://github.com/src-d/awesome-machine-learning-on-source-code 


 
