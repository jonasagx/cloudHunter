#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;

int main( int argc, char** argv ){
    Mat image, gray_scale;
    image = imread( argv[1], 1 );

    if( argc != 2 || !image.data ){
	printf( "No image data \n" );
	return -1;
    }

    //gray_scale = cvCreateImage(cvGetSize(image), 8, 1);
    cvtColor(image, gray_scale, CV_RGB2GRAY);

    threshold(gray_scale, gray_scale, 80, 255, CV_THRESH_TRUNC);
    //gray_scale = gray_scale > 80;

    namedWindow( "Display Image", CV_WINDOW_AUTOSIZE );
    imshow( "Display Image", gray_scale );

    waitKey(0);

    return 0;
}
