# Label detection App with Soracom Cloud Camera Service and Amazon Rekognition

This application retrieves images from the Soracom Cloud Camera Service (Sorakame) using the SORACOM API, detects specific labels with Amazon Rekognition, and sends notifications via LINE Notify. You can deploy it using the AWS Serverless Application Model (SAM) template.

**Please note that it runs every minute by default.**

## Caution

The scripts in this repository are just examples and do not guarantee their operation. Also, the content of these scripts is not intended for commercial use. Please use at your own risk.

## Configuration

1. Regularly invoke AWS Lambda with Amazon EventBridge
2. Retrieve a list of events from the last minute with the Sorakame API
3. Download still images from when the event occurred
4. Label the still images with Amazon Rekognition
5. Notify the labeling results via LINE Notify

## Usage

You can use it following the steps below.

### Preparation

Prepare the necessary accounts and environment.

1. Prepare a camera compatible with [Soracom Cloud Camera Service](https://soracom.jp/sora_cam/) (A license agreement is required to use the API)
2. Set up [LINE Notify](https://notify-bot.line.me/ja/)
3. Prepare an [AWS](https://aws.amazon.com/jp/?nc2=h_lg) account
4. Prepare authentication information (authentication key ID, authentication key) for [SORACOM SAM Users](https://users.soracom.io/ja-jp/docs/sam/)
5. Set up [AWS Serverless Application Model](https://aws.amazon.com/jp/serverless/sam/) (SAM)

### Application Deployment

1. Prepare the necessary environment variables for deploying `sora-cam-label-detection-with-rekognition`.
   - soracomAuthKeyId: Authentication key ID for SORACOM SAM user
   - soracomAuthKey: Authentication key for SORACOM SAM user
   - deviceId: Device ID of the Sorakame compatible camera
   - lineNotifyToken: LINE Notify token
   - rekognitionRegion: Amazon Rekognition region
   - targetLabelName: Name of the label you want to detect
   - targetConfidence: Detect labels with this confidence or higher
2. Build and deploy `sora-cam-label-detection-with-rekognition`
   - Use `sam build` `sam deploy --guided --capabilities CAPABILITY_NAMED_IAM`

NOTE: If `sam build` fails due to a `PythonPipBuilder:ResolveDependencies` error, run `pip install wheel` or `pip3 install wheel` and try again.

NOTE: If you're running from CloudShell, install Python 3.9 on CloudShell. You can build and deploy with the following steps:

```
script/cloudshell_install_python39.sh
python3.9 -m venv .venv
source .venv/bin/activate
pip install wheel
sam build
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM
```

### Application Deletion

Applications deployed with SAM can be deleted using the `sam delete` command, or from the CloudFormation menu in the AWS Console.
