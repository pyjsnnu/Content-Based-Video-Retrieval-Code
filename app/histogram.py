import cv2
from matplotlib import pyplot as plt
import numpy as np


def main():
    frame_count = 0
    colours = ('b', 'g', 'r')
    histograms_dict = {
        'b': list(),
        'g': list(),
        'r': list()
    }
    avg_histogram = np.zeros(shape=(255, 1))

    file_name = "test_video"
    video_capture = cv2.VideoCapture("../footage/{}.mp4".format(file_name))
    if not video_capture.isOpened():
        print("Error opening video file")

    # read the video and store the histograms for each frame per color channel in a dict
    while video_capture.isOpened():
        ret, frame = video_capture.read()  # read capture frame by frame
        if ret:
            frame_count = frame_count + 1
            if frame_count in [1, 5, 9]:  # todo - replace with some logic to only calculate specific frames
                for i, col in enumerate(colours):
                    histogram = cv2.calcHist([frame], [i], None, [256], [0, 256])
                    histograms_dict[col].append(histogram)
                    # debugging:
                    # print("i: {}, col: {}".format(i, col))
                    # plt.plot(histogram, color=col)
                    # plt.xlim([0, 256])
                # plt.show()

                # user exit on "q" or "Esc" key press
                k = cv2.waitKey(30) & 0xFF
                if k == 25 or k == 27:
                    break
        else:
            break

    # generate a single histogram by averaging all histograms of a video
    for col, hists in histograms_dict.items():
        for i in range(0, 255):  # loop through all bins
            bin_sum = 0

            # get value for each colour histogram in bin i
            for arr_index in range(0, len(hists)):
                bin_value = hists[arr_index].item(i)
                bin_sum = bin_sum + bin_value

            # average all bins values to store in new histogram
            new_bin_value = bin_sum / len(hists)
            avg_histogram[i] = new_bin_value

        np.savetxt('../histogram_data/{}-avg-histogram-{}'.format(file_name, col), avg_histogram, fmt='%d')
        plt.plot(avg_histogram, color=col)
        plt.xlim([0, 256])
    plt.show()

    # tidying up OpenCV video environment
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
