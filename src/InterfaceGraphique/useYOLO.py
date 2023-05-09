from ultralytics import YOLO

# Load a model
model = YOLO('/home/romain/Perso/Cours/L3_deuxieme_semestre/projet-Programmation/TestYolo/runs/classify/train14/weights/best.pt')


results = model.predict(source='/home/romain/Perso/Cours/L3_deuxieme_semestre/projet-Programmation/images/imageSegmentee/') # source already setup

# print("test")

# for r in results:
#     print(r.probs)


