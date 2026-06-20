**Navigation:**  
[Research](index.md) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](history.md)

# What are add ons?
Add ons are extra pieces of data that expand a programs function. One of the iterations of datacentral was entirely focused on privacy and data sovereignty and security. Because of this, I split my codebase into "add ons" and a main installer which installs the prequisite requirements onto the system and adds the add ons. This has remained as a permanent design choice for the server component. 

#Contemporary add ons list

### File_server
The file server add on facilitates communication between the server component and the mobile app. It does this by exposing a specific subsection of the filesystem of the system running the server component which the mobile app connects to (this connection is cryptographically encrypted with credentials set by the user). Likewise it also facilitates the transfer of project metadata between the mobile device and the server component. 

### Projects
The projects add on lets you interact with your projects and connect them to tasks and local files.

### Schematic_pipeline
The schematic pipeline has all the functionality of the scheduling component but it also processes custom schematics. This can be any data formatted in two rows of numbers seperated by commas. You can get information about row one, row two or data about correlation and association between the rows (with integrated hypothesis testing). 

#Legacy add ons specifications

### File_edit
An add on that allows you to edit text files. It is chunked under the hood meaning you can make infinite edits with a constant amount of lag (because each chunk has a small size and adding edits just adds more chunks)

Specification:

/CreateChunk/{file_name]
Type: GET
Description: Creates a new chunk

/Edit_uploads/{file_name}
Type: POST(Accepts a request with form data attatched with a file object included in the form data in "file")
Description: Adds the file to the local directory

/Get_file/{file_name}
Type: GET
Description: Returns a file from the local directory

/Get_files
Type: GET
Description: Returns a list of files from the local directory

/Recieve_file/{file_name}
Type: POST(with the file embedded in the post request directly)
Description: Adds the file to the local directory

### File_read

An add on that allows you to upload files to the solid database 

Specification:
/Download_files/chunks
Type: POST(with the file embedded in form data)
Description: Uploads the file to the local directory

/Get_files
Type: GET
Description: Returns a list of files in the local directory

/Reference_index/{file_name}
Type: GET
Description: Returns a list of reference indices of a file (Basically if you choose to "encrypt" a file the file is actually stored within solid in an encrypted form and a reference index is generated which is a list of all the words in the file and this is required to de-encrypt the file providing an extra layer of security however reference indices are going to have a special use in the future as well). 

/Reference_index/{file_name}/{Chunk_no}
Type: GET 
Description: Returns the file index of a given chunk

### File_set

An add on that allows you to view the files in your solid database and send them to the text editor add on

Specification:

/download/{file_name}
Type: GET
Description: Returns the corresponding file from the local directory

/sendFile/{file_name}
Type: GET
Description: Sends the file from solid to the text editor
