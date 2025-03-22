GitDotPlan
==========

## Introduction

.plan files were very popular in the 90's by developers who wanted to update the world on what they were doing,
popularized mainly by John Carmack of id software.

## Benefits of a .plan file

* Don't have to spend days formatting it to get it working with HTML and CSS

* Don't have to find or make pictures, and integrate them in with formatting

* Less of a focus on vocabulary and editing

* Quicker updates

* No video or audio required

## Important Terms

* .profile file: A file that provides information about the owner

* .project file: A file that provides information about the project(s) that the owner is working on

* .plan file: A file that provides updates about whatever the owner wants to update about

* Fingering: To "finger" a user means to download their .plan file for viewing

## Requirements

* Python (I use 3.10.10)

* Write-access to a git repo

## Implementation

The old .plan files were accessible on a specific port on a server.  However, this protocol has long been seen
as insecure, so the .plan files effectively disappeared as companies stopped having the port on their servers
open.

I decided to host everything on Github, as you get security and storage for free, and an entire data transfer
mechanism via the git protocol also for free.

## Usage

### Initialization

A git repo with the 3 files listed above (.plan, .project, .profile) must be set up, github is ideal but you can
use any repo you want (Github is what has been tested by me)

### Fingering 

```
finger.py [-h] [-f {.plan,.project,.profile}] --repo GIT_REPO [--test-only]
```

The -f option allows you to fetch individual files; if omitted, a formatted file
combining all 3 files will be returned

The GIT_REPO format can either be a full URL (https://github.com/andrewsomahony/fingers.git),
or a "short" URL (andrewsomahony/fingers.git).  For fingering, only read access to the repo
is required

### Updating

```
update.py [-h] [-f {.plan,.project,.profile}] --repo GIT_REPO [--test-only] < CONTENTS
```

The options apply the same as the finger command, but the repo must have write access by whoever
is calling the script, as well as the file to update already present.  If not supplied, the file
parameter defaults to ".plan".

The CONTENTS must be supplied via STDIN; either via a pipe, a file, etc, whatever your preference.
