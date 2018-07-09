import learning_data
import sys, os
from PIL import Image
import numpy as np


# 명령줄에서 파일 이름 지정하기 --- (※1)
if len(sys.argv) <= 1:
    print("image-checker.py (<파일 이름>)")
    quit()
image_size = 50
root_dir = "../cropped_test_image/"
categories = os.listdir(root_dir)
# 입력 이미지를 Numpy로 변환하기 --- (※2)
X = []
files = []
for fname in sys.argv[1:]:
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    in_data = np.asarray(img)
    X.append(in_data)
    files.append(fname)
X = np.array(X)
# CNN 모델 구축하기 --- (※3)
model = learning_data.build_model(X.shape[1:])
model.load_weights("./data/celeb-model.hdf5")
# 데이터 예측하기 --- (※4)
html = ""
pre = model.predict(X)
for i, p in enumerate(pre):
    y = p.argmax()
    print("+입력:", files[i])
    print("|규동 이름:", categories[y])
    html += """
        <h3>입력:{0}</h3>
        <div>
          <p><img src="{1}" width=300></p>
          <p>규동 이름:{2}</p>
        </div>
    """.format(os.path.basename(files[i]),
        files[i],
        categories[y])
# 리포트 저장하기 --- (※5)
html = "<html><body style='text-align:center;'>" + \
    "<style> p { margin:0; padding:0; } </style>" + \
    html + "</body></html>"
with open("celeb-result.html", "w") as f:
    f.write(html)