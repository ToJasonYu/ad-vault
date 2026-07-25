package main

import (
	"encoding/json"
	"log"
	"net/http"
)

const port = ":8080"

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", healthHandler)

	log.Printf("bidder-go listening on %s", port)
	log.Fatal(http.ListenAndServe(port, mux))
}
