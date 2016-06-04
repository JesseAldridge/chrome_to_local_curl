#!/usr/bin/python
import shlex, sys, re

chrome_curl = ' '.join('"{}"'.format(s) for s in sys.argv[1:])
tokens = shlex.split(chrome_curl)

local_domain_name = 'localhost:5001'

token_iter = iter(tokens)
filtered_tokens = []
for token in token_iter:
    if token.startswith('http'):
        filtered_tokens.append(local_domain_name)
    elif token == '-H':
        next_token = token_iter.next()
        for regex in (r'(^Content-Type\:)', r'(^Accept\:)'):
            if re.search(regex, next_token):
                filtered_tokens += (token, '"{}"'.format(next_token))
                break
    elif token in {'--data-binary', '--data', 'd'}:
        next_token = token_iter.next()
        filtered_tokens += (token, '"{}"'.format(next_token))
    elif token == '--compressed':
        continue
    else:
        filtered_tokens.append(token)

print
print ' '.join(filtered_tokens)
