use strict;
use warnings;

my $COLS = 8;
my $MIN  = 32;
my $MAX  = 127;

binmode(STDOUT, ':utf8');

for ( my $ord = $MIN; $ord <= $MAX; $ord++ )
{
    printf('%-3s %s', $ord, chr($ord));

    if ( ($ord + 1) % $COLS == 0 )
    {
        print "\n";
    }
    else
    {
        print ' ' x 4;
    }
}
