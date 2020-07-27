use strict;
use warnings;

sub strings
{
    my ( $rem, $acc ) = @_;

    $acc = '' if ! defined $acc;
    print $acc, "\n";
    return if $rem < 1;

    foreach my $sym ( '-', '0'..'9', 'a'..'z' )
    {
        strings( $rem - 1, $acc . $sym );
    }
}

my $max = shift;
strings( $max );
