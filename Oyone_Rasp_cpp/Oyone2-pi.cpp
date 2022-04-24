#include <opencv2/opencv.hpp>
#include <raspicam_cv.h>
#include <iostream>
#include <chrono>
#include <ctime>
#include <wiringPi.h>
#include <wiringSerial.h> // To get the information from sensor(Arduino)
#include <termios.h>        //for make tty Structure to set the options

using namespace std;
using namespace cv;
using namespace raspicam;

// Image Processing variables
Mat image, frame, Matrix, framePers, frameGray, frameThresh, frameEdge, frameFinal, frameFinalDuplicate, frameFinalDuplicate1;
Mat ROILane, ROILaneEnd, frameHSV, mask;
int LeftLanePos, RightLanePos, frameCenter, laneCenter, Result, laneEnd, Direction;

RaspiCam_Cv Camera;

stringstream ss;

vector<int> histogramLane;
vector<int> histogramLaneEnd;
// create a vector to store points of line
vector<Vec4i> lines;

Point2f Source[] = {Point2f(100,30),Point2f(300,30),Point2f(0,110), Point2f(400,110)};
Point2f Destination[] = {Point2f(140,0),Point2f(260,0),Point2f(140,120), Point2f(260,120)};

//Machine Learning variables
CascadeClassifier Stop_Cascade, Object_Cascade;
Mat frame_Stop, ROI_Stop, gray_Stop, frame_Object, ROI_Object, gray_Object;
vector<Rect> Stop, Object;
int dist_Stop, dist_Object;

unsigned char txdData;  //Received Data
struct termios options;     // the structure of communication's options

 void Setup ( int argc,char **argv, RaspiCam_Cv &Camera )
 {
    Camera.set ( CAP_PROP_FRAME_WIDTH,  ( "-w",argc,argv,400 ) );
    Camera.set ( CAP_PROP_FRAME_HEIGHT,  ( "-h",argc,argv,240 ) );
    Camera.set ( CAP_PROP_BRIGHTNESS, ( "-br",argc,argv,60) );
    Camera.set ( CAP_PROP_CONTRAST ,( "-co",argc,argv,50 ) );
    Camera.set ( CAP_PROP_SATURATION,  ( "-sa",argc,argv,50 ) );
    Camera.set ( CAP_PROP_GAIN,  ( "-g",argc,argv ,50 ) );
    Camera.set ( CAP_PROP_FPS,  ( "-fps",argc,argv,0));
 }

void Capture()
{
    Camera.grab();
    Camera.retrieve(image);
    cvtColor(image, image, COLOR_BGR2RGB);

}

void HoughTrans()
{
	frame = image(Rect(0,120,400,120));
	cvtColor(frame, frameGray, COLOR_RGB2GRAY);

	GaussianBlur( frameGray, frameGray, Size(1, 1), 2, 2 );

	Canny(frameGray,frameEdge,600,240);

	// apply hough line transform
	HoughLinesP(frameEdge, lines, 2, CV_PI/180, 80, 30,250);

	// draw lines on the detected points
	for( size_t i = 0; i < lines.size(); i++ )
	{
	    Vec4i l = lines[i];
	    line( frame, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 5, LINE_AA);
	}
}


void Perspective()
{
    // draw lines ( -> trapezoid )
	line(frame,Source[0], Source[1], Scalar(0,255,0), 2);
	line(frame,Source[1], Source[3], Scalar(0,255,0), 2);
	line(frame,Source[3], Source[2], Scalar(0,255,0), 2);
	line(frame,Source[2], Source[0], Scalar(0,255,0), 2);

	Matrix = getPerspectiveTransform(Source, Destination);
	warpPerspective(frame, framePers, Matrix, Size(400,120));
}


void Threshold()
{
	//detecting red
	inRange(framePers, Scalar(0, 0, 255), Scalar(100, 100, 255), mask);
	cvtColor(mask, frameFinal, COLOR_GRAY2RGB);

	cvtColor(frameFinal, frameFinalDuplicate, COLOR_RGB2BGR);   //used in Histogram function only
	cvtColor(frameFinal, frameFinalDuplicate1, COLOR_RGB2BGR);   //used in Histogram function only
}

void Histogram()
{
    histogramLane.resize(400);
    histogramLane.clear();

    for(int i=0; i<400; i++)       //frame.size().width = 400
    {
	ROILane = frameFinalDuplicate(Rect(i,80,1,40));
	divide(255, ROILane, ROILane);
	histogramLane.push_back((int)(sum(ROILane)[0]));
    }
}

