from dotenv import load_dotenv
import os
import json
import base64
import io
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# MODULE VARIABLES
OK_FACE_LANDMARKS = False
FACE_ATTR = ["emotion"]
API_PARAMS = dict(
    detection_model="detection_01",
    return_face_id=True,
    return_face_landmarks=OK_FACE_LANDMARKS,
    return_face_attributes=FACE_ATTR,
    recognition_model="recognition_04",
)


# LOAD ENV VARIABLES
# Create your own .env file and add SUBS_KEY & ENDPOINT
load_dotenv()

KEY = os.getenv("SUBS_KEY")
ENDPOINT = os.getenv("ENDPOINT")
print(KEY, ENDPOINT)

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


def get_image_stream(data):
    byte_stream = None
    byte_stream = io.BytesIO(base64.b64decode(data))
    return byte_stream


def face_detect(face_image: str, is_local: bool) -> json:
    """
    Params:
        is_local: Boolean to denote wether image is available locally or hosted
        face_image: path of image
    Desc:
    Returns face parameters and emotions
    Need to use detection model 01 for recognising emotions
    """
    try:
        if not is_local:
            detected_faces = face_client.face.detect_with_url(
                url=face_image, **API_PARAMS
            )
        else:
            detected_faces = face_client.face.detect_with_stream(
                image=get_image_stream(face_image), **API_PARAMS
            )

    except Exception as e:
        print("Services Module:", e)
        if str(e).find("429") != -1:
            raise Exception("API LIMIT")
        else:
            raise Exception("API FAIL")

    if not detected_faces:
        print("Services module: NO FACE DETECTED")
        return {}

    res = {}

    # Detected faces are in descending order of their face bounding boxes
    for face in detected_faces:
        res["emotion"] = json.loads(str(face.face_attributes.emotion).replace("'", '"'))
        break

    try:
        res["emotion"].pop("additional_properties")
    except:
        print("FAILED ADDITIONAL PROPERTIES DELETE IN FACE DETECT API")
    return res["emotion"]

print(face_detect("https://images.tribuneindia.com/cms/gall_content/2015/4/2015_4$largeimg07_Apr_2015_012525683.jpg",False))