"""
weathering code -- this is the code for the decay function in TAP, when post-processed

"""

"""
Code from the C++ TAP viewer NOAA.c file

 typedef struct {
        char  name[64];
        float api;
        float   constituentPercent[3];
        float   constituentHalfLife[3];
 } OilType, *OilTypeP, **OilTypeH;

OilType OilForItem(short itemNum)
{
    short index = 0;
    OilType oil;

    switch(itemNum)
    {
        default:// fall through
        case 1: oil = InitOil("Gasoline",60.0,0.5,0.12,0.5,5.3,0.0,1.0e9);break;
        case 2: oil = InitOil("Kerosene / Jet Fuels",44.0,0.35,5.3,0.50,14.4,0.15,69.2);break;
        case 3: oil = InitOil("Diesel",39.0,0.30,14.4,0.45,48.6,0.25,243.0);break;
        case 4: oil = InitOil("Fuel Oil #4",25.0,0.24,14.4,0.37,48.6,0.39,1.0e9);break;
        case 5: oil = InitOil("Medium Crude",30.0,0.22,14.4,0.26,48.6,0.52,1.0e9);break;
        case 6: oil = InitOil("Fuel Oil #6",11.84,0.20,14.4,0.15,48.6,0.65,1.0e9);break;
        case 7: oil = InitOil("Non-Weathering",10.0,1.0,1.0e9,0.0,1.0e9,0.0,1.0e9);break;
        // code goes here what is the API of non-weathering ??? 10.0 ??
    }
    return oil;
}

OilType InitOil(char* name,float api, float percent0,float halfLife0,float percent1,float halfLife1,float percent2,float halfLife2)
{
    OilType oil;
    strcpy(oil.name,name);
    oil.api = api;
    oil.constituentPercent[0] =percent0;
    oil.constituentPercent[1] =percent1;
    oil.constituentPercent[2] =percent2;
    oil.constituentHalfLife[0] =halfLife0;
    oil.constituentHalfLife[1] =halfLife1;
    oil.constituentHalfLife[2] =halfLife2;
    return oil;
}

double FractionOilLeftAtTime(OilTypeP oil,float timeInHours)
{ // returns a number from 0.0-1.0
    double percentOilLeftAtTime = 0.0;
    short i;

    if(oil)
    {
        for(i = 0;i<3;i++)
        {
            if(oil->constituentPercent[i] > 0.0)
            {
                percentOilLeftAtTime +=  (oil->constituentPercent[i])*pow(0.5,timeInHours/(oil->constituentHalfLife[i]));
            }
        }
    }

    return percentOilLeftAtTime;
}

"""

# Python versions here:




