import urllib.parse
import urllib.request
import re
import io


def iri_to_uri(iri, encoding='Latin-1'):
    "Takes a Unicode string that can contain an IRI and emits a URI."
    scheme, authority, path, query, frag = urllib.parse.urlsplit(iri)
    scheme = scheme.encode(encoding)
    if ":" in authority:
        host, port = authority.split(":", 1)
        authority = host.encode('idna') + ":%s" % port
    else:
        authority = authority.encode(encoding)
    path = urllib.parse.quote(
      path.encode(encoding),
      safe="/;%[]=:$&()+,!?*@'~"
    )
    query = urllib.parse.quote(
      query.encode(encoding),
      safe="/;%[]=:$&()+,!?*@'~"
    )
    frag = urllib.parse.quote(
      frag.encode(encoding),
      safe="/;%[]=:$&()+,!?*@'~"
    )

    url = scheme.decode('utf-8') + "://" + authority.decode('utf-8') + "/" + path
    return url


def download_content(iri):
    url = iri_to_uri(iri, 'utf-8')
    html = urllib.request.urlopen(url).read().decode('utf-8')
    return html


def sanitize_string(input_str):
    return re.sub(r'[*."/\\\[\]:;|,?]', '_', input_str)



