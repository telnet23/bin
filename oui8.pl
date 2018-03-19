use strict;
use warnings;
no warnings 'uninitialized';

use FindBin;
chdir $FindBin::Bin;

open my $fh, '<', 'oui.txt';
$/ = undef;
my @ouis = split "\r\n\r\n", <$fh>;
shift @ouis;
close $fh;

my %tr;

foreach my $record ( @ouis )
{
    my @record = split( "\r\n", $record );

    foreach my $line ( @record )
    {
        if ( $line =~ /^([0-9A-Z-]{8})\s+\(hex\)\s+(.+)$/ )
        {
            my $oui = $1;
            my $vendor = $2;

            my $tr;
            foreach my $word ( split( /\s+/, $vendor ) )
            {
                $tr .= ucfirst lc $word;
            }
    
            $tr = substr $tr, 0, 8;
            $oui =~ s/-//g;
            push @{ $tr{$tr} }, $oui;
        }
    }
}

foreach my $tr ( sort { scalar( @{ $tr{$b} } ) <=> scalar( @{ $tr{$a} } ) } keys %tr )
{
    printf( "%-8s    %4s    %s\n", $tr, scalar( @{ $tr{$tr} } ), $tr{$tr}->[-1] );
}
