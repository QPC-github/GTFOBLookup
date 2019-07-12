#!/usr/bin/python3


import argparse
from git import Repo
from md2py import md2py
import os
import shutil
import sys


repoDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  "GTFOBins.github.io")

types = {"shell": "shell",
         "cmd": "command",
         "rev": "reverse-shell",
         "nrev": "non-interactive-reverse-shell",
         "bind": "bind-shell",
         "nbind": "non-interactive-bind-shell",
         "upload": "file-upload",
         "download": "file-download",
         "write": "file-write",
         "read": "file-read",
         "load": "library-load",
         "suid": "suid",
         "sudo": "sudo",
         "cap": "capabilities",
         "lsuid": "limited-suid"
        }


def parseArgs():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='GTFOBins Lookup')
    subparsers = parser.add_subparsers()
    #Update
    parserUpdate = subparsers.add_parser('update', help="update local copy " + 
                                         "of GTFOBins")
    parserUpdate.set_defaults(func=update)
    #Purge
    parserPurge = subparsers.add_parser('purge', help="remove local copy of " + 
                                        "GTFOBins")
    parserPurge.set_defaults(func=purge)
    #Shell
    parserShell = subparsers.add_parser('shell', help="search for " + 
                                        "applications that can be used to " + 
                                        "spawn an interactive shell")
    parserShell.set_defaults(func=search, typ=types['shell'])
    parserShell.add_argument('binary', help='the binary to search for')
    #Command
    parserCmd = subparsers.add_parser('cmd', help="search for applications " + 
                                      "that can be used to run " + 
                                      "non-interactive system commands")
    parserCmd.set_defaults(func=search, typ=types['cmd'])
    parserCmd.add_argument('binary', help='the binary to search for')
    #Reverse shell
    parserRev = subparsers.add_parser('rev', help="search for applications " + 
                                      "that can be used to spawn a reverse " + 
                                      "shell")
    parserRev.set_defaults(func=search, typ=types['rev'])
    parserRev.add_argument('binary', help='the binary to search for')
    #Non-interactive reverse shell
    parserNrev = subparsers.add_parser('nrev', help="search for applications " + 
                                       "that can be used to spawn a " + 
                                       "non-interactive reverse shell")
    parserNrev.set_defaults(func=search, typ=types['nrev'])
    parserNrev.add_argument('binary', help='the binary to search for')
    #Bind shell
    parserBind = subparsers.add_parser('bind', help="search for applications " + 
                                       "that can be used to spawn a bind shell")
    parserBind.set_defaults(func=search, typ=types['bind'])
    parserBind.add_argument('binary', help='the binary to search for')
    #Non-interactive bind shell
    parserNbind = subparsers.add_parser('nbind', help="search for " + 
                                        "applications that can be used to " + 
                                        "spawn a non-interactive bind shell")
    parserNbind.set_defaults(func=search, typ=types['nbind'])
    parserNbind.add_argument('binary', help='the binary to search for')
    #File upload
    parserUpload = subparsers.add_parser('upload', help="search for " + 
                                         "applications that can be used to " + 
                                         "upload files")
    parserUpload.set_defaults(func=search, typ=types['upload'])
    parserUpload.add_argument('binary', help='the binary to search for')
    #File download
    parserDownload = subparsers.add_parser('download', help="search for " + 
                                           "applications that can be used to " +
                                           "download files")
    parserDownload.set_defaults(func=search, typ=types['download'])
    parserDownload.add_argument('binary', help='the binary to search for')
    #File write
    parserWrite = subparsers.add_parser('write', help="search for " + 
                                        "applications that can be used to " + 
                                        "write to files")
    parserWrite.set_defaults(func=search, typ=types['write'])
    parserWrite.add_argument('binary', help='the binary to search for')
    #File read
    parserRead = subparsers.add_parser('read', help="search for applications " +
                                       "that can be used to read files")
    parserRead.set_defaults(func=search, typ=types['read'])
    parserRead.add_argument('binary', help='the binary to search for')
    #Library load
    parserLoad = subparsers.add_parser('load', help="search for applications " +
                                       "that load shared libraries")
    parserLoad.set_defaults(func=search, typ=types['load'])
    parserLoad.add_argument('binary', help='the binary to search for')
    #SUID
    parserSuid = subparsers.add_parser('suid', help="search for applications " +
                                       "that, with the SUID bit set, can be " + 
                                       "used to escalate privileges")
    parserSuid.set_defaults(func=search, typ=types['suid'])
    parserSuid.add_argument('binary', help='the binary to search for')
    #Sudo
    parserSudo = subparsers.add_parser('sudo', help="search for applications " + 
                                       "that, when run with sudo, can be used" + 
                                       " to escalate privileges")
    parserSudo.set_defaults(func=search, typ=types['sudo'])
    parserSudo.add_argument('binary', help='the binary to search for')
    #Capabilities
    parserCap = subparsers.add_parser('cap', help="search for applications " + 
                                      "that have the 'CAP_SETUID' capability " +
                                      "set")
    parserCap.set_defaults(func=search, typ=types['cap'])
    parserCap.add_argument('binary', help='the binary to search for')
    #Limited SUID
    parserLsuid = subparsers.add_parser('lsuid', help="search for " + 
                                        "applications that, with the SUID " + 
                                        "bit set, can be used to escalate " + 
                                        "privileges on systems that allow " + 
                                        "the default 'sh' shell to run with " + 
                                        "sudo privileges")
    parserLsuid.set_defaults(func=search, typ=types['lsuid'])
    parserLsuid.add_argument('binary', help='the binary to search for')
    #All
    parserAll = subparsers.add_parser('all', help="search for applications " +
                                      "in all categories")
    parserAll.set_defaults(func=search, typ="all")
    parserAll.add_argument('binary', help='the binary to search for')
    #No args
    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(0)
    else:
        return parser.parse_args()

def update(args):
    """Updates local copy of GTFOBins"""
    repoUrl = "https://github.com/GTFOBins/GTFOBins.github.io.git"
    print("Checking {0} for updates...".format(repoUrl))
    if not os.path.exists(repoDir):
        print("Local copy of GTFOBins not found, downloading...")
        Repo.clone_from(repoUrl, repoDir)
    else:
        repo = Repo(repoDir)
        current = repo.head.commit
        repo.remotes.origin.pull()
        if current == repo.head.commit:
            print("Local copy of GTFOBins is up to date")
        else:
            print("Local copy of GTFOBins updated")
            
def purge(args):
    """Removes local copy of GTFOBins"""
    if os.path.exists(repoDir):
        shutil.rmtree(repoDir)
    else:
        print("Local copy of GTFOBins not found")
    
def extract(typ, md):
    """Extracts details of a specified function of a specified binary from local
    copy of GTFOBins
    """
    #TODO

def search(args):
    """Searches local copy of GTFOBins for a specified binary in a specified 
    category
    """
    if not os.path.exists(repoDir):
        sys.exit("Local copy of GTFOBins not found, please update")
    mdPath = os.path.join(repoDir, "_gtfobins", "{0}.md".format(args.binary))
    if os.path.isfile(mdPath):
        with open(mdPath, 'r') as f:
            md = md2py(f.read())
        if args.typ == "All":
            for typ in types.values():
                extract(typ, md)
        else:
            extract(args.typ, md)
    else:
        sys.exit("{0} was not found in the local copy of GTFOBins".format(
                 args.binary))
        
        
if __name__ == "__main__":
    args = parseArgs()
    args.func(args)
