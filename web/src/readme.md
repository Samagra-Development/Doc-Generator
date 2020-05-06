---
id: PDFModuleArchitecture
title: Architecture
sidebar_label: Architecture
---

## 1. Overview

The following diagram illustrates the overall architecture of PDF Builder solution that allows various applications to interact with the PDF Builder solution to send requests and retrieve outputs.

![enter image description here](https://i.ibb.co/NSk5p2H/Architecture-Diagram-PDF-Builder.png)

## 2. What are these things?

A brief description of the function of each element of the architecture is provided below.

- **External Application**: This is the exit part of the application. This could be any mobile application, server or publishing platform that searches pdf status and retrieves them async.

- **Auth Server**: It issues tokens to users verifies whether request is made to the srever is a verified request or not.

- **PDF Server**: This is a simple server that authorises the request from any external application and returns the valid PDFs for that API request. This is essesntiallyt the interface to the outside world. It opens up APIs to the outputs of the PDF builder.

- **Queue Manager**: It does all the heavy lifting by actually running all the code to generate the PDF. Without this everything else is just a code layer.

- **Database**: It saves requested data and and progress of pdf generation process and if pdf is generated then it’s path is save.

- **Plugin**: This is more an application specific code. It has information on how to get the data from an external resourse, how to modifiy a particular resource and how to manage the outputs.

- **PDF Base**: The glue that holds them all. Manages the queue system, has interfaces to the plugin system, checks for authenticity of a plugin.

- **Logging Module**: This module is responsible for getting the logs from all the other modules and pass this data to central logging system.

- **Central Logging System**: All logs are then subsequently sent to a central logging system where they are archived, processed and monitored.

## 3. FAQs

To be added based on incoming feedback

## 4. Coming Soon

Please review the following section to get information about planned updates to this module.
