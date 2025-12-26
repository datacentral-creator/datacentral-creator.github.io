[Research](https://datacentral-creator.github.io/) | [Datacentral](https://github.com/datacentral-creator/Datacentral) | [History](https://github.com/datacentral-creator/Datacentral/blob/main/Theory/History.md)

# A Brief History of Datacentral

I began working on Datacentral approximately five years ago. Before this project existed, I relied heavily on Google Docs for note‑taking. I accumulated a vast number of notes over the years, but they were scattered across countless documents with no unifying structure. Two major frustrations emerged from this system.

First, Google Docs and Google Slides imposed limitations on how I could record information. In particular, they made it difficult to write complex formulae, which I frequently needed to include in my notes.  
Second, although I had amassed a large collection of data, retrieving knowledge from it proved nearly impossible. The information I needed was distributed across too many documents to search manually, and the built‑in search tools could only surface a small fraction of what I had recorded.

These frustrations eventually pushed me to create my own solution. The earliest version of this idea was something I called *the everything project* — a kind of “second brain,” but one intended to encompass an entire life rather than just cognitive tasks.

---

## Early Experiments: Kivy, JSON, and Electron

The first implementation was built using Kivy. To address the problem of retrieval, I designed a “tagger” system that associated semantic tags with pieces of data. These tags were meant to become the building blocks of the structure that the data would eventually take.

However, I soon realised that Kivy could not provide the level of customisability I needed. HTML offered far more flexibility, so I built a converter that transformed Kivy objects into JSON, which I then rendered as HTML inside Electron. Although this approach worked, the architecture became increasingly convoluted. Communication between Kivy, the converter, and Electron relied on an event‑bus system that grew fragile over time. After one particularly disruptive error, I recognised that the codebase had become too tangled to maintain, and starting over was the only viable option.

---

## Rebuilding as a Web Application

I rebuilt the system from scratch as a React web application, drawing on my prior experience with the framework. This time, I separated the program’s functions into independent web pages. One of these pages — a text editor — became the foundation for a new version of the tagger.

The project underwent another major reconstruction when I migrated from React to Next.js. By this stage, privacy had become a central principle of Datacentral. The project had evolved into an expression of a broader philosophy: a vision of a new kind of internet built around individual autonomy and data sovereignty, reminiscent of the ideals associated with “Web3.” As part of this shift, each web page became an independent website, which I referred to as “add‑ons.”

---

## Self‑Hosting, Networking, and Infrastructure

At this point, I decided that users should be able to self‑host Datacentral and connect through a decentralised network. After exploring various options, I settled on Yggdrasil. Over the course of a year, I developed a system that packaged each add‑on into a docker image and created a setup program capable of installing the necessary tools on a user’s machine and running the image. The system also included functionality for deploying the images across a Kubernetes cluster — a feature that remains dormant for now but reflects the original multi‑machine vision.

I later added a self‑hosted database, drawing on the programming principles I had gradually learned through experience and through resources such as dev.to. This required rewriting most of the add‑ons yet again, a process that took another year.

---

## Catastrophic Data Loss and a New Direction

Just as the system finally became functional, my computer suffered a severe BIOS error. This occurred shortly after my Google accounts had been compromised, leaving my local machine as the sole repository of all my data. The failure resulted in the loss of everything — not only Datacentral, but also the years of notes that had originally motivated its creation. The only surviving file was the one responsible for generating the Kubernetes architecture.

This event fundamentally changed the direction of Datacentral. Until then, the system had been tightly coupled to the Google Drive API, which complicated the codebase and constrained the design. The loss of my Google data removed this dependency entirely. It also forced me to confront the messy legacy code that had accumulated over the years. Rewriting the add‑ons from scratch made them dramatically faster and cleaner.

During this period, I also discovered the Solid project. Its emphasis on personal data pods aligned closely with the philosophical foundations of Datacentral, and integrating Solid became a natural extension of the system’s evolution.

---

## Summary

Datacentral has undergone multiple transformations — from a Kivy prototype, to an Electron‑based hybrid, to a React application, to a Next.js ecosystem of modular add‑ons. Along the way, it has absorbed lessons about privacy, data sovereignty, decentralised networking, and the importance of clean architecture. The project continues to evolve, shaped by both technical challenges and philosophical commitments.
