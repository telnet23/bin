#!/usr/bin/env perl

use strict;
use warnings;
no warnings 'uninitialized';

use MaxMind::DB::Reader;

use FindBin;
chdir $FindBin::Bin;

my @COLUMNS =
qw(
    date
    time
    remote_host
    connection_type
    organization
    city_name
    subdivision_name
    country_name
    method
    path
    status
    bytes_sent
    referer
    user_agent
);

my @LOCAL =
qw(
    10.0.0.\d+
    172.16.1.\d+
    192.168.1.\d+
);

my $local_re = '^(' . join( '|', @LOCAL ) . ')$';
$local_re =~ s/\./\\./g;
$local_re = qr/$local_re/;

my %geoip;
load_geoip( '.' );

sub load_geoip
{
    my ( $dirname ) = @_;

    foreach my $filename ( do { opendir( my $dh, $dirname ); readdir $dh; } )
    {
        my $path = "$dirname/$filename";

        if ( -d $path && $filename =~ /^Geo(?:IP|Lite)2-(?:.+)_(?:.+)$/ )
        {
            load_geoip( $path );
        }
        elsif ( -f $path && $filename =~ /^Geo(?:IP|Lite)2-(.+)\.mmdb$/ )
        {
            my $type = $1;
            $geoip{$type} = MaxMind::DB::Reader->new( file => $path );
        }
    }
}

my $in_name = $ARGV[0];
my $out_name = $ARGV[1];
my $out2_name = $out_name;
$out2_name =~ s/(\.[^\.]+)$/_recent$1/;
my $dat_name = 'apache_csv.dat';

open( my $in, '<', $in_name ) or die 'cannot open in';
open( my $out, '>>', $out_name ) or die 'cannot open out';

my $out2;
if ( -f $out2_name )
{
    open( $out2, '>>', $out2_name );
}

if ( open( my $dat, '<', $dat_name ) )
{
    my $pos = <$dat>;
	seek $in, $pos, 0;
    close $dat;
}

while ( my $line = <$in> )
{
    chomp $line;

    if ( $line =~ m,^([^ ]+):(\d+) (\d+\.\d+\.\d+\.\d+) ([^ ]+) ([^ ]+) \[(\d+/.+/\d+):(\d+:\d+:\d+) ([^ ]+)\] "([^ ]+) (.+) (HTTP/[^ ]+)" (\d+) (\d+) "(.*)" "(.*)"$, )
    {
        my %row;

        $row{server_name} = $1;
        $row{server_port} = $2;
        $row{remote_host} = $3;
        $row{remote_log}  = $4;
        $row{remote_user} = $5;
        $row{date}        = $6;
        $row{time}        = $7;
        $row{time_zone}   = $8;
        $row{method}      = $9;
        $row{path}        = $10;
        $row{protocol}    = $11;
        $row{status}      = $12;
        $row{bytes_sent}  = $13;
        $row{referer}     = $14;
        $row{user_agent}  = $15;

        if ( $row{remote_host} =~ $local_re )
        {
            next;
        }

        my $connection_type = geoip_record( $row{remote_host}, 'Connection-Type' );
        $row{connection_type} = $connection_type->{connection_type};

        my $isp = geoip_record( $row{remote_host}, 'ISP' );
        $row{organization} = $isp->{organization};
        $row{isp} = $isp->{isp};

        my $city = geoip_record( $row{remote_host}, 'City' );
        $row{city_name} = $city->{city}->{names}->{en};
        $row{subdivision_name} = $city->{subdivisions}->[-1]->{names}->{en};
        $row{country_name} = $city->{country}->{names}->{en};

        my @row = map { $row{$_} } @COLUMNS;
        my $line = '"' . join( '","', @row ) . '"' . "\n";
        print $out $line;
        print $out2 $line if $out2;
    }
}

my $pos = tell $in;

close $in;
close $out;
close $out2 if $out2;

if ( ! -f $out2_name || rand() < 1/720 )
{
    open my $out2, '>', $out2_name;
    print $out2 join( ',', @COLUMNS ), "\n";
    close $out2;

    system "tail -10000 '$out_name' >> '$out2_name'";
}

if ( open( my $dat, '>', $dat_name ) )
{
    print $dat $pos;
    close $dat;
}
