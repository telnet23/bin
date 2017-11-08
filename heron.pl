use strict;
use warnings;

my ($x, $y, $z) = ($ARGV[0], $ARGV[1], $ARGV[2]);
my $s = ($x + $y + $z) / 2;
my $area = sqrt($s * ($s - $x) * ($s - $y) * ($s - $z));

print "The area is $area\n";
