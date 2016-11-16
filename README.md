TAP Viewer
==========

This project will hold the design discussion and ultimately code, for the new Web-based TAP vieweer.

Project TEAM:
-------------

Alex Miranda: Web UI developer

Dylan Righi: Back end computation developer and subject matter expert

Chris Barker: Subject mater expert, software architecture support -- maybe some code :-)

Glen Watabayashi: Making sure we get it done on schedule :-)

Running the API Server
======================

* Make sure to activate a relevant virtualenv (if necessary)
* To install the API package:

```
cd TAP_Viewer_API
python setup.py develop
```

* After successful installation run this command:

```
pserve --reload development.ini
```

* Now your server should be running on the port you specified in the development.ini file. The port provided will be displayed after you run the above command.





