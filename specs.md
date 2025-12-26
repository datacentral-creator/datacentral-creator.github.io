# Specifications

## Extensions

Extensions are external programs integrated directly into the Server component (Server.exe)

### [The solid project](https://solidproject.org/)
The solid project is used to store the data. The add ons File_read and File_set are interfaces to the solid project. All data should flow throgh these interfaces allowing you to terminate any given add-ons acess to your data from within the solid project. 

## [Kubernetes](https://kubernetes.io/)
Kubernetes are integrated into the Server.exe file however currently the kubernete functionality is not used

## [Docker](https://www.docker.com/)
Docker is integrated into the Server.exe file and it is the back bone that runs add ons. 

## Add ons

Add ons (aka packages) are docker images that are run by the Server.exe component through the docker extension however in the future I will introduce the capability to run add ons on a kubernete instead. Conceptually add ons are such that they aren't neccessarily open source however the specification of a given add on should be provided such that you can create a new add on with the same specification and it will work the same within the datacentral ecosystem. 

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

### File_read

### File_set

### Package_manager


