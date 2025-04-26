from ultralytics import YOLO
import cv2
import numpy as np
import os
import pandas as pd
import asyncio

async def detect_vehicles(image_path):
    # Load the YOLO model
    dir_path = r'combined_data'
    model = YOLO("yolo11x.pt")  # Use a pretrained YOLO11 model

    # Load and resize the image for higher resolution detection
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.equalizeHist(image)
    high_res_image = cv2.resize(image, (1920, 1080))
    high_res_image = cv2.cvtColor(high_res_image, cv2.COLOR_GRAY2RGB)
    results = model(high_res_image, conf=0.1)

    # Define the vehicle classes based on the COCO dataset labels
    vehicle_classes = [1, 2, 3, 5, 7]  # 1: Bicycle, 2: Car, 3: Motorbike, 5: Bus, 7: Truck

    filename = os.path.basename(image_path)
    number = filename.replace('traffic_image', '').replace('.jpg', '')

    # Define the line for left/right separation
    if number == "2701":
        line_start = (1912, 277)
        line_end = (845, 845)
    elif number == "4703":
        line_start = (1813, 597)
        line_end = (211, 25)
    elif number == "4713":
        line_start = (1347, 70)
        line_end = (36, 1046)
    elif number == "2702":
        top_l = (779, 634)
        bot_l = (1177, 1073)
        top_r = (1392, 420)
        bot_r = (1809, 1017)

    # Function to determine if a point is to the left of a line
    def is_left_of_line(point, line_start, line_end):
        return (line_end[0] - line_start[0]) * (point[1] - line_start[1]) - (line_end[1] - line_start[1]) * (point[0] - line_start[0]) > 0

    # Create one more for the area of an enclosed rectangle
    def within_area(point, top_l, bot_l, top_r, bot_r):
        x, y = point
        return (top_l[0] <= x <= top_r[0] and top_l[1] <= y <= bot_l[1])

    # Count for left and right side vehicles
    left_count = 0
    right_count = 0
    total_count = 0
    # Process the detection results
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            if class_id in vehicle_classes:
                # Calculate the center point of the box
                x_center = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
                y_center = int((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
                center_point = (x_center, y_center)
                if number == "2701" or number == "4703" or number == "4713":
                    # Determine if the vehicle is on the left or right side of the line
                    if is_left_of_line(center_point, line_start, line_end):
                        left_count += 1
                        color = (0, 0, 255)  # Red for left side
                    else:
                        right_count += 1
                        color = (255, 0, 0)  # Blue for right side

                    # Draw the bounding box
                    cv2.rectangle(
                        high_res_image,
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                        (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                        color,
                        2
                    )
                    # Add the class label above the box
                    cv2.putText(
                        high_res_image,
                        f"{int(class_id)}",  # Display class ID (can replace with class name)
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )
                elif number == "2702":
                    color = (0, 0, 255)  # Red for left side
                    if within_area(center_point, top_l, bot_l, top_r, bot_r):
                        total_count += 1
                        # Draw the bounding box
                        cv2.rectangle(
                            high_res_image,
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                            (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                            color,
                            2
                        )
                        # Add the class label above the box
                        cv2.putText(
                            high_res_image,
                            f"{int(class_id)}",  # Display class ID (can replace with class name)
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            color,
                            2
                        )

    if number == '2701' or number == '4703' or number == '4713':
        # Draw the separation line on the image
        cv2.line(high_res_image, line_start, line_end, (0, 255, 0), 2)

    elif number == '2702':
        # Draw the box by connecting the corners
        cv2.line(high_res_image, top_l, top_r, (0, 255, 0), 2)
        cv2.line(high_res_image, top_r, bot_r, (0, 255, 0), 2)
        cv2.line(high_res_image, bot_r, bot_l, (0, 255, 0), 2)
        cv2.line(high_res_image, bot_l, top_l, (0, 255, 0), 2)

    file_name = os.path.join(dir_path, f"filtered_image{number}.jpg")
    print("Saved to:", file_name)
    cv2.imwrite(file_name, high_res_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    total_count = max(total_count, left_count + right_count)
    print("left_count: ", left_count)
    print("right_count: ", right_count)
    print("total_count: ", total_count)

    return left_count, right_count, total_count

async def main():
    df = pd.DataFrame(columns=['date', 'johor', 'woodlands', 'tuas'])
    johor = 0
    woodlands = 0
    tuas = 0

    for image_jpg in ['2701', '4703', '4713', '2702']:
        temp_j = 0
        temp_w = 0
        temp_t = 0
        mapping = {'2701': 'Johor_Woodlands', '2702': 'Woodlands_Customs', '4703': 'Johor_Tuas', '4713': 'Tuas_Johor'}
        image_path = r"motor_traffic_data\traffic_image{}.jpg".format(image_jpg)

        if image_jpg == '2701':
            temp_j, temp_w, temp = await detect_vehicles(image_path)
            johor += temp_j
            woodlands += temp_w
        elif image_jpg == '2702':
            temp, temp, temp_w = await detect_vehicles(image_path)
            woodlands += temp_w
        elif image_jpg == '4703':
            temp_t, temp_j, temp = await detect_vehicles(image_path)
            tuas += temp_t
            johor += temp_j
        elif image_jpg == '4713':
            temp_t, temp_j, temp = await detect_vehicles(image_path)
            tuas += temp_t
            johor += temp_j

    current_date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    row_df = pd.DataFrame({'date': [current_date], 'johor': [johor], 'woodlands': [woodlands], 'tuas': [tuas]})
    df = pd.concat([df, row_df], ignore_index=True)

    dir_path = r'combined_data'
    df.to_csv(os.path.join(dir_path, 'motor_traffic_data.csv'), index=False)

if __name__ == '__main__':
    asyncio.run(main())