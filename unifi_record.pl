use strict;
use warnings;

use JSON;
use LWP::UserAgent;

my $base = 'https://unifi:7443/api/2.0';
my $apikey = $ENV{UNIFI_VIDEO_APIKEY};
$ENV{PERL_LWP_SSL_VERIFY_HOSTNAME} = 0;

my $ua = LWP::UserAgent->new();
$ua->add_handler( 'request_send',  sub { shift->dump; return } );
$ua->add_handler( 'response_done', sub { shift->dump; return } );

#my $login =
#{
#    username => $ENV{UNIFI_VIDEO_USERNAME},
#    password => $ENV{UNIFI_VIDEO_PASSOWRD},
#};
#
#$ua->cookie_jar( {} );
#request( 'POST', 'login', encode_json( $login ) );

my $cameras = decode_json( request( 'GET', 'camera' ) );

foreach my $camera ( @{ $cameras->{data} } )
{
    if ( $camera->{name} eq 'Front Yard' )
    {
        print $camera->{_id}, "\n";

        my $settings =
        {
            _id  => $camera->{_id},
            name => $camera->{name},
            recordingSettings =>
            {
                channel => 0,
                fullTimeRecordEnabled => JSON::false,
                motionRecordEnabled   => JSON::true,
            }
        };

        request( 'PUT', "camera/$camera->{_id}", encode_json( $settings ) );
        last;
    }
}

sub request
{
    my ( $method, $resource, $content ) = @_;

    my $request = HTTP::Request->new( $method => "$base/$resource?apiKey=$apikey" );

    if ( defined $content )
    {
        $request->content_type( 'application/json' );
        $request->content( $content );
    }

    my $response = $ua->request( $request );
    return $response->content;
}
