#!/bin/bash

cat /dev/null > cf-ips.new
curl --location --silent https://www.cloudflare.com/ips-v4 >> cf-ips.new
curl --location --silent https://www.cloudflare.com/ips-v6 >> cf-ips.new
#cat cf-ips cf-ips.new | grep -P '/\d+' | sort | uniq | sponge cf-ips
cat cf-ips cf-ips.new | grep -P '/\d+' | sort | uniq > cf-ips.tmp
cat cf-ips.tmp > cf-ips
cat cf-ips | sed 's/^/set_real_ip_from /' | sed 's/$/;/' > cf-ips.conf
