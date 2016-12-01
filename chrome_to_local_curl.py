#!/usr/bin/python
import shlex, sys, re, json, os

with open(os.path.expanduser('~/curl_creds.json')) as f:
    text = f.read()
host_to_creds = json.loads(text)


# Get rid of formatting issues caused by YouTrack converting pasted curls to utf8.
# \xe2\x80\x8b == ZERO WIDTH SPACE
# \xe2\x80\x93 == EN DASH
params = [
    s.replace('\xe2\x80\x8b', ' ').replace('\xe2\x80\x93', '--')
    for s in sys.argv[1:]]
chrome_curl = ' '.join("'{}'".format(s) for s in params)
tokens = shlex.split(chrome_curl)

local_domain_name = 'localhost:5001'

token_iter = iter(tokens)
filtered_tokens = []
for token in token_iter:
    print 'token:', token

    if token.startswith('http'):
        domain_match = re.search(r'(https?\://.+?)/', token)
        domain_str = domain_match.group(1)
        host_name = re.search(r'https?\://(.+?)$', domain_str).group(1)
        filtered_tokens.append("'{}'".format(token.replace(domain_str, local_domain_name)))
        creds = host_to_creds[host_name]
        user = '"{}"'.format(':'.join((creds['username'], creds['password'])))
        filtered_tokens += ['--user', user]
    elif token in {'--data-binary', '--data', '-d'}:
        next_token = token_iter.next()
        post_data = json.loads(next_token)
        filtered_tokens += (token, "'{}'".format(json.dumps(post_data)))
    elif ' ' in token:
        filtered_tokens += ("'{}'".format(token),)
    elif token == '--compressed':
        continue
    else:
        filtered_tokens.append(token)

print
print ' '.join(filtered_tokens)
