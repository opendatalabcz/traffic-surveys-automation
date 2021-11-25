from matplotlib import pyplot as plt
import numpy as np


def visualize_detections(image, boxes, classes, scores, line_width=1, color=(0, 0, 1)):
    """Visualize Detections"""
    boxes = boxes * np.array([720, 1260, 720, 1260])

    plt.axis("off")
    plt.figure(figsize=(20, 15))
    plt.imshow(image)
    ax = plt.gca()
    for box, _cls, score in zip(boxes, classes, scores):
        text = "{}: {:.2f}".format(_cls, score)
        y1, x1, y2, x2 = box
        w, h = x2 - x1, y2 - y1
        patch = plt.Rectangle((x1, y1), w, h, fill=False, edgecolor=color, linewidth=line_width)
        ax.add_patch(patch)
        ax.text(
            x1,
            y1,
            text,
            bbox={"facecolor": color, "alpha": 0.4},
            clip_box=ax.clipbox,
            clip_on=True,
        )
    plt.show()
