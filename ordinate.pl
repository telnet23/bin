#!/usr/bin/env perl

use strict;
use warnings;

sub ordinate
{
    my ( $n ) = @_;
    return $n . ordinate_suffix( $n );
}

sub ordinate_suffix
{
    my ( $n ) = @_;

    $n %= 100;
    return 'th' if $n == 11 || $n == 12 || $n == 13;

    $n %= 10;
    return 'st' if $n == 1; 
    return 'nd' if $n == 2;
    return 'rd' if $n == 3;
    return 'th';
}

my $n = shift;
print ordinate($n), "\n";
