use strict;
use warnings;

use Time::HiRes qw(usleep);

$| = 1;

my $delay = shift || 1e5;

while ( my $char = getc )
{
    print $char;
    usleep $delay;
}
