#!/usr/bin/env perl

use strict;
use warnings;

my $n = shift || 80;

while ( my $s = <> )
{
    chomp $s;

    while ( length $s > $n )
    {
        my $k = $n;

        while ( $k >= 0 && substr( $s, $k, 1 ) ne ' ' )
        {
            $k--;
        }

        if ( $k >= 0 )
        {
            print substr( $s, 0, $k ), "\n";
            $s = substr( $s, $k+1 );
        }
        else
        {
            print substr( $s, 0, $n ), "\n";
            $s = substr( $s, $n );
        }
    }

    print $s, "\n";
}
