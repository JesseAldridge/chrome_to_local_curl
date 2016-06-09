#!/usr/bin/python
import shlex, sys, re, json, os

with open(os.path.expanduser('~/curl_creds.json')) as f:
    text = f.read()
host_to_creds = json.loads(text)

chrome_curl = ' '.join("'{}'".format(s) for s in sys.argv[1:])
tokens = shlex.split(chrome_curl)

local_domain_name = 'localhost:5001'

token_iter = iter(tokens)
filtered_tokens = []
for token in token_iter:
    if token.startswith('http'):
        domain_match = re.search(r'(https?\://.+?)/', token)
        domain_str = domain_match.group(1)
        host_name = re.search(r'https?\://(.+?)$', domain_str).group(1)
        filtered_tokens.append("'{}'".format(token.replace(domain_str, local_domain_name)))
        creds = host_to_creds[host_name]
        filtered_tokens += ['--user', ':'.join((creds['username'], creds['password']))]
    elif token == '-H':
        next_token = token_iter.next()
        for regex in (r'(^Content-Type\:)', r'(^Accept\:)'):
            if re.search(regex, next_token):
                filtered_tokens += (token, '"{}"'.format(next_token))
                break
    elif token in {'--data-binary', '--data', '-d'}:
        next_token = token_iter.next()
        post_data = json.loads(next_token)
        filtered_tokens += (token, "'{}'".format(json.dumps(post_data)))
    elif token == '--compressed':
        continue
    else:
        filtered_tokens.append(token)

print
print ' '.join(filtered_tokens)
