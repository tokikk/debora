import os
import boto3
from PIL import Image, ImageDraw
import datetime

target_bucket_name = os.environ['BUCKET_NAME']
access_key_id = os.environ['ACCESS_KEY_ID']
secret_access_key = os.environ['SECRET_ACCESS_KEY']
region_name = os.environ['REGION_NAME']


def put_to_s3_storage(src_img_path, key_name):
  try:    
    s3_client = boto3.client(
      's3',
      aws_access_key_id=access_key_id,
      aws_secret_access_key=secret_access_key,
      region_name=region_name
    )    
    # response = s3_client.head_bucket(Bucket=target_bucket_name)
        
    with open(src_img_path, 'rb') as f:
        destination_key = rf'{key_name}.{os.path.splitext(src_img_path)[1]}'
        s3_client.put_object(Body=f, Bucket=target_bucket_name, Key=destination_key)
        
    return destination_key
  except Exception as e:
    print(e, flush=True)
    return "err"


def detect_object_by_rekognition(result_img_path):
  try:
    client = boto3.client(
      'rekognition',
      aws_access_key_id=access_key_id,
      aws_secret_access_key=secret_access_key,
      region_name=region_name
)
    
    callback_text = ""
    response = client.detect_labels(Image={'S3Object':{'Bucket':target_bucket_name,'Name':'00.jpg'}}, MaxLabels=10)
    img = Image.open('')
    draw = ImageDraw.Draw(img)    
    for label in response['Labels']:
        callback_text += f"Label: {label['Name']}\n"
        callback_text += f"Confidence: {str(label['Confidence'])}\n"
        callback_text += "Instances:\n"
        for instance in label['Instances']:
            callback_text += "  Bounding box\n"
            callback_text += f"    Top: {str(instance['BoundingBox']['Top'])}\n"
            callback_text += f"    Left: {str(instance['BoundingBox']['Left'])}\n"
            callback_text += f"    Width: {str(instance['BoundingBox']['Width'])}"
            callback_text += f"    Height: {str(instance['BoundingBox']['Height'])}"
            callback_text += f"  Confidence: {str(instance['Confidence'])}\n\n"
            draw.rectangle(instance['BoundingBox']['Top'] * img.height,
                           instance['BoundingBox']['Left'] * img.width,
                           instance['BoundingBox']['Height'] * img.height,
                           instance['BoundingBox']['Width'] * img.width,
                           outline=(255, 0, 0), width=4)
            saved_path = os.path.join(rf"{result_img_path}", rf"result_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
            img.save(saved_path)

        callback_text += f"Parents:\n"
        for parent in label['Parents']:
            callback_text += f"   {parent['Name']}\n"
        callback_text += "\n"
        
    return {'text': callback_text, 'image': saved_path}
  except Exception as e:
    print(e, flush=True)
    return {'text': "err", 'image':''}
    