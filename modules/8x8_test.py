import elsys as e
raw='AQElAjYEAMIFAwcOJBMYNDU6MBcPCgYyQUdDGQ0LBjQ8QiQQDwwLKjEdEAwPDAkgDQ0ODQ0HBysMDA0OCAkGKRMLCQ0KBgMiHwkEAwYICg=='
pre=e.b64toBytes(raw)
a=e.decodePayload(pre)
print(a)