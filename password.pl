#!/usr/bin/env perl

use strict;
use warnings;

use Getopt::Long;

my $complexity;
my $length;
my $repeat;

my $options =
{
    'complexity=s' => \$complexity,
    'length=s'     => \$length,
    'repeat=s'     => \$repeat,
};

exit if ! GetOptions($options);

my $alphabets =
[
    [ 0..9 ],
    [ 0..9, 'a'..'f' ],
    [ 0..9, 'a'..'z' ],
    [ 0..9, 'a'..'z', 'A'..'Z' ],
    [ 0..9, 'a'..'z', 'A'..'Z', qw( _ - ) ],
    [ 0..9, 'a'..'z', 'A'..'Z',
           qw( ! " $ % & ' \( \) * + - . / @ [ \\ ] ^ _ ` { | } ~ ), '#', ',' ],
];

if ( defined $complexity && ( $complexity !~ /^[0-9]+$/ || $complexity > $#$alphabets ) )
{
    print "Invalid complexity: $complexity\n";
    exit;
}

if ( defined $length && ( $length !~ /^[0-9]+$/ || $length == 0 ) )
{
    print "Invalid length: $length\n";
    exit;
}

if ( defined $repeat && ( $repeat !~ /^[0-9]+$/ || $repeat == 0 ) )
{
    print "Invalid repeat: $repeat\n";
    exit;
}

$complexity = 3  if ! defined $complexity;
$length     = 32 if ! defined $length;
$repeat     = 1  if ! defined $repeat;

my $alphabet = $alphabets->[$complexity];
my $permutations = scalar( @$alphabet ) ** $length;
my $per = '';
$per = ' per password' if $repeat > 1;
printf "Permutations%s: %.3e\n", $per, $permutations;
printf "Entropy%s: %.0f bits\n", $per, log($permutations) / log(2);
print "\n";

foreach my $i ( 1 .. $repeat )
{
    my $password;

    for ( 1 .. $length )
    {
        $password .= $alphabet->[ int rand $#$alphabet ];
    }

    if ( $repeat != 1 )
    {
        printf '%' . length($repeat) . 's  ', $i;
    }

    print "$password\n";
}
