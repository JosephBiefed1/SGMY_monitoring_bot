import requests
import os
import asyncio

def get_traffic_images():
    url = "https://api.data.gov.sg/v1/transport/traffic-images"
    response = requests.get(url)
    camera_list = list(filter(lambda x: x['camera_id'] in ['2701', '2702', '4713', '4703'], response.json()['items'][0]['cameras']))
    return camera_list

async def download_traffic_images(camera_list):
    for camera_info in camera_list:
        response = requests.get(camera_info['image'])
        if response.status_code == 200:
            image_path = os.path.join(r'motor_traffic_data', f'traffic_image{camera_info["camera_id"]}.jpg')
            with open(image_path, 'wb') as f:
                f.write(response.content)
                print("Image downloaded")
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")

async def main():
    camera_list = get_traffic_images()
    await download_traffic_images(camera_list)

if __name__ == '__main__':
    asyncio.run(main())