void LaneFinder()
{
    vector<int>:: iterator LeftPtr;
    LeftPtr = max_element(histogramLane.begin(), histogramLane.begin() + 150);
    LeftLanePos = distance(histogramLane.begin(), LeftPtr);

    vector<int>:: iterator RightPtr;
    RightPtr = max_element(histogramLane.begin() +250, histogramLane.end());
    RightLanePos = distance(histogramLane.begin(), RightPtr);

    line(frameFinal, Point2f(LeftLanePos, 0), Point2f(LeftLanePos, 240), Scalar(0, 255,0), 2);
    line(frameFinal, Point2f(RightLanePos, 0), Point2f(RightLanePos, 240), Scalar(0,255,0), 2);
}

void LaneCenter()
{
    laneCenter = (RightLanePos-LeftLanePos)/2 +LeftLanePos;
    frameCenter = 198;

    line(frameFinal, Point2f(laneCenter,0), Point2f(laneCenter,240), Scalar(0,0,255), 3);
    line(frameFinal, Point2f(frameCenter,0), Point2f(frameCenter,240), Scalar(255,0,0), 3);

    Result = laneCenter-frameCenter;
}

void Serial(int order, int fd)  //send or receive data to Other devices
{
    serialPutchar(fd, order); //send the order for Arduino(Serial Port)
    Direction = serialGetchar(fd); //receive the data from Arduino(Serial Port)

    if (Direction == -1) {//error
        cout << "Direction : no data" << endl;
    }
    else {//display the Direction(on Console)
        if (Direction >= 5 && Direction <= 13) cout << Direction << "0:E" << endl;  //East
        else if (Direction >= 14 && Direction <= 22) cout << Direction << "0:S" << endl;    //Sauth
        else if (Direction >= 23 && Direction <= 31) cout << Direction << "0:W" << endl;    //West
        else  cout << Direction << "0:N" << endl;    //North
    }
}


int main(int argc,char **argv)
{
    Setup(argc, argv, Camera);
    cout<<"Connecting to camera"<<endl;
    if (!Camera.open())
    {
    	cout<< "Failed to Connect to camera" << endl;
    }

	cout<<"Camera Id = "<<Camera.getId()<<endl;

    //SerialPort(for receiving info from Arduino) Open
    int fd = serialOpen("/dev/ttyS0", 9600);
    if (fd < 0)
    {
        cout << "Failed to Connect to Arduino" << endl;
    }

    cout<<"Connecting to QMC5887L"<<endl;

    //Setup of SerialPorts
    tcgetattr(fd, &options);        //Get the Options(Sending & Receiving)
    options.c_cflag |= CS8;         //Data:8bit
    options.c_cflag &= ~PARENB;     //NO Parity
    options.c_cflag |= CSTOPB;      //StopBit:2bit
    options.c_iflag &= ~IXON;       //NO XON/XOFF Flow Control(output)
    options.c_iflag &= ~IXOFF;      //NO XON/XOFF Flow Control(input)
    tcsetattr(fd, TCSANOW, &options); // Finish the chenging Options

    serialFlush(fd);                //Clear the input(receiving) buffer

    while(1)
    {
        auto start = std::chrono::system_clock::now();

        Capture(); // take a picture
        HoughTrans(); // Hough Transform
        Perspective(); // reshape the picture(?)
        Threshold(); // check with threshold
        Histogram(); // make histogram
        LaneFinder(); // find lane(which the boat should go along)
        LaneCenter(); // put the boat on lane

        //turn or go straight
        if (Result == 0) Serial(1, fd);
        else if (Result > 0) Serial(2, fd);
        else if (Result < 0) Serial(3, fd);

        namedWindow("Original", WINDOW_KEEPRATIO);
        moveWindow("Original", 0, 100);
        resizeWindow("Original", 640, 480);
        imshow("Original", image);

        namedWindow("Frame Edge", WINDOW_KEEPRATIO);
        moveWindow("Frame Edge", 640, 100);
        resizeWindow("Frame Edge", 640, 480);
        imshow("Frame Edge", frameEdge);

        namedWindow("Perspective", WINDOW_KEEPRATIO);
        moveWindow("Perspective", 1280, 100);
        resizeWindow("Perspective", 640, 480);
        imshow("Perspective", framePers);

        namedWindow("Final", WINDOW_KEEPRATIO);
        moveWindow("Final", 0, 580);
        resizeWindow("Final", 640, 480);
        imshow("Final", frameFinal);

        namedWindow("Grayscale", WINDOW_KEEPRATIO);
        moveWindow("Grayscale", 640,580);
        resizeWindow("Grayscale", 640, 480);
        imshow("Grayscale", frameGray);

        waitKey(1);
        auto end = std::chrono::system_clock::now();
        std::chrono::duration<double> elapsed_seconds = end-start;

        float t = elapsed_seconds.count();
        int FPS = 1/t;
    }

    serialClose(fd);    //end the Serial Communication
    return 0;
}
