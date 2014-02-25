/*
 * Author: Jonas
 * License: MIT
 * Date: Feb, 24th 2014
 */

#include <iostream>
#include <list>
#include <iterator>
#include <stdio.h>
#include <opencv2/opencv.hpp>

#define LOG

using namespace std;

void loadAlbum(list<cv::Mat> &album)
{
    cout << "Loading images to album" << endl;
    string images[] = {"3.png", "4.png", "5.png"};

    for(int i = 0; i < 3; i++)
    {
        //read images as grayscale cv::Mat
        album.push_back(cv::imread( images[i], 0));
    }

    for (list<cv::Mat>::iterator it = album.begin(); it != album.end(); ++it)
    {
        if(!it->data){
            fprintf(stderr, "IO Exception :P\n");    
        }
    }
}

void extractRoi(list<cv::Mat> &album)
{
    cout << "Extracting region of interest" << endl;
    //cv::Mat imageRoi = image(cv::Rect(0, 22, 501, 500));

    for (list<cv::Mat>::iterator image = album.begin(); image != album.end(); ++image)
    {
        cv::Mat roi = (*image)(cv::Rect(0, 22, 501, 500));
        *image = roi;
    }
}

void info(list<cv::Mat> &album){
    for (list<cv::Mat>::iterator it = album.begin(); it != album.end(); ++it)
    {
        cout << "Rows: " << it->rows << endl;
        cout << "Cols: " << it->cols << endl;
        cout << "Channels: " << it->channels() << endl;        
    }
}

void showUp(list<cv::Mat> &album)
{
    for (list<cv::Mat>::iterator image = album.begin(); image != album.end(); ++image)
    {
        cv::namedWindow( "Display Image", CV_WINDOW_AUTOSIZE );
        cv::imshow( "Display Image", *image );
        cv::waitKey(0);
    }
}

void grayFilter(list<cv::Mat> &album)
{
    for (list<cv::Mat>::iterator image = album.begin(); image != album.end(); ++image)
    {
        cv::threshold(*image, *image, 81, 100, 4);
    }
}

int main(int argc, char** argv)
{
    list<cv::Mat> album;

    //load/read step I
    loadAlbum(album);
    info(album);
    cout << endl;
    extractRoi(album);
    info(album);
    grayFilter(album);
    showUp(album);

     return 0;
}

