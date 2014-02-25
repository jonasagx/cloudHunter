#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include "Photo.h"
#define LOGGING

using namespace cv;
using namespace std;

/*
 * Base class for algortihms's decorator
 */
    
void Photo::Photo(const char* image_filename){
    this->image = this->loadImage(image_filename);
}	    

Mat* Photo::loadImage(string image_filename){
    Mat image = imread(image_filename);
#ifdef LOGGING
    cout << image_filename << " loaded" << endl;
#endif
    return &image;  
}
