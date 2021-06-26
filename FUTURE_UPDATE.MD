##JSON EXAMPLES :

this category will likely be subject to changes as we are still minding on what type of files we should make a special interface.

- text scan : (important to app request)
{"file_type" : "text_scan","date" : "time","text" : "file_content"}

- image : (only used in PC software, the app just send multipart request )
{"file_name" : "{file.filename}","file_type" : "{file_type}","date" : "{time}","path" : "{path}"}

- others files : (only used in PC software, the app just send multipart request)
{"file_name" : "{file.filename}","file_type" : "{file_type}","date" : "{time}","path" : "{path}"}



data support ideas :

- locations
- wifi connection qr code
- calendar event



Informations for the app :

- url to post requests : http://<ip_addr>/upload
response  of the server : {"upload_status\" : "true"} or {"upload_status" : "false"} if upload failed
- to upload files, you need to POST a multipart request of the files
- to upload text, you need to POST a simple request with the JSON content specified on upper part.
- maybe i will add a version number in the JSON integrated in the QR code, so the app will be able to notify the user when the desktop app needs an update. (need to see with my friend that is coding the app if he's okay with that )
