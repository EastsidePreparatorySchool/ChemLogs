""" code from https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/ """

import cv2
from pyzbar.pyzbar import decode


def BarcodeReader(image):
    

    # read the image in numpy array using cv2
    img = cv2.imread(image)
      
    # Decode the barcode image
    detectedBarcodes = decode(img)
      
    # If not detected then print the message
    if not detectedBarcodes:
        print("no barcode")
    elif detectedBarcodes.__len__() > 1:
        print("multiple barcodes detected. move camera so there is only one in view")
        print(detectedBarcodes.__len__())
    else:
        # this shouldn't need to be a for loop -- should only happen once
          # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes: 
           
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
             
            # Put the rectangle in image using
            # cv2 to highlight the barcode. is this necessary? what does it do?
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10),
                          (255, 0, 0), 2)
             
            if barcode.data == "":
                print("no data")
            else:
                # Print the barcode data
                print("data and type:")
                print(barcode.data)
                print(barcode.type)
                 
    #Display the image
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
  # Take the image from user
    image="barcodeTest/random5.png"
    BarcodeReader(image)

# using camera. does this work on iOS, and how?
# camera = cv2.VideoCapture(0)
# result, image = camera.read()
# if result:
#     cv2.imshow("cameraimg.png", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()