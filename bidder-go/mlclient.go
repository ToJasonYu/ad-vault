package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

var mlServiceURL = getEnv("ML_SERVICE_URL", "http://127.0.0.1:8000")
var httpClient = &http.Client{Timeout: 2 * time.Second}

func getEnv(key, fallback string) string {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	return value
}

type predictRequest struct {
	InterestSegment string  `json:"interest_segment"`
	DeviceType      string  `json:"device_type"`
	AgeBracket      string  `json:"age_bracket"`
	Category        string  `json:"category"`
	BidAmount       float64 `json:"bid_amount"`
}

type predictResponse struct {
	ClickProbability float64 `json:"click_probability"`
}

// scoreCandidate calls ml-service's /predict endpoint for a single candidate ad.
func scoreCandidate(req BidRequest, candidate Candidate) (float64, error) {
	body := predictRequest{
		InterestSegment: req.InterestSegment,
		DeviceType:      req.DeviceType,
		AgeBracket:      req.AgeBracket,
		Category:        candidate.Category,
		BidAmount:       candidate.BidAmount,
	}

	payload, err := json.Marshal(body)
	if err != nil {
		return 0, err
	}

	resp, err := httpClient.Post(mlServiceURL+"/predict", "application/json", bytes.NewReader(payload))
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("ml-service returned status %d", resp.StatusCode)
	}

	var result predictResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return 0, err
	}

	return result.ClickProbability, nil
}
