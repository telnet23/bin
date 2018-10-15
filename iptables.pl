use strict;
use warnings;

foreach my $filename ( @ARGV )
{
    open my $fh, '<', $filename;

    while ( my $line = <$fh> )
    {
        $line =~ s/\s+//g;

        if ( $line =~ /^\d+\.\d+\.\d+\.\d+$/ )
        {
            print "iptables -A INPUT -s $line -j DROP -m comment --comment '$filename'", "\n";
        }
        elsif ( $line =~ /^\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+$/ )
        {
            print "iptables -A INPUT -m iprange --src-range $line -j DROP -m comment --comment '$filename'", "\n";
        }
        else
        {
            print "iptables -A INPUT -s $line -j DROP -m comment --comment '$filename'", "\n";
        }
    }
    
    close $fh;
}

print 'iptables-save > /etc/iptables/rules.v4', "\n";
print 'iptables -L', "\n";
