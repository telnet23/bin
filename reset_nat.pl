#!/usr/bin/env perl

use strict;
use warnings;

use Expect;
use MIME::Base64;
use POSIX;

my $external = $ENV{NAT_EXTERNAL};
my $password = $ENV{NAT_PASSWORD};

my $nc = `nc -vz $external 80 2>&1`;
chomp $nc;

if ( $nc eq "Connection to $external 80 port [tcp/http] succeeded!" )
{
	exit;
}

my $expect = Expect->new;
$expect->log_stdout( 0 );

if ( ! $expect->spawn( 'ssh', qw( -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no admin@router ) ) )
{
	print_log( 'Router is inaccessible' );
	exit;
}

$expect->expect( 10, [ 'Password: ' ] );
$expect->send( "$password\r" );

$expect->expect( 1, [ 'Router>' ] );
$expect->send( "enable\r" );

$expect->expect( 1, [ 'Password: ' ] );
$expect->send( "$password\r" );

$expect->expect( 1, [ 'Router#' ] );
$expect->send( "configure terminal\r" );

$expect->expect( 1, [ 'Router(config)#' ] );
$expect->send( "no ip nat source static tcp 10.0.0.11 80 interface GigabitEthernet8 80\r" );

$expect->expect( 1, [ 'Router(config)#' ] );
$expect->send( "ip nat source static tcp 10.0.0.11 80 interface GigabitEthernet8 80\r" );

$expect->expect( 1, [ 'Router(config)#' ] );
$expect->send( "no ip nat source static tcp 10.0.0.12 8000 interface GigabitEthernet8 8000\r" );

$expect->expect( 1, [ 'Router(config)#' ] );
$expect->send( "ip nat source static tcp 10.0.0.12 8000 interface GigabitEthernet8 8000\r" );

$expect->expect( 1, [ 'Router(config)#' ] );
$expect->send( "exit\r" );

$expect->expect( 1, [ 'Router#' ] );
$expect->send( "exit\r" );

$expect->soft_close();
print_log( 'Reset was successful' );

sub print_log
{
	my ( $message ) = @_;
	open my $fh, '>>', 'reset_nat.log';
	my $timestamp = strftime '%Y-%m-%d %H:%M:%S %Z', localtime;
	print $fh "[$timestamp] $message\n";
	close $fh;
}
