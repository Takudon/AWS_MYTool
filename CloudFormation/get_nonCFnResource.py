import boto3
import pandas as pd
import argparse

############################################################
# Module      : get_args
# Description : 
#  Get command line args. 
#  Refer to https://qiita.com/stkdev/items/e262dada7b68ea91aa0c.
############################################################
def get_args():
    # 準備
    parser = argparse.ArgumentParser()

    parser.add_argument("StackName", type=str)

    # 結果を受ける
    args = parser.parse_args()

    return(args)

def get_credential():
    session = boto3.session.Session(profile_name='odh')
    sts = session.client('sts')
    credentials = sts.get_session_token(
        SerialNumber='arn:aws:iam::745132880338:mfa/osk-taku_tanaka',
        TokenCode=str(input("MFA OneTime Token Code >>"))
    )['Credentials']

    return credentials

if __name__ == "__main__":
    args = get_args()
    credentials = get_credential()

    # Launch a cloudformation client.
    client = boto3.client(
        'cloudformation',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name="ap-southeast-1"
    )

    stack_resource = client.list_stack_resources(StackName=args.StackName)
    key = stack_resource["StackResourceSummaries"][0].keys()
    resouce_summary = stack_resource["StackResourceSummaries"]

    summary = pd.DataFrame(stack_resource["StackResourceSummaries"], columns = key)
    unique_resource = summary.ResourceType.unique()

    with open("../data/CFn_resource.csv", "r") as f:
        resource_txt = f.read()
        CFn_resource = resource_txt.split(",")

    not_CFnResource = list(set(unique_resource) - set(CFn_resource))
    for s in not_CFnResource:
        print(s)