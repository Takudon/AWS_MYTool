############################################################
# File        : list_functionINFO.py
# Author      : Taku Tanaka
# Description :
#  The python file is storing some modules to get AWS Lambda
#  usage information. I have used it them when I inventory 
#  Lambda functions.
############################################################


############################################################
# Module      : get_session_token
# Description : 
#  Get STS session token. 
#  Using access key, secret access key.
#  Care for usage of credentials
############################################################
def get_session_token():
    pass

############################################################
# Module      : get_functions
# Description :
#  Get information of AWS Lambda functions.
#  Return data will be format as dictionally data like json.
############################################################
def get_functions():
    pass

############################################################
# Module      : check env
# Description :
#  This module is used for check where the environment of 
#  lambda development. 
############################################################
def check_env():
    return env

############################################################
# Module      : process_functions
# Description :
#  Processing function information. I have got FunctionName,
#  Region, LastModified, 
#  LastExecution(get_latest_execution_time).
#  
############################################################
def process_functions():
    pass

############################################################
# Module      : get_latest_execution_time
# Description :
#  This module is used for get last execution time of each
#  Lambda functions.
############################################################
def get_latest_execution_time():
    pass

############################################################
# Module      : format_dataset
# Description :
#  Format dataset for replace and make CSV.
############################################################
def format_dataset():
    pass

############################################################
# Module      : type_dataframe
# Description :
#  irankamo.
#  
############################################################
def type_dataframe():
    pass
