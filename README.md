prof : Upload your work from the command line !
===============================================

[PROF] is the website where peoples studying computer science at Lille1 should upload their work.

This tool give you ability to upload your archive from the command line.

## Installation

## On your university account

You can install prof to your ``$HOME`` directory

    export HTTP_PROXY=cache-etu.univ-lille1.fr:3128
    pip-3.2 install --user prof
    ~/.local/bin/prof

I suggest you to create the following alias in your ``.bashrc``

    alias prof=HTTP_PROXY=cache-etu.univ-lille1.fr:3128 $HOME/.local/bin/prof

### On your computer (if your root)

Download from Pypi and run the program

    sudo pip3 install prof
    prof

## Configuration

You *must* specify to which server ``prof`` need to connect in ``$HOME/.profrc``, as the following :

    [DEFAULT]
    baseurl = https://your-prof-instance
    login = yourlogin

Note that ``login`` is not mandatory, but you should set it for convenience.

## Usage

On the command line, run

    prof

If needed, a Firefox windows will pop so you can fill your credentials, and check the captcha.

In exchange, it give you the tree of all avalaible works.

    TP_ACT_Groupe1
    - 23  : TP Ordres de Grandeu          Closed    (calve-act-1.tar.gz)
    - 88  : TP Diviser pour Régn          Closed    (calve-act2.tar.gz)
    - 103 :  TP 3 Compression Im          Open - Time remaining: 6 days, 17:09:56.090487
    TP ASE Contextes
    - 45  : TP 2                          Closed    (calve-ase-2.tar.gz)
    - 46  : TP 4                          Closed    (calve-ase-2.tar.gz)
    TP ASE Disques
    - 47  : TP 1                          Closed    (calve-ase-3.tar.gz)
    - 48  : TP 2                          Open - Time remaining: 4 days, 20:54:56.090348
    - 49  : TP 3                          Open - Time remaining: 32 days, 20:54:56.090310
    TP ASE MMU
    - 50  : TP 1                          Open - Time remaining: 53 days, 20:54:56.090262
    - 51  : TP 2                          Open - Time remaining: 60 days, 20:54:56.090225
    M1AEO
    - 95  : Bonus TD                      Closed
    - 184 : TP roulette                   Open - Time remaining: 5 days, 17:54:56.090157


It ask for an id (you guessed it, the number printed in front of the work title)

    id? 95
    filename? test.tar.gz

If the file is a ``tar.gz``, it will untar it in a temporary directory, and try to compile the project using ``make``. You can override this comportement with ``--compil-command "cmake"`` or ``--no-compile``

    Running make in /tmp/tmp3n3knca6prof for file test.tar.gz
    mkdir -p bin
    gcc -Wall -ansi -pedantic -m32 -g   -c -o src/mkhd.o src/mkhd.c
    gcc -Wall -ansi -pedantic -m32 -g -o ./lib/mkhd.o -c src/mkhd.c -I./include
    Successfully compiled

And it is done

    done, you should verify the upload on the website

prof is still under devel, it may crash, loose your files, eat your goat.
Always check your file is actually send on the remote server.

[PROF]: https://prof.fil.univ-lille1.fr

## Set up a post commit hook for git

You can easily setup a postcommit hook for git, so it compile and upload your work on each commit.
In your project, create ``.git/post-commit``

    git archive --output archive.tar.gz master
    prof --filename archive.tar.gz --login yourlogin -i workid --compil-command "make"

and ``chmod +x .git/post-commit``

## CHANGELOG

 - Persisting sessions
 - True Pypi package
 - Check proper compilation before pushing
 - ``--sorted`` option came back
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

## Development

    git clone https://github.com/calve/prof
    cd prof
    python3 run.py

## CONTACT

    calvinh34 at gmail

Bugs, patches and suggestions are welcome !

## Last word

If nothing work, or if you just want an easy sh script, you may find one in legacy/prof.sh that nearly do the same thing.
