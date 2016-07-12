use strict;
use warnings;

use Time::HiRes 'time';

my $start = time;

my $iterations    = 0;
my $cars_switch   = 0;
my $cars_noswitch = 0;

my @doors = qw( car goat goat );

while ( $iterations < 1_000_000 )
{
    $iterations++;

    my $choose = int rand scalar @doors;
    my $reveal = 0;

    while ( $doors[$reveal] eq 'car' || $reveal == $choose )
    {
        $reveal++;
    }

    if ( $doors[$choose] eq 'car' )
    {
        $cars_noswitch++;
    }

    my $switch = 0;

    while ( $switch == $reveal || $switch == $choose )
    {
        $switch++;
    }

    if ( $doors[$switch] eq 'car' )
    {
        $cars_switch++;
    }
}

printf "Iterations                %i\n",           $iterations;
printf "Cars (with Switching)     %i (%f)\n",      $cars_switch,   $cars_switch   / $iterations;
printf "Cars (without Switching)  %i (%f)\n",      $cars_noswitch, $cars_noswitch / $iterations;
printf "Run Time                  %.2f seconds\n", time - $start;
