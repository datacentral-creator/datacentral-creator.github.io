**Navigation:**  
[Research](index.md) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](history.md)

# Specifications

## Extensions

Extensions are (locally run) external programs integrated directly into the Server component (Server.exe)

### [The solid project](https://solidproject.org/)
The solid project is used to store the data. The add ons File_read and File_set are interfaces to the solid project. All data should flow throgh these interfaces allowing you to terminate any given add-ons acess to your data from within the solid project. 

## [Kubernetes](https://kubernetes.io/)
Kubernetes are integrated into the Server.exe file however currently the kubernete functionality is not used

## [Docker](https://www.docker.com/)
Docker is integrated into the Server.exe file and it is the back bone that runs add ons. 

## [Scheduling_project](https://github.com/datacentral-creator/Scheduling-project)
A side project I created as an add on however it ended up becoming an extension instead. It acts as a statistical inference engine optimised for revision.

## My tagger component
The basis of my simulatrix system which intends to act as a multimodal AI for bidirectional media interaction and potentially a new approach to computational physics in the future. It is the brain that extracts form from information.


### Package_manager

An add on that allows you to view the details of packages, remove packages and add new packages (by pulling new images)

Specification:
This add on does not have a specification as such as it is independent from all other add ons so there are no routes used by other add ons
