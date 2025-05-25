# Cloud Functions

This directory contains AWS Lambda functions for the security camera system that provides automated object detection and notification services.

## Overview

The cloud functions process security camera frames uploaded to S3, perform AI-powered object detection using AWS Rekognition, and send real-time notifications when important objects are detected.

## Files

- `lambda.py` - Main AWS Lambda function for frame processing and object detection

## Architecture

### AWS Lambda Function (`lambda.py`)

Processes uploaded camera frames and provides:

- **Object Detection**: Uses AWS Rekognition to detect objects in uploaded frames
- **Smart Filtering**: Identifies important objects (Person, Human, Vehicle, Car, Dog, Cat, Male, Female)
- **Dual Notifications**: Sends both IoT and SMS notifications
- **Media Access**: Generates signed URLs for frame and video access

### Workflow

1. **Trigger**: S3 bucket upload event for files in `frames/` directory
2. **Analysis**: AWS Rekognition analyzes the frame for objects
3. **Filtering**: Checks for important labels with minimum 70% confidence
4. **Notification**: Sends alerts via IoT topic and SMS if important objects detected
5. **Response**: Returns detection results with signed URLs

## Configuration

### Environment Variables

- `NOTIFICATION_TOPIC_ARN` - SNS topic ARN for notifications
- Phone number configured in code: `+61432430383` (must be verified in SNS sandbox)

### AWS Services Used

- **Rekognition** - Object detection and image analysis
- **SNS** - SMS notifications
- **S3** - Frame and video storage with signed URL generation
- **IoT Core** - Real-time notifications to web application

### Detection Settings

- **Important Labels**: Person, Human, Vehicle, Car, Dog, Cat, Male, Female
- **Minimum Confidence**: 70%
- **Max Labels**: 10 per analysis
- **URL Expiry**: 24 hours

## Notification Types

- **Warning**: Person/Human detection
- **Info**: Vehicle/Car detection  
- **Default**: Other important objects

## Deployment

This Lambda function should be configured with:

1. S3 trigger for the security camera bucket
2. Appropriate IAM permissions for Rekognition, SNS, S3, and IoT
3. Environment variables set
4. Phone number verified in SNS console (for sandbox)

## Infrastructure

Terraform can be used to configure all AWS infrastructure components for this system.

## Region

All AWS services configured for `ap-southeast-2` (Sydney) region.
