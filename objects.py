class Box:
    left = None
    right = None
    upper = None
    bottom = None

    color = (100, 100, 100)

    def __init__(self, rect):
        self.preFilled = True
        self.playerFilled = False

        self.rect = rect

    def filled_box(self):
        return self.left.active and self.right.active and self.upper.active and self.bottom.active

    def get_color(self):
        if self.filled_box():
            # if self.preFilled:
            return self.color
        return (50, 50, 50)


class Edge:
    color = (150, 150, 150)

    active = True

    left_box = None
    right_box = None

    def __init__(self, rect):
        self.rect = rect

    def get_color(self):
        if self.active:
            return 150, 150, 150
        else:
            return self.color

    def reset_color(self, color):
        if not self.active:
            self.color = (40, 40, 40)

    def complete_edge(self, color):
        if self.left_box:
            if self.left_box.filled_box():
                # self.left_box.preFilled = False
                self.left_box.color = color
        if self.right_box:
            if self.right_box.filled_box():
                # self.right_box.preFilled = False
                self.right_box.color = color
        if self.left_box:
            if self.left_box.filled_box():
                return True

        if self.right_box:
            if self.right_box.filled_box():
                return True

        return False

