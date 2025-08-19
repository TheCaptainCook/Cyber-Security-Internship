from zxcvbn import zxcvbn

#https://github.com/dwolfhub/zxcvbn-python

results = zxcvbn('hello', user_inputs=['John', 'Smith'])

print(results)