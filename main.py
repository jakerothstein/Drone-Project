import cv2, imutils


class Drone:
    def __init__(self, frameScale):
        self.objectLoc = []
        self.frameScale = frameScale
        self.frameWidth = 0
        self.frameHeight = 0

    def motionDetection(self):

        tracker = cv2.TrackerCSRT_create()

        video = cv2.VideoCapture(0)

        self.frameWidth = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frameHeight = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(self.frameWidth)
        print(self.frameHeight)

        _, frame = video.read()
        frame = imutils.resize(frame, width=self.frameScale)
        self.objectLoc = cv2.selectROI('Target Selector', frame, False)
        tracker.init(frame, self.objectLoc)

        while video.isOpened():
            _, frame = video.read()
            frame = imutils.resize(frame, width=self.frameScale)
            track_success, self.objectLoc = tracker.update(frame)

            if track_success:
                top_left = (int(self.objectLoc[0]), int(self.objectLoc[1]))
                bottom_right = (int(self.objectLoc[0] + self.objectLoc[2]), int(self.objectLoc[1] + self.objectLoc[3]))
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 5)
            cv2.imshow('DroneView', frame)
            print(self.centerImg())

            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()

    def centerImg(
            self):  # used for gimbal pos gets the target area of the circle used to show how far off the gimbal is to the subject for optimal tracking
        return [((int(self.objectLoc[0] + self.objectLoc[2])) / 2) - self.frameHeight / 2,
                (int(self.objectLoc[1])) - (self.frameHeight / 2)]


drone = Drone(720)
drone.motionDetection()
