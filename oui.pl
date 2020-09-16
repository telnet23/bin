#!/usr/bin/env perl

use strict;
use warnings;
no warnings 'uninitialized';

use FindBin;
chdir $FindBin::Bin;

my $RESET  = "\e[0m";
my $BOLD   = "\e[1m";
my $RED    = "\e[31m";
my $GREEN  = "\e[32m";
my $YELLOW = "\e[33m";
my $BLUE   = "\e[34m";
my $PURPLE = "\e[35m";
my $CYAN   = "\e[36m";
my $WHITE  = "\e[37m";

for ( my $i = 0; $i < scalar @ARGV; $i++ )
{
    if ( $ARGV[$i] =~ /^([0-9A-F]{2})[-: .]?([0-9A-F]{2})[-: .]?([0-9A-F]{2})(?:[-: .]?[0-9A-F]{2}[-: .]?[0-9A-F]{2}[-: .]?[0-9A-F]{2})?$/i )
    {
        $ARGV[$i] = "^$1-$2-$3";
    }
}

my $re = join '|', @ARGV;
my $n = 0;

open my $fh, '<', 'oui.txt';
$/ = undef;
my @ouis = split "\r\n\r\n", <$fh>;
shift @ouis;
close $fh;

foreach my $record ( @ouis )
{
    if ( ! defined $re || $record =~ /$re/i )
    {
        my @record = split( "\r\n", $record );

        foreach my $line ( @record )
        {
            if ( $line =~ /^([0-9A-Z-]{8})\s+\(hex\)\s+(.+)$/ )
            {
                my $oui = $1;
                my $vendor = $2;
                $oui =~ s/-/:/g;

                print $BOLD, $GREEN, $oui, '  ', $CYAN, $vendor, $RESET, "\n";
            }
            elsif ( $line =~ /^\t{4}(.+)$/ )
            {
                print ' ' x 10, $BLUE, $1, $RESET, "\n";
            }
        }

        print "\n";
        $n++;
    }
}

print $WHITE, "Found $n records.", $RESET, "\n";
