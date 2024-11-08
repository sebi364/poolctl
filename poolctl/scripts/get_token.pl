#!/usr/bin/perl 
# Perl script to get a csrftoken
# inspired by https://git.proxmox.com/?p=pve-apiclient.git;a=blob;f=src/examples/example1.pl

use strict; 
use warnings; 

use PVE::APIClient::LWP;
use PVE::AccessControl;
use PVE::INotify;
use JSON;

my $cookie = PVE::AccessControl::assemble_ticket('root@pam');
my $csrftoken = PVE::AccessControl::assemble_csrf_prevention_token('root@pam');

# Print everything, so we can perse & use it with python
print("$cookie;$csrftoken"); 
