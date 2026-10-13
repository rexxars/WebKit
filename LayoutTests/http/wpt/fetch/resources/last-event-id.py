import json


def main(request, response):
    response.headers.set(b"Cache-Control", b"no-store")
    if b"frame" in request.GET:
        response.headers.set(b"Content-Type", b"text/html")
        return b"<!doctype html><title>Controlled frame</title>"

    last_event_id = request.headers.get(b"Last-Event-ID", b"")
    if b"id" in request.GET:
        response.headers.set(b"Content-Type", b"text/event-stream")
        if last_event_id:
            return b"event: reconnected\ndata: " + last_event_id.hex().encode("ascii") + b"\n\n"
        return b"id: " + request.GET.first(b"id") + b"\nretry: 200\ndata: initial\n\n"

    response.headers.set(b"Content-Type", b"application/json")
    return json.dumps({
        "lastEventId": last_event_id.hex(),
        "control": request.headers.get(b"X-Test", b"").hex(),
    })
