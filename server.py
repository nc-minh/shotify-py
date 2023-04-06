from concurrent import futures
import logging
import grpc
import service_shotifypy_pb2_grpc
import rpc_make_img_pb2
import imgkit
from PIL import Image


def gen_img_from_html(html):
    FILE_NAME = "source.html"
    OUTPUT_FILE = 'out.png'

    with open(FILE_NAME, "w") as file:
        file.write(html)
        file.close()

    options = {
        'encoding': "UTF-8",
    }

    imgkit.from_file(FILE_NAME, 'out.png', options=options)
    print("Starting to generate image from html")

    image = Image.open(OUTPUT_FILE)
    # Get the current size of the image
    width, height = image.size
    # Set the desired width
    desired_width = 600
    # Calculate the left and right coordinates for cropping
    left = (width - desired_width) // 2
    right = left + desired_width
    # Define the area to crop
    area = (left, 0, right, height)

    # Crop the image
    cropped_image = image.crop(area)
    cropped_image.save(OUTPUT_FILE)


class Shotifypy(service_shotifypy_pb2_grpc.ShotifypyServicer):

    def HtmlSnapshot(self, request, context):
        print("Start")
        # request.html
        print(request.html)
        gen_img_from_html(request.html)
        return rpc_make_img_pb2.MakeImageFromHtmlResponse(message="Done")


def serve():
    port = '6060'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_shotifypy_pb2_grpc.add_ShotifypyServicer_to_server(
        Shotifypy(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
