use strict;
use warnings;

$| = 1;  # Automatically flush stdout

# Bit 0 corresponds to (0, 0)
# Bit 1 corresponds to (0, 1)
#  .
#  .
#  .
# Bit 8 corresponds to (2, 2)

my @faces =
(
    0b000010000,
    0b001000100,
    0b001010100,
    0b101000101,
    0b101010101,
    0b101101101,
);

sub main
{
    my $delay = shift @ARGV || 0.25;  # Time between frames in seconds
    my $iterations = 10 + int rand 20;
    my $previous_roll;

    print "\e[?25l";  # Hide cursor
    print "\e(0";  # Enable DEC Special Graphics

    while ( $iterations-- > 0 )
    {
        my $roll = int rand 6;

        if ( defined $previous_roll && $previous_roll == $roll )
        {
            next;
        }

        print "\e[2J";  # Clear terminal

        my $x = 1 + int(rand(80 - 10));
        my $y = 1 + int(rand(24 - 10));

        printf "\e[%d;%dH", $y++, $x;  # Move cursor
        print "\x6C" . "\x71" x 7 . "\x6B";  # Draw horizontal bar with corners

        for ( my $i = 0; $i < 9; $i++ )
        {
            if ( $i % 3 == 0 )
            {
                printf "\e[%d;%dH", $y++, $x;  # Move cursor
                print "\x78";  # Draw vertical bar
            }

            print " ";

            if ( ( $faces[$roll] >> $i ) & 1 )  # Get ith bit
            {
                print "\x60";  # Draw black dot
            }
            else
            {
                print " ";
            }

            if ( $i % 3 == 2 )
            {
                print " ";
                print "\x78";  # Draw vertical bar
            }
        }

        printf "\e[%d;%dH", $y++, $x;  # Move cursor
        print "\x6D" . "\x71" x 7 . "\x6A";  # Draw horizontal bar with corners

        select undef, undef, undef, $delay;
    }

    printf "\e[%d;%dH", 24, 1;  # Move cursor
    print "\e(B";  # Disable DEC Special Graphics
    print "\e[?25h";  # Show cursor
}

main;
