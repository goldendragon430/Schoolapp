import cv2
import fitz
import numpy as np
def extract_image_pdf(pdfpath):
    doc = fitz.open(pdfpath)
    for page in doc:
        pix = page.get_pixmap()
        pix.save("outfile.png")
        break
def is_true_image(thresh):
    # Count the number of black pixels
    black_pixels = np.count_nonzero(thresh == 0)
    # Calculate the total number of pixels
    total_pixels = thresh.shape[0] * thresh.shape[1]
    # Calculate the percentage of black pixels
    percent_black = (black_pixels / total_pixels) * 100
    return percent_black > 80
if __name__ == '__main__':

    image = cv2.imread('outfile.png')
    height, width, _ = image.shape
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 180, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
         if len(contour) > 10:
            ellipse = cv2.fitEllipse(contour) 
            (x, y), (major_axis, minor_axis), angle = ellipse

            # Calculate the aspect ratio of the ellipse
            aspect_ratio = major_axis / minor_axis

            # Check if the aspect ratio is within a certain range to consider it as an ellipse
            if  0.3 < aspect_ratio and major_axis > 10 and angle < 160 and y > height/3:
                # Draw the contour
                x, y, w, h = cv2.boundingRect(contour)
                # Extract the subimage within the bounding rectangle
                subimage = image[y:y+h, x:x+w]
                # Display the subimage
                if is_true_image(subimage) == True:
                    cv2.drawContours(image, [contour], -1, (0, 255, 0), 1)

    cv2.imshow('finalImg',image)
    cv2.waitKey(0)