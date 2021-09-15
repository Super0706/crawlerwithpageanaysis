from skimage.metrics import structural_similarity as compare_ssim
import cv2


class PopSimilarity:

    def check_popup(self, img_one, img_two):
        # load the two input images
        image_first = cv2.imread(img_one)
        image_second = cv2.imread(img_two)
        # convert the images to grayscale
        gray_a = cv2.cvtColor(image_first, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_second, cv2.COLOR_BGR2GRAY)
        (score, diff) = compare_ssim(gray_a, gray_b, full=True)
        diff = (diff * 255).astype("uint8")
        print("similarity: {}".format(score))
        if score > 0.90:
            return False
        else:
            return True

