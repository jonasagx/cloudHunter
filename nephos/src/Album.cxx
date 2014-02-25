#include <list>

class Album {
    /*
     * Composite class for image data
     */
    
    public:
    static const char* sccsid = "@(#) Nephos - jonas.agx@gmail.com";
    //Empty vector, define its size on the fly
    list<Photo> photos;  
}
