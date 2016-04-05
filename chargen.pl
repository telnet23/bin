use strict;
use warnings;

my $delay = shift;
$delay = 0.01 if ! $delay;

while (1)
{
    for ( my $i = 0; $i < 94; $i++ )
    {
        for ( my $j = 0; $j < 72; $j++ )
        {
            print chr( ( ( $i + $j ) % 94 ) + 33 );
        }

        print "\n";
        select undef, undef, undef, $delay;
    }
}
