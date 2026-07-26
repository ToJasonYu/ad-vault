import kotlin.random.Random

const val DEFAULT_BASE_URL = "http://127.0.0.1:3000"
const val EVENTS_TO_SEND = 20
const val CLICK_RATE = 0.1

fun main(args: Array<String>) {
    val baseUrl = args.getOrElse(0) { DEFAULT_BASE_URL }
    val campaignIds = args.getOrElse(1) { "1" }.split(",").map { it.trim().toInt() }

    val logger = EventLogger(baseUrl)
    var logged = 0
    var failed = 0

    repeat(EVENTS_TO_SEND) {
        val campaignId = campaignIds.random()
        val eventType = if (Random.nextDouble() < CLICK_RATE) "click" else "impression"

        if (logger.logEvent(campaignId, eventType)) {
            logged++
        } else {
            failed++
        }
    }

    println("logged $logged events, $failed failed")
}
