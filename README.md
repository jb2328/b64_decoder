# b64_decoder
--
### b64 decoder and for MQTT message parsing.
The parser checks the dev_id field of an incoming message and import the right decoder dynamically:
`importlib.import_module("modules."+lib, package=None)`
The decoders are stored in /modules directory. To add an additional decoders, they just have to be pasted in the /modules. 
