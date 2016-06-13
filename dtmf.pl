use strict;
use warnings;

use Audio::Wav;
use Term::ReadKey;

my $sample_rate  = 8000;
my $bits_sample  = 8;
my $channels     = 1;
my $duration     = 0.5 * $sample_rate;
my $pi           = 4 * atan2( 1, 1 );

my %keypad =
(
    '1' => [ 697, 1209 ],
    '2' => [ 697, 1336 ],
    '3' => [ 697, 1477 ],
    'A' => [ 697, 1633 ],
    '4' => [ 770, 1209 ],
    '5' => [ 770, 1336 ],
    '6' => [ 770, 1477 ],
    'B' => [ 770, 1633 ],
    '7' => [ 852, 1209 ],
    '8' => [ 852, 1336 ],
    '9' => [ 852, 1477 ],
    'C' => [ 852, 1633 ],
    '*' => [ 941, 1209 ],
    '0' => [ 941, 1336 ],
    '#' => [ 941, 1477 ],
    'D' => [ 941, 1633 ],
);

sub play
{
    my $key = shift;
    my $f1 = 2 * $pi * $keypad{$key}->[0];
    my $f2 = 2 * $pi * $keypad{$key}->[1];

    my $tmp = '.' . rand() . '.wav';
    my $wav = Audio::Wav->new();
    my $writer = $wav->write( $tmp, {
            bits_sample => $bits_sample,
            sample_rate => $sample_rate,
            channels => $channels
        } );

    for ( my $k = 0; $k < $duration; $k++ )
    {
        my $t = $k / $sample_rate;
        my $value = 63 * sin( $t * $f1 ) + 63 * sin( $t * $f2 );
        $writer->write($value);
    }

    $writer->finish();
    my $pid = fork();
    if ( defined $pid && $pid == 0 )
    {
        system "afplay $tmp";
        unlink $tmp;
        exit;
    }
}

while (1)
{
    ReadMode(3);
    my $key = uc ReadKey();
    ReadMode(0);
    next if ! defined $keypad{$key};
    print $key;
    play($key);
}
