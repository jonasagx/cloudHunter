#include <iostream>
#include <opencv2/opencv.hpp>
#include "Photo.h"

#define LOGGING

using namespace cv;
using namespace std;

/*
 * Base class for algortihms's decorator
 */

class Photo {
public:
//Version identification string for compiler 
static const char* sccsid = "@(#) Nephos - jonas.agx@gmail.com";

Photo(string image_filename){
this->image = this->loadImage(image_filename);
}	    


Mat *loadImage(string image_filename){
Mat image = imread(image_filename);
#ifdef LOGGING
cout << image_filename << " loaded" << endl;
#endif
return &image;  
}

private:
Mat image;

}
