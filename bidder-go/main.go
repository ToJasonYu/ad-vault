package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
)

const port = ":8080"

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

// bidHandler scores every candidate against ml-service concurrently and
// returns whichever has the highest expected value (click probability * bid).
func bidHandler(w http.ResponseWriter, r *http.Request) {
	var req BidRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}

	if len(req.Candidates) == 0 {
		http.Error(w, "no candidates provided", http.StatusBadRequest)
		return
	}

	var wg sync.WaitGroup
	results := make(chan ScoredCandidate, len(req.Candidates))

	for _, candidate := range req.Candidates {
		wg.Add(1)
		go func(c Candidate) {
			defer wg.Done()

			probability, err := scoreCandidate(req, c)
			if err != nil {
				log.Printf("scoring %s failed: %v", c.CampaignID, err)
				return
			}

			results <- ScoredCandidate{
				CampaignID:       c.CampaignID,
				ClickProbability: probability,
				ExpectedValue:    probability * c.BidAmount,
			}
		}(candidate)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	var winner *ScoredCandidate
	for scored := range results {
		scored := scored
		if winner == nil || scored.ExpectedValue > winner.ExpectedValue {
			winner = &scored
		}
	}

	if winner == nil {
		http.Error(w, "no candidates could be scored", http.StatusBadGateway)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(BidResponse{Winner: winner})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", healthHandler)
	mux.HandleFunc("POST /bid", bidHandler)

	log.Printf("bidder-go listening on %s", port)
	log.Fatal(http.ListenAndServe(port, mux))
}
