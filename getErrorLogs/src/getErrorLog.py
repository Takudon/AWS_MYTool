############################################################
# Module      : ErrorLog
# Description : 
#  Get STS session token. 
#  
############################################################
import boto3
import json
import datetime
import argparse
import sys

import user_io

############################################################
# Module      : get_args
# Description : 
#  Get command line args. 
#  Refer to https://qiita.com/stkdev/items/e262dada7b68ea91aa0c.
############################################################
def get_args():
    # 準備
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--default", action="store_true")
    parser.add_argument("--app", type=str, required=False)  
    parser.add_argument("--init", required=False, action="store_true")
    parser.add_argument("--update", required=False, action="store_true")

    # 結果を受ける
    args = parser.parse_args()

    return(args)

############################################################
# Module      : get_credential
# Description : 
#  Get STS session token. 
#  I must use configured profile for secret data.
#  Care for usage of credentials
############################################################
def get_credential():
    session = boto3.session.Session(profile_name='odh')
    sts = session.client('sts')

    with open("../config/user_credential.json", "r") as f:
        u_credential = json.load(f)

    credentials = sts.get_session_token(
        SerialNumber=u_credential["_custom"]["MFAARN"],
        TokenCode=str(input("MFA OneTime Token Code >>"))
    )['Credentials']

    return credentials

############################################################
# Module      : get_error_events
# Description : 
#  Generate CloudWatchLogs client with session token.
#  Following method get focused log event.
#   >> logs.filter_log_events
############################################################

def get_error_events(credentials, config):
    # CloudWatch logs client.
    logs_client = boto3.client(
        'logs',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name=config["Region"]
    )

    # Paginator
    logs_paginator = logs_client.get_paginator('filter_log_events')
    
    # Pagineation
    events_list = []
    for page in logs_paginator.paginate(
            logGroupName=config["LogGroup"],
            logStreamNames=config["LogStreams"],
            filterPattern=config["Filter"],
            startTime=from_timestamp,
            endTime=to_timestamp
        ):
        events_list += page["events"]

    return events_list

############################################################
# Module      : isPresense
# Description : 
#  Search the specified parameter into 1 level json list.
#  This function returns True(Boolean) if the param presents,
#  False otherwise.
############################################################
def isPresense(dict, param):
    if param in dict.values():
        return True
    else:
        return False

############################################################
# Module      : get_credential
# Description : 
#  Get STS session token. 
#  I must use configured profile for secret data.
#  Care for usage of credentials
############################################################

if __name__ == "__main__":
    # Get app name;
    args = get_args()

    # Get one time access token.
    credentials = get_credential()

    # Get reseach configurations.
    with open("../config/config.json", "r") as f:
        configs = json.load(f)

    if args.default:
        for config in configs["Configurations"]:
            # 期間を指定する タイムゾーンに注意
            (from_datetime, to_datetime) = user_io.get_datetime(config["App"])

            OUTPUT_FILE = "{0:%Y%m%d%H%M%S}".format(from_datetime) \
                + "-" + "{0:%Y%m%d%H%M%S}".format(to_datetime)\
                + ".log"

            #filter_log_eventsの期間指定はミリ秒なので1000倍する必要がある
            from_timestamp = int(from_datetime.timestamp()) * 1000
            to_timestamp = int(to_datetime.timestamp()) * 1000

            events = get_error_events(credentials, config)

            message = []
            for log in events:
                tmp_msg = "".join(log["message"].splitlines())
                tmp_msg.replace("\t", "")
                message.append(tmp_msg)

            message = "\n".join(message)

            with open("../data/"+config["App"]+"/"+OUTPUT_FILE, "w") as f:
                f.write(message)
    elif args.update:
        app = args.app
        for config in configs["Configurations"]:
            # Check the exsitance.
            if not isPresense(config, str(app)):
                continue

            # 期間を指定する タイムゾーンに注意
            (from_datetime, to_datetime) = user_io.get_datetime(config["App"])

            OUTPUT_FILE = "{0:%Y%m%d%H%M%S}".format(from_datetime) \
                + "-" + "{0:%Y%m%d%H%M%S}".format(to_datetime)\
                + ".log"

            #filter_log_eventsの期間指定はミリ秒なので1000倍する必要がある
            from_timestamp = int(from_datetime.timestamp()) * 1000
            to_timestamp = int(to_datetime.timestamp()) * 1000

            events = get_error_events(credentials, config)

            message = []
            for log in events:
                tmp_msg = "".join(log["message"].splitlines())
                tmp_msg.replace("\t", "")
                message.append(tmp_msg)

            message = "\n".join(message)

            with open("../data/"+config["App"]+"/"+OUTPUT_FILE, "w") as f:
                f.write(message)
    elif args.init:
        app = args.app
        for config in configs["Configurations"]:
            # Check the exsitance.
            if not isPresense(config, str(app)):
                continue

            # 期間を指定する タイムゾーンに注意
            to_datetime = datetime.datetime.now()
            from_datetime = to_datetime - datetime.timedelta(days=7)

            OUTPUT_FILE = "{0:%Y%m%d%H%M%S}".format(from_datetime) \
                + "-" + "{0:%Y%m%d%H%M%S}".format(to_datetime)\
                + ".log"

            #filter_log_eventsの期間指定はミリ秒なので1000倍する必要がある
            from_timestamp = int(from_datetime.timestamp()) * 1000
            to_timestamp = int(to_datetime.timestamp()) * 1000

            events = get_error_events(credentials, config)

            message = []
            for log in events:
                tmp_msg = "".join(log["message"].splitlines())
                tmp_msg.replace("\t", "")
                message.append(tmp_msg)

            message = "\n".join(message)

            with open("../data/"+config["App"]+"/"+OUTPUT_FILE, "w") as f:
                f.write(message)
