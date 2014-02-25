//#include "stdafx.h"
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
//using namespace cv;

int main(){
  IplImage* img = cv::cvLoadImage("/home/jonas/apps/nephos/3.png");
  cout << "Olá" << endl;
  
  return 0;
}
