# Overview

This document aims to clearly explain what pipelines are and why they are needed.

# What is an add on?

To understand what a pipeline is you first need to know what an add on is. At its core, datacentral should allow users to store,process and exchange data privately (An example of this could be communication, where the data is a social artefact). 

Add ons are a direct implementation of this philosophy. Add-ons are fundamentally isolated processes. This isolation is important because it means if any given add on is compromised by malware no other add on is compromised by extension. Add-ons do not interact with each other; however communication between add-ons is coordinated using a shared interface called the “server component” (simply an exe). If an add on were to become compromised it would not be able to communicate with another addon even using this shared interface, nor would it be able to spread its malware to the server component as the interaction between the server component and the add ons are non-executive \- nothing is executed as a response to the input. 

This is a direct implementation to the question “How can I minimise the risks of malware affecting vulnerable data?”.

*Side note: Why focus on local privacy before communications privacy?*  
Local privacy must be secured before communicational privacy because communicational privacy is utterly useless if each node that is communicating the data is vulnerable to attack.

# What is a pipeline?

As it has been made clear these privacy measures(data isolation) are not perfect as data still has to be transferred between processes on different machines in order for users to communicate this data. To combat this we can use encryption. A pipeline is an encryption method that directly integrates with add-ons, as well as the operations that are extensions of this.

This encryption method is token based \- digital media is converted into tokens which are indexed then each instance of this token is replaced by the index of that token. This both encrypts the data and optimises transmission of data by reducing the amount of data that needs to be transferred. The problem with this that still remains however is that these indexes need to be originally synchronised across computers. If both computers have the same index then only the sequences of token indexes need to be transmitted \- this is completely encrypted and unable to be brute force decrypted without the indexes of tokens due to inherent limitations of the ways language works. In terms of synchronising the token indexes this can be done using classical encryption methods and coordinating encryption keys externally.

Since this encryption is semantic based I built effectively a computational implementation of a set of operations to process and organise the semantics of the file. These “file semantics” are discussed in great detail in my research and philosophy essays.

A pipeline is a specific type of add-on where the isolated process uses these semantic operations as an input.

Temporarily turning a blind eye to the element of semantic response you can consider a pipeline as effectively a class of operations where encrypted data is the input and output. This enhances privacy for obvious reasons but it also nullifies the issue of hazard points such as the public nodes in the yggdrasil network because only encrypted data is exposed or processed.

It is important to note that as a type of add-on pipelines also obey other properties for instance a pipeline should be such that it can connect to the server component but still operates in offline conditions (this is another property of add ons).

Pipelines can also be split into categories such as simple pipelines which simply allow the user to modify and transmit data. My primary focus of datacentral so far has been to build a text based simple pipeline as this is the easiest type of pipeline to build providing proof of concept.

*Side note:*   
When modifying the contents of data in a pipeline it is de-encrypted. Data should only be de-encrypted whilst being modified and the de-encrypted data should exist in a minimal number of locations (in an ideal scenario de-encrypted data would only exist as characters on a screen for a text based simple pipeline however this also introduces security risks such as screen recording malware accessing de-encrypted data or nearby cameras reading it.). 

As well as simple pipelines we have complex pipelines. Complex pipelines are able to respond to data. This could be done through LLMs (local LLMs would be used for privacy) for instance the data could be a video recording from a remote camera as well as a motor and the LLM could be prompted to create an output for the motor that optimises distance from a target, for example if we wanted to remote control a drone for astronomical research.

We can also consider open and closed complex pipelines.

In an open complex pipeline the output of the pipeline is continuous. Using our previous example, in an open complex pipeline the motor would accept inputs from the complex pipeline to produce any given motion. This means that the motor needs no embedded programming aside from connection to the pipeline (a physical connection would be suggested). This significantly reduces operational costs as less work actually needs to be performed.

In a closed complex pipeline the output of the pipeline is discrete. Using our previous example the LLM would decide which preconfigured action it wants the motor to take. This can limit the scope of what the LLM can do when compared to the open pipeline however it also has it’s benefits. If you want the output of the pipeline to do something very specialised within a small margin of error these discrete outputs act as guard rails. Additionally, an LLM probably wouldn’t be used in a closed complex pipeline \- instead those semantic operations I mentioned could be chained together to create dynamic responses. An example of this is you might want the motor to reduce it’s speed when the target it’s following reduces it’s speed. Well the base set of semantic operations would identify the variable of the “speed” of the target (this is an example of a semantic thread and why the semantic threads are so important). From there we could pass the speed data into an algorithm to convert the speed into a numeric quantity then implement a feedback mechanism for the speed of the motor. 
