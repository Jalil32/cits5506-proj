import json
import boto3
import os
import urllib.parse
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='ap-southeast-2')
sns = boto3.client('sns', region_name='ap-southeast-2')
s3 = boto3.client('s3', region_name='ap-southeast-2')
iot_client = boto3.client('iot-data', region_name='ap-southeast-2')

# Configuration
IMPORTANT_LABELS = ['Person', 'Human', 'Vehicle', 'Car', 'Dog', 'Cat', 'Male', 'Female']
MIN_CONFIDENCE = 70
NOTIFICATION_TOPIC_ARN = os.environ.get('NOTIFICATION_TOPIC_ARN', 'arn:aws:sns:ap-southeast-2:123456789012:security-camera-notifications')
# Use your sandbox verified phone number - this must be verified in the SNS console first
PHONE_NUMBER = '+61432430383'  # Australian phone number format with country code - must be verified in sandbox

# IoT Topic for notifications
IOT_NOTIFICATION_TOPIC = "home/cameras/notification"
 
def lambda_handler(event, _):
    """
    Process uploaded frames from the security camera, detect labels with Rekognition,
    and send SMS notifications when important objects are detected.
    """
    try:
        # Extract S3 bucket and object information
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        logger.info(f"Processing new upload: {bucket}/{key}")
        
        # Only process files in the frames/ directory
        if not key.startswith('frames/'):
            logger.info(f"Skipping non-frame file: {key}")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Not a frame file, skipping'})
            }
        
        # Get timestamp directory from key
        # Format: frames/20230510_123045/frame_0.jpg
        key_parts = key.split('/')
        if len(key_parts) >= 3:
            timestamp = key_parts[1]
            video_key = f"clips/motion_{timestamp}.mp4"
            logger.info(f"Associated video file: {video_key}")
        else:
            video_key = None
            logger.warning(f"Could not determine associated video for frame: {key}")
        
        # Analyze the frame using Rekognition
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket, 
                    'Name': key
                }
            },
            MaxLabels=10,
            MinConfidence=MIN_CONFIDENCE
        )
        
        # Print all detected labels
        logger.info(f"All detected labels for {key}:")
        for label in response['Labels']:
            logger.info(f"  - {label['Name']}: {label['Confidence']:.2f}%")
        
        # Filter for important labels
        important_detections = []
        for label in response['Labels']:
            if label['Name'] in IMPORTANT_LABELS:
                important_detections.append({
                    'name': label['Name'],
                    'confidence': label['Confidence']
                })
        
        # Check if important labels were detected
        if important_detections:
            logger.info(f"Important labels detected in {key}:")
            for detection in important_detections:
                logger.info(f"  - {detection['name']}: {detection['confidence']:.2f}%")
            
            # Generate signed URLs for frame and video (valid for 24 hours)
            expire_time = 3600 * 24
            
            frame_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expire_time
            )
            
            video_url = None
            if video_key:
                video_url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket, 'Key': video_key},
                    ExpiresIn=expire_time
                )
            
            # Prepare result with important detections
            result = {
                'message': 'Important objects detected',
                'frame': key,
                'video': video_key,
                'detections': important_detections,
                'urls': {
                    'frame': frame_url,
                    'video': video_url
                }
            }
            
            # Create a message with detected objects for notifications
            detected_objects = ", ".join([f"{detection['name']} ({detection['confidence']:.1f}%)" 
                                       for detection in important_detections])
            
            timestamp_formatted = timestamp.replace('_', ' ').replace('T', ' ')
            notification_message = f"Security Alert: {detected_objects} detected at {timestamp_formatted}"
            
            # 1. Publish to IoT Topic
            try:
                # Determine notification type based on detected labels
                notification_type = "warning"  # Default
                
                # Person = warning, Vehicle = info, Other = info
                if any(d['name'] in ['Person', 'Human', 'Male', 'Female'] for d in important_detections):
                    notification_type = "warning"
                elif any(d['name'] in ['Vehicle', 'Car'] for d in important_detections):
                    notification_type = "info"
                
                # Prepare the IoT notification payload
                iot_payload = {
                    "message": notification_message,
                    "type": notification_type,
                    "timestamp": datetime.now().isoformat(),
                    "deviceId": "security-camera",
                    "metadata": {
                        "detections": important_detections,
                        "frameKey": key,
                        "videoKey": video_key,
                        "urls": {
                            "frame": frame_url,
                            "video": video_url if video_url else None
                        }
                    }
                }
                
                # Publish to IoT topic
                iot_response = iot_client.publish(
                    topic=IOT_NOTIFICATION_TOPIC,
                    qos=1,
                    payload=json.dumps(iot_payload)
                )
                
                logger.info(f"Published to IoT topic: {IOT_NOTIFICATION_TOPIC}")
                result['iot_notification'] = {
                    'status': 'sent',
                    'topic': IOT_NOTIFICATION_TOPIC
                }
            except Exception as iot_error:
                logger.error(f"Error publishing to IoT topic: {str(iot_error)}")
                result['iot_notification'] = {
                    'status': 'failed',
                    'error': str(iot_error)
                }
            
            # 2. Send SMS notification (existing functionality)
            try:
                # Create SMS message
                sms_message = f"Security Alert: {detected_objects} detected at {timestamp_formatted}."
                
                # Send the SMS
                sns_response = sns.publish(
                    PhoneNumber=PHONE_NUMBER,
                    Message=sms_message,
                    MessageAttributes={
                        'AWS.SNS.SMS.SenderID': {
                            'DataType': 'String',
                            'StringValue': 'SecCam'
                        },
                        'AWS.SNS.SMS.SMSType': {
                            'DataType': 'String',
                            'StringValue': 'Transactional'
                        }
                    }
                )
                logger.info(f"SMS notification sent. MessageId: {sns_response['MessageId']}")
                
                # Add SMS info to result
                result['sms_notification'] = {
                    'status': 'sent',
                    'phone': PHONE_NUMBER,
                    'messageId': sns_response['MessageId']
                }
            except Exception as sms_error:
                logger.error(f"Error sending SMS notification: {str(sms_error)}")
                result['sms_notification'] = {
                    'status': 'failed',
                    'error': str(sms_error)
                }
            
            logger.info(f"Processing complete. Result: {json.dumps(result)}")
            
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            logger.info(f"No important labels detected in {key}")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No important objects detected',
                    'frame': key
                })
            }
            
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}")
        raise e
