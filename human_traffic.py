import cv2
import numpy as np

# Load YOLO model
net = cv2.dnn.readNet(r"darknet\yolov3.weights", r'darknet\cfg\yolov3.cfg') # edit the weights and cfg paths as per your setup

# Get the output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

print("Model loaded successfully.")

def extract_traffic_details(img_path):
    # Load an image to test
    
    image = cv2.imread(img_path)
    height, width, _ = image.shape


    # Prepare the image for the model
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Perform a forward pass to get the output
    outs = net.forward(output_layers)

    # Process the detections
    class_ids = []
    confidences = []
    boxes = []

    # Load the image

    # Iterate over the detections
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # Confidence threshold
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Draw rectangles around the detected objects
    for i in range(len(boxes)):
        box = boxes[i]
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the image with rectangles
    cv2.imwrite(img_path, image)
    # Count vehicles (assuming class_id for vehicles is known)
    human_count = len(class_ids)  # Example class IDs for vehicles

    print("Number of humans detected:", human_count)
    return human_count

extract_traffic_details(r"motor_traffic_data\traffic_image4713.jpg")