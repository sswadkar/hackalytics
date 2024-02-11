import cv2
import torch
import torchvision.transforms as transforms
from datetime import datetime

class ImageClassifier:

    class_names = [
        "person", "bicycle", "car", "motorcycle", "airplane",
        "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
        "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
        "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
        "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
        "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
        "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
        "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
        "couch", "potted plant", "bed", "dining table", "toilet", "TV", "laptop",
        "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
        "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
        "teddy bear", "hair drier", "toothbrush"
    ]

    def __init__(self):
        #self.classifier = torch.hub.load('ultralytics/yolov5', 'custom', path="/Users/swadkar/gatech/hackalytics/flask/yolov5/runs/train/exp/weights/best.pt", force_reload=True)
        #self.classifier.eval()
        self.classifier = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


    def runDetection(self, frame):

        # convert cv2 frame to tensor frame

        #frame_resized = frame
        frame_resized = cv2.resize(frame, (640, 640))  # Replace with expected dimensions

        tensor = transforms.ToTensor()(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))[None, ...]
        
        results = self.classifier(tensor)

        output = results.squeeze(0)  # Remove the batch dimension, now shape is [25200, 85]

        # Define thresholds
        conf_threshold = 0.5
        nms_threshold = 0.6

        # Separate components of the output
        boxes = output[:, :4]  # Bounding box coordinates
        scores = output[:, 4]  # Objectness scores
        class_probs = output[:, 5:]  # Class probabilities

        # Filter out detections with objectness score below the threshold
        mask = scores >= conf_threshold
        boxes = boxes[mask]
        scores = scores[mask]
        class_probs = class_probs[mask]

        # Calculate the class scores by multiplying objectness score with class probabilities
        class_scores = scores.unsqueeze(-1) * class_probs

        # For each detection, find the class with the highest score
        max_scores, max_classes = class_scores.max(dim=1)

        # Filter out detections with max class score below a threshold (this is optional and depends on your use case)
        mask = max_scores >= conf_threshold
        boxes = boxes[mask]
        max_scores = max_scores[mask]
        max_classes = max_classes[mask]

        # Apply Non-Maximum Suppression (NMS) for each class
        nms_indices = torch.ops.torchvision.nms(boxes, max_scores, nms_threshold)

        # Final detections
        final_boxes = boxes[nms_indices]
        final_scores = max_scores[nms_indices]
        final_classes = max_classes[nms_indices]

        # final_boxes, final_scores, and final_classes now contain your filtered, scored, and suppressed detections
        
    
        height, width, _ = frame.shape
        height_r, width_r, _ = frame_resized.shape

        print(height, width)

        # Iterate over the detections
        for i in range(len(final_boxes)):
            box = final_boxes[i]
            score = final_scores[i]
            class_id = final_classes[i]

            # If your box coordinates are normalized (between 0 and 1), scale them to image dimensions
            # This step depends on how your boxes are formatted; adjust as necessary
            x_min, y_min, x_max, y_max = box
            x_min = int(x_min)
            x_max = int(x_max)
            y_min = int(y_min)
            y_max = int(y_max)

            # Define the box's color and label
            # You might want to have a predefined list of class names to convert class_id to a name
            color = (0, 0, 255)  # Blue color in BGR
            label = f"{self.class_names[class_id]}: {score:.2f}"

            # Draw the bounding box rectangle and label on the image
            frame_resized = cv2.rectangle(frame_resized, (x_min, y_min), (x_max, y_max), color, 2)
            frame_resized = cv2.putText(frame_resized, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        return frame_resized
        #return cv2.resize(frame_resized, (width, height))

i = ImageClassifier()

vid = cv2.VideoCapture(0) 
  
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    a = i.runDetection(frame)
  
    # Display the resulting frame 
    print(a.shape)
    cv2.imshow('frame', a) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 