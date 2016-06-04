$ python chrome_to_local_curl.py curl 'http://a.fake.domain.com/a/fake/endpoint' -X PUT -H 'Pragma: no-cache' -H 'Origin: http://localhost:3000' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'Authorization: Token abcdefghijklmnop12345' -H 'Connection: keep-alive' -H 'Referer: http://localhost:3000/another/fake/endpoint' --data-binary '{"foo":"bar","baz":[64]}' --compressed

Output:

curl localhost:5001/a/fake/endpoint -X PUT -H "Content-Type: application/json" -H "Accept: application/json, text/javascript, */*; q=0.01" --data-binary "{foo:bar,baz:[64]}"
