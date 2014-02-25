#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

#define LOGGING

using namespace std;
using namespace cv;

class Photo {
    private:
    Mat image;
    
    public:
    //static const char* sccsid = "@(#) Nephos - jonas.agx@gmail.com";
    Photo(string image_filename);
    Mat loadImage(string image_filename):
    //void thresholdGray(int max, int min);
    //void crop(int heigth, int widht);
};
