# event-logger-kotlin

Client-side impression/click logging. `EventLogger` posts events to `backoffice-rails`'s
`/events` endpoint (JDK's built-in `HttpClient`, no external dependencies — no Gradle needed,
just the Kotlin compiler). `Main.kt` simulates a client firing a batch of events so the
logger can be exercised without a real ad surface.

These events are what drives campaign budget decrements in Rails today, and are the same
shape of data (`campaign_id`, `event_type`) that would eventually become new training rows
for `ml-service`.

## Build & run

Requires `backoffice-rails` running (see `backoffice-rails/README.md`).

```
kotlinc src/EventLogger.kt src/Main.kt -include-runtime -d event-logger.jar
java -jar event-logger.jar [baseUrl] [campaignIds]
```

`baseUrl` defaults to `http://127.0.0.1:3000`, `campaignIds` is a comma-separated list of
campaign IDs to log against (defaults to `1`). Sends 20 simulated events at a ~10% click
rate and prints how many succeeded.
