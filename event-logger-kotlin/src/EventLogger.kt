import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse

// Client-side logger: fires impression/click events at the Rails back office.
// Uses the JDK's built-in HTTP client so this has zero external dependencies.
class EventLogger(private val baseUrl: String) {
    private val client = HttpClient.newHttpClient()

    fun logEvent(campaignId: Int, eventType: String): Boolean {
        val body = """{"campaign_id":$campaignId,"event_type":"$eventType"}"""
        val request = HttpRequest.newBuilder()
            .uri(URI.create("$baseUrl/events"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build()

        val response = client.send(request, HttpResponse.BodyHandlers.ofString())
        return response.statusCode() == 201
    }
}
