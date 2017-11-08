use strict;
use warnings;

my $pi = 3.14159265358979;

my $i = 140;
my $j = 20.44;
my $delta = 90;
my $a = 175;
my $b = 225;
my $c = 20;
my $beta = 15 + 6 / 60 + 31 / 3600;
my $h = sqrt( $i ** 2 + $j ** 2 - 2 * $i * $j * cos( $delta * 2 * $pi / 360 ) );
my $gamma = 77 + 59 / 60 + 43 / 3600;
my $epsilon = ( 180 - $gamma ) / 2;
my $alpha = 33 + 1 / 60 + 54 / 3600;
my $zeta = ( 180 - $alpha ) / 2;
my $e = 2 * $c * sin( $gamma / 2 * 2 * $pi / 360 );
my $f = 2 * $a * sin( $alpha / 2 * 2 * $pi / 360 );
my $g = sqrt( $e ** 2 + $f ** 2 - 2 * $e * $f * cos( ( $epsilon + $zeta ) * 2 * $pi / 360 ) );
my $d = 2 * $b * sin( $beta / 2 * 2 * $pi / 360 );
my $A4 = $i * $j * sin( $delta * 2 * $pi / 360 ) / 2;
my $S5 = ( $d + $g + $h ) / 2;
my $A5 = sqrt( $S5 * ( $S5 - $d ) * ( $S5 - $g ) * ( $S5 - $h ) );
my $A3 = $e * $f * sin( ( $epsilon + $zeta ) * 2 * $pi / 360 ) / 2;
my $A2 = $b ** 2 * ( $beta / 360 * $pi - sin( $beta * 2 * $pi / 360 ) / 2 );
my $A6 = $c ** 2 * ( $gamma / 360 * $pi - sin( $gamma * 2 * $pi / 360 ) / 2 );
my $A1 = $a ** 2 * ( $alpha / 360 * $pi - sin( $alpha * 2 * $pi / 360 ) / 2 );
my $A = $A1 + $A3 + $A4 + $A5 + $A6 - $A2;

print "A1=$A1\n";
print "A2=$A2\n";
print "A3=$A3\n";
print "A4=$A4\n";
print "A5=$A5\n";
print "A6=$A6\n";
print "A=$A\n";
