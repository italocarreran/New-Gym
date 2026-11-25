import mediapipe as mp, json, glob, os
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
opts=vision.PoseLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path='pose_heavy.task'),running_mode=vision.RunningMode.IMAGE,num_poses=1,min_pose_detection_confidence=0.3)
det=vision.PoseLandmarker.create_from_options(opts)
out={}
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__),'../fotos/*.jpg'))):
    img=mp.Image.create_from_file(f); r=det.detect(img)
    k=os.path.basename(f)[:-4]
    if not r.pose_landmarks: print('NO POSE',k); continue
    out[k]={'img':[[l.x,l.y,l.z,l.visibility] for l in r.pose_landmarks[0]],
            'world':[[l.x,l.y,l.z,l.visibility] for l in r.pose_world_landmarks[0]]}
    print(k,'ok')
json.dump(out,open('poses.json','w'))
