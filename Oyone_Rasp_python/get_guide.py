import numpy as np
import cv2

class Guide_getter():
    """
    initialize parameters of
    Canny edges detection
    HoughLines
    perspective transform
    """
    def __init__(self) -> None:
        # Canny parameters
        self.high_thresh = 450
        self.low_thresh = 150

        # HoughLinesP parameters
        self.rho = 2
        self.theta = np.pi/180
        self.threshold = 30
        self.mini_line_length = 10

        # perspective transform parammeters
        # [top_left, top_right, lower_left, lower_right]
        self.src_coordinate = np.float32([(200, 200), (420, 200), (0, 280), (620, 280)])
        self.dst_coordinate = np.float32([(0, 400), (400, 400), (0, 0), (400, 0)])
        self.bird_view_size = (400, 400)

        # ROI(Region of Interest) top coordinate
        self.ROI_top = 200

    """
    set frame to get guide line
    input
    frame: np.ndarray
    """
    def set_frame(self, frame) -> None:
        self.frame = frame

    """
    Get guide line index of bird's eye frame
    edges_img, bgr_bird_line_img are instance variables
    """
    def get_guide_line(self)->int:
        histogramLane = []        
        self.bgr_bird_line_img = self.frame.copy()

        # noise reduction -> edges detection -> lines detection
        non_noise = cv2.GaussianBlur(self.frame, (3,3), 2, 2)
        gray_img = cv2.cvtColor(non_noise, cv2.COLOR_BGR2GRAY)
        self.edges_img = cv2.Canny(gray_img, self.high_thresh, self.low_thresh)
        lines = cv2.HoughLinesP(self.edges_img, self.rho, self.theta, self.threshold, minLineLength=self.mini_line_length)

        # write detected line to frame
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(self.bgr_bird_line_img, (x1,y1),(x2,y2),(255, 0, 0),2)

        # transform input frame which line written to bird's eye frame
        trans_mat = cv2.getPerspectiveTransform(self.src_coordinate, self.dst_coordinate)
        self.bgr_bird_line_img = cv2.warpPerspective(self.bgr_bird_line_img, trans_mat, self.bird_view_size)

        #  bird's eye frame -> binary frame
        mask = cv2.inRange(self.bgr_bird_line_img, (255, 0,0), (255, 100, 100))
        gray_bird_line_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # calculate guide line from binary frame 
        for i in range(self.bird_view_size[0]):
            ROILane = np.sum(gray_bird_line_img[self.ROI_top:,i])
            histogramLane.append(ROILane)

        center_index = int(self.bird_view_size[0]/2)
        left_index = np.argmax(histogramLane[:center_index])
        right_index = np.argmax(histogramLane[center_index:]) + center_index
        guideline_index = int((right_index - left_index)/2 + left_index)

        # write right, left, center guide lines
        cv2.line(self.bgr_bird_line_img,(guideline_index,0),(guideline_index,self.bird_view_size[1]),(0,0,255),2)
        cv2.line(self.bgr_bird_line_img,(center_index,0),(center_index,self.bird_view_size[1]),(255,0,255),2)
        return guideline_index

    # get edge frame
    def get_edges_frame(self) -> np.ndarray:
        return self.edges_img

    # get bird's view frame with guide line
    def get_final_frame(self) -> np.ndarray:
        return self.bgr_bird_line_img
    
    # get input frame
    def get_input_frame(self) -> np.ndarray:
        return self.frame

"""
    If this file "get_guide.py" is executed directly, 
    guideline detection of the test image will be performed.
"""
if __name__=='__main__':
    img_path = 'load.jpeg'
    test = cv2.imread(img_path)

    test_getter = Guide_getter()
    test_getter.set_frame(frame=test)

    guide_line_index = test_getter.get_guide_line()
    guide_frame = test_getter.get_final_frame()

    cv2.imshow('test',guide_frame)
    cv2.waitKey(0)