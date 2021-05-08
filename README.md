This repo contains a multimodal CNN implemented in Keras for appearence-based gaze prediction.
CNN is based on LeNet architecture [1] and was created following descriptions and available information from "Appearance-Based Gaze Estimation in the Wild" by Zhang etal. [2].

The model as an input accepts an eye region image and 2 angles for the head (camera - yaw and pitch) rotation. The ouput of the model is a vector of two eye rotation angles (gaze estimation - yaw and pitch).

The repo also contains dataset [3] generated using UnityEyes[4] - a freely available tool for rapid generation of large numbers of variable eye region images[5].

The dataset consists of 3 files in NPY format:
dataset_x_img.npy - images of synthesised eye regions (36x60x1)
dataset_x_head_angles.npy - head (camera) rotation angles (radians)
dataset_y_gaze_angles.npy - eye gaze vectors (radians)


[1] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” 
    Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998. 
    [Online]. Available: https://doi.org/10.1109/5.726791

[2] X. Zhang, Y. Sugano, M. Fritz, and A. Bulling, “Appearance-based gaze estimation in the wild,”
    Proceedings of the IEEE conference on computer vision and pattern recognition, 2015, pp. 4511–4520. 
    [Online]. Available: https://doi.org/10.1109/CVPR.2015.7299081
    
[3] https://tinyurl.com/UnityEyesDataset

[4] https://www.cl.cam.ac.uk/research/rainbow/projects/unityeyes/tutorial.html

[5] E. Wood, T. Baltrušaitis, L.-P. Morency, P. Robinson, and A. Bulling, “Learning an appearance-based gaze estimator from one million synthesised images,” 
    ser. ETRA ’16. New York, NY, USA: Association for Computing Machinery, 2016, p. 131–138. 
    [Online]. Available: https://doi.org/10.1145/2857491.2857492
