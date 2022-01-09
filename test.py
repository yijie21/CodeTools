import os
img_folder = 'D:/datasets/stars/'
img_paths = os.listdir(img_folder)
for i, img_path in enumerate(img_paths):
    os.rename(os.path.join(img_folder, img_path), 
              os.path.join(img_folder, '{:0>6}.jpg'.format(i)))
    