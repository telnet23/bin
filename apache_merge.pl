use strict;
use warnings;

use Time::Local 'timelocal';

my @months = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my %months = map { $months[$_] => $_ } 0 .. $#months;

my @lines;
my %lines;

foreach my $arg ( @ARGV )
{
    open my $fh, '<', $arg;

    while ( my $line = <$fh> )
    {
        next if $lines{$line};
        next if $line !~ m, \[([0-9]{2})/([A-Z][a-z]{2})/([0-9]{4}):([0-9]{2}):([0-9]{2}):([0-9]{2}) (-[0-9]{4})\] ,;

        my $utc = timelocal( $6, $5, $4, $1, $months{$2}, $3 ) - ( $7 / 100 * 3600 );
        push @lines, [ $utc, $arg, $line ];
        $lines{$line} = 1;
    }

    close $fh;
}

foreach my $line ( sort { $a->[0] <=> $b->[0] || $a->[1] cmp $b->[1] } @lines )
{
    print $line->[2];
}
