package main

// Candidate is one campaign competing for this impression.
type Candidate struct {
	CampaignID string  `json:"campaign_id"`
	Category   string  `json:"category"`
	BidAmount  float64 `json:"bid_amount"`
}

// BidRequest describes the user and the campaigns competing for their impression.
type BidRequest struct {
	InterestSegment string      `json:"interest_segment"`
	DeviceType      string      `json:"device_type"`
	AgeBracket      string      `json:"age_bracket"`
	Candidates      []Candidate `json:"candidates"`
}

// ScoredCandidate is a candidate after ml-service has scored it.
type ScoredCandidate struct {
	CampaignID       string  `json:"campaign_id"`
	ClickProbability float64 `json:"click_probability"`
	ExpectedValue    float64 `json:"expected_value"`
}

// BidResponse is the winning ad returned to the caller.
type BidResponse struct {
	Winner *ScoredCandidate `json:"winner"`
}
