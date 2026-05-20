import cv2
import numpy as np

def main():
    cv2.namedWindow("pac_man", cv2.WINDOW_AUTOSIZE)
    while(True):
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.circle(frame, (320, 320), 200, (255, 0, 0), 5, cv2.LINE_AA)
        cv2.imshow("pac_man", frame)
        cv2.waitKey(1)
        if(cv2.getWindowProperty("pac_man", cv2.WND_PROP_VISIBLE) < 1):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()