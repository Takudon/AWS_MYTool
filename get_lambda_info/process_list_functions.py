import pandas as pd
import numpy as np
import glob
import json

######################################################################################
# Function: check_env
# Author  : Taku Tanaka
# Check product environment of lambda function and return env name.
# Env devided to STG, PROD, DEV, and F that is short of Fuck.
######################################################################################
def check_env(function_name):
    if "stg" in function_name:
        return "stg"
    elif "prod" in function_name:
        return "prod"
    elif "dev" in function_name:
        return "dev"
    else:
        return "F"

######################################################################################
# Function: process_list_functions
# Author  : Taku Tanaka
# Process AWS Lambda functions INFO listed up by following aws cli command into CSV.
# COMMAND: aws lambda list-functions --region $REGION
######################################################################################
def process_list_functions(dir):
    columns = ["Region", "Env", "Name", "Runtime", "LastModified"]

    filenames = glob.glob("./"+dir+"/*")

    func_list = []
    for fname in filenames:
        print(fname)
        with open(fname, encoding="utf_8_sig") as f:
            data = json.load(f)["Functions"]
            for d in data:
                region = d["FunctionArn"].split(":")[3]
                env = check_env(d["FunctionName"])
                func_list.append([region, env, d["FunctionName"], d["Runtime"], d["LastModified"][0:10]])
    
    df = pd.DataFrame(func_list, columns=columns)
    print(df.head())

    df.to_csv("./csv/list_functions.csv", encoding="utf8", index=True)


if __name__ == "__main__":
    process_list_functions("json")