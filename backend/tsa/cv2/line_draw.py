import cv2


class LineDrawer:
    def __init__(self, frame, frame_name):
        self.frame = frame
        self.frame_name = frame_name
        self.lines = []
        self.current_line = None

    def __call__(self, event, x, y, flags, param):
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        if self.current_line is None:
            self._create_new_line(x, y)
        else:
            self._finish_existing_line(x, y)

        cv2.imshow(self.frame_name, self.frame)

    def _create_new_line(self, x, y):
        self.current_line = (x, y)
        cv2.circle(self.frame, (x, y), 2, (0, 0, 0))

    def _finish_existing_line(self, x, y):
        self.lines.append((self.current_line[0], self.current_line[1], x, y))

        cv2.line(self.frame, (self.current_line[0], self.current_line[1]), (x, y), (0, 0, 0), 2)

        self.current_line = None
