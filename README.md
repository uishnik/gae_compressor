# GAE Compressor #

GAE Compressor it's a compressor of JS and CSS for [Google App Engine](https://developers.google.com/appengine/).

### Example ###
Input:
```
{% compress css %}
    <link href="/static/css/style.1.css" rel="stylesheet" />
    <link href="/static/css/style.2.css" rel="stylesheet" />
{% endcompress %}

{% compress js %}
    <script src="/static/js/script.1.js"></script>
    <script src="/static/js/script.2.js"></script>
{% endcompress %}
```

Output:
```
<link rel="stylesheet" href="/static/compress/css/d348c7ea1dd8.css" type="text/css" />
<script type="text/javascript" src="/static/compress/js/7b7e44390e78.js"></script>
```

### Usage ###
1. Put 'gae_compressor' package and 'settings.py' in the root of your project.
2. Set 'settings.py' variables as you need.
3. Specify 'compress' blocks in your templates as in the example above. 
4. Run 'compress.py'.

### Settings ###
#### Required settings ####
* PROJECT_ROOT - the absolute path to the root of your project.
* TEMPLATE_DIRS - list of locations of the template source files.
* STATIC_ROOT - the absolute path to the directory where stored static files.
* STATIC_URL - URL to use when referring to static files located in STATIC_ROOT.
* COMPRESS_ENABLED - just True or False.

#### Optional settings ####
* YUICOMPRESSOR - the absolute path to yuicompressor binary. GAE compressor uses YUI compressor to compress CSS.
* CLOSURE_COMPILER - the absolute path to closure compiler binary. GAE compressor uses closure compiler to compress JS.
* COMPRESSED_DIR_NAME - name of the directory in which compressed files will be written to. Default - 'compress'.
* MANIFEST_FILE_NAME - the name of the file to be used for saving the names of the compressed files. Default - 'gae_compressor.json'.
* COMPRESSOR_ENGINE - template engine that you use. Jinja2 or Django. Default - 'Jinja2'.

### Sample settings.py ###
```
import os


PROJECT_ROOT = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

YUICOMPRESSOR = os.path.join(PROJECT_ROOT, 'compressors/yuicompressor.jar')
CLOSURE_COMPILER = os.path.join(PROJECT_ROOT, 'compressors/closure_compiler.jar')

COMPRESS_ENABLED = True
```