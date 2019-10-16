##############################################################################
# get_latest_datetime
# Display datetime of latest execution time of an AWS Lambda function.
##############################################################################
function get_latest_datetime($lambda_function){
    # Get LogGroupNams
    $LogGroup = aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/$lambda_function" | ConvertFrom-Json

    if($null -eq $LogGroup.LogGroups[0]){
        return "F"
        exit
    }

    $LogGroupName = $LogGroup.logGroups[0].logGroupName
    $LogStreams = aws logs describe-log-streams --log-group-name $LogGroupName --output=text --query "logStreams[*].logStreamName"
    $LatestLog = $LogStreams[-1].Split("`t")[-1]

    return $LatestLog.Substring(0, 10)
}

##############################################################################
# read_function_name
# Read CSV file and get AWS Lambda function name.
##############################################################################
function list_function_execdatetime($input_csv, $Destination){ 

    $contents = Import-Csv $input_csv
    foreach($function in $contents){
        $datetime = get_latest_datetime($function.Name)
        $element = $function.Name + ", " + $datetime
        Write-Output  $element | Add-Content -Encoding utf8 $Destination
    }
}

list_function_execdatetime "./csv/list_functions.csv" "./csv/function_execdatetime.csv"
