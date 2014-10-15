prof
====

### An useful program to upload your work on PROF

[PROF] is the website where peoples studying computer science at Lille1 should upload their work.

This tool give you ability to upload your archive from the command line.

First you give your credentials

    login? calve
    pass?

In exchange, it give you the tree of all avalaible works.

    TP_ACT_Groupe1
    - 23 : TP Ordres de Grandeu (Closed)
    - 88 : TP Diviser pour Régn (Closed)
    - 103 :  TP 3 Compression Im (Open - Time remaining: 6 days, 17:43:18.160355)
    TP ASE Contextes
    - 45 : TP 2 (Closed)
    - 46 : TP 4 (Closed)
    TP ASE Disques
    - 47 : TP 1 (Closed)
    - 48 : TP 2 (Open - Time remaining: 4 days, 21:28:18.160231)
    - 49 : TP 3 (Open - Time remaining: 32 days, 21:28:18.160197)
    TP ASE MMU
    - 50 : TP 1 (Open - Time remaining: 53 days, 21:28:18.160153)
    - 51 : TP 2 (Open - Time remaining: 60 days, 21:28:18.160116)
    M1AEO
    - 95 : Bonus TD (Closed)
    - 184 : TP roulette (Open - Time remaining: 5 days, 18:28:18.160059)

It ask for an id (you guessed it, the number printed in front of the work title)

    id? 95
    filename? test.tar.gz

And it is done

    done, you should verify the upload on the website

prof is still under devel, it may crash, loose your files, eat your goat.
Always check your file is actually send on the remote server.

[PROF]: https://prof.fil.univ-lille1.fr

## Fast setup

    sudo apt-get install python3-pip

Or whatever your packet manager is and how it named ``pip`` for python3

    sudo pip3 install requests
    git clone https://github.com/calve/prof.git
    cd prof
    python3 prof.py


To get a usable global command, add ``alias prof=/path/to/prof/prof.py`` in your ``~.bashrc`` file.
Alternatively, you could add it to your ``$PATH``

## Download & Execute

To download latests source and run the software

    git clone https://github.com/calve/prof.git
    python3 prof.py


## Requirements

 * python3
 * python3-requests

You can get requests with ``sudo pip install requests``


## CHANGELOG

 - Rewrite in Python
 - Better ui, now loop thru tp and ue list
 - Fix : Date comparaison
 - Added argument --sorted to list all TPs sorted by time. Still experimental
 - QuickFix : Clear buffer containing downloaded pages before getting TP list
 - TPs contains their UE
 - TPs contains their deadline. Maybe in a future we could sort TP by deadline
 - TPs and UEs numbers are now from 0 to n, and not the actual id on the server
 - raise exception when procedures fail
 - upload a file
 - delete a remote file
 - retrieve TP list
 - connect to the prof website, get cookie, log and retrieve an UE list

## TODO

  - Improve ui and cli
  - Validate archive before upload

## CONTACT

    calvinh34 at gmail

Bugs, patches and suggestions are welcome !

## Last word

If nothing work, or if you just want an easy sh script, you may find one in legacy/prof.sh that nearly do the same thing.
