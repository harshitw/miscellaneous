# non maximum compression for object detection
# nms.py

# NOTE: common values for overlapThresh are generally between 0.3 and 0
import numpy as np
def non_max_suppresion(boxes, overlapThresh):
    if len(boxes) == 0:
        return []

    # initialize the list of picked indexes
    pick = []
    x1, y1, x2, y2 = boxes[:,0], boxes[:,1], boxes[:,2], boxes[:,3]

    # computing the area of the bounding boxes and sort the boxes by the bottom right y coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0 :
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        suppress = [last]

        # loop over all the indexes in idexes list
        for pos in range(0, last):
            j = idxs[pos]
            # find the largest (x, y) coordinates for the start of the bounding box and the smallest x,y coordinates for the end of the bounding box
            xx1 = max(x1[i], x1[j])
            yy1 = max(y1[i], y1[j])
            xx2 = min(x2[i], x2[j])
            yy2 = min(y2[i], y2[j])

            # compute the width and the height of the bounding box
            w = max(0, xx2 - xx1 + 1)
            h = max(0, yy2 - yy1 + 1)

            # compute the ratio of overlap between the computed bounding box and the bounding box in the area list
            overlap = (w * h)/area[j]
            # if there is sufficient overlap then suppress the current bounding box
            if overlap > overlapThresh:
                suppress.append(pos)

        # delete all the indexes that are in the suppression list
        idxs = np.delete(idxs, suppress)

    # return only the bpunding boxes that were picked
    return boxes[pick]

###########################333  The faster version of non maximum compression is also possible